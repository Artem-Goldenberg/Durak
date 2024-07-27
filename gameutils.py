from primitives import Card, CardValue
import dataclasses as dc


@dc.dataclass
class Table:
    """A representation of a card battle happening on the table"""
    attack: list[Card] = dc.field(default_factory=list)
    defense: list[Card] = dc.field(default_factory=list)
    isForfeited: bool = False

    @property
    def isEmpty(self) -> bool:
        return not self.attack
    
    def getTossableValues(self) -> set[CardValue]:
        valueGetter = lambda card: card.value
        # challenge: can you make it better?
        return set(map(valueGetter, self.attack + self.defense))
    
    def clear(self):
        self.attack.clear()
        self.defense.clear()
        self.isForfeited = False


@dc.dataclass(frozen=True)
class GameConfiguration:
    ## CC - card count
    InitialDeckCC: int = 36
    HandCC: int = 6
    ## BD - before discard, AD - after discard
    # first discard - not more than 5 cards on the table, 
    MaxTossBD: int = HandCC - 1
    MaxTossAD: int = HandCC


@dc.dataclass(frozen=True)
class GameState:
    """This is a snapshot of a current game state that players are allowed to see"""
    ## CC - card count
    deckCC: int
    trumpCard: Card
    table: Table
    discardPile: set[Card]
