import tkinter as tk
from tkinter import messagebox

# Функция для проверки пароля и определения степени доступа
def check_password():
    password = password_entry.get()
    access_level = ""

    if password in ["9583", "1747"]:
        access_level = "Доступ к модулям базы А, В, С"
    elif password in ["3331", "7922"]:
        access_level = "Доступ к модулям базы А, В"
    elif password in ["9455", "8997"]:
        access_level = "Доступ к модулю базы С"
    else:
        messagebox.showerror("Ошибка", "Неверный пароль!")
        return

    messagebox.showinfo("Степень доступа", access_level)

# Функция для определения действия в зависимости от второй цифры числа
def process_number():
    number = int(number_entry.get())
    second_digit = number // 10 % 10
    
    if 0 <= second_digit <= 5:
        result = second_digit ** 2
    elif 6 <= second_digit <= 7:
        result = (number % 10) + (number // 100)
    elif second_digit >= 8:
        result = sum(int(digit) for digit in str(number))
    else:
        messagebox.showerror("Ошибка", "Некорректное число!")
        return

    messagebox.showinfo("Результат", f"Результат: {result}")

# Функция для определения следующего дня и праздничных дней
def next_day():
    date = date_entry.get()
    day = int(date[:2])
    month = int(date[2:4])
    year = int(date[4:])

    if day == 31:
        messagebox.showinfo("Результат", "Последний день месяца!")
    else:
        next_date = ""

        if day == 30 or (month == 2 and day == 28):
            next_date += "01."
            month += 1
        elif day == 31 or (month == 12 and day == 31):
            next_date += "01."
            month = 1
            year += 1
        else:
            day += 1

        next_date += str(month).zfill(2) + "." + str(year)
        
        holiday = ""
        if date == "31122014":
            holiday = "С наступающим новым годом!"
        elif date == "06012015":
            holiday = "С Рождеством!"

        if next_date in ["01.01." + str(year), "07.01." + str(year), "23.02." + str(year), "08.03." + str(year)]:
            messagebox.showinfo("Результат", f"{holiday} Завтра {next_date} (праздник)")
        else:
            messagebox.showinfo("Результат", f"{holiday} Завтра {next_date}")

# Создание главного окна
root = tk.Tk()
root.title("Групповая работа №4")

# Задание 1
task1_frame = tk.LabelFrame(root, text="Задание 1: Проверка пароля")
task1_frame.pack(padx=10, pady=10)

password_label = tk.Label(task1_frame, text="Введите пароль:")
password_label.pack()

password_entry = tk.Entry(task1_frame, show="*")
password_entry.pack(pady=5)

password_button = tk.Button(task1_frame, text="Проверить", command=check_password)
password_button.pack()

# Задание 2
task2_frame = tk.LabelFrame(root, text="Задание 2: Обработка числа")
task2_frame.pack(padx=10, pady=10)

number_label = tk.Label(task2_frame, text="Введите трехзначное число:")
number_label.pack()

number_entry = tk.Entry(task2_frame)
number_entry.pack(pady=5)

number_button = tk.Button(task2_frame, text="Выполнить", command=process_number)
number_button.pack()

# Задание 3
task3_frame = tk.LabelFrame(root, text="Задание 3: Определение следующего дня")
task3_frame.pack(padx=10, pady=10)

date_label = tk.Label(task3_frame, text="Введите дату (ддммгггг):")
date_label.pack()

date_entry= tk.Entry(task3_frame)
date_entry.pack(pady=5)

date_button = tk.Button(task3_frame, text="Выполнить", command=next_day)
date_button.pack()

# Запуск главного цикла обработки событий
root.mainloop()
