from pydantic import BaseModel
from json import loads

from .position import Position
from .move import Move
from .user import UserOut

class Game(BaseModel):
    id: int
    white: str
    black: str
    positions: list[Position]
    fen: str

    @classmethod
    def create(self, id: int, white: UserOut | None = None, black: UserOut | None = None, moves: str | None = None):
        moves = loads(moves) if moves else []
        position = Position.start()

        positions = []
        for mv in moves:
            if mv:
                position = position.makemove(Move(**mv))
            positions.append(position)
        
        return Game(
            id = id,
            white = white.login if white else '',
            black = black.login if black else '',
            positions = positions,
            fen = ''
        )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.positions:
            self.positions = [Position.start()]

        self._refreshfen()

    @property
    def position(self):
        if len(self.positions):
            return self.positions[-1]
        return None

    @property
    def turn(self):
        return self.position.turn

    def ended(self):
        return self.position.children()

    # TODO we dont need both ended and end
    @property
    def end(self):
        return ''

    def makemove(self, move: Move):
        pos = self.position

        next = pos.makemove(move)

        return Game(
            id = self.id,
            white = self.white,
            black = self.black,
            positions = self.positions + [next],
            fen = ''
        )

    def _refreshfen(self):
        pos = self.position

        if not pos:
            self.fen = '--------------------------------/w'

        field = pos.board()
        self.fen = ''
        for y in range(8):
            for x in range(8):
                if (x + y) % 2 == 0:
                    continue
                self.fen += field[y][x]
        
        self.fen += '/' + pos.turn
