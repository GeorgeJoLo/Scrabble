import random


class SakClass:
    def __init__(self):
        self.letters = ['A', 'A', 'A', 'A', 'B', 'B', 'C', 'C']
        self.randomize_sak()

    def randomize_sak(self):
        """adsfasdfad asdfasdf"""
        random.shuffle(self.letters)

    def get_letters(self, nof_letters):
        res = []
        for i in range(nof_letters):
            temp = random.randint(0, len(self.letters)-1)
            res.append(self.letters.pop(temp))
        return res

    def put_back_letters(self, letters_back):
        self.letters.extend(letters_back)
        self.randomize_sak()
        return True

