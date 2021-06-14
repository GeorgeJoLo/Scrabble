from Player import *
from SakClass import *
import random


class Game:
    def __init__(self):
        self.sak = SakClass()
        self.human = Human()
        self.algorithm = '1'
        self.computer = Computer(self.algorithm)
        self.playing = None

    def __repr__(self):
        return f'Class: {self.__class__}, algorithm = {self.algorithm}, playing = {self.playing.__class__}'

    def __str__(self):
        """
        Εμφανίζει την κατάσταση του παιχνιδιού αν τελείωνε την δεδομένη στηγμή.
        """
        if (self.computer.score > self.human.score):
            return "Νικητής ο Η/Υ με Σκορ: " + str(self.computer.score)+'\n'\
                   +"Σκορ Παίκτη: " + str(self.human.score)
        elif (self.computer.score < self.human.score):
            return "Νικητής ο Παίκτης με Σκορ: " + str(self.human.score)+'\n'\
                   +"Σκορ Η/Υ: " + str(self.computer.score)
        else:
            return "Ισοπαλία"+'\n'\
                   +"Σκορ Η/Υ: " + str(self.computer.score)+'\n'\
                   +"Σκορ Παίκτη: " + str(self.human.score)

    def setup(self):
        self.sak = SakClass()
        self.human = Human()
        self.computer = Computer(self.algorithm)
        self.sak.randomize_sak()
        self._initialize_player(self.human)
        self._initialize_player(self.computer)
        self.playing = random.choice([self.human, self.computer])

    def menu(self):
        print("***** SCRABBLE *****")
        print("--------------------")
        print("1: Σκορ")
        print("2: Ρυθμίσεις")
        print("3: Παιχνίδη")
        print("4: Έξοδος")
        print("--------------------")

        menu_choice = input("Επιλογή Μενού: ")
        if menu_choice == '1':
            # TODO δειξε το σκορ
            print("Σκορ :")
            game.menu()

        if menu_choice == '2':
            game.settings()
            game.menu()

        if menu_choice == '3':
            game.run()
            game.menu()

        if menu_choice == '4':
            print("---- Έξοδος ----")
            exit()

        print("--------------------")
        print("Πληκρολόγησε 1, 2, 3 ή 4")
        print("--------------------")
        game.menu()

    def settings(self):
        print("***** Ρυθμίσεις *****")
        print("---------------------")
        print("1: MIN_letters")
        print("2: MAX_letters")
        print("3: SMART")
        print("4: FAIL")
        print("---------------------")

        settings_choice = input("Επιλογή Ρυθμίσεων: ")
        if settings_choice == '1' or settings_choice == '2' or settings_choice == '3' or settings_choice == '4':
            self.algorithm = settings_choice

        print("--------------------")
        print("Πληκρολόγησε 1, 2, 3 ή 4")
        print("--------------------")

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
        print("----------------------------------------------------------")
        print("Τέλος παιχνιδιού")
        print(self)

        # TODO να βαλουμε το Σκορ σε αρχειο

    def _initialize_player(self, player):
        player.take_letters(self.sak.get_letters(7))

    def store_score(self):
        pass



if __name__ == '__main__':
    game = Game()
    game.menu()
