from dataclasses import dataclass, field
from primitives import Suit, Card, Turn


@dataclass
class Player:
    game: 'Game'
    turn: Turn
    hand: list[Card] = field(default_factory=list)

    def play(self, card: Card):
        """Plays one card, when it's this player's turn"""
        self.assertTurn()
        if card not in self.hand:
            raise RuntimeError("Don't have that card")
        
        card, *newHand = self.hand
        self.game.table.player.append(card)
        self.hand = newHand
    
    def playAt(self, index: int):
        self.assertTurn()
        card = self.hand.pop(index)
        self.game.table.player.append()

    def add(self, card: Card):
        """Toss in one more card on the table for the opponent to beat"""
        pass

    def beat(self, card: Card, withCard: Card):
        pass

    def beatAt(self, index: int, withCardAt: int):
        pass

    def take(self):
        pass

    def assertTurn(self):
        if self.game.turn != self.turn:
            raise RuntimeError("Not your turn")


@dataclass
class Table:
    game: 'Game'
    player: list[Card]
    opponent: list[Card]

    def clear(self):
        self.player.clear()
        self.opponent.clear()
    
    def place(self, card: Card):
        assert len(self.player) == len(self.opponent)
        if not self.validPlacing(card):
            raise RuntimeError("Can't place that card")
        self.player.append(card)
    
    def beat(self, card: Card):
        assert len(self.player) == len(self.opponent) + 1
        if not self.canBeat(card, self.player[-1]):
            raise RuntimeError("Can't beat with this card")
        self.opponent.append(card)
    

    def validPlacing(self, card: Card) -> bool:
        for mine, his in zip(self.player, self.opponent):
            if mine.value == card.value or his.value == card.value:
                return True
        return False
    
    def canBeat(self, card: Card, another: Card) -> bool:
        if self.game.isTrump(card):
            return card.value > another.value
        return card.suit == another.suit and card.value > another.value


@dataclass
class Game:
    DeckCount: int = 36
    HandCount: int = 6

    player1: Player
    player2: Player

    deck: list[Card]
    trump: Card

    table: Table
    turn: Turn

    def __init__(self, shuffled: list[Card]):
        assert len(set(shuffled)) == self.DeckCount

        self.player1 = Player(self, 1)
        self.player2 = Player(self, 1)
        i = 0
        for _ in range(self.HandCount):
            self.player1.hand.append(shuffled[i])
            self.player2.hand.append(shuffled[i + 1])
            i += 2
 
        self.trump = shuffled[i].suit
        self.deck = shuffled[i + 1 :] + [self.trump]
        self.table = Table([], [])
    
    def isTrump(self, card: Card) -> bool:
        return card.suit == self.trump.suit
