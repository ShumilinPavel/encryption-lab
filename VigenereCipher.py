import string
import re


def create_matrix():
    matrix = dict()
    for i in string.ascii_uppercase:
        index = string.ascii_uppercase.find(i)
        matrix[i] = dict()
        for j in string.ascii_uppercase:
            matrix[i][j] = string.ascii_uppercase[index]
            index = (index + 1) % len(string.ascii_uppercase)
    return matrix


class VigenereCipher:
    alphabet = string.ascii_uppercase
    matrix = create_matrix()

    def __init__(self, file_name):
        # Получение слов, приведенных к верхнему регистру и без знаков препинания
        with open(file_name, "r") as f:
            self.content = ' '.join([w for w in re.split(r'[^\w]', f.read().upper()) if w != ""])
        self.encrypted_content = []

    def encrypt(self, key_word):
        key_word = key_word.upper()
        index = 0
        for c in self.content:
            if c in VigenereCipher.alphabet:
                self.encrypted_content.append(VigenereCipher.matrix[key_word[index]][c])
                index = (index + 1) % len(key_word)
            # если c - пробел
            else:
                self.encrypted_content.append(c)

    def write_cipher_to_file(self, file_name):
        with open(file_name, "w") as f:
            f.write("".join(self.encrypted_content))
