from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
    scopes: list[str] = []


class SampleUser(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None


class User(SampleUser):
    disabled: bool | None = False


class UserRequestForm(SampleUser):
    password: str


class UserInDB(User):
    hashed_password: str
