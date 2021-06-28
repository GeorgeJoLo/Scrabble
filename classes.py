from itertools import permutations
import random
from datetime import date
import json


class Player:
    """
    Αναπαριστά έναν παίκτη Scrabble
    """
    def __init__(self):
        self.score = 0
        self.letters = []

    def __repr__(self):
        return f'Class: {self.__class__}, score = {self.score}, letters = {self.letters}'

    def take_letters(self, taken_letters):
        """
        Τα γράμματα του παίκτη εμπλουτίζονται με τα taken_letters
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

    def __str__(self):
        """
        Εμφανίζει τα γράμματα του παίχτη.
        """
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
    """
    Αναπαριστά τον User.
    """
    def play(self, sak):
        """
        Προσομοιώνει τον γύρο παιχνιδιού του User.
        :param sak:
        :return: false αν τελειώσει το παιχνίδη.
        """
        # Εμφάνισε πληροφορίες για τα γράμματα
        print("----------------------------------------------------------")
        print(f"Στο σακουλάκι: {sak.get_nof_letters()} γράμματα - Παίζεις:")
        print(f"Διαθέσιμα Γράμματα: {self}")

        word = self._check_validity(sak)

        # Αν θέλει να αλλάξει γράμματα
        if word == 'P':
            sak.put_back_letters(self.letters.copy())
            super().remove_letters(self.letters.copy())
            super().take_letters(sak.get_letters(7))
            print(f"Τα νέα σου γράμματα: {self}")
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
        print("----------------------------------------------------------")
        print(f"Διαθέσιμα Γράμματα: {self}")
        return True

    def _check_validity(self, sak):
        """
        Ελέγχει αν η είσοδος του χρήστη ειναι έγκυρη.
        :param sak: ο σάκος με τα γράμματα.
        :return: P ή Q ή έγκυρη λέξη.
        """
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
    """
    Αναπαριστά τον Η/Π.
    """
    def __init__(self, algorithm='1'):
        super().__init__()
        self.algorithm = algorithm

    def play(self, sak):
        """
        Προσομοιώνει τον γύρο παιχνιδιού του Η/Π.
        :param sak:
        :return: false αν τελειώσει το παιχνίδη.
        """
        # Εμφάνισε πληροφορίες για τα γράμματα
        print("----------------------------------------------------------")
        print(f"Στο σακουλάκι: {sak.get_nof_letters()} γραμματα - Παίζει ο Η/Υ:")
        print(f"Γράμματα Η/Υ: {self}")

        # Φτιάχνει τη λέξη με βάση τον αλγόριθμο.
        word = ""
        if self.algorithm == '1':
            word = self.MIN_letters()
        elif self.algorithm == '2':
            word = self.MAX_letters()
        elif self.algorithm == '3':
            word = self.SUCCESS()
        elif self.algorithm == '4':
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
        for i in range(2, len(self.letters)+1):
            perms = [''.join(p) for p in permutations(self.letters, i)]
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
            perms = [''.join(p) for p in permutations(self.letters, i)]
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
            perms = [''.join(p) for p in permutations(self.letters, i)]
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
    """
    Αναπαριστά ολους τους κανόνες του παιχνιδιού σχετικά με τις λέξεις.
    Αποθηκεύουμε σε λεξικό για να έχουμε πρόσβαση σε Ο(1)
    """
    values = {'Α': 1, 'Β': 8, 'Γ': 4, 'Δ': 4, 'Ε': 1, 'Ζ': 10, 'Η': 1, 'Θ': 10,
              'Ι': 1, 'Κ': 2, 'Λ': 3, 'Μ': 3, 'Ν': 1, 'Ξ': 10, 'Ο': 1, 'Π': 2,
              'Ρ': 2, 'Σ': 1, 'Τ': 1, 'Υ': 2, 'Φ': 8, 'Χ': 8, 'Ψ': 10, 'Ω': 3}

    # Read the greek7.txt
    greek7 = {}
    try:
        with open('greek7.txt', 'r', encoding="utf-8") as f:
            for line in f.read().splitlines():
                greek7[line] = len(line)
    except FileNotFoundError:
        print('Δε βρέθηκε αρχείο με λέξεις! Βye!')
        exit()

    @staticmethod
    def value_of_letter(letter):
        """
        :param letter: Ένα γράμμα.
        :return: η αξία του.
        """
        return WordMaster.values[letter]

    @staticmethod
    def value_of_word(word):
        """
        :param letter: μια λέξη.
        :return: η αξία της.
        """
        return sum([WordMaster.values[letter] for letter in word])

    @staticmethod
    def valid_word(word):
        """
        :param word: μια λέξη.
        :return: true , αν υπάρχει μια τέτοια λέξη.
        """
        return word in WordMaster.greek7


class SakClass:
    def __init__(self):
        self.letters = ['Α', 'Α', 'Α', 'Α', 'Α', 'Α', 'Α', 'Α', 'Α', 'Α', 'Α', 'Α',
                        'Β',
                        'Γ', 'Γ',
                        'Δ', 'Δ',
                        'Ε', 'Ε', 'Ε', 'Ε', 'Ε', 'Ε', 'Ε', 'Ε',
                        'Ζ',
                        'Η', 'Η', 'Η', 'Η', 'Η', 'Η', 'Η',
                        'Θ',
                        'Ι', 'Ι', 'Ι', 'Ι', 'Ι', 'Ι', 'Ι', 'Ι',
                        'Κ', 'Κ', 'Κ', 'Κ',
                        'Λ', 'Λ', 'Λ',
                        'Μ', 'Μ', 'Μ',
                        'Ν', 'Ν', 'Ν', 'Ν', 'Ν', 'Ν',
                        'Ξ',
                        'Ο', 'Ο', 'Ο', 'Ο', 'Ο', 'Ο', 'Ο', 'Ο', 'Ο',
                        'Π', 'Π', 'Π', 'Π',
                        'Ρ', 'Ρ', 'Ρ', 'Ρ', 'Ρ',
                        'Σ', 'Σ', 'Σ', 'Σ', 'Σ', 'Σ', 'Σ',
                        'Τ', 'Τ', 'Τ', 'Τ', 'Τ', 'Τ', 'Τ', 'Τ',
                        'Υ', 'Υ', 'Υ', 'Υ',
                        'Φ',
                        'Χ',
                        'Ψ',
                        'Ω', 'Ω', 'Ω']

        self.randomize_sak()

    def __repr__(self):
        return f'Class: {self.__class__}, letters = {self.letters}'

    def randomize_sak(self):
        """
        Ανακατεύει τα γράμματα στο σάκο.
        """
        random.shuffle(self.letters)

    def get_letters(self, nof_letters):
        """
        Ο σάκος δίνει nof_letters γράμματα. Αν δεν έχει τόσα, επιστρέφει None.
        Τα γράμματα αυτά βγαίνουν από το σάκο
        :param nof_letters: πλήθος γραμμάτων
        :return: γράμματα από τον σάκο
        """
        if len(self.letters) <= nof_letters:
            return None

        res = random.sample(self.letters, nof_letters)
        for i in res:
            self.letters.remove(i)
        return res

    def put_back_letters(self, letters_back):
        """
        Ο σάκος παίρνει και γεμίζει με τα letters_back, και ανακατεύουμε.
        :param letters_back: γραμματα για τον σάκο
        """
        self.letters.extend(letters_back)
        self.randomize_sak()

    def get_nof_letters(self):
        return len(self.letters)

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
            self.menu()

        if menu_choice == '2':
            self.settings()
            self.menu()

        if menu_choice == '3':
            self.run()
            self.menu()

        if menu_choice == '4':
            print("---- Έξοδος ----")
            exit()

        print("--------------------")
        print("Πληκρολόγησε 1, 2, 3 ή 4")
        print("--------------------")
        self.menu()

    def settings(self):
        """
        Προσομοιώνει το menu ρυθμίσεων του παιχνιδιού.
        Ορίζει τον αλγόριθμο με τον οποίο παίζει ο Η/Υ
        """
        if self.algorithm == '1':
            print(f'Ο υπολογιστής παίζει με τον αλγόριθμο MIN_letters')
        elif self.algorithm == '2':
            print(f'Ο υπολογιστής παίζει με τον αλγόριθμο MAX_letters')
        elif self.algorithm == '3':
            print(f'Ο υπολογιστής παίζει με τον αλγόριθμο SMART')
        elif self.algorithm == '4':
            print(f'Ο υπολογιστής παίζει με τον αλγόριθμο SMART-FAIL')

        print("***** Ρυθμίσεις *****")
        print("---------------------")
        print("1: MIN_letters")
        print("2: MAX_letters")
        print("3: SMART")
        print("4: SMART-FAIL")
        print("---------------------")

        settings_choice = input("Επιλογή Ρυθμίσεων: ")
        if settings_choice in ['1', '2', '3', '4']:
            self.algorithm = settings_choice
            if settings_choice == '1':
                print(f'Ο υπολογιστής θα παίζει με τον αλγόριθμο MIN_letters')
            elif settings_choice == '2':
                print(f'Ο υπολογιστής θα παίζει με τον αλγόριθμο MAX_letters')
            elif settings_choice == '3':
                print(f'Ο υπολογιστής θα παίζει με τον αλγόριθμο SMART')
            elif settings_choice == '4':
                print(f'Ο υπολογιστής θα παίζει με τον αλγόριθμο FAIL')

            return

        print("--------------------")
        print("Πληκρολόγησε 1, 2, 3 ή 4")
        print("--------------------")
        self.settings()

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
