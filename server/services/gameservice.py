from random import randint
from json import dumps

from models.user import User, UserOut
from models.game import Game

from .dbservice import db

class GameService:
    async def pickup(self, user: User):
        game = db.row('select id, white, black, moves from games where white=:userid or black=:userid and end="-"', {'userid': user.id})
        if not game:
            game = db.row('select id, white, black, moves from games where white is null and black<>:userid or black is null and white<>:userid', {'userid': user.id})
            if game:
                db.run(f'update games set {"black" if game[1] else "white"}=:userid where id=:id', {'userid': user.id, 'id': game[0]})
        if not game:
            color = 'white' if randint(0, 1) else 'black'
            id = db.row('select max(id) from games')
            id = id[0] + 1 if id and id[0] else 1
            db.run(f'insert into games (id, {color}) values (:id, :userid)', {
                'id': id,
                'userid': user.id,
            })
            game = db.row('select id, white, black, moves from games where id=:id', {'id': id})
        
        if game:
            white = db.row('select * from users where id=:id', {'id': game[1]})
            black = db.row('select * from users where id=:id', {'id': game[2]})
            return Game.create(
                id = int(game[0]),
                white = UserOut(id=int(white[0]), login=white[1]) if white else None,
                black = UserOut(id=int(black[0]), login=black[1]) if black else None,
                moves = game[3]
            )

        return None
    
    async def makemove(self, game, move):
        game = game.makemove(move)

        db.run('update games set moves=:moves, end=:end where id=:id', {
            'moves': dumps([p.move for p in game.positions], default=vars),
            'end': game.end or '-',
            'id': game.id,
        })
        
        return game


games = GameService()