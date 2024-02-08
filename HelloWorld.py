Извините за недоразумение. Вот исправленный код, который использует библиотеку Tkinter и выводит результаты, соответствующие значениям из приведенных тестов:

```python
import tkinter as tk

def calculate_speed():
    distance = float(distance_entry.get())
    hours = int(hours_entry.get())
    minutes = int(minutes_entry.get())
    seconds = int(seconds_entry.get())

    total_hours = hours + minutes / 60 + seconds / 3600

    speed_kmph = distance / total_hours
    speed_mps = speed_kmph * 1000 / 3600

    speed_kmph_result.config(text=f"{speed_kmph:.1f} км/час")
    speed_mps_result.config(text=f"{speed_mps:.1f} м/сек")

root = tk.Tk()
root.title("Speed Calculator")

distance_label = tk.Label(root, text="Расстояние (в километрах):")
distance_label.pack()

distance_entry = tk.Entry(root)
distance_entry.pack()

hours_label = tk.Label(root, text="Количество часов:")
hours_label.pack()

hours_entry = tk.Entry(root)
hours_entry.pack()

minutes_label = tk.Label(root, text="Количество минут:")
minutes_label.pack()

minutes_entry = tk.Entry(root)
minutes_entry.pack()

seconds_label = tk.Label(root, text="Количество секунд:")
seconds_label.pack()

seconds_entry = tk.Entry(root)
seconds_entry.pack()

speed_kmph_label = tk.Label(root, text="Скорость (в км/час):")
speed_kmph_label.pack()

speed_kmph_result = tk.Label(root)
speed_kmph_result.pack()

speed_mps_label = tk.Label(root, text="Скорость (в м/сек):")
speed_mps_label.pack()

speed_mps_result = tk.Label(root)
speed_mps_result.pack()

calculate_button = tk.Button(root, text="Рассчитать", command=calculate_speed)
calculate_button.pack()

root.mainloop()
```

Сохраните этот код в файле `speed_calculator.py` и запустите его. Вы сможете ввести значения из тестов (например, расстояние - 22, часы - 1, минуты - 25, секунды - 30) и получить результаты, соответствующие значениям из тестов.
