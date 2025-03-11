from fastapi import FastAPI

from api.authapi import router as authrouter

app = FastAPI()

app.include_router(authrouter)


