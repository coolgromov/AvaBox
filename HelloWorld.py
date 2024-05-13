import tkinter as tk
from tkinter import messagebox, filedialog
import urllib.request
import os

# Запуск обновленного кода
def download_and_run_code():
    # URL, где расположен код для выполнения
    code_url = "https://raw.githubusercontent.com/coolgromov/AvaBox/main/HelloWorld.py"  # Замените на URL вашего кода
    try:
        # Загружаем код из удаленного файла
        with urllib.request.urlopen(code_url) as response:
            code = response.read().decode("utf-8")
        # Выполняем загруженный код
        exec(code, globals())
    except Exception as e:
        # Обрабатываем ошибки при загрузке или выполнении кода
        print("Ошибка при выполнении кода:")
        import traceback
        traceback.print_exc()

# Функция которая проверяет версию
def get_version():
    file_path = os.path.join(os.path.expanduser("~"), "version.txt")
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            version = file.read().strip()
            import requests
            response = requests.get('https://raw.githubusercontent.com/coolgromov/AvaBox/main/1.txt')
            if version != response.text:
                download_and_run_code()
                import sys
                sys.exit()
            else:
                return version
    else:
        return "1.0"

VERSION = get_version()

class CharacterCounterApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Подсчет символов в тексте")
        self.window.geometry("600x400")
        self.create_menu()
        self.version = '1.1.3'
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
        self.count_button = tk.Button(self.window, text="Подсчитать", bg='green', command=self.count_characters)
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
        messagebox.showinfo("О программе", f"Название: Counter Application\nВерсия: 1.0\nАвтор: Бабаев Роман")

    def show_help(self):
        messagebox.showinfo("Справка", "Это программа для подсчета количества символов в тексте.\nВведите текст в поле ввода и нажмите кнопку 'Подсчитать', чтобы узнать количество символов.")

    def check_update(self):
        import requests
        response = requests.get('https://raw.githubusercontent.com/coolgromov/AvaBox/main/1.txt')
        if self.version == response.text:
            messagebox.showinfo("Обновление ПО", "Программа не требует обновления")
            return
        else:
            user_input = messagebox.askquestion("Обновление ПО", "Обнаружено обновление. Хотите обновить программу?")
            if user_input == "yes":
                import threading
                threading.Thread(target=self.install_update).start()

    def install_update(self):
        from PIL import Image, ImageTk, ImageSequence
        # Display the installation GIF
        gif_path = "installation.gif"
        installation_gif = tk.Toplevel()
        installation_gif.title("Установка обновления")
        installation_gif.geometry("414x281")
        installation_gif.resizable(False, False)
        installation_gif.attributes('-topmost', 'true')
        installation_gif_label = tk.Label(installation_gif)
        installation_gif_label.pack()
        gif = Image.open(gif_path)
        gif_frames = [ImageTk.PhotoImage(frame) for frame in ImageSequence.Iterator(gif)]
        gif_index = 0
        delay = gif.info['duration']
        while True:
            installation_gif_label.config(image=gif_frames[gif_index])
            installation_gif.update_idletasks()
            installation_gif.after(delay, lambda: None)
            gif_index = (gif_index + 1) % len(gif_frames)
            import time
            time.sleep(5) # Щас как потерпим, а потом как потерпим
            messagebox.showinfo("Обновление ПО",
                                "Программа успешно обновилась до последней версии!\nПерезагрузите приложение для появления обновления")
            break
        installation_gif.destroy()  # Закрытие окна
        # Update the version after installation
        file_path = os.path.join(os.path.expanduser("~"), "version.txt")
        with open(file_path, "w") as file:
            import requests
            response = requests.get('https://raw.githubusercontent.com/coolgromov/AvaBox/main/1.txt')
            file.write(response.text)

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
