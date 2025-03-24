from random import randint

from models.user import User, UserOut
from models.game import Game

from .dbservice import db

class GameService:
    async def pickup(self, user: User):
        game = db.row('select id, white, black, moves from games where white=:userid or black=:userid and end is null', {'userid': user.id})
        if not game:
            game = db.row('select id, white, black, moves from games where (white is null or black is null) and white<>:userid and black<>:userid', {'userid': user.id})
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
                id = game[0],
                white = UserOut(id=white[0], login=white[1]) if white else None,
                black = UserOut(id=black[0], login=black[1]) if black else None,
                moves = game[3]
            )

        return None
    
    async def addmove(self, game, move):
        game = game.move(move)
        
        if game:


games = GameService()