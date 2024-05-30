from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from src.config import config


class Auth(config.Base):
    __tablename__ = "auth"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, unique=True)
