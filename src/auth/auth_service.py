from nest.core import Injectable
from nest.core.decorators.database import async_db_request_handler
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .auth_entity import Auth as AuthEntity
from .auth_model import Auth


@Injectable
class AuthService:

    @async_db_request_handler
    async def add_auth(self, auth: Auth, session: AsyncSession):
        new_auth = AuthEntity(
            **auth.dict()
        )
        session.add(new_auth)
        await session.commit()
        return new_auth.id

    @async_db_request_handler
    async def get_auth(self, session: AsyncSession):
        query = select(AuthEntity)
        result = await session.execute(query)
        return result.scalars().all()
