import tkinter as tk
from tkinter import messagebox
import sys
import os

def count_characters():
    text = text_entry.get("1.0", "end-1c")
    character_count = len(text)
    count_label.config(text="Количество символов: " + str(character_count))

def show_about():
    messagebox.showinfo("О программе", "Название программы: Подсчет символов в тексте\nВерсия: 1.1\nАвтор: Бабаев Роман")

def show_help():
    messagebox.showinfo("Справка", "Это программа для подсчета количества символов в тексте.\nВведите текст в поле ввода и нажмите кнопку 'Подсчитать', чтобы узнать количество символов.")

def select_installation_folder():
    folder_path = tk.filedialog.askdirectory()
    if folder_path:
        messagebox.showinfo("Выбрана папка для установки", "Выбрана папка: " + folder_path)

def uninstall_program():
    uninstall_path = os.path.join(sys.path[0], "uninstall.py")
    os.system("python " + uninstall_path)

# Создание графического интерфейса
window = tk.Tk()
window.title("Подсчет символов в тексте")
window.geometry("400x300")

# Меню
menu_bar = tk.Menu(window)
window.config(menu=menu_bar)

file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Файл", menu=file_menu)
file_menu.add_command(label="Выбрать папку установки", command=select_installation_folder)
file_menu.add_command(label="Удалить программу", command=uninstall_program)
file_menu.add_separator()
file_menu.add_command(label="Выход", command=window.quit)

help_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Справка", menu=help_menu)
help_menu.add_command(label="О программе", command=show_about)
help_menu.add_command(label="Справка", command=show_help)

# Поле ввода текста
text_entry = tk.Text(window, height=10, width=40)
text_entry.pack()

# Кнопка "Подсчитать"
count_button = tk.Button(window, text="Подсчитать", command=count_characters)
count_button.pack()

# Метка для вывода результата
count_label = tk.Label(window, text="Количество символов: 0")
count_label.pack()

# Запуск главного цикла обработки событий
window.mainloop()