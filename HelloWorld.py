import tkinter as tk

class HelpHandler:
    def __init__(self, successor=None):
        self.successor = successor

    def handle_help(self, widget):
        if self.successor:
            self.successor.handle_help(widget)

class WindowHandler(HelpHandler):
    def handle_help(self, widget):
        if isinstance(widget, tk.Tk):
            print("Справка о главном окне")
        else:
            super().handle_help(widget)

class ButtonHandler(HelpHandler):
    def handle_help(self, widget):
        if isinstance(widget, tk.Button):
            print("Справка о кнопке:", widget['text'])
        else:
            super().handle_help(widget)

class DialogHandler(HelpHandler):
    def handle_help(self, widget):
        if isinstance(widget, tk.Toplevel) and widget.title() == "Печать документов":
            print("Справка о диалоговом окне 'Печать документов'")
        else:
            super().handle_help(widget)

# Создаем иерархию обработчиков
handler = WindowHandler(ButtonHandler(DialogHandler()))

# Создаем графический интерфейс
root = tk.Tk()
root.title("Help System")

# Функция для обработки события щелчка правой кнопкой мыши
def show_help(event):
    widget = event.widget
    handler.handle_help(widget)

# Привязываем событие щелчка правой кнопкой мыши к функции show_help
root.bind("<Button-3>", show_help)

# Создаем кнопку и диалоговое окно для тестирования
button = tk.Button(root, text="Печать")
button.pack()

dialog = tk.Toplevel(root)
dialog.title("Печать документов")

# Запускаем главный цикл обработки событий
root.mainloop()
