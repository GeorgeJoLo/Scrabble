from Player import *
from SakClass import *


class Game:
    def __init__(self):
        self.sak = SakClass()
        self.player1 = Player()
        self.player2 = Player()

    def __repr__(self):
        pass

    def setup(self):
        self.sak.randomize_sak()
        self._initialize_player(self.player1)
        self._initialize_player(self.player2)
        pass

    def run(self):
        pass

    def end(self):
        pass

    def _initialize_player(self, player):
        player.take_letters(self.sak.get_letters(7))
