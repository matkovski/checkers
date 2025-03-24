from pydantic import BaseModel

class UserIn(BaseModel):
    login: str
    pwd: str

class UserOut(BaseModel):
    login: str

    @classmethod
    def make(self, row):
        return UserOut(
            login = row[0],
        )

class User(BaseModel):
    login: str
    pwd: str
    code: str | None

    @classmethod
    def make(self, row):
        return User(
            login = row[0],
            pwd = row[1],
            code = row[2],
        )
