from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str
    pwd: str
    active: bool
