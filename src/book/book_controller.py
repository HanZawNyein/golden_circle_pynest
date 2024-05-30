from typing import Annotated

from fastapi import Security
from nest.core import Controller, Get, Post, Depends, Put, Delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import config
from .book_model import Book
from .book_service import BookService
from ..auth.auth_model import User
from ..auth.token_utils import get_current_active_user


@Controller("book")
class BookController:

    def __init__(self, book_service: BookService):
        self.book_service = book_service

    @Get("/")
    async def get_books(self,session: AsyncSession = Depends(config.get_db),):
        return await self.book_service.get_books(session)

    @Get('/:book_id')
    async def get_book(self, book_id: int, session: AsyncSession = Depends(config.get_db)):
        return await self.book_service.get_book(book_id, session)

    @Post("/")
    async def add_book(self, book: Book, session: AsyncSession = Depends(config.get_db)):
        return await self.book_service.add_book(book, session)

    @Put('/:book_id')
    async def update_book(self, book_id: int, book: Book, session: AsyncSession = Depends(config.get_db)):
        await self.book_service.update_book(book_id, book, session)
        return {"message": "Book updated successfully!", "book": book}

    #
    @Delete('/:book_id')
    async def delete_book(self, book_id: int, session: AsyncSession = Depends(config.get_db)):
        result = await self.book_service.delete_book(book_id, session)
        return {"message": "Book deleted successfully!", "book": result}
