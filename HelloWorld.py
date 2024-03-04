import tkinter as tk
from tkinter import filedialog
from googletrans import Translator
from cryptography.fernet import Fernet

translator = Translator()

def translate_text():
    input_filename = 'input.txt'
    output_filename = 'output.txt'
    translate_to = 'en'

    with open(input_filename, 'r') as input_file:
        text = input_file.read()

    translated_text = translator.translate(text, dest=translate_to).text

    with open(output_filename, 'w') as output_file:
        output_file.write(translated_text)

    print('Translation complete!')

def encrypt_text():
    input_filename = 'output.txt'
    output_filename = 'encrypt.txt'
    encryption_key = Fernet.generate_key()
    cipher_suite = Fernet(encryption_key)

    with open(input_filename, 'r') as input_file:
        text = input_file.read().encode()

    encrypted_text = cipher_suite.encrypt(text)

    with open(output_filename, 'wb') as output_file:
        output_file.write(encrypted_text)

    print('Encryption complete!')

def decrypt_text():
    input_filename = 'encrypt.txt'
    output_filename = 'decrypt.txt'
    encryption_key = Fernet.generate_key()
    cipher_suite = Fernet(encryption_key)

    with open(input_filename, 'rb') as input_file:
        encrypted_text = input_file.read()

    decrypted_text = cipher_suite.decrypt(encrypted_text).decode()

    with open(output_filename, 'w') as output_file:
        output_file.write(decrypted_text)

    print('Decryption complete!')

def main():
    root = tk.Tk()
    root.title('Text Transformation')

    translate_button = tk.Button(root, text='Translate', command=translate_text)
    translate_button.pack()

    encrypt_button = tk.Button(root, text='Encrypt', command=encrypt_text)
    encrypt_button.pack()

    decrypt_button = tk.Button(root, text='Decrypt', command=decrypt_text)
    decrypt_button.pack()

    root.mainloop()

if __name__ == '__main__':
    main()
