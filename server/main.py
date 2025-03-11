from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from api.authapi import router as authrouter

app = FastAPI()

app.include_router(authrouter)
app.mount('/', StaticFiles(directory = '../client/dist/', html = True))