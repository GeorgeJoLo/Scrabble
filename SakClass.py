import random


class SakClass:
    values = {'A': 1, 'B': 2, 'C': 3}

    def __init__(self):
        self.letters = ['A', 'A', 'A', 'A', 'B', 'B', 'C', 'C']
        self.randomize_sak()

    def randomize_sak(self):
        random.shuffle(self.letters)

    def get_letters(self, nof_letters):
        """
        Ο σάκος δίνει nof_letters γράμματα. Αν δεν έχει τόσα, δίνει όσα έχει.
        Τα γράμματα αυτά βγαίνουν από το σάκο
        :param nof_letters: πλήθος γραμμάτων
        :return: γράμματα από τον σάκο
        """
        if len(self.letters) >= nof_letters:
            res = []
            for i in range(nof_letters):
                temp = random.randint(0, len(self.letters)-1)
                res.append(self.letters.pop(temp))
            return res

        res = self.letters.copy()
        self.letters = []
        return res

    def put_back_letters(self, letters_back):
        """
        Ο σάκος παίρνει και γεμίζει με τα letters_back
        :param letters_back: γραμματα για τον σάκο
        """
        self.letters.extend(letters_back)
        self.randomize_sak()

    def get_nof_letters(self):
        return len(self.letters)

    @staticmethod
    def value_of_letter(letter):
        return SakClass.values[letter]

    @staticmethod
    def value_of_word(word):
        return sum([SakClass.values[letter] for letter in word])
