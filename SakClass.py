import random


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

    def randomize_sak(self):
        random.shuffle(self.letters)

    def get_letters(self, nof_letters):
        """
        Ο σάκος δίνει nof_letters γράμματα. Αν δεν έχει τόσα, δίνει όσα έχει.
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
        Ο σάκος παίρνει και γεμίζει με τα letters_back
        :param letters_back: γραμματα για τον σάκο
        """
        self.letters.extend(letters_back)
        self.randomize_sak()

    def get_nof_letters(self):
        return len(self.letters)
