from pydantic import BaseModel

from .constants import Piece, Color
from .move import Move, Movement

bvalues = [
    [0, 3, 0, 3, 0, 3, 0, 3],
    [2, 0, 2, 0, 2, 0, 2, 0],
    [0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 2, 0, 2, 0, 1, 0],
    [0, 2, 0, 4, 0, 4, 0, 2],
    [3, 0, 6, 0, 6, 0, 3, 0],
    [0, 5, 0, 8, 0, 8, 0, 5],
    [5, 0, 9, 0, 9, 0, 6, 0],
]
wvalues = [row[::-1] for row in bvalues[::-1]]

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
    field: list[list[Piece]] = []

    @classmethod
    def start(self):
        position = Position()
        position.board = [
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

    def possiblemoves(self):
        dirs = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        moves = []
        for y, row in enumerate(self.field):
            for x, pc in enumerate(row):
                if pc == '-':
                    continue
                for dx, dy in dirs:
                    moves += self.getmoves(x, y, dx, dy)

        return moves
    
    def children(self):
        moves = self.possiblemoves()
        return [self.makemove(move) for move in moves]
    
    @property
    def value(self):
        result = 0
        for y, row in enumerate(self.field):
            for x, pc in enumerate(row):
                if pc == '-':
                    continue
                coef = 10 if pc == 'q' or pc == 'Q' else 1
                if pc == 'C' or pc == 'Q':
                    result += coef * wvalues[y][x]
                else:
                    result -= coef * bvalues[y][x]

        return result
    
    @property
    def bottom2(self):
        return min(1000000000, *[p.value for p in self.children()])

    @property
    def top2(self):
        return max(-1000000000, *[p.value for p in self.children()]);


    @property
    def board(self):
        return self.field
    
    @board.setter
    def board(self, board):
        self.field = board

    def makemove(self, move: Move):
        # TODO check against children
        
        field = [row[:] for row in self.field]
        for mv in move.movements:
            x0 = mv.srcx
            y0 = mv.srcy
            x1 = mv.dstx
            y1 = mv.dsty
            piece = 'q' if mv.piece == 'c' and y1 == 7 else ('Q' if mv.piece == 'C' and y1 == 0 else mv.piece)
            field[y0][x0] = '-'
            field[y1][x1] = piece
            if mv.take:
                stepx = 1 if x1 > x0 else -1
                stepy = 1 if y1 > y0 else -1
                i = 1
                while x0 + stepx * i != x1:
                    field[y0 + stepy * i][x0 + stepx * i] = '-'
                    i += 1

        turn = 'b' if self.turn == 'w' else 'w'

        position = Position(move = move, turn = turn)
        position.board = field

        return position
    
    def getmoves(self, x, y, dx, dy):
        moves = []
        if x + dx < 0 or x + dx > 7 or y + dy < 0 or y + dy > 7:
            return moves

        pc = self.field[y][x]
        if pc in ('c', 'q') and self.turn == 'w' or pc in ('C', 'Q') and self.turn == 'b' or pc == 'c' and dy <= 0 or  pc == 'C' and dy >= 0:
            return moves

        enemies = ('C', 'Q') if pc in ('c', 'q') else ('c', 'q')
        friends = ('c', 'q') if pc in ('c', 'q') else ('C', 'Q')

        if pc == 'c' or pc == 'C':
            if self.field[y + dy][x + dx] == '-':
                moves.append(Move(movements = [
                    Movement(piece = pc, srcx = x, srcy = y, dstx = x + dx, dsty = y + dy, take = '-')
                ]))
    
            if x + dx * 2 >= 0 and x + dx * 2 <= 7 and y + dy * 2 >= 0 and y + dy * 2 <= 7:
                if self.field[y + dy][x + dx] in enemies and self.field[y + dy * 2][x + dx * 2] == '-':
                    moves.append(Move(movements = [
                        Movement(piece = pc, srcx = x, srcy = y, dstx = x + dx * 2, dsty = y + dy * 2, take = self.field[y + dy][x + dx])
                    ]))

        if pc == 'Q' or pc == 'q':
            taken = False
            i = 1
            while True:
                if x + dx * i < 0 or x + dx * i > 7 or y + dy * i < 0 or y + dy * i > 7:
                    break
                if self.field[y + dy * i][x + dx * i] in friends:
                    break

                if self.field[y + dy * i][x + dx * i] == '-':
                    moves.append(Move(movements = [
                        Movement(piece = pc, srcx = x, srcy = y, dstx = x + dx * i, dsty = y + dy * i, take = '-')
                    ]))

                if x + dx * (i + 1) < 0 or x + dx * (i + 1) > 7 or y + dy * (i + 1) < 0 or y + dy * (i + 1) > 7:
                    break

                if not taken and self.field[y + dy * i][x + dx * i] in enemies and self.field[y + dy * (i + 1)][x + dx * (i + 1)] == '-':
                    taken = True
                    moves.append(Move(movements = [
                        Movement(piece = pc, srcx = x, srcy = y, dstx = x + dx * (i + 1), dsty = y + dy * (i + 1), take = self.field[y + dy * i][x + dx * i])
                    ]))

                i += 1

        return moves


