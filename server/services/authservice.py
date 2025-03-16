from asyncio import sleep
from time import time
from random import randint

from models.user import UserIn, User

# TODO performance is probably bad, use dicts for users and sessions
# TODO use a database, too

class AuthService:
    def __init__(self):
        self._sessions = []
        self._users = []

    async def findsession(self, token: str, refresh: bool = True):
        self.cleanup()
        for s in self._sessions:
            if s['token'] == token:
                if refresh:
                    s['expires'] = time() + 24 * 3600 * 1000
                return s['user']
        
        return None
    
    async def register(self, user: UserIn):
        self.cleanup()

        # TODO plaintext password
        if any(u.pwd == user.pwd for u in self._users):
            # TODO raise something good
            return None
        
        created = User(
            id = 1 if not len(self._users) else max(u.id for u in self._users) + 1,
            login = user.login,
            pwd = user.pwd,
            code = str(randint(10000000000000, 100000000000000))
        )
        self._users.append(created)
        return created
    
    async def confirm(self, code: str):
        # TODO this probably should also use user id or login, just in case
        self.cleanup()

        user = next((u for u in self._users if u.code == code), None)

        if not user:
            print(self._users)
            return None
        
        user.code = None
        return user

    async def login(self, login: str, pwd: str):
        self.cleanup()

        session = next((s for s in self._sessions if s['user'].login == login), None)

        if session and not session['user'].code:
            return session['token']
        
        for u in self._users:
            if u.login == login:
                if u.pwd == pwd:
                    user = next((u for u in self._users if u.login == login), None)
                    token = str(randint(10000000000000, 100000000000000))
                    if not user:
                        # raise something good
                        return None
                    if user.code:
                        # raise something here too
                        return None
                    self._sessions.append({
                        'expires': time() + 24 * 3600 * 1000,
                        'token': token,
                        'user': user
                    })
                    return token
                else:
                    return None
        
        return None

    async def logout(self, token: str):
        self.cleanup()

        session = next((s for s in self._sessions if s['token'] == token), None)
        if not session:
            return False
        
        self._sessions.remove(session)
        return True
    
    async def cleanup(self):
        now = time()
        self._sessions = [s for s in self._sessions if s['expires'] < now]
        await sleep(10)
        yield True

authservice = AuthService()
