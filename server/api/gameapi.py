from typing import Annotated
from fastapi import APIRouter, Header

from models.game import Game
from models.position import Position
from models.move import Move
from models.error import Error
from models.user import UserOut

from services.authservice import auth as auth
from services.dbservice import db

router = APIRouter('/api/game')

@router.get('/running', response_model=Game)
async def running(token: Annotated[str, Header(alias = 'x-token')] = None):
    user = await auth.findsession(token)
    if not user:
        return Error(errors = ['not authenticated'])
    
    game = db.query('select id, white, black, moves from games where white=? or black=? and end is null')
    if len(game):
        white = db.row('select * from users where id=?', (game[0],))
        black = db.row('select * from users where id=?', (game[1],))
        return Game.create(UserOut(id=white[0], login=white[1]), UserOut(id=black[0], login=black[1]), game[2])
    pass

