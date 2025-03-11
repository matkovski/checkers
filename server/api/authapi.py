from typing import Union, Annotated
from fastapi import APIRouter, Header

from models.user import UserIn, UserOut
from models.login import Login
from models.error import Error
from services.authservice import authservice

router = APIRouter(prefix = '/api/auth')

@router.get('/shake', response_model = Union[UserOut, Error])
async def shake(token: Annotated[str, Header(alias = 'x-token')] = None):
    user = await authservice.findsession(token)

    if user:
        return user
    
    return Error(errors = ['not authenticated'])

@router.post('/login', response_model = Union[str, Error])
async def login(login: Login):
    token = await authservice.login(login.login, login.pwd)

    if token:
        return token
    
    return Error(errors = ['user not found'])

@router.post('/register', response_model = Union[UserOut, Error])
async def register(userin: UserIn):
    user = await authservice.register(userin)

    if user:
        return user

    return Error(errors = ['could not register'])

@router.get('/confirm', response_model = Union[UserOut, Error])
async def confirm(code: str):
    user = await authservice.confirm(code)

    if user:
        return user
    
    return Error(errors = ['could not confirm'])

@router.get('/logout', response_model = bool)
async def logout(token: Annotated[str, Header(alias = 'x-token')] = None):
    ok = await authservice.logout(token)

    return ok