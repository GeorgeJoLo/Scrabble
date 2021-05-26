from itertools import permutations


class Player(object):
    def __init__(self):
        self.score = 0
        self.letters = []

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
            res = res + " " + i + "," + str(WordMaster.value_of_letter(i)) + " -"
        return res[:len(res) - 2]

    def own_letters(self, word):
        """
        Επιστρέφει true αν ο παίκτης μπορεί να σχηματίσει τη λέξη με τα
        γράμματα που διαθέτει
        :param word: μία λέξη
        :return: αν μπορεί να φτιάξει τη λέξη
        """
        temp = self.letters.copy()
        for i in word:
            if i not in temp:
                return False
            temp.remove(i)
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
            super().remove_letters(self.letters.copy())
            super().take_letters(sak.get_letters(7))
            print(f"Τα νέα σου γράμματα: {self.print_letters()}")
            return True

        # Αν θέλει να σταματήσει
        if word == 'Q':
            return False

        super().remove_letters(word)
        self.score += WordMaster.value_of_word(word)
        print(f'Αποδεκτή Λέξη - Βαθμοί: {str(WordMaster.value_of_word(word))} - Σκορ: {str(self.score)}')
        input(f'ENTER για συνέχεια...')
        temp = sak.get_letters(7 - len(self.letters))
        # Αν το σακουλάκι άδειασε
        if temp is None:
            return False

        super().take_letters(temp)
        return True

    def _check_validity(self, sak):
        word = input("Λέξη: ")
        word = word.upper()

        if word == 'P' or word == 'Q':
            return word

        # check if invalid letters
        if len(word) > 7 or not super().own_letters(word):
            print(f'Δε μπορείς να σχηματίσεις αυτή τη λέξη!')
            return self._check_validity(sak)

        # check if invalid word
        if not WordMaster.valid_word(word):
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

        # Αν ο υπολογιστής δε μπορεί να σχηματίσει λέξη
        if word is None:
            return False

        super().remove_letters(word)
        self.score += WordMaster.value_of_word(word)
        print(f'Λέξη: {word}, Βαθμοί: {str(WordMaster.value_of_word(word))} - Σκορ H/Y: {str(self.score)}')
        temp = sak.get_letters(7 - len(self.letters))
        # Αν το σακουλάκι άδειασε
        if temp is None:
            return False

        super().take_letters(temp)
        return True

    def MIN_letters(self):
        """
        Γυρνάει τη πρώτη λέξη με τα λιγότερα γράμματα
        :return:
        """
        for i in range(2, len(self.letters)):
            perms = permutations(self.letters, i)
            print(list(perms))
            # TODO ta perms na ginoun string
            for combination in perms:
                if WordMaster.valid_word(combination):
                    return combination
        return None

    def MAX_letters(self):
        """
        Γυρνάει τη πρώτη λέξη με τα περισσότερα γράμματα
        :return:
        """
        for i in range(len(self.letters), 1, -1):
            perms = permutations(self.letters, i)
            for combination in perms:
                if WordMaster.valid_word(combination):
                    return combination
        return None

    def _SMART(self):
        """
        Γυρνάει όλες τις αποδεκτές λέξεις
        :return:
        """
        valid_combinations = []
        for i in range(2, len(self.letters)):
            perms = permutations(self.letters, i)
            for combination in perms:
                if WordMaster.valid_word(combination):
                    valid_combinations.append(combination)

        if len(valid_combinations) == 0:
            return None
        return valid_combinations

    def SUCCESS(self):
        """
        Γυρνάει τη καλύτερη λέξη
        :return:
        """
        valid_combinations = self._SMART()
        if not valid_combinations:
            return None

        max_word = valid_combinations[0]
        max_value = WordMaster.value_of_word(max_word)
        for combination in valid_combinations:
            if max_value < WordMaster.value_of_word(combination):
                max_word = combination
                max_value = WordMaster.value_of_word(combination)

        return max_word

    def FAIL(self):
        """
        Γυρνάει τη δεύτερη καλύτερη λέξη
        :return:
        """
        valid_combinations = self._SMART()
        if not valid_combinations:
            return None

        max_word = self.SUCCESS()
        valid_combinations.remove(max_word)
        max_word = valid_combinations[0]
        max_value = WordMaster.value_of_word(max_word)
        for combination in valid_combinations:
            if max_value < WordMaster.value_of_word(combination):
                max_word = combination
                max_value = WordMaster.value_of_word(combination)

        return max_word


class WordMaster:
    values = {'Α': 1, 'Β': 8, 'Γ': 4, 'Δ': 4, 'Ε': 1, 'Ζ': 10, 'Η': 1, 'Θ': 10,
              'Ι': 1, 'Κ': 2, 'Λ': 3, 'Μ': 3, 'Ν': 1, 'Ξ': 10, 'Ο': 1, 'Π': 2,
              'Ρ': 2, 'Σ': 1, 'Τ': 1, 'Υ': 2, 'Φ': 8, 'Χ': 8, 'Ψ': 10, 'Ω': 3}

    # Read the greek7.txt
    greek7 = {}
    try:
        with open('greek7.txt', 'r', encoding="utf-8") as f:
            for line in f:
                greek7[line] = len(line)
    except FileNotFoundError:
        print('Δε βρέθηκε αρχείο με λέξεις! Βye!')
        exit()

    @staticmethod
    def value_of_letter(letter):
        return WordMaster.values[letter]

    @staticmethod
    def value_of_word(word):
        return sum([WordMaster.values[letter] for letter in word])

    @staticmethod
    def valid_word(word):
        return word in WordMaster.greek7
