from Player import *
from SakClass import *
import random


class Game:
    def __init__(self):
        self.sak = SakClass()
        self.human = Human()
        self.computer = Computer(algorithm=1)
        self.playing = None

    def __repr__(self):
        pass

    def setup(self):
        self.sak.randomize_sak()
        self._initialize_player(self.human)
        self._initialize_player(self.computer)
        # self.playing = random.choice([self.human, self.computer])
        self.playing = self.human

    def run(self):
        self.setup()

        while True:
            if not self.playing.play(self.sak):
                break

            if self.playing == self.human:
                self.playing = self.computer
            else:
                self.playing = self.human

        self.end()

    def end(self):
        pass

    def _initialize_player(self, player):
        player.take_letters(self.sak.get_letters(7))


game = Game()
game.run()
