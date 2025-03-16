from pydantic import BaseModel

class UserIn(BaseModel):
    login: str
    pwd: str

class UserOut(BaseModel):
    id: int
    login: str
    code: str | None

class User(BaseModel):
    id: int
    login: str
    pwd: str
    code: str | None
