from typing import Union, Annotated
from fastapi import APIRouter, Header

from models.user import UserIn, UserOut
from models.login import Login
from models.error import Error
from services.authservice import auth

router = APIRouter(prefix = '/api/auth')

@router.get('/shake', response_model = Union[UserOut, Error])
async def shake(token: Annotated[str, Header(alias = 'x-token')] = None):
    user = await auth.finduser(token)

    if user:
        return user
    
    return Error(errors = ['not authenticated'])

@router.post('/login', response_model = Union[str, Error])
async def login(login: Login):
    token = await auth.login(login.login, login.pwd)

    if token:
        return token
    
    return Error(errors = ['user not found'])

@router.post('/register', response_model = Union[str, Error])
async def register(userin: UserIn):
    user = await auth.register(userin)

    if user:
        return user.code

    return Error(errors = ['could not register'])

@router.get('/confirm', response_model = Union[UserOut, Error])
async def confirm(code: str):
    user = await auth.confirm(code)

    if user:
        return user
    
    return Error(errors = ['could not confirm'])

@router.get('/logout', response_model = bool)
async def logout(token: Annotated[str, Header(alias = 'x-token')] = None):
    ok = await auth.logout(token)

    return ok