import tkinter as tk
from tkinter import filedialog
from googletrans import Translator
import random


class FileStream:
    def __init__(self, file_path):
        self.file_path = file_path

    def write_data(self, data):
        with open(self.file_path, 'w', encoding='utf-8') as file:
            file.write(data)

    def read_data(self):
        with open(self.file_path, 'r', encoding='utf-8') as file:
            return file.read()


class TranslationDecorator:
    def __init__(self, stream):
        self.stream = stream
        self.translator = Translator()

    def translate(self, text):
        translation = self.translator.translate(text, src='ru', dest='en')
        return translation.text

    def write_data(self, data):
        translated_data = self.translate(data)
        self.stream.write_data(translated_data)

    def read_data(self):
        return self.stream.read_data()


class WordPermutationEncryptionDecorator:
    def __init__(self, stream):
        self.stream = stream

    def encrypt(self, text, permutation_scheme):
        words = text.split()
        encrypted_words = [words[i] for i in permutation_scheme]
        return ' '.join(encrypted_words)

    def decrypt(self, text, permutation_scheme):
        words = text.split()
        decrypted_words = [''] * len(words)
        for i, index in enumerate(permutation_scheme):
            decrypted_words[index] = words[i]
        return ' '.join(decrypted_words)

    def write_data(self, data, permutation_scheme):
        encrypted_data = self.encrypt(data, permutation_scheme)
        self.stream.write_data(encrypted_data)

    def read_data(self, permutation_scheme):
        encrypted_data = self.stream.read_data()
        decrypted_data = self.decrypt(encrypted_data, permutation_scheme)
        return decrypted_data


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Text Transformation App")
        self.geometry("400x200")
        self.file_path = ""

        self.create_widgets()

    def create_widgets(self):
        label = tk.Label(self, text="Select a file:")
        label.pack()

        select_button = tk.Button(self, text="Select", command=self.select_file)
        select_button.pack()

        translate_button = tk.Button(self, text="Translate", command=self.translate_file)
        translate_button.pack()

        encrypt_button = tk.Button(self, text="Encrypt", command=self.encrypt_file)
        encrypt_button.pack()

        decrypt_button = tk.Button(self, text="Decrypt", command=self.decrypt_file)
        decrypt_button.pack()

    def select_file(self):
        self.file_path = filedialog.askopenfilename()

    def translate_file(self):
        if not self.file_path:
            return

        stream = FileStream(self.file_path)
        translator = TranslationDecorator(stream)

        translated_data = translator.read_data()
        translated_data = translator.translate(translated_data)

        output_path = "output.txt"
        output_stream = FileStream(output_path)
        output_stream.write_data(translated_data)

    def encrypt_file(self):
        if not self.file_path:
            return

        stream = FileStream(self.file_path)
        encryptor = WordPermutationEncryptionDecorator(stream)

        permutation_scheme = [2, 1, 0]  # Пример схемы перестановки слов

        encrypted_data = encryptor.read_data(permutation_scheme)

        encrypt_path = "encrypt.txt"
        encrypt_stream = FileStream(encrypt_path)
        encrypt_stream.write_data(encrypted_data)

    def decrypt_file(self):
        if not self.file_path:
            return

        encrypt_path = "encrypt.txt"
        encrypt_stream = FileStream(encrypt_path)
        encryptor = WordPermutationEncryptionDecorator(encrypt_stream)

        permutation_scheme = [2, 1, 0]  # Пример схемы перестановки слов

        encrypted_data = encryptor.read_data(permutation_scheme)

        decrypt_path = "decrypt.txt"
        decrypt_stream = FileStream(decrypt_path)
        decrypt_stream.write_data(encrypted_data)


if __name__ == "__main__":
    app = Application()
    app.mainloop()
