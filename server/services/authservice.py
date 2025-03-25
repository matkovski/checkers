from hashlib import md5

from asyncio import sleep
from time import time
from random import randint

from models.user import UserIn, User, UserOut
from .dbservice import db

class AuthService:
    async def finduser(self, token: str):
        self._cleanup()
        session = db.row('select id, user, expires from sessions where id=:id', {'id': token})
        if not session:
            return None
        
        if session[2] < time():
            db.run('delete from sessions where id=:id', {'id': token})
            return None
        
        db.run('update sessions set expires=:time where id=:id', {'id': token, 'time': time() + 24 * 3600 * 1000})

        user = db.row('select * from users where login=:login', {'login': session[1]})
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
        
        created = User(
            login = user.login,
            pwd = user.pwd,
            code = str(randint(10000000000000, 100000000000000))
        )

        db.query('insert into users (login, pwd, code) values (:login, :pwd, :code)', {
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

        db.run('update users set code="" where login=:login', {'login': user[0]})
        
        return UserOut.make(user)

    async def login(self, login: str, pwd: str):
        self._cleanup()

        user = db.row('select * from users where login=:login', {'login': login})
        if not user or user[2]:
            return None
        
        if user[1] != self._encodepwd(pwd):
            return None

        user = User.make(user)
        session = db.row('select id from sessions where user=:login', {'login': user.login})

        if session:
            print(f"RETURNING session[0] {session[0]} which is a {type(session[0])}")
            return session[0]

        token = str(randint(10000000000000, 100000000000000))
        db.run('insert into sessions (id, user, expires) values (:id, :user, :expires)', {
            'id': token,
            'user': user.login,
            'expires': time() + 24 * 3600 * 1000,
        })

        print(f"RETURNING token {token} which is a {type(token)}")
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

