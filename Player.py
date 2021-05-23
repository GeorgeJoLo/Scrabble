from SakClass import *
from itertools import permutations


class Player(object):
    def __init__(self):
        self.score = 0
        self.letters = []
        pass

    def __repr__(self):
        return f'Class: {self.__class__}, score = {self.score}, letters = {self.letters}'

    def take_letters(self, taken_letters):
        """
        Τα γράμματα του παίκετει εμπλουτίζονται με τα taken_letters
        :param taken_letters: εισερχόμενα γράμματα
        """
        self.letters.extend(taken_letters)

    def remove_letters(self, given_letters):
        """
        Αφαίρεί τα given_letters από τα γράμματα του παίκτη
        :param given_letters: λίστα γραμμάτων
        """
        for i in range(len(given_letters)):
            self.letters.remove(given_letters[i])

    def print_letters(self):
        res = ""
        for i in self.letters:
            res = res + " " + i + "," + str(SakClass.value_of_letter(i)) + " -"
        return res[:len(res) - 2]

    def own_letters(self, word):
        temp = self.letters.copy()
        for i in word:
            if i not in temp:
                return False
            temp.remove(i)
        return True

    @staticmethod
    def valid_word(word):
        # TODO check if word is in greek7.txt
        return True


class Human(Player):
    def play(self, sak):
        # Εμφάνισε πληροφορίες για τα γράμματα
        print(f"Στο σακουλάκι: {sak.get_nof_letters()} γραμματα - Παίζεις:")
        print(f"Διαθέσιμα Γράμματα: {self.print_letters()}")
        word = self._check_validity(sak)

        # Αν θέλει να αλλάξει γράμματα
        if word == 'P':
            sak.put_back_letters(self.letters.copy())
            super().remove_letters(self.letters)
            super().take_letters(sak.get_letters(7))
            print(f"Τα νέα σου γράμματα: {self.print_letters()}")
            return

        super().remove_letters(word)
        self.score += SakClass.value_of_word(word)
        print(f'Αποδεκτή Λέξη - Βαθμοί: {str(SakClass.value_of_word(word))} - Σκορ: {str(self.score)}')
        input(f'ENTER για συνέχεια...')
        super().take_letters(sak.get_letters(7 - len(self.letters)))
        return

    def _check_validity(self, sak):
        word = input(f"Λέξη: ")
        word.upper()

        if word == 'P':
            return word

        # check if invalid letters
        if not super().own_letters(word):
            print(f'Δε μπορείς να σχηματίσεις αυτή τη λέξη!')
            return self._check_validity(sak)

        # check if invalid word
        if not Player.valid_word(word):
            print(f'Δεν υπάρχει αυτή η λέξη!')
            return self._check_validity(sak)

        return word


class Computer(Player):
    def __init__(self, algorithm):
        super().__init__()
        self.algorithm = algorithm

    def play(self, sak):
        # Εμφάνισε πληροφορίες για τα γράμματα
        print(f"Στο σακουλάκι: {sak.get_nof_letters()} γραμματα - Παίζει ο Η/Υ:")
        print(f"Γράμματα Η/Υ: {self.print_letters()}")

        # Φτιάχνει τη λέξη
        word = ""
        if self.algorithm == 1:
            word = self.MIN_letters()
        elif self.algorithm == 2:
            word = self.MAX_letters()
        elif self.algorithm == 3:
            word = self.SUCCESS()
        elif self.algorithm == 4:
            word = self.FAIL()

        super().remove_letters(word)
        self.score += SakClass.value_of_word(word)
        print(f'Λέξη: {word}, Βαθμοί: {str(SakClass.value_of_word(word))} - Σκορ H/Y: {str(self.score)}')
        super().take_letters(sak.get_letters(7 - len(self.letters)))
        return

    def MIN_letters(self):
        """
        Γυρνάει τη πρώτη λέξη με τα λιγότερα γράμματα
        :return:
        """
        for i in range(2, len(self.letters)):
            perms = permutations(self.letters, i)
            for combination in perms:
                if self.valid_word(combination):
                    return combination

    def MAX_letters(self):
        """
        Γυρνάει τη πρώτη λέξη με τα περισσότερα γράμματα
        :return:
        """
        for i in range(len(self.letters), 1, -1):
            perms = permutations(self.letters, i)
            for combination in perms:
                if self.valid_word(combination):
                    return combination

    def _SMART(self):
        """
        Γυρνάει όλες τις αποδεκτές λέξεις
        :return:
        """
        valid_combinations = []
        for i in range(2, len(self.letters)):
            perms = permutations(self.letters, i)
            for combination in perms:
                if self.valid_word(combination):
                    valid_combinations.append(combination)
        return valid_combinations

    def SUCCESS(self):
        """
        Γυρνάει τη καλύτερη λέξη
        :return:
        """
        valid_combinations = self._SMART()
        max_word = valid_combinations[0]
        max_value = SakClass.value_of_word(max_word)
        for combination in valid_combinations:
            if max_value<SakClass.value_of_word(combination):
                max_word = combination
                max_value = SakClass.value_of_word(combination)

        return max_word

    def FAIL(self):
        """
        Γυρνάει τη δεύτερη καλύτερη λέξη
        :return:
        """
        valid_combinations = self._SMART()
        max_word = self.SUCCESS()
        valid_combinations.remove(max_word)
        max_word = valid_combinations[0]
        max_value = SakClass.value_of_word(max_word)
        for combination in valid_combinations:
            if max_value < SakClass.value_of_word(combination):
                max_word = combination
                max_value = SakClass.value_of_word(combination)

        return max_word
