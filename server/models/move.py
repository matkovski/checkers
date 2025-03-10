from pydantic import BaseModel

from .constants import Piece

class Move(BaseModel):
    piece: Piece
    srcx: int
    srcy: int
    dstx: int
    stty: int
    take: Piece
