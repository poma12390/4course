import random
import sys

N = 16
def generate_squares():
    bytes_list = list(range(256))
    square1 = bytes_list[:]
    square2 = bytes_list[:]
    square3 = bytes_list[:]
    square4 = bytes_list[:]
    random.shuffle(square3)
    random.shuffle(square4)
    return square1, square2, square3, square4

def squares_to_string(square3, square4):
    squares_data = ','.join(map(str, square3)) + '\n' + ','.join(map(str, square4))
    return squares_data

def encrypt_data(data, square1, square2, square3, square4):
    encrypted_data = bytearray()
    for i in range(0, len(data), 2):
        b1 = data[i]
        b2 = data[i+1]
        idx1 = square1.index(b1)
        idx2 = square2.index(b2)
        row1, col1 = divmod(idx1, N)
        row2, col2 = divmod(idx2, N)
        enc_b1 = square3[row1*N + col2]
        enc_b2 = square4[row2*N + col1]
        encrypted_data.extend([enc_b1, enc_b2])
    return encrypted_data

def decrypt_data(data, square1, square2, square3, square4):
    decrypted_data = bytearray()
    for i in range(0, len(data), 2):
        b1 = data[i]
        b2 = data[i+1]
        idx1 = square3.index(b1)
        idx2 = square4.index(b2)
        row1, col2 = divmod(idx1, N)
        row2, col1 = divmod(idx2, N)
        dec_b1 = square1[row1*N + col1]
        dec_b2 = square2[row2*N + col2]
        decrypted_data.extend([dec_b1, dec_b2])
    return decrypted_data

def main():
    square1, square2, square3, square4 = generate_squares()
    try:
        with open('input.txt', 'rb') as f_in:
            data = f_in.read()
    except FileNotFoundError:
        print("Ошибка: 'input.txt' не найден.")
        sys.exit(1)

    orig_length = len(data)
    if len(data) % 2 != 0:
        data += bytes([0])

    encrypted_data = encrypt_data(data, square1, square2, square3, square4)
    try:
        with open('encrypted.txt', 'wb') as f_out:
            f_out.write(encrypted_data)
    except:
        print("Ошибка при записи в 'encrypted.txt'.")
        sys.exit(1)

    squares_data = squares_to_string(square3, square4)
    print("Шифрование успешно. Использованные квадраты:")
    print(squares_data)
    print(f"Original Length: {orig_length}")

    decrypted_data = decrypt_data(encrypted_data, square1, square2, square3, square4)
    decrypted_data = decrypted_data[:orig_length]

    try:
        with open('decrypted.txt', 'wb') as f_out:
            f_out.write(decrypted_data)
    except:
        print("Ошибка при записи в 'decrypted.txt'.")
        sys.exit(1)

    print("Дешифрация успешна. Вывод записан в 'decrypted.txt'.")

if __name__ == '__main__':
    main()
