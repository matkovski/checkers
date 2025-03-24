from typing import Annotated, Union
from fastapi import APIRouter, Header
from random import randint

from models.game import Game
from models.move import Move
from models.error import Error

from services.authservice import auth as auth
from services.gameservice import games

router = APIRouter(prefix = '/api/game')

@router.get('/pickup', response_model = Union[Game, Error])
async def pickup(token: Annotated[str, Header(alias = 'x-token')] = None):
    user = await auth.finduser(token)
    if not user:
        return Error(errors = ['not authenticated'])
    
    return await games.pickup(user)

@router.post('/move', response_model = Union[Game, Error])
async def move(move: Move, token: Annotated[str, Header(alias = 'x-token')] = None):
    user = await auth.finduser(token)
    if not user:
        return Error(errors = ['not authenticated'])

    game = await games.pickup(user)
    if not game:
        return Error(errors = ['no running game'])
    
    if not game.white or not game.black:
        return Error(errors = ['game not started, waiting for opponent'])
    
    if game.ended():
        return Error(errors = ['game ended with ' + game.ended()])
    
    if game.white != user.login and game.black != user.login:
        return Error(errors = ['it is not your game'])
    
    color = 'w' if game.white == user.login else 'b'

    if game.turn != color:
        return Error(errors = ['it is not your turn'])
    
    return await games.makemove(game, move)
