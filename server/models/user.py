from pydantic import BaseModel

class UserIn(BaseModel):
    login: str
    pwd: str
    name: str

class UserIn(BaseModel):
    login: str
    pwd: str | None
    name: str

class UserOut(BaseModel):
    id: int
    login: str
    name: str
    code: str | None

class User(BaseModel):
    id: int
    login: str
    pwd: str
    name: str
    code: str | None
