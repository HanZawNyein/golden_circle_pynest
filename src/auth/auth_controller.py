import os
from datetime import timedelta
from typing import Annotated

from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm, SecurityScopes
from nest.core import Controller, Post, Depends, Get
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import config
from .auth_model import Token, UserRequestForm, SampleUser
from .auth_service import AuthService
from .token_utils import oauth2_scheme, authenticate_user, create_access_token, get_current_user


@Controller("auth")
class AuthController:

    def __init__(self, auth_service: AuthService):
        self.auth_service = auth_service

    @Post("/")
    async def register(self, new_user: UserRequestForm, session: AsyncSession = Depends(config.get_db)) -> SampleUser:
        new_user = await self.auth_service.register(new_user, session=session)
        return SampleUser(username=new_user.username, email=new_user.email, full_name=new_user.full_name)

    @Post("/token")
    async def login_for_access_token(self,
                                     form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                     session: AsyncSession = Depends(config.get_db),
                                     ) -> Token:
        user = await authenticate_user(session, form_data.username, form_data.password)
        if not user:
            raise HTTPException(status_code=400, detail="Incorrect username or password")
        access_token_expires = timedelta(minutes=int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES', 30)))
        access_token = create_access_token(
            data={"sub": user.username, "scopes": form_data.scopes},
            expires_delta=access_token_expires,
        )
        return Token(access_token=access_token, token_type="bearer")

    #
    @Get("/users/me/")
    async def read_users_me(self, security_scopes: SecurityScopes, token: Annotated[str, Depends(oauth2_scheme)],
                            session: AsyncSession = Depends(config.get_db), ) -> SampleUser:
        user = await get_current_user(session, security_scopes, token)
        return SampleUser(username=user.username, email=user.email, full_name=user.full_name)
