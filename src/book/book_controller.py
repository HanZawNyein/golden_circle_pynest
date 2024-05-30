from nest.core import Controller, Get, Post, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.config import config


from .book_service import BookService
from .book_model import Book


@Controller("book")
class BookController:

    def __init__(self, book_service: BookService):
        self.book_service = book_service

    @Get("/")
    async def get_book(self, session: AsyncSession = Depends(config.get_db)):
        return await self.book_service.get_book(session)

    @Post("/")
    async def add_book(self, book: Book, session: AsyncSession = Depends(config.get_db)):
        return await self.book_service.add_book(book, session)
 