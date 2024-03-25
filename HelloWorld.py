import tkinter as tk

class GUIElement:
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent
        self.help_text = ""

    def set_help_text(self, help_text):
        self.help_text = help_text

    def get_help_text(self):
        return self.help_text

    def show_help(self):
        help_text = self.get_help_text()
        if help_text:
            print(help_text)
        elif self.parent:
            self.parent.show_help()

class Button(GUIElement):
    def __init__(self, name, parent=None):
        super().__init__(name, parent)

class Dialog(GUIElement):
    def __init__(self, name, parent=None):
        super().__init__(name, parent)

class TextEditor(GUIElement):
    def __init__(self, name, parent=None):
        super().__init__(name, parent)

# Создаем элементы графического интерфейса
text_editor = TextEditor("Текстовый редактор")
dialog = Dialog("Диалоговое окно 'Печать документов'", parent=text_editor)
print_button = Button("Кнопка 'Печать'", parent=dialog)

# Устанавливаем справочную информацию для элементов
text_editor.set_help_text("Общая справка о текстовом редакторе")
dialog.set_help_text("Справка о диалоговом окне 'Печать документов'")
print_button.set_help_text("Справка о кнопке 'Печать'")

# Функция-обработчик щелчка правой кнопкой мыши
def show_help_info():
    clicked_element = print_button  # Здесь нужно получить объект, по которому был произведен щелчок
    clicked_element.show_help()

# Создаем окно с кнопкой и контекстным меню
window = tk.Tk()
button = tk.Button(window, text="Правая кнопка мыши", command=show_help_info)
button.pack()

# Запускаем главный цикл обработки событий
window.mainloop()
