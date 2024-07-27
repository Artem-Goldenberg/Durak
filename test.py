import functools
from random import shuffle
from gameutils import GameState
from move import Move
from new import *
from primitives import *
from player import Player

def standardDeck() -> list[Card]:
    def allCardsFor(suit: Suit) -> list[Card]:
        return list(map(lambda value: Card(value, suit), CardValue))
    gen = functools.reduce(lambda acc, suit: acc + allCardsFor(suit), Suit, [])
    return list(gen)

def intersuitDeck() -> list[Card]:
    def allCardsFor(value: CardValue) -> list[Card]:
        return list(map(lambda suit: Card(value, suit), Suit))
    gen = functools.reduce(lambda acc, value: acc + allCardsFor(value), CardValue, [])
    return list(gen)

class MrLogger(Player):
    def nextMove(self, state: GameState, options: list[Move]) -> int:
        print(f"[{id(self)}]Choosing move for:\n{state}\nand for: {options}\n")
        return 0
    
six = CardValue.Six
seven = CardValue.Seven
eight = CardValue.Eight
nine = CardValue.Nine
ten = CardValue.Ten
jack = CardValue.Jack
queen = CardValue.Queen
king = CardValue.King
ace = CardValue.Ace

heart = Suit.Heart
spade = Suit.Spade
cross = Suit.Cross
diamond = Suit.Diamond

def sortofGeneralTest():
    deck = intersuitDeck()
    p1 = MrLogger()
    p2 = MrLogger()
    g = Game(deck, p1, p2)

    assert g.trump == Card(nine, heart)

    p1Hand = [
        Card(six, heart), Card(six, spade), 
        Card(seven, heart), Card(seven, spade),
        Card(eight, heart), Card(eight, spade)
    ]
    p2Hand = [
        Card(six, cross), Card(six, diamond), 
        Card(seven, cross), Card(seven, diamond), 
        Card(eight, cross), Card(eight, diamond)
    ]
    assert p1.hand == p1Hand
    assert p2.hand == p2Hand

    assert g.turn == g.move == Switch.First

    print(g.kickoff())
    

def test1():
    deck = standardDeck()
    print(deck)
    # shuffle(deck)
    # p1 = TestPlayer()
    # p2 = TestPlayer()
    # g = Game(deck, p1, p2)


if __name__ == "__main__":
    sortofGeneralTest()
    # test1()