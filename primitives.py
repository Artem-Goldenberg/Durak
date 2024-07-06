from dataclasses import dataclass
from enum import Enum, auto

class Suit(Enum):
    Heart = 0
    Cross = 1
    Spade = 2
    Diamond = 3

class Value(Enum):
    Six = auto()
    Seven = auto()
    Eight = auto()
    Nine = auto()
    Ten = auto()
    Jack = auto()
    Queen = auto()
    King = auto()
    Ace = auto()

@dataclass
class Card:
    suit: Suit
    value: Value

class Turn(Enum):
    First = 1
    Second = 2