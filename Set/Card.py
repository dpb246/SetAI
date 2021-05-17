#Simple card helper object, including functionality to determine if 3 cards make a set
from enum import Enum
from dataclasses  import dataclass

class COLOUR(Enum):
    ORANGE = 1
    PINK = 2
    GREEN = 3

class SHAPE(Enum):
    DIAMOND = 1
    OVAL = 2
    SQUIGGLE = 3

class SHADING(Enum):
    SOLID = 1
    STRIPED = 2
    OUTLINED = 3

@dataclass(frozen=True)
class Card:
    colour: COLOUR
    shape: SHAPE
    shading: SHADING
    count: int

    def __repr__(self):
        return f"[{self.colour.value}, {self.shape.value}, {self.shading.value}, {self.count}]"

def get_match(a: int, b: int):
    if a == b: return a
    return 6 - a - b

def check_set(card1: Card, card2: Card, card3: Card):
    #count
    if get_match(card1.count, card2.count) != card3.count:
        return False
    #shading
    if get_match(card1.shading.value, card2.shading.value)  != card3.shading.value:
        return False
    #shape
    if get_match(card1.shape.value, card2.shape.value)  != card3.shape.value:
        return False
    #colour
    if get_match(card1.colour.value, card2.colour.value)  != card3.colour.value:
        return False
    return True