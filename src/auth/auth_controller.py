from nest.core import Controller, Get, Post, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import config
from .auth_model import Auth
from .auth_service import AuthService


@Controller("auth")
class AuthController:

    def __init__(self, auth_service: AuthService):
        self.auth_service = auth_service

    @Get("/")
    async def get_auth(self, session: AsyncSession = Depends(config.get_db)):
        return await self.auth_service.get_auth(session)

    @Post("/")
    async def add_auth(self, auth: Auth, session: AsyncSession = Depends(config.get_db)):
        return await self.auth_service.add_auth(auth, session)
