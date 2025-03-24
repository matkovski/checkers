from hashlib import md5

from asyncio import sleep
from time import time
from random import randint

from models.user import UserIn, User, UserOut
from .dbservice import db

class AuthService:
    async def finduser(self, token: str, refresh: bool = True):
        self._cleanup()
        session = db.row('select id, userid, expires from sessions where id=:id', {'id': token})
        if not session:
            return None
        
        if session[2] < time():
            db.run('delete from sessions where id=:id', {'id': token})
            return None
        
        db.run('update sessions set expires=:time where id=:id', {'id': token, 'time': time() + 24 * 3600 * 1000})

        user = db.row('select * from users where id=:id', {'id': session[1]})
        if not user:
            db.run('delete from sessions where id=:id', {'id': token})
            return None
        
        return User.make(user)
    
    async def register(self, user: UserIn):
        self._cleanup()

        already = db.query('select * from users where login=:login', {'login': user.login})
        if already:
            # TODO raise something good
            return None
        
        id = db.row('select max(id) from users')

        created = User(
            id = id[0] + 1 if id and id[0] else 1,
            login = user.login,
            pwd = user.pwd,
            code = str(randint(10000000000000, 100000000000000))
        )

        db.query('insert into users (id, login, pwd, code) values (:id, :login, :pwd, :code)', {
            'id': created.id,
            'login': created.login,
            'pwd': self._encodepwd(created.pwd),
            'code': created.code,
        })
        return created
    
    async def confirm(self, code: str):
        # TODO this probably should also use user id or login, just in case
        self._cleanup()

        user = db.row('select * from users where code=:code', {'code': code})
        if not user:
            return None

        db.run('update users set code="" where id=:id', {'id': user[0]})
        
        return UserOut.make(user)

    async def login(self, login: str, pwd: str):
        self._cleanup()

        user = db.row('select * from users where login=:login', {'login': login})
        if not user or user[3]:
            return None
        
        if user[2] != self._encodepwd(pwd):
            return None

        user = User.make(user)
        session = db.row('select * from sessions where userid=:id', {'id': user.id})

        if session:
            return session[0]

        token = str(randint(10000000000000, 100000000000000))
        db.run('insert into sessions (id, userid, expires) values (:id, :userid, :expires)', {
            'id': token,
            'userid': user.id,
            'expires': time() + 24 * 3600 * 1000,
        })

        return token

    async def logout(self, token: str):
        self._cleanup()

        session = db.row('select * from sessions where id=:id', {'id': token})
        if not session:
            return False
        
        db.run('delete from sessions where id=:id', {'id': token})
        return True
    
    def _cleanup(self):
        db.run('delete from sessions where expires<:time', {'time': time()})
    
    def _encodepwd(self, pwd: str):
        return md5(pwd.encode('utf-8')).hexdigest()

auth = AuthService()

