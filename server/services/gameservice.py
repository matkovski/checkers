from asyncio import sleep
from random import randint
from json import dumps

from models.user import UserOut
from models.game import Game
from models.move import Move

from .dbservice import db

class GameService:
    def __init__(self):
        self._queue = {}

    async def pickup(self, login: str):
        notifyother = None
        game = db.row('select id, white, black, moves from games where white=:user or black=:user and (end="-" or end is null)', {'user': login})
        if not game:
            game = db.row('select id, white, black, moves from games where white is null and black<>:user or black is null and white<>:user', {'user': login})
            if game:
                db.run(f'update games set {"black" if game[1] else "white"}=:user where id=:id', {'user': login, 'id': game[0]})
                notifyother = game[1] or game[2]
                game = db.row('select id, white, black, moves from games where id=:id', {'id': game[0]})
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
            game = Game.create(
                id = int(game[0]),
                white = UserOut(login=white[0]) if white else None,
                black = UserOut(login=black[0]) if black else None,
                moves = game[3]
            )
            if notifyother:
                self._enqueue(notifyother, game)

            return game

        return None
    
    async def restart(self, login):
        game = await self.pickup(login)
        self._enqueue(login, game)

        return game
    
    async def makemove(self, game, move):
        game = game.makemove(move)

        db.run('update games set moves=:moves, end=:end where id=:id', {
            'moves': dumps([p.move for p in game.positions], default=vars),
            'end': game.end or '-',
            'id': game.id,
        })

        if game.white:
            self._enqueue(game.white, move)
        if game.black:
            self._enqueue(game.black, move)
        
        return game
    
    def _enqueue(self, login, data):
        if login in self._queue:
            print(f"Enqueue {(dumps(data, default=vars))} for {login}")
            self._queue[login].append(data)
    
    async def listen(self, login):
        game = await self.pickup(login)
        self._queue[login] = [game]

        while True:
            if login in self._queue:
                while len(self._queue[login]):
                    item = self._queue[login][0]
                    json = dumps(item, default=vars)
                    self._queue[login] = self._queue[login][1:]
                    if isinstance(item, Game):
                        yield f"event: game\ndata: {json}\n\n"
                    elif isinstance(item, Move):
                        yield f"event: move\ndata: {json}\n\n"
                await sleep(0.2)
            else:
                await sleep(0.2)


games = GameService()