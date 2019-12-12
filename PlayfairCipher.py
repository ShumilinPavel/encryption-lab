import string
import re


class PlayfairCipher:
    alphabet = string.ascii_uppercase
    matrix = [list('00000') for i in range(5)]

    def __init__(self, file_name, keyword):
        # Получение слов, приведенных к верхнему регистру и без знаков препинания
        with open(file_name, "r") as f:
            self.content = ''.join([w for w in re.split(r'[^\w]', f.read().upper()) if w != ""])  #''.join(f.read().upper().split())
        self.encrypted_content = []
        self.keyword = keyword.upper()
        self.__create_matrix()

    def encrypt(self):
        bigrams = self.__create_bigrams()
        for bigram in bigrams:
            pos1, pos2 = self.__find_positions_in_matrix(bigram[0], bigram[1])
            self.encrypted_content.append(self.__get_encrypted_bigram(pos1, pos2))

    def write_cipher_to_file(self, file_name):
        f = open(file_name, "w")
        f.write("".join(self.encrypted_content))

    def __create_matrix(self):
        letters_left = {c: True for c in list(self.alphabet)}
        # Исключение буквы J из матрицы 5x5
        letters_left['J'] = False
        # Заполнение матрицы буквами из ключевого слова
        i, j = self.__fill_matrix_based_on_str(letters_left, self.keyword, 0, 0)
        # Продолжение заполнеия матрицы оставшимися буквами, которые не были встречены в ключевом слове
        self.__fill_matrix_based_on_str(letters_left, self.alphabet, i, j)

    def __fill_matrix_based_on_str(self, letters_left, iterable_str, i, j):
        index = 0
        while index < len(iterable_str):
            cur_letter = iterable_str[index]
            if letters_left[cur_letter]:
                self.matrix[i][j] = cur_letter
                letters_left[cur_letter] = False
                j += 1
                if j == 5:
                    i += 1
                    j = 0
            index += 1
        return i, j

    def __create_bigrams(self):
        bigrams = []
        i = 0
        while i < len(self.content):
            if len(self.content[i:i + 2]) == 2 and self.content[i] != self.content[i + 1]:
                bigrams.append(self.content[i:i + 2])
                i += 2
            elif len(self.content[i:i + 2]) == 1:
                bigrams.append(self.content[i] + 'X')
                i += 1
            elif self.content[i] == self.content[i + 1]:
                bigrams.append(self.content[i] + 'X')
                i += 1
        return bigrams

    def __find_positions_in_matrix(self, c1, c2):
        i1 = j1 = i2 = j2 = 0
        for i in range(5):
            for j in range(5):
                if self.matrix[i][j] == c1:
                    i1 = i
                    j1 = j
                elif self.matrix[i][j] == c2:
                    i2 = i
                    j2 = j
        return (i1, j1), (i2, j2)

    def __get_encrypted_bigram(self, pos1, pos2):
        i1 = pos1[0]
        j1 = pos1[1]
        i2 = pos2[0]
        j2 = pos2[1]
        # Если в одной строке, то смещение вправо на 1
        if i1 == i2:
            c1 = self.matrix[i1][(j1 + 1) % 5]
            c2 = self.matrix[i2][(j2 + 1) % 5]
        # Если в однном столбце, то смещение вниз на 1
        elif j1 == j2:
            c1 = self.matrix[(i1 + 1) % 5][j1]
            c2 = self.matrix[(i2 + 1) % 5][j2]
        # Если в разных строках и столбцах, то замена на противополжные углы прямоугольника в тех же строках
        else:
            c1 = self.matrix[i1][j2]
            c2 = self.matrix[i2][j1]
        return c1 + c2
