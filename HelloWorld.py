import tkinter as tk
from tkinter import messagebox

class WindowObject:
    def __init__(self, name):
        self.name = name
        self.help_text = "Справка для объекта окна"

    def get_help_text(self):
        return self.help_text

class ButtonObject:
    def __init__(self, name, parent_window):
        self.name = name
        self.parent_window = parent_window
        self.help_text = "Справка для кнопки"

    def get_help_text(self):
        return self.help_text

class DialogObject:
    def __init__(self, name, parent_window):
        self.name = name
        self.parent_window = parent_window
        self.help_text = "Справка для диалогового окна"

    def get_help_text(self):
        return self.help_text

class GeneralHelpObject:
    def __init__(self):
        self.help_text = "Общая справка"

    def get_help_text(self):
        return self.help_text

class HelpChain:
    def __init__(self):
        self.chain = self.build_chain()

    def build_chain(self):
        window_obj = WindowObject("Окно")
        button_obj = ButtonObject("Кнопка", window_obj)
        dialog_obj = DialogObject("Диалоговое окно", window_obj)
        general_help_obj = GeneralHelpObject()

        window_obj.help_successor = button_obj
        button_obj.help_successor = dialog_obj
        dialog_obj.help_successor = general_help_obj

        return window_obj

    def get_help(self, obj):
        current_obj = self.chain

        while current_obj:
            if isinstance(obj, type(current_obj)):
                return current_obj.get_help_text()

            current_obj = current_obj.help_successor

        return "Справка не найдена"

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.help_chain = HelpChain()
        self.create_widgets()

    def create_widgets(self):
        button = tk.Button(self, text="Печать")
        button.pack()
        button.bind("<Button-3>", self.show_context_menu)

    def show_context_menu(self, event):
        context_menu = tk.Menu(self, tearoff=0)
        context_menu.add_command(label="Справка", command=lambda: self.show_help(event))
        context_menu.post(event.x_root, event.y_root)

    def show_help(self, event):
        widget = event.widget
        help_text = self.help_chain.get_help(widget)
        messagebox.showinfo("Справка", help_text)

if __name__ == "__main__":
    app = Application()
    app.mainloop()
