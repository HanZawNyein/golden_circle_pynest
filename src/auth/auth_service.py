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
from .token_utils import get_password_hash




@Injectable
class AuthService:

    @async_db_request_handler
    async def register(self, user: UserRequestForm, session: AsyncSession) -> SampleUser:
        context = {
            "username": user.username,
            "email": user.email,
            "full_name": user.full_name,
            "hashed_password": get_password_hash(password=user.password)
        }
        new_user = UserInDB(**context)
        new_auth = AuthUserEntity(**new_user.dict())
        session.add(new_auth)
        await session.commit()
        return new_auth
