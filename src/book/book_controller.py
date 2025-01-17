from typing import Annotated

from fastapi.security import SecurityScopes
from nest.core import Controller, Get, Post, Depends, Put, Delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import config
from .book_model import Book
from .book_service import BookService
from ..auth.token_utils import oauth2_scheme


@Controller("book")
class BookController:
    def __init__(self, book_service: BookService):
        self.book_service = book_service

    @Get("/")
    async def get_books(self, security_scopes: SecurityScopes, token: Annotated[str, Depends(oauth2_scheme)],
                        session: AsyncSession = Depends(config.get_db), ):
        return await self.book_service.get_books(session)

    @Get('/:book_id')
    async def get_book(self,security_scopes: SecurityScopes, token: Annotated[str, Depends(oauth2_scheme)],
                       book_id: int, session: AsyncSession = Depends(config.get_db)):
        return await self.book_service.get_book(book_id, session)

    @Post("/")
    async def add_book(self,security_scopes: SecurityScopes, token: Annotated[str, Depends(oauth2_scheme)],
                       book: Book, session: AsyncSession = Depends(config.get_db)):
        return await self.book_service.add_book(book, session)

    @Put('/:book_id')
    async def update_book(self,security_scopes: SecurityScopes, token: Annotated[str, Depends(oauth2_scheme)],
                          book_id: int, book: Book, session: AsyncSession = Depends(config.get_db)):
        await self.book_service.update_book(book_id, book, session)
        return {"message": "Book updated successfully!", "book": book}

    #
    @Delete('/:book_id')
    async def delete_book(self,security_scopes: SecurityScopes, token: Annotated[str, Depends(oauth2_scheme)],
                          book_id: int, session: AsyncSession = Depends(config.get_db)):
        result = await self.book_service.delete_book(book_id, session)
        return {"message": "Book deleted successfully!", "book": result}
