import os
from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from jwt import InvalidTokenError
from nest.core import Injectable
from nest.core.decorators.database import async_db_request_handler
from passlib.context import CryptContext
from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.auth.auth_model import TokenData, UserRequestForm, UserInDB, SampleUser
from .auth_entity import AuthUser as AuthUserEntity

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/token",
    scopes={"me": "Read information about the current user.", "items": "Read items."},
)


@Injectable
class AuthService:

    def verify_password(self, plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password):
        return pwd_context.hash(password)

    @async_db_request_handler
    async def get_user_by_username(self, session: AsyncSession, username: str):
        try:
            query = select(AuthUserEntity).filter(AuthUserEntity.username == username)
            result = await session.execute(query)
            return result.scalars().first()
        except NoResultFound:
            return None
        except Exception as _:
            return None

    async def authenticate_user(self, session: AsyncSession, username: str, password: str):
        user = await self.get_user_by_username(session, username)
        if not user:
            return False
        if not self.verify_password(password, user.hashed_password):
            return False
        return user

    def create_access_token(self, data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, os.getenv('SECRET_KEY'), algorithm=os.getenv('ALGORITHM'))
        return encoded_jwt

    async def get_current_user(self,
                               session: AsyncSession,
                               security_scopes: SecurityScopes, token: Annotated[str, Depends(oauth2_scheme)]
                               ):
        if security_scopes.scopes:
            authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
        else:
            authenticate_value = "Bearer"
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": authenticate_value},
        )
        try:
            payload = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=[os.getenv('ALGORITHM')])
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
            token_scopes = payload.get("scopes", [])
            token_data = TokenData(scopes=token_scopes, username=username)
        except (InvalidTokenError, ValidationError):
            raise credentials_exception
        user = await  self.get_user_by_username(session, username=token_data.username)
        if user is None:
            raise credentials_exception
        for scope in security_scopes.scopes:
            if scope not in token_data.scopes:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not enough permissions",
                    headers={"WWW-Authenticate": authenticate_value},
                )
        return user

    # async def get_current_active_user(self, session: AsyncSession,
    #                                   current_user: Annotated[User, Security(self.get_current_user, scopes=["me"])], ):
    #     if current_user.disabled:
    #         raise HTTPException(status_code=400, detail="Inactive user")
    #     return current_user

    @async_db_request_handler
    async def register(self, user: UserRequestForm, session: AsyncSession) -> SampleUser:
        context = {
            "username": user.username,
            "email": user.email,
            "full_name": user.full_name,
            "hashed_password": self.get_password_hash(password=user.password)
        }
        new_user = UserInDB(**context)
        new_auth = AuthUserEntity(**new_user.dict())
        session.add(new_auth)
        await session.commit()
        return new_auth

    @async_db_request_handler
    async def get_auth(self, session: AsyncSession):
        query = select(AuthUserEntity)  # Selecting id and username columns, adjust as needed
        result = await session.execute(query)
        return result.scalars().all()
