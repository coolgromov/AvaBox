import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import os

class FileStream:
    def __init__(self, file_path):
        self.file_path = file_path

    def write_data(self, data):
        with open(self.file_path, 'wb') as file:
            file.write(data)

    def read_data(self):
        with open(self.file_path, 'rb') as file:
            return file.read()

# Базовый декоратор
class FileStreamDecorator:
    def __init__(self, stream):
        self.stream = stream

    def write_data(self, data):
        self.stream.write_data(data)

    def read_data(self):
        return self.stream.read_data()

# Декоратор для кодирования в формате Base64
class Base64EncodingDecorator(FileStreamDecorator):
    def write_data(self, data):
        encoded_data = base64.b64encode(data)
        self.stream.write_data(encoded_data)

    def read_data(self):
        encoded_data = self.stream.read_data()
        return base64.b64decode(encoded_data)

# Декоратор для шифрования криптографическим алгоритмом
class EncryptionDecorator(FileStreamDecorator):
    def __init__(self, stream, key):
        super().__init__(stream)
        self.key = key

    def write_data(self, data):
        iv = os.urandom(16)  # Генерация случайного вектора инициализации
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        padder = padding.PKCS7(algorithms.AES.block_size).padder()

        padded_data = padder.update(data) + padder.finalize()
        encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

        self.stream.write_data(iv + encrypted_data)

    def read_data(self):
        encrypted_data = self.stream.read_data()
        iv = encrypted_data[:16]
        encrypted_data = encrypted_data[16:]

        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()

        decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()
        unpadded_data = unpadder.update(decrypted_data) + unpadder.finalize()

        return unpadded_data

# Пример использования
file_path = 'data.bin'

# Создание экземпляра FileStream
stream = FileStream(file_path)

# Создание декорированного экземпляра FileStream с кодированием в Base64
base64_stream = Base64EncodingDecorator(stream)

# Создание декорированного экземпляра FileStream с шифрованием
key = b'thisisasecretkey'
encrypted_stream = EncryptionDecorator(base64_stream, key)

# Запись данных в файл с применением всех преобразований
data = b'Hello, World!'
encrypted_stream.write_data(data)

# Чтение данных из файла с обратными преобразованиями
decoded_data = encrypted_stream.read_data()
print(decoded_data)  # Вывод: b'Hello, World!'
