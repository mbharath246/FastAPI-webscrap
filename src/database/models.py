from pydantic import BaseModel, EmailStr


"""User Details"""
class User(BaseModel):
    name: str
    phone: int
    username: EmailStr


class UserIn(User):
    password: str


"""Token Details"""
class Token(BaseModel):
    access_token: str
    token_type: str
