import random
import dataclasses as dc
from primitives import Card
from move import Move
from gameutils import GameState

@dc.dataclass
class Player:
    hand: list[Card] = dc.field(default_factory=list, init=False)

    def nextMove(self, state: GameState, options: list[Move]) -> int:
        """Gets current game state and a non-empty list of available moves,
        must return an index of the move to make
        """
        raise NotImplementedError("Subclasses should implement that")

@dc.dataclass
class MrFirst(Player):
    def nextMove(self, state: GameState, options: list[Move]) -> int:
        return 0

@dc.dataclass
class MrRandom(Player):
    def nextMove(self, state: GameState, options: list[Move]) -> int:
        return random.randint(0, len(options) - 1) 
