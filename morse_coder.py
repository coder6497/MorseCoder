import json


class MorseCoder:
    def __init__(self, user_input):
        with open("morse_code.json", "r", encoding="utf-8") as f:
            self.morse = json.load(f)
        self.count = user_input
        self.words = list(map(lambda x: input(), range(self.count)))
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
        return ' '.join(self.n_words)


if __name__ == "__main__":
    try:
        print("* точка\n- линия")
        mode = input("Выберите режим\n1.Закодировать\n2.Раскодировать\n")
        coder = MorseCoder(int(input("Введите колличество слов или символов:\t")))
        match mode:
            case "1":
                print(coder.to_morse())
            case "2":
                print(coder.to_normal())
            case _:
                print("Неверное значение")
    except ValueError:
        print("Неверное значение")