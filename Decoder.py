import string
import re
import Dictionary


class Decoder:
    alphabet = string.ascii_uppercase
    eng_char_freq = {
        'A': 0.0651738, 'B': 0.0124248, 'C': 0.0217339, 'D': 0.0349835, 'E': 0.1041442, 'F': 0.0197881,
        'G': 0.0158610, 'H': 0.0492888, 'I': 0.0558094, 'J': 0.0009033, 'K': 0.0050529, 'L': 0.0331490,
        'M': 0.0202124, 'N': 0.0564513, 'O': 0.0596302, 'P': 0.0137645, 'Q': 0.0008606, 'R': 0.0497563,
        'S': 0.0515760, 'T': 0.0729357, 'U': 0.0225134, 'V': 0.0082903, 'W': 0.0171272, 'X': 0.0013692,
        'Y': 0.0145984, 'Z': 0.0007836
    }
    # Индекс совпадения в достаточно длинном осмысленном английском тексте
    eng_text_ci = 0.065
    # Минимальное число совпадений расшифрованных слов со словами из словаря
    match_threshold = 20

    def __init__(self, file_name, playfair_keyword=""):
        # Получение слов, приведенных к верхнему регистру и без знаков препинания
        with open(file_name, "r") as f:
            self.encrypted_text = ' '.join([w for w in re.split(r'[^\w]', f.read().upper()) if w != ""])
        self.encrypted_text_no_spaces = ''.join(self.encrypted_text.split())
        self.decoded_text = ''
        self.playfair_keyword = playfair_keyword

    def decode(self):
        if self.__try_caesor():
            return "Successfully hacked. Caesor cipher."
        elif self.__try_vigenere():
            return "Successfully hacked. Vigenere cipher."
        # Шифрограмма Плейфера не взламывается, а преобразуется в исходный текст на основе знания ключа
        elif self.playfair_keyword != "" and self.__try_playfair():
            return "Successfully decoded. Playfair cipher."
        return "Hacking/decoding failed."

    def write_decoded_text_to_file(self, output_file):
        with open(output_file, "w") as f:
            f.write(self.decoded_text)

    def __try_caesor(self):
        char_freq = self.__calculate_char_freq(self.encrypted_text)
        most_freq_char = sorted(char_freq.items(), key=lambda pair: pair[1], reverse=True)[0][0]
        shift = ord(most_freq_char) - ord('E')

        open_text_chars = []
        for c in self.encrypted_text:
            if c == " ":
                open_text_chars.append(c)
                continue
            new_pos = (Decoder.alphabet.find(c) - shift + len(Decoder.alphabet)) % len(Decoder.alphabet)
            open_text_chars.append(Decoder.alphabet[new_pos])

        open_text_candidate = ''.join(open_text_chars)
        if self.__match_with_dictionary(open_text_candidate):
            self.decoded_text = open_text_candidate
            return True
        else:
            return False

    def __try_vigenere(self):
        keyword_length = self.__find_keyword_length()
        caesar_shifts = self.__calculate_caesar_shifts(keyword_length)

        shift_index = 0
        open_text_chars = []
        for c in self.encrypted_text:
            if c == " ":
                open_text_chars.append(c)
                continue
            cur_shift = caesar_shifts[shift_index]
            new_pos = (Decoder.alphabet.find(c) - cur_shift + len(Decoder.alphabet)) % len(Decoder.alphabet)
            open_text_chars.append(Decoder.alphabet[new_pos])
            # Циклический переход к сдвигу следующего шифра Цезаря (следующая буква ключевого слова)
            shift_index = (shift_index + 1) % len(caesar_shifts)

        open_text_candidate = ''.join(open_text_chars)
        if self.__match_with_dictionary(open_text_candidate):
            self.decoded_text = open_text_candidate
            return True
        else:
            return False

    def __try_playfair(self):
        playfair_matrix = self.__create_playfair_matrix()
        open_text_chars_with_x = []

        for i in range(0, len(self.encrypted_text_no_spaces), 2):
            c1_enc = self.encrypted_text_no_spaces[i]
            c2_enc = self.encrypted_text_no_spaces[i + 1]
            pos1, pos2 = self.__find_positions_in_matrix(playfair_matrix, c1_enc, c2_enc)
            c1_open, c2_open = self.__get_open_text_bigram(playfair_matrix, pos1, pos2)
            open_text_chars_with_x.append(c1_open)
            open_text_chars_with_x.append(c2_open)

        self.decoded_text = ''.join(self.__remove_X(open_text_chars_with_x))
        return True

    def __match_with_dictionary(self, open_text_candidate):
        mismatch_count = 0
        for word in open_text_candidate.split():
            if word.lower() not in Dictionary.words:
                mismatch_count += 1
        matched_count = abs(len(open_text_candidate.split()) - mismatch_count)
        return matched_count > Decoder.match_threshold

    def __find_keyword_length(self):
        min_diff_ci = abs(self.__calculate_index_of_coincidence(1) - Decoder.eng_text_ci)
        keyword_length = 1
        # Длина ключа для шифра Плейфера ограничена 10 символами
        for period in range(2, 11):
            ci = self.__calculate_index_of_coincidence(period)
            diff_ci = abs(ci - Decoder.eng_text_ci)
            if diff_ci < min_diff_ci:
                min_diff_ci = diff_ci
                keyword_length = period
        return keyword_length

    def __calculate_caesar_shifts(self, keyword_length):
        caesar_shifts = []
        for start_pos in range(0, keyword_length):
            # Выборка букв из текста, закодированных одним алфавитом:
            text_sample_caesar = ''.join([self.encrypted_text_no_spaces[i]
                                          for i in
                                          range(start_pos, len(self.encrypted_text_no_spaces), keyword_length)])
            char_freq = self.__calculate_char_freq(text_sample_caesar)
            most_freq_char = sorted(char_freq.items(), key=lambda pair: pair[1], reverse=True)[0][0]
            shift = ord(most_freq_char) - ord('E')
            caesar_shifts.append(shift)
        return caesar_shifts

    def __calculate_char_freq(self, text):
        char_freq = dict()
        chars_count = 0
        for c in text:
            if c == ' ':
                continue
            chars_count += 1
            if c not in char_freq:
                char_freq[c] = 1
            else:
                char_freq[c] += 1
        for c in char_freq.keys():
            char_freq[c] /= chars_count
        return char_freq

    def __calculate_index_of_coincidence(self, period):
        chars_to_count = dict()
        total_count = 0
        for i in range(0, len(self.encrypted_text_no_spaces), period):
            total_count += 1
            cur_char = self.encrypted_text_no_spaces[i]
            if cur_char not in chars_to_count.keys():
                chars_to_count[cur_char] = 1
            else:
                chars_to_count[cur_char] += 1
        ci = 0
        for c in chars_to_count.keys():
            ci += (chars_to_count[c] / total_count) ** 2
        return ci

    def __create_playfair_matrix(self):
        matrix = [list('00000') for i in range(5)]
        letters_left = {c: True for c in list(self.alphabet)}
        # Исключение буквы J из матрицы 5x5
        letters_left['J'] = False
        # Заполнение матрицы буквами из ключевого слова
        i, j = self.__fill_matrix_based_on_str(matrix, letters_left, self.playfair_keyword, 0, 0)
        # Продолжение заполнеия матрицы оставшимися буквами, которые не были встречены в ключевом слове
        self.__fill_matrix_based_on_str(matrix, letters_left, self.alphabet, i, j)
        return matrix

    def __fill_matrix_based_on_str(self, matrix, letters_left, iterable_str, i, j):
        index = 0
        while index < len(iterable_str):
            cur_letter = iterable_str[index]
            if letters_left[cur_letter]:
                matrix[i][j] = cur_letter
                letters_left[cur_letter] = False
                j += 1
                if j == 5:
                    i += 1
                    j = 0
            index += 1
        return i, j

    def __find_positions_in_matrix(self, matrix, c1, c2):
        i1 = j1 = i2 = j2 = 0
        for i in range(5):
            for j in range(5):
                if matrix[i][j] == c1:
                    i1 = i
                    j1 = j
                elif matrix[i][j] == c2:
                    i2 = i
                    j2 = j
        return (i1, j1), (i2, j2)

    def __get_open_text_bigram(self, matrix, pos1, pos2):
        i1 = pos1[0]
        j1 = pos1[1]
        i2 = pos2[0]
        j2 = pos2[1]
        # Если в одной строке, то смещение влево на 1
        if i1 == i2:
            c1 = matrix[i1][(j1 - 1 + 5) % 5]
            c2 = matrix[i2][(j2 - 1 + 5) % 5]
        # Если в однном столбце, то смещение вверх на 1
        elif j1 == j2:
            c1 = matrix[(i1 - 1 + 5) % 5][j1]
            c2 = matrix[(i2 - 1 + 5) % 5][j2]
        # Если в разных строках и столбцах, то замена на противополжные углы прямоугольника в тех же строках
        else:
            c1 = matrix[i1][j2]
            c2 = matrix[i2][j1]
        return c1 + c2

    def __remove_X(self, chars):
        filtered_chars = [chars[0]]
        # Обратное преобразование для правила разделения одинаковых букв в биграмме буквой X
        for i in range(1, len(chars) - 1):
            if chars[i] == 'X' and chars[i - 1] == chars[i + 1]:
                continue
            filtered_chars.append(chars[i])
        # Обратное преобраозование для правила добавления буквы X в конец в случае нечетной длины текста
        if chars[-1] != 'X':
            filtered_chars.append(chars[-1])
        return filtered_chars
