from pydantic import BaseModel
from json import loads

from .position import Position
from .move import Move
from .user import UserOut

class Game(BaseModel):
    id: str
    white: str
    black: str
    positions: list[Position]
    fen: str

    @classmethod
    def create(self, id: str, white: UserOut | None = None, black: UserOut | None = None, moves: str | None = None):
        moves = loads(moves) if moves else []
        position = Position.start()

        positions = [position]
        for mv in moves:
            position = position.move(Move(**mv))
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
    def turn(self):
        if len(self.positions):
            return self.positions[0].turn
        else:
            return None

    def ended(self):
        pos = self.positions[-1] if len(self.positions) else None

        if pos:
            return len(pos.children())
        else:
            return False

    def makemove(self, move: Move):
        # TODO
        self._refreshfen()

    def _refreshfen(self):
        pos = self.positions[-1]

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
