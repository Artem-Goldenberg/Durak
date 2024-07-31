from enum import Enum, auto
import functools
import random

from .primitives import Card, Suit, CardValue
from .gameutils import GameConfiguration
from .history import GameHistory
from .player import Player
from .game import Game


class DeckShuffle(Enum):
    random = auto()
    sortBySuit = auto()
    sortByValue = auto()
    custom = auto()


def standardDeck() -> list[Card]:
    def allCardsFor(suit: Suit) -> list[Card]:
        return list(map(lambda value: Card(value, suit), CardValue))
    gen = functools.reduce(lambda acc, suit: acc + allCardsFor(suit), Suit, [])
    return list(gen)


def play(
    p1: Player, p2: Player, 
    shuffleType: DeckShuffle = DeckShuffle.random, 
    customDeck: list[Card] | None = None,
    gameConfig: GameConfiguration | None = None,
    moveLimit: int | None = None
) -> GameHistory:
    deck = standardDeck()
    match shuffleType:
        case DeckShuffle.random:
            random.shuffle(deck)
        case DeckShuffle.sortBySuit:
            deck.sort(key=lambda card: (card.suit, card.value))
        case DeckShuffle.sortByValue:
            deck.sort(key=lambda card: (card.value, card.suit))
        case DeckShuffle.custom:
            assert customDeck is not None
            deck = customDeck
    
    if gameConfig != None:
        g = Game(deck, p1, p2, config=gameConfig)
    else:
        g = Game(deck, p1, p2)
    
    g.kickoff(numberOfMoves=moveLimit)

    return g.history
