class Player(object):
    def __init__(self):
        self.score = 0
        self.letters = []
        pass

    def __repr__(self):
        return f'Class: {self.__class__}, score = {self.score}, letters = {self.letters}'

    def take_letters(self, taken_letters):
        self.letters.extend(taken_letters)

    def remove_letters(self, given_letters):
        for i in range(len(given_letters)):
            self.letters.remove(given_letters[i])


class Human(Player):
    def play(self):
        pass

    def give_letters(self):
        res = []
        ...
        self.remove_letters(res)
        return res

    def write_word(self):
        word = []
        ...
        self.remove_letters(word)
        return word


class Computer(Player):
    def play(self):
        pass

    def give_letters(self):
        res = []
        ...
        self.remove_letters(res)
        return res

    def write_word(self):
        word = []
        ...
        self.remove_letters(word)
        return word
