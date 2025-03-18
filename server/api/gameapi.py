from typing import Annotated, Union
from fastapi import APIRouter, Header
from random import randint

from models.game import Game
from models.error import Error
from models.user import UserOut

from services.authservice import auth as auth
from services.dbservice import db

router = APIRouter(prefix = '/api/game')

@router.get('/running', response_model=Union[Game | Error | None])
async def running(token: Annotated[str, Header(alias = 'x-token')] = None):
    user = await auth.findsession(token)
    if not user:
        return Error(errors = ['not authenticated'])
    
    game = db.row('select id, white, black, moves from games where white=:userid or black=:userid and end is null', {'userid': user.id})
    if len(game):
        white = db.row('select * from users where id=:id', {'id': game[1]})
        black = db.row('select * from users where id=:id', {'id': game[2]})
        return Game.create(UserOut(id=white[0], login=white[1]), UserOut(id=black[0], login=black[1]), game[2])
    else:
        return None

@router.get('/pickup', response_model=Union[Game | Error | None])
async def pickup(token: Annotated[str, Header(alias = 'x-token')] = None):
    user = await auth.findsession(token)
    if not user:
        return Error(errors = ['not authenticated'])
    
    game = db.row('select id, white, black, moves from games where white=:userid or black=:userid and end is null', {'userid': user.id})
    if not game:
        game = db.row('select id, white, black, moves from games where (white is null or black is null) and white<>:userid and black<>:userid', {'userid': user.id})
    if not game:
        color = 'white' if randint(0, 1) else 'black'
        id = db.row('select max(id) from games')
        id = id[0] + 1 if id else 1
        db.run(f'insert into games (id, {color}) values (:id, :userid)', {
            'id': id,
            'userid': user.id,
        })
        game = db.row('select id, white, black, moves from games where id=:id', {'id': id})
    
    if game:
        white = db.row('select * from users where id=:id', {'id': game[1]})
        black = db.row('select * from users where id=:id', {'id': game[2]})
        return Game.create(UserOut(id=white[0], login=white[1]), UserOut(id=black[0], login=black[1]), game[2])
    else:
        return None
