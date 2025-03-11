from pydantic import BaseModel

class Login(BaseModel):
    login: str
    pwd: str