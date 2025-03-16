from pydantic import BaseModel

from .position import Position
from .move import Move
from .user import UserOut

class Game(BaseModel):
    white: str
    black: str
    positions: list[Position]

    @classmethod
    def create(self, white: UserOut, black: UserOut, moves: str):
        return Game()

    def __init__(self, position: Position = None):
        self.positions = [position if position else Position.start()]

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
