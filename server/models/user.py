from pydantic import BaseModel

class UserIn(BaseModel):
    login: str
    pwd: str

class UserOut(BaseModel):
    id: int
    login: str

    @classmethod
    def make(self, row):
        return UserOut(
            id = row[0],
            login = row[1],
        )

class User(BaseModel):
    id: int
    login: str
    pwd: str
    code: str | None

    @classmethod
    def make(self, row):
        return User(
            id = row[0],
            login = row[1],
            pwd = row[2],
            code = row[3],
        )
