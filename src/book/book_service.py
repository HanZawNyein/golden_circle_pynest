from sqlalchemy.exc import NoResultFound

from .book_model import Book
from .book_entity import Book as BookEntity
from nest.core.decorators.database import async_db_request_handler
from nest.core import Injectable

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


@Injectable
class BookService:

    @async_db_request_handler
    async def get_books(self, session: AsyncSession):
        query = select(BookEntity)
        result = await session.execute(query)
        return result.scalars().all()

    @async_db_request_handler
    async def get_book(self, book_id: int, session: AsyncSession):
        try:
            query = select(BookEntity).filter(BookEntity.id == book_id)
            result = await session.execute(query)
            return result.scalars().first()
        except NoResultFound:
            return None

    @async_db_request_handler
    async def add_book(self, book: Book, session: AsyncSession):
        new_book = BookEntity(**book.dict())
        session.add(new_book)
        await session.commit()
        return new_book.id

    @async_db_request_handler
    async def update_book(self, book_id: int, updated_book: Book, session: AsyncSession):
        try:
            query = select(BookEntity).filter(BookEntity.id == book_id)
            result = await session.execute(query)
            existing_book = result.scalars().first()
            if existing_book:
                for key, value in updated_book.dict().items():
                    setattr(existing_book, key, value)
                await session.commit()
                return True
            else:
                return False
        except NoResultFound:
            return False

    @async_db_request_handler
    async def delete_book(self, book_id: int, session: AsyncSession):
        try:
            query = select(BookEntity).filter(BookEntity.id == book_id)
            result = await session.execute(query)
            book_to_delete = result.scalars().first()
            if book_to_delete:
                await session.delete(book_to_delete)
                await session.commit()
                return True
            else:
                return False
        except NoResultFound:
            return False
