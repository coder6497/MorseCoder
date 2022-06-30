import json


class MorseCoder:
    def __init__(self, user_input):
        with open("code_files/morse_code.json", "r", encoding="utf-8") as f:
            self.morse = json.load(f)
        self.words = user_input.split(' ')
        self.words_l = list(map(list, self.words))

    def to_morse(self):
        for k, v in self.morse.items():
            for i in range(len(self.words_l)):
                for j in range(len(self.words_l[i])):
                    if self.words_l[i][j] == k or self.words_l[i][j] == k.lower():
                        self.words_l[i][j] = v
        return ' '.join(list(map(lambda x: ' '.join(x), self.words_l)))

    def to_normal(self):
        for k, v in self.morse.items():
            for i in range(len(self.words)):
                if self.words[i] == v:
                    self.words[i] = k
        return ' '.join(self.words)

