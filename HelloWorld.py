Для выполнения лабораторной работы №1 вам потребуется создать четыре файлы Python, используя библиотеку Tkinter для создания графического интерфейса. Каждый файл будет содержать код для решения соответствующей задачи.

Первая часть лабораторной работы:

Файл 1: decimal_to_other_bases.py
```python
import tkinter as tk

def convert_to_binary():
    decimal_value = int(decimal_entry.get())
    binary_value = bin(decimal_value)[2:]
    binary_result.config(text=binary_value)

def convert_to_octal():
    decimal_value = int(decimal_entry.get())
    octal_value = oct(decimal_value)[2:]
    octal_result.config(text=octal_value)

def convert_to_hexadecimal():
    decimal_value = int(decimal_entry.get())
    hexadecimal_value = hex(decimal_value)[2:]
    hexadecimal_result.config(text=hexadecimal_value)

root = tk.Tk()
root.title("Decimal to Other Bases Converter")

decimal_label = tk.Label(root, text="Decimal:")
decimal_label.pack()

decimal_entry = tk.Entry(root)
decimal_entry.pack()

binary_label = tk.Label(root, text="Binary:")
binary_label.pack()

binary_result = tk.Label(root)
binary_result.pack()

octal_label = tk.Label(root, text="Octal:")
octal_label.pack()

octal_result = tk.Label(root)
octal_result.pack()

hexadecimal_label = tk.Label(root, text="Hexadecimal:")
hexadecimal_label.pack()

hexadecimal_result = tk.Label(root)
hexadecimal_result.pack()

convert_button = tk.Button(root, text="Convert", command=lambda: [convert_to_binary(), convert_to_octal(), convert_to_hexadecimal()])
convert_button.pack()

root.mainloop()
```

Файл 2: binary_to_other_bases.py
```python
import tkinter as tk

def convert_to_decimal():
    binary_value = binary_entry.get()
    decimal_value = int(binary_value, 2)
    decimal_result.config(text=decimal_value)

def convert_to_octal():
    binary_value = binary_entry.get()
    decimal_value = int(binary_value, 2)
    octal_value = oct(decimal_value)[2:]
    octal_result.config(text=octal_value)

def convert_to_hexadecimal():
    binary_value = binary_entry.get()
    decimal_value = int(binary_value, 2)
    hexadecimal_value = hex(decimal_value)[2:]
    hexadecimal_result.config(text=hexadecimal_value)

root = tk.Tk()
root.title("Binary to Other Bases Converter")

binary_label = tk.Label(root, text="Binary:")
binary_label.pack()

binary_entry = tk.Entry(root)
binary_entry.pack()

decimal_label = tk.Label(root, text="Decimal:")
decimal_label.pack()

decimal_result = tk.Label(root)
decimal_result.pack()

octal_label = tk.Label(root, text="Octal:")
octal_label.pack()

octal_result = tk.Label(root)
octal_result.pack()

hexadecimal_label = tk.Label(root, text="Hexadecimal:")
hexadecimal_label.pack()

hexadecimal_result = tk.Label(root)
hexadecimal_result.pack()

convert_button = tk.Button(root, text="Convert", command=lambda: [convert_to_decimal(), convert_to_octal(), convert_to_hexadecimal()])
convert_button.pack()

root.mainloop()
```

Файл 3: octal_addition_and_subtraction.py
```python
import tkinter as tk

def convert_to_decimal():
    octal_value_a = octal_entry_a.get()
    octal_value_b = octal_entry_b.get()
    decimal_value_a = int(octal_value_a, 8)
    decimal_value_b = int(octal_value_b, 8)
    decimal_result_a.config(text=decimal_value_a)
    decimal_result_b.config(text=decimal_value_b)

    sum_result = decimal_value_a + decimal_value_b
    difference_result = decimal_value_a - decimal_value_b

    sum_result_label.config(text=sum_result)
    difference_result_label.config(text=difference_result)

root = tk.Tk()
root.title("Octal Addition and Subtraction")

octal_label_a = tk.Label(root, text="Octal A:")
octal_label_a.pack()

octal_entry_a = tk.Entry(root)
octal_entry_a.pack()

decimal_label_a = tk.Label(root, text="Decimal A:")
decimal_label_a.pack()

decimal_result_a = tk.Label(root)
decimal_result_a.pack()

octal_label_b = tk.Label(root, text="Octal B:")
octal_label_b.pack()

octal_entry_b = tk.Entry(root)
octal_entry_b.pack()

decimal_label_b = tk.Label(root, text="Decimal B:")
decimal_label_b.pack()

decimal_result_b = tk.Label(root)
decimal_result_b.pack()

sum_label = tk.Label(root, text="Sum:")
sum_label.pack()

sum_result_label = tk.Label(root)
sum_result_label.pack()

difference_label =Файл 4: triangle_area.py
```python
import tkinter as tk

def calculate_area():
    base = float(base_entry.get())
    side = float(side_entry.get())
    area = (base * side) / 2
    area_result.config(text=area)

root = tk.Tk()
root.title("Triangle Area Calculator")

base_label = tk.Label(root, text="Base:")
base_label.pack()

base_entry = tk.Entry(root)
base_entry.pack()

side_label = tk.Label(root, text="Side:")
side_label.pack()

side_entry = tk.Entry(root)
side_entry.pack()

area_label = tk.Label(root, text="Area:")
area_label.pack()

area_result = tk.Label(root)
area_result.pack()

calculate_button = tk.Button(root, text="Calculate", command=calculate_area)
calculate_button.pack()

root.mainloop()
```

Извините за пропущенный код. Вот полный код для файла `triangle_area.py`:

```python
import tkinter as tk

def calculate_area():
    base = float(base_entry.get())
    side = float(side_entry.get())
    area = (base * side) / 2
    area_result.config(text=area)

root = tk.Tk()
root.title("Triangle Area Calculator")

base_label = tk.Label(root, text="Base:")
base_label.pack()

base_entry = tk.Entry(root)
base_entry.pack()

side_label = tk.Label(root, text="Side:")
side_label.pack()

side_entry = tk.Entry(root)
side_entry.pack()

area_label = tk.Label(root, text="Area:")
area_label.pack()

area_result = tk.Label(root)
area_result.pack()

calculate_button = tk.Button(root, text="Calculate", command=calculate_area)
calculate_button.pack()

root.mainloop()
```

Сохраните этот код в файле `triangle_area.py` и запустите его для проверки работы программы.
