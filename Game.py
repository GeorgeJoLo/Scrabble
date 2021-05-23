from Player import *
from SakClass import *
import random


class Game:
    def __init__(self):
        self.sak = SakClass()
        self.player1 = Human()
        self.player2 = Computer(algorithm=1)
        self.playing = None

    def __repr__(self):
        pass

    def setup(self):
        self.sak.randomize_sak()
        self._initialize_player(self.player1)
        self._initialize_player(self.player2)
        self.playing = random.choice([self.player1, self.player2])
        # TODO ...

    def run(self):
        self.playing.play(self.sak)
        pass

    def end(self):
        pass

    def _initialize_player(self, player):
        player.take_letters(self.sak.get_letters(7))

    def _write_word(self):
        pass
