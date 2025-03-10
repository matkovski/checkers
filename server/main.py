from typing import Union

from models.move import Move

from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def root():
    return {"one": 1}

@app.post('/')
def item(move: Move):
    move.piece = 'Q'
    return move