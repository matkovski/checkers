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

class Move(BaseModel):
    movements: List[Movement]
