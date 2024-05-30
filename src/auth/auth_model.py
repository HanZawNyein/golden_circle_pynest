from pydantic import BaseModel


class Auth(BaseModel):
    name: str
