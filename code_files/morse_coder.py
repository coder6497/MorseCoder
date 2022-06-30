import json


class MorseCoder:
    def __init__(self, user_input):
        with open("code_files/morse_code.json", "r", encoding="utf-8") as f:
            self.morse = json.load(f)
        self.words = user_input.split(' ')
        self.words_l = list(map(list, self.words))
        self.n_words = []

    def to_morse(self):
        for key, value in self.morse.items():
            for elems in range(len(self.words_l)):
                for elem in range(len(self.words_l[elems])):
                    if self.words_l[elems][elem] == key or self.words_l[elems][elem] == key.lower():
                        self.words_l[elems][elem] = value
                        self.n_words.append(''.join(self.words_l[elems][elem]))
        return " ".join(self.n_words)

    def to_normal(self):
        for key, value in self.morse.items():
            for elem in range(len(self.words)):
                if self.words[elem] == value:
                    self.words[elem] = key
                    self.n_words.append(''.join(self.words[elem]))
        return ' '.join(self.n_words)[::-1]

