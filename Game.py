from Player import *
from SakClass import *
import random
from datetime import date
import json


class Game:
    def __init__(self):
        self.sak = SakClass()
        self.human = Human()
        self.algorithm = '1'
        self.computer = Computer(self.algorithm)
        self.playing = None
        self.stats = Game.load_stats()
        self.winner = None

    def __repr__(self):
        return f'Class: {self.__class__}, algorithm = {self.algorithm}, playing = {self.playing.__class__}'

    def __str__(self):
        """
        Εμφανίζει την κατάσταση του παιχνιδιού αν τελείωνε την δεδομένη στηγμή.
        """
        if self.winner == self.computer:
            return "Νικητής ο Η/Υ με Σκορ: " + str(self.computer.score)+'\n'\
                   +"Σκορ Παίκτη: " + str(self.human.score)
        elif self.winner == self.human:
            return "Νικητής ο Παίκτης με Σκορ: " + str(self.human.score)+'\n'\
                   +"Σκορ Η/Υ: " + str(self.computer.score)
        else:
            return "Ισοπαλία"+'\n'\
                   +"Σκορ Η/Υ: " + str(self.computer.score)+'\n'\
                   +"Σκορ Παίκτη: " + str(self.human.score)

    def setup(self):
        """
        Αρχικοποιεί ένα παιχνίδι
        """
        self.sak = SakClass()
        self.human = Human()
        self.computer = Computer(self.algorithm)
        self.sak.randomize_sak()
        self._initialize_player(self.human)
        self._initialize_player(self.computer)
        self.playing = random.choice([self.human, self.computer])
        self.stats = Game.load_stats()
        self.winner = None

    def menu(self):
        """
        Προσομοιώνει το main menu του παιχνιδιού
        Δέχετε τις εισόδους τους χρήστη και ανακατευθεύνει στις επιλογές
        """
        print("***** SCRABBLE *****")
        print("--------------------")
        print("1: Σκορ")
        print("2: Ρυθμίσεις")
        print("3: Παιχνίδι")
        print("4: Έξοδος")
        print("--------------------")

        menu_choice = input("Επιλογή Μενού: ")
        if menu_choice == '1':
            self.stats = Game.load_stats()

            if len(self.stats) == 0:
                print("Σκορ : Κενό")

            else:
                print("Σκορ :")
                for stat in self.stats:
                    print(stat)
                    print()
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
        """
        Προσομοιώνει το menu ρυθμίσεων του παιχνιδιού.
        Ορίζει τον αλγόριθμο με τον οποίο παίζει ο Η/Υ
        """
        print("***** Ρυθμίσεις *****")
        print("---------------------")
        print("1: MIN_letters")
        print("2: MAX_letters")
        print("3: SMART")
        print("4: FAIL")
        print("---------------------")

        settings_choice = input("Επιλογή Ρυθμίσεων: ")
        if settings_choice in ['1', '2', '3', '4']:
            self.algorithm = settings_choice

        print("--------------------")
        print("Πληκρολόγησε 1, 2, 3 ή 4")
        print("--------------------")

    def run(self):
        """
        Προσομειώνει ένα παιχνίδι scrabble
        :return:
        """
        self.setup()

        while True:
            if not self.playing.play(self.sak):
                break

            if self.playing == self.human:
                self.playing = self.computer
            else:
                self.playing = self.human

        if self.computer.score > self.human.score:
            self.winner = self.computer
        elif self.computer.score < self.human.score:
            self.winner = self.human

        self.end()

    def end(self):
        """
        Εκτελεί τις ενέργειες τερματισμού του παιχνιδιού
        """
        print("----------------------------------------------------------")
        print("Τέλος παιχνιδιού")
        print(self)

        # Κατασκευάζει το στατιστικό του παιχνιδιού
        # temp = f'{len(self.stats) + 1}. '
        #
        # temp += f'{date.today()} '
        #
        # if self.winner == self.computer:
        #     temp += f'Lose'
        # elif self.winner == self.human:
        #     temp += f'Win'
        # else:
        #     temp += f'Draw'
        #
        # temp += f' Your score: {self.human.score}'

        temp = f'{len(self.stats) + 1}. {date.today()} '
        temp += self.__str__()

        # Προσθέτει το στατιστικό στα υπόλοιπα στατιστικά
        self.stats.append(temp)
        Game.store_stats(self.stats)

    def _initialize_player(self, player):
        player.take_letters(self.sak.get_letters(7))

    @staticmethod
    def load_stats():
        """
        Διαβάζει τα στατιστικά του παίκτη
        :return: τα στατιστικά
        """
        try:
            with open('stats.json', 'r') as f:
                return json.load(f)["stats"]
        except FileNotFoundError:
            temp = []
            with open("stats.json", 'w') as f:
                json.dump({"stats": temp}, f)
            return temp

    @staticmethod
    def store_stats(stats):
        """
        Αποθηκεύει τα στατιστικά του παίκτη στο αρχείο
        """
        try:
            with open('stats.json', 'w') as f:
                json.dump({"stats": stats}, f)
        except FileNotFoundError:
            print("File Error!!")


if __name__ == '__main__':
    game = Game()
    game.menu()
