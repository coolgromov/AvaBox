Хорошо! Ниже приведен полный код для выполнения лабораторной работы №2, включая оба индивидуальных задания.

```python
import tkinter as tk
from tkinter import messagebox
import math

# Задание 1: Вычисление значения функции U(x, y)
def calculate_u(x, y):
    if x + y == 0:
        return x * math.exp(-y * x)
    elif 0 <= x + y < 3:
        return x * math.sin(x)
    else:
        return y**x + math.cos(x)**3

# Задание 2: Вычисление значения функции a
def calculate_a(fx, y, xy):
    if xy > 0:
        return (fx + y)**2 - math.sqrt(fx * y)
    elif xy < 0:
        return (fx + y)**2 - math.sqrt(abs(fx * y))
    else:
        return (fx + y)**2 + 1

# Функция для открытия нового окна с заданием 1
def open_task1_window():
    x = float(task1_x_entry.get())
    y = float(task1_y_entry.get())

    result = calculate_u(x, y)

    new_window = tk.Toplevel(root)
    new_window.title("Задание 1")
    new_window.geometry("300x200")

    result_label = tk.Label(new_window, text=f"Результат: {result}")
    result_label.pack()

    formula_photo = tk.PhotoImage(file="formula1.png")
    formula_label = tk.Label(new_window, image=formula_photo)
    formula_label.pack()

# Функция для открытия нового окна с заданием 2
def open_task2_window():
    fx = float(task2_fx_entry.get())
    y = float(task2_y_entry.get())
    xy = float(task2_xy_entry.get())

    result = calculate_a(fx, y, xy)

    new_window = tk.Toplevel(root)
    new_window.title("Задание 2")
    new_window.geometry("300x200")

    result_label = tk.Label(new_window, text=f"Результат: {result}")
    result_label.pack()

    formula_photo = tk.PhotoImage(file="formula2.png")
    formula_label = tk.Label(new_window, image=formula_photo)
    formula_label.pack()

# Функция для обработки выбора задания в ComboBox
def handle_selection(event):
    selected_task = combo_box.get()

    if selected_task == "Задание 1":
        open_task1_window()
    elif selected_task == "Задание 2":
        open_task2_window()
    else:
        messagebox.showerror("Ошибка", "Выберите задание")

# Создание основного окна приложения
root = tk.Tk()
root.title("Мое приложение")
root.geometry("400x300")

# Добавление ComboBox для выбора задания
combo_box = tk.Combobox(root, values=["Задание 1", "Задание 2"])
combo_box.pack()
combo_box.bind("<<ComboboxSelected>>", handle_selection)

# Задание 1: Создание формы для ввода данных
task1_frame = tk.Frame(root)
task1_frame.pack()

task1_label = tk.Label(task1_frame, text="Введите значения x и y:")
task1_label.pack()

task1_x_label = tk.Label(task1_frame, text="x:")
task1_x_label.pack(side=tk.LEFT)

task1_x_entry = tk.Entry(task1_frame)
task1_x_entry.pack(side=tk.LEFT)

task1_y_label = tk.Label(task1_frame, text="y:")
task1_y_label.pack(side=tk.LEFT)

task1_y_entry = tk.Entry(task1_frame)
task1_y_entry.pack(side=tk.LEFT)

# Задание 2: Создание формы для ввода данных
task2_frame = tk.Frame(root)
task2_frame.pack()

task2_label = tk.Label(task2_frame, text="Введите значения f(x), y и xy:")
task2_label.pack()

task2_fx_label = tk.Label(task2_frame, text="f(x):")
task2_fx_label.pack(side=tk.LEFT)

task2_fx_entry = tk.Entry(task2_frame)
task2_fx_entry.pack(side=tk.LEFT)

task2_y_label = tk.Label(task2_frame, text="y:")
task2_y_label.pack(side=tk.LEFT)

task2_y_entry = tk.Entry(task2_frame)
task2_y_entry.pack(side=tk.LEFT)

task2_xy_label = tk.Label(task2_frame, text="xy:")
task2_xy_label.pack(side=tk.LEFT)

task2_xy_entry = tk.Entry(task2_frame)
task2_xy_entry.pack(side=tk.LEFT)

root.mainloop()
``Обратите внимание, что в коде предполагается наличие двух фотографий с формулами, "formula1.png" и "formula2.png". Вы должны заменить эти имена файлов на соответствующие имена фотографий, которые вы используете. Также убедитесь, что фотографии находятся в той же папке, где находится ваш скрипт.

Данный код позволяет выбрать одно из двух заданий с помощью ComboBox. При выборе задания открывается новое окно с формой для ввода данных и выводом результата вычислений. Фотография с формулой также отображается на форме.

Вы можете добавить или изменить элементы интерфейса в соответствии с вашими потребностями. Также не забудьте добавить свои формулы и логику вычислений для индивидуальных заданий.
