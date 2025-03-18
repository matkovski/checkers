from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from api.authapi import router as authrouter
from api.gameapi import router as gamerouter

app = FastAPI()

app.include_router(authrouter)
app.include_router(gamerouter)
app.mount('/', StaticFiles(directory = '../client/dist/', html = True))