from typing import List
from pydantic import BaseModel

from .constants import Piece

class Movement(BaseModel):
    piece: Piece
    srcx: int
    srcy: int
    dstx: int
    dsty: int
    take: Piece

    @classmethod
    def parse(self, data):
        return Movement(
            piece = data['piece'],
            srcx = data['srcx'],
            srcy = data['srcy'],
            dstx = data['dstx'],
            dsty = data['dsty'],
            take = data['take'],
        )


class Move(BaseModel):
    movements: List[Movement]

    @classmethod
    def parse(self, data):
        return Move(movements = [Movement.parse(mv) for mv in data['movements']])
