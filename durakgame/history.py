import dataclasses as dc
from typing import Generator

from .primitives import GameResult, Card
from .move import Move

@dc.dataclass
class GameHistory:
    p1StartHand: list[Card]
    p2StartHand: list[Card]
    startDeck: list[Card]
    p1Moves: list[Move] = dc.field(default_factory=list, init=False)
    p2Moves: list[Move] = dc.field(default_factory=list, init=False)
    result: GameResult = dc.field(default=GameResult.Unfinished, init=False)

    @property
    def moveSequence(self) -> Generator[Move, None, None]:
        for move1, move2 in zip(self.p1Moves, self.p2Moves):
            yield move1
            yield move2
