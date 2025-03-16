from hashlib import md5

from asyncio import sleep
from time import time
from random import randint

from models.user import UserIn, User
from .dbservice import db

class AuthService:
    def __init__(self):
        self._sessions = []

    async def findsession(self, token: str, refresh: bool = True):
        self._cleanup()
        for s in self._sessions:
            if s['token'] == token:
                if refresh:
                    s['expires'] = time() + 24 * 3600 * 1000
                return s['user']
        
        return None
    
    async def register(self, user: UserIn):
        self._cleanup()

        already = db.query('select * from users where login=?', (user.login,))
        if already:
            # TODO raise something good
            return None
        
        (id) = db.row('select max(id) from users')

        created = User(
            id = id + 1 if id else 1,
            login = user.login,
            pwd = user.pwd,
            code = str(randint(10000000000000, 100000000000000))
        )

        db.query('insert into users (id, login, pwd, code) values (?, ?, ?, ?)', (created.id, created.login, created.pwd, created.code))
        return created
    
    async def confirm(self, code: str):
        # TODO this probably should also use user id or login, just in case
        self._cleanup()

        user = db.row('select * from users where code = ?', (code,))
        if not user:
            return None

        db.run('update users set code='' where id=?', (user.id,))
        return user

    async def login(self, login: str, pwd: str):
        self._cleanup()

        session = next((s for s in self._sessions if s['user'].login == login), None)

        if session and not session['user'].code:
            return session['token']
        
        user = db.row('select * from users where login = ?', (login,))
        if not user or user.code:
            return None

        if user.pwd != self._encodepwd(pwd):
            return None

        token = str(randint(10000000000000, 100000000000000))
        self._sessions.append({
            'expires': time() + 24 * 3600 * 1000,
            'token': token,
            'user': user
        })
        return token

    async def logout(self, token: str):
        self._cleanup()

        session = next((s for s in self._sessions if s['token'] == token), None)
        if not session:
            return False
        
        self._sessions.remove(session)
        return True
    
    async def _cleanup(self):
        now = time()
        self._sessions = [s for s in self._sessions if s['expires'] < now]
        await sleep(10)
        yield True
    
    async def _encodepwd(self, pwd: str):
        return md5(pwd.encode('utf-8')).hexdigest()

auth = AuthService()
