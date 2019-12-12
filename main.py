from CaesarCipher import *
from VigenereCipher import *
from PlayfairCipher import *
from Decoder import *

# Параметры конфигурации
CaesarCipher_shift = 6
VigenereCipher_keyword = "LEMON"  # длина [1; 10]
PlayfairCipher_keyword = "WHEATSON"
Open_text_file = "text.txt"
Encrypted_text_file = "encrypted_text.txt"
Decoded_text_file = "decoded_text.txt"

if __name__ == "__main__":
    print("1 - Зашифровать")
    print("2 - Расшифровать")
    print("Ожидание...")

    code = int(input())

    if code == 1:
        print("1 - Шифр Цезаря")
        print("2 - Шифр Вижинера")
        print("3 - Шифр Плейфера")
        print("Ожидание...")
        code = int(input())
        if code == 1:
            encryptor = CaesarCipher(Open_text_file)
            encryptor.encrypt(CaesarCipher_shift)
            encryptor.write_cipher_to_file(Encrypted_text_file)
        elif code == 2:
            encryptor = VigenereCipher(Open_text_file)
            encryptor.encrypt(VigenereCipher_keyword)
            encryptor.write_cipher_to_file(Encrypted_text_file)
        elif code == 3:
            encryptor = PlayfairCipher(Open_text_file, PlayfairCipher_keyword)
            encryptor.encrypt()
            encryptor.write_cipher_to_file(Encrypted_text_file)
        else:
            print("Неизвестная команда")
    elif code == 2:
        decoder = Decoder(Encrypted_text_file, PlayfairCipher_keyword)
        msg = decoder.decode()
        print(msg)
        decoder.write_decoded_text_to_file(Decoded_text_file)
    else:
        print("Неизвестная команда")
