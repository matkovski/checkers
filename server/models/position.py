from pydantic import BaseModel

from .constants import Piece, Color
from .move import Move

def steps(x, y, dx, dy):
    x += dx
    y += dy

    while x >= 0 and x <= 7 and y >= 0 and y <= 7:
        yield (x, y)
        x += dx
        y += dy

class Position(BaseModel):
    move: Move = None
    field: list[list[Piece]] = []
    turn: Color = 'w'

    @classmethod
    def start():
        position = Position()
        position.field = [
            ['-', 'c', '-', 'c', '-', 'c', '-', 'c'],
            ['c', '-', 'c', '-', 'c', '-', 'c', '-'],
            ['-', 'c', '-', 'c', '-', 'c', '-', 'c'],
            ['c', '-', 'c', '-', 'c', '-', 'c', '-'],
            ['-', '-', '-', '-', '-', '-', '-', '-'],
            ['-', '-', '-', '-', '-', '-', '-', '-'],
            ['-', '-', '-', '-', '-', '-', '-', '-'],
            ['-', '-', '-', '-', '-', '-', '-', '-'],
            ['-', 'C', '-', 'C', '-', 'C', '-', 'C'],
            ['C', '-', 'C', '-', 'C', '-', 'C', '-'],
            ['-', 'C', '-', 'C', '-', 'C', '-', 'C'],
            ['C', '-', 'C', '-', 'C', '-', 'C', '-'],
        ]
        position.turn = 'w'
        return position

    def allpossiblemoves(self):
        yield (1, 1)


    def move(self, move: Move, last: bool):
        # TODO check against allpossiblemoves
        
        child = Position()

        child.move = move
        child.field = [row[:] for row in self.field]
        child.field[move.srcy][move.srcx] = '-'
        child.field[move.dsty][move.dstx] = move.piece
        # TODO taking

        if last:
            child.turn = 'w' if self.turn == 'b' else 'b'

        return child

