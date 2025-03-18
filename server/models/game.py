from pydantic import BaseModel
from json import loads

from .position import Position
from .move import Move
from .user import UserOut

class Game(BaseModel):
    white: str
    black: str
    positions: list[Position]

    @classmethod
    def create(self, white: UserOut | None = None, black: UserOut | None = None, moves: str | None = None):
        moves = loads(moves) if moves else []
        position = Position.start()

        positions = [position]
        for mv in moves:
            position = position.move(Move(**mv))
            positions.append(position)
        
        return Game(
            white = white.login if white else '',
            black = black.login if black else '',
            positions = positions,
        )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.positions:
            self.positions = [Position.start()]

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

    def move(self, moves: list[Move]):
        # TODO
        pass
