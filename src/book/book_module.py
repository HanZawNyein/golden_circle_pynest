from nest.core import Module
from .book_controller import BookController
from .book_service import BookService


@Module(
    controllers=[BookController],
    providers=[BookService],
    imports=[]
)   
class BookModule:
    pass

    