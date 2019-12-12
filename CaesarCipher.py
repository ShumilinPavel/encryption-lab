import string
import re


class CaesarCipher:
    alphabet = string.ascii_uppercase

    def __init__(self, file_name):
        # Получение слов, приведенных к верхнему регистру и без знаков препинания
        with open(file_name, "r") as f:
            self.content = ' '.join([w for w in re.split(r'[^\w]', f.read().upper()) if w != ""])
        self.encrypted_content = []

    def encrypt(self, shift):
        for c in self.content:
            if c in CaesarCipher.alphabet:
                new_pos = (CaesarCipher.alphabet.find(c) + shift) % len(CaesarCipher.alphabet)
                self.encrypted_content.append(CaesarCipher.alphabet[new_pos])
            else:
                self.encrypted_content.append(c)

    def write_cipher_to_file(self, file_name):
        with open(file_name, "w") as f:
            f.write("".join(self.encrypted_content))
