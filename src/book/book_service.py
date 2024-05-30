from .book_model import Book
from .book_entity import Book as BookEntity
from nest.core.decorators.database import async_db_request_handler
from nest.core import Injectable

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

@Injectable
class BookService:

    @async_db_request_handler
    async def add_book(self, book: Book, session: AsyncSession):
        new_book = BookEntity(
            **book.dict()
        )
        session.add(new_book)
        await session.commit()
        return new_book.id

    @async_db_request_handler
    async def get_book(self, session: AsyncSession):
        query = select(BookEntity)
        result = await session.execute(query)
        return result.scalars().all()
