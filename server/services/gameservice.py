from asyncio import sleep
from random import randint
from json import dumps

from models.user import User, UserOut
from models.game import Game

from .dbservice import db

class GameService:
    def __init__(self):
        self._queue = {}

    async def pickup(self, login: str):
        game = db.row('select id, white, black, moves from games where white=:user or black=:user and (end="-" or end is null)', {'user': login})
        if not game:
            game = db.row('select id, white, black, moves from games where white is null and black<>:user or black is null and white<>:user', {'user': login})
            if game:
                db.run(f'update games set {"black" if game[1] else "white"}=:user where id=:id', {'user': login, 'id': game[0]})
        if not game:
            color = 'white' if randint(0, 1) else 'black'
            id = db.row('select max(id) from games')
            id = id[0] + 1 if id and id[0] else 1
            db.run(f'insert into games (id, {color}) values (:id, :user)', {
                'id': id,
                'user': login,
            })
            game = db.row('select id, white, black, moves from games where id=:id', {'id': id})
        
        if game:
            white = db.row('select * from users where login=:login', {'login': game[1]})
            black = db.row('select * from users where login=:login', {'login': game[2]})
            return Game.create(
                id = int(game[0]),
                white = UserOut(login=white[0]) if white else None,
                black = UserOut(login=black[0]) if black else None,
                moves = game[3]
            )
        self._queue[login] = []

        return None
    
    async def makemove(self, game, move):
        game = game.makemove(move)

        db.run('update games set moves=:moves, end=:end where id=:id', {
            'moves': dumps([p.move for p in game.positions], default=vars),
            'end': game.end or '-',
            'id': game.id,
        })

        if game.white:
            if game.white not in self._queue:
                self._queue[game.white] = []
            self._queue[game.white].append(game)
        if game.black:
            if game.black not in self._queue:
                self._queue[game.black] = []
            self._queue[game.black].append(game)
        
        return game
    
    async def listen(self, login):
        game = await self.pickup(login)
        self._queue[login] = [game]

        while True:
            if login in self._queue:
                while len(self._queue[login]):
                    item = self._queue[login][0]
                    self._queue[login] = self._queue[login][1:]
                    yield f"event: message\ndata: {dumps(item, default=vars)}\n\n"
                await sleep(1)
            else:
                await sleep(1)


games = GameService()