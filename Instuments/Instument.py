from Game import Game
from abc import abstractmethod


class Instrument:
    def __init__(self, game: Game):
        self.game = game
    
    @abstractmethod
    def play(self, melody: list[int]):
        pass
    
