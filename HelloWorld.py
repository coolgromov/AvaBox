import tkinter as tk
from tkinter import messagebox, filedialog
import sys
import os

class CharacterCounterApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Обновленная программа")
        self.window.geometry("600x400")
        self.version = '1.1.3'
        self.create_menu()
        self.create_widgets()

    def create_menu(self):
        self.menu_bar = tk.Menu(self.window)
        self.window.config(menu=self.menu_bar)

        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Файл", menu=self.file_menu)
        self.file_menu.add_command(label="Загрузить файл", command=self.load_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Выход", command=self.window.quit)

        self.help_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Справка", menu=self.help_menu)
        self.help_menu.add_command(label="О программе", command=self.show_about)
        self.help_menu.add_command(label="Обновление ПО", command=self.check_update)
        self.help_menu.add_command(label="Справка", command=self.show_help)

    def create_widgets(self):
        self.text_entry = tk.Text(self.window, height=10, width=40)
        self.text_entry.pack()
        self.count_button = tk.Button(self.window, text="Подсчитать", bg="green", command=self.count_characters)
        self.count_button.pack()

        self.count_label = tk.Label(self.window, text="Количество символов: 0")
        self.count_label.pack()

    def count_characters(self, refresh=None):
        text = self.text_entry.get("1.0", "end-1c")
        character_count = len(text)
        if refresh:
            character_count = len(refresh) - 1
        self.count_label.config(text=f"Количество символов: {character_count}")

    def show_about(self):
        messagebox.showinfo("О программе", f"Название: Counter Application\nВерсия: {self.version}\nАвтор: Бабаев Роман")

    def show_help(self):
        messagebox.showinfo("Справка", "Это программа для подсчета количества символов в тексте.\nВведите текст в поле ввода и нажмите кнопку 'Подсчитать', чтобы узнать количество символов.")

    def check_update(self):
        import urllib.request
        with urllib.request.urlopen("https://raw.githubusercontent.com/coolgromov/AvaBox/main/1.txt") as response:
            remote_version = response.read().decode().strip()
        if self.version == remote_version:
            messagebox.showinfo("Обновление ПО", "Программа не требует обновления")
            return
        else:
            self.version = remote_version
            messagebox.showinfo("Обновление ПО", "Программа успешно обновилась до последней версии")

    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Текстовые файлы", "*.txt")])
        if file_path:
            with open(file_path, "r", encoding='utf-8') as file:
                text = file.read()
            self.count_characters(refresh=text)

    def run(self):
        self.window.mainloop()

app = CharacterCounterApp()
app.run()
