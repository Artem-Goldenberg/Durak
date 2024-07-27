import dataclasses as dc
import itertools
from typing import Sequence
from player import Player
from move import *
from gameutils import *
from primitives import *


@dc.dataclass
class Game:
    """Manages the flow of the durak game, letting players choose their moves"""

    deck: list[Card]

    player1: Player
    player2: Player

    # turn is a big rotation, defines who's attacking and who's defending
    turn: Switch = dc.field(default=Switch.First, init=False)
    # move is smaller, it goes from player to player allowing one to attack and the other to defend
    move: Switch = dc.field(default=Switch.First, init=False)

    trump: Card = dc.field(init=False)
    table: Table = dc.field(default_factory=Table, init=False)
    discardPile: set[Card] = dc.field(default_factory=set, init=False)

    config: GameConfiguration = dc.field(default_factory=GameConfiguration)

    @property
    def isFinished(self) -> bool:
        if not self.table.isEmpty:
            return False
        if not self.player1.hand or not self.player2.hand:
            return True
        return False
    
    @property
    def state(self) -> GameState:
        return GameState(
            deckCC=len(self.deck),
            trumpCard=self.trump,
            table=self.table,
            discardPile=self.discardPile,
        )
    
    @property
    def currentPlayer(self) -> Player:
        match self.move:
            case Switch.First: return self.player1
            case Switch.Second: return self.player2
    
    @property
    def currentOpponent(self) -> Player:
        match self.move:
            case Switch.First: return self.player2
            case Switch.Second: return self.player1

    def __post_init__(self):
        assert len(set(self.deck)) == self.config.InitialDeckCC

        i = 0
        for _ in range(self.config.HandCC):
            self.player1.hand.append(self.deck[i])
            self.player2.hand.append(self.deck[i + 1])
            i += 2
 
        self.trump = self.deck[i]
        self.deck = self.deck[i + 1 :] + [self.trump]
    
    def kickoff(self, numberOfTurns: int | None = None) -> GameResult:
        turns = 0
        while not self.isFinished:
            oldTurn = self.turn
            if numberOfTurns is not None and turns >= 2 * numberOfTurns:
                return GameResult.Unfinished
            options = self.generateOptions()
            index = self.currentPlayer.nextMove(self.state, options)
            self.process(options[index])
            if self.turn != oldTurn:
                turns += 1
        
        match not self.player1.hand, not self.player2.hand:
            case True, True: # both hands are empty
                return GameResult.Draw
            case True, False:
                return GameResult.Win
            case False, True:
                return GameResult.Loss
            case False, False:
                return GameResult.Unfinished
        assert False
    
    def generateOptions(self) -> list[Move]:
        """Generates a list of all available moves in the current state
        The list is empty if game is finished.
        """
        if self.table.isEmpty:
            assert self.turn == self.move
            # it's an opening stage, can start with any card
            return list(map(OpeningMove, self.currentPlayer.hand))
        
        if self.turn == self.move: # we are attacking
            return self.generateAttackOptions()
        
        # we are defending
        return self.generateDefenseOptions()
        
    def generateAttackOptions(self) -> list[Move]:
        cards = self.currentPlayer.hand
        tossableValues = self.table.getTossableValues()

        maxCards = self.config.MaxTossAD if self.discardPile else self.config.MaxTossBD
        if len(self.table.defense) == maxCards:
            # just random assert
            assert not self.table.isForfeited
            return [EndingMove()]

        attackCards = list(filter(lambda card: card.value in tossableValues, cards))

        if self.table.isForfeited:
            # initial opponent's card count
            opponentCC = len(self.table.defense) + len(self.currentOpponent.hand)
            cardsToToss = min(opponentCC, self.config.HandCC) - len(self.table.attack)

            result: list[Move] = []
            n = min(len(attackCards), cardsToToss)
            for k in range(n + 1):
                # k is amount of cards we will be tossing in
                variants = itertools.combinations(attackCards, k)
                moves = map(FinishingMove, map(list, variants))
                result += list(moves)
            
            return result

        result = list(map(AttackingMove, attackCards))
        return result + [EndingMove()]
    
    def generateDefenseOptions(self) -> list[Move]:
        assert len(self.table.attack) == len(self.table.defense) + 1

        cards = self.currentPlayer.hand
        cardToBeat = self.table.attack[-1]
        defendCards = filter(lambda card: self.canBeat(card, cardToBeat), cards)

        result: list[Move] = list(map(DefensiveMove, defendCards))
        return result + [ForfeitingMove()]

    def process(self, move: Move):
        """Method that actually makes changes to the game fields according to the move
        We do not check for correctness of the move here, it is not needed"""

        match move:
            case OpeningMove(card) | AttackingMove(card):
                assert self.turn == self.move # TODO: remove
                self.currentPlayer.hand.remove(card)
                self.table.attack.append(card)
                self.toggleMove()
            case DefensiveMove(card):
                assert self.turn != self.move # TODO: remove
                self.currentPlayer.hand.remove(card)
                self.table.defense.append(card)
                self.toggleMove()
            case ForfeitingMove():
                assert self.turn != self.move # TODO: remove
                self.table.isForfeited = True
                self.toggleMove()
            case EndingMove():
                assert self.turn == self.move # TODO: remove
                self.discardPile = self.discardPile.union(self.table.attack, self.table.defense)
                self.table.clear()
                self.takeCards(self.currentPlayer)
                self.takeCards(self.currentOpponent)
                self.toggleTurn()
            case FinishingMove(cards):
                assert self.turn == self.move # TODO: remove
                assert self.table.isForfeited # TODO: remove
                self.currentOpponent.hand += self.table.defense
                self.currentOpponent.hand += self.table.attack
                self.currentOpponent.hand += cards
                self.table.clear()
                self.takeCards(self.currentPlayer)
            case _:
                assert False

    def toggleMove(self):
        self.move = self.move.toggled()

    def toggleTurn(self):
        assert self.table.isEmpty
        self.toggleMove()
        self.turn = self.turn.toggled()

    def takeCards(self, p: Player):
        neededCC = max(self.config.HandCC - len(p.hand), 0)
        cardsToTake = min(neededCC, len(self.deck))
        p.hand.extend(self.deck[:cardsToTake])
        self.deck = self.deck[cardsToTake:]

    def canBeat(self, card: Card, another: Card) -> bool:
        if self.isTrump(card):
            return not self.isTrump(another) or card.value > another.value 
        return card.suit == another.suit and card.value > another.value
    
    def isTrump(self, card: Card) -> bool:
        return card.suit == self.trump.suit
