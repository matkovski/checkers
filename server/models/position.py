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
    turn: Color = 'w'
    _field: list[list[Piece]] = []

    @classmethod
    def start(self):
        position = Position()
        position._field = [
            ['-', 'c', '-', 'c', '-', 'c', '-', 'c'],
            ['c', '-', 'c', '-', 'c', '-', 'c', '-'],
            ['-', 'c', '-', 'c', '-', 'c', '-', 'c'],
            ['-', '-', '-', '-', '-', '-', '-', '-'],
            ['-', '-', '-', '-', '-', '-', '-', '-'],
            ['C', '-', 'C', '-', 'C', '-', 'C', '-'],
            ['-', 'C', '-', 'C', '-', 'C', '-', 'C'],
            ['C', '-', 'C', '-', 'C', '-', 'C', '-'],
        ]
        position.turn = 'w'
        return position

    def children(self):
        # TODO
        return []

    def board(self):
        return self._field

    def makemove(self, move: Move):
        # TODO check against children
        
        child = Position()

        child.move = move
        child.turn = 'w' if self.turn == 'b' else 'b'
        child._field = [row[:] for row in self._field]
        for mv in move.movements:
            child._field[mv.srcy][mv.srcx] = '-'
            child._field[mv.dsty][mv.dstx] = mv.piece
            # TODO taking


        return child

