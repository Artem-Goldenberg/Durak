import dataclasses as dc
from primitives import Card

@dc.dataclass
class Move:
    """Base class for all kinds of moves you can do in Durak"""

@dc.dataclass
class AttackingMove(Move):
    """Move to continue attack by throwing another `card` on the table"""
    card: Card

@dc.dataclass
class DefensiveMove(Move):
    """Move to defend against current attacking card on the table with `card`"""
    card: Card

@dc.dataclass
class ForfeitingMove(Move):
    """Move to forfeit the table and take all the cards on it"""

@dc.dataclass
class OpeningMove(Move):
    """Move when your turn has just started"""
    card: Card

@dc.dataclass
class EndingMove(Move):
    """Move to end your turn and throw cards to the discard pile"""

@dc.dataclass
class FinishingMove(Move):
    """When your opponent forfeits the table, finish them off by giving more cards to them.
    This move also implies an EndingMove
    """
    cards: list[Card]
