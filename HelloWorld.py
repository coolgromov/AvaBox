Извините за недоразумение. Вот исправленный код, который учитывает ваши пожелания:

```python
import tkinter as tk

# Создание окна
window = tk.Tk()
window.title("Мой рисунок")

# Размеры окна
width = 600
height = 400

# Создание холста
canvas = tk.Canvas(window, width=width, height=height)
canvas.pack()

# Рисование верхней половины экрана
canvas.create_rectangle(0, 0, width, height // 2, fill="blue")

# Рисование нижней половины экрана
canvas.create_rectangle(0, height // 2, width // 2, height, fill="yellow")
canvas.create_rectangle(width // 2, height // 2, width, height, fill="blue")

# Рисование облака на голубой половине
cloud_x = 70
cloud_y = height // 4
circle_radius = 20
circle_margin = 10

for _ in range(7):
    canvas.create_oval(cloud_x - circle_radius, cloud_y - circle_radius,
                       cloud_x + circle_radius, cloud_y + circle_radius,
                       fill="white", outline="black")
    cloud_x += circle_margin

# Рисование солнца на голубой половине
sun_x = width - 100
sun_y = height // 4
sun_radius = 50

canvas.create_oval(sun_x - sun_radius, sun_y - sun_radius,
                   sun_x + sun_radius, sun_y + sun_radius,
                   fill="yellow")

# Рисование лодки на синей половине
boat_x = width // 4
boat_y = height // 2 + 50
boat_width = 120
boat_height = 30

canvas.create_rectangle(boat_x, boat_y, boat_x + boat_width, boat_y + boat_height,
                        fill="brown")

# Рисование палки и паруса на синей половине
mast_x = boat_x + boat_width // 2
mast_y = boat_y

canvas.create_rectangle(mast_x - 5, mast_y, mast_x + 5, height // 2,
                        fill="brown")

canvas.create_polygon(mast_x, mast_y,
                      mast_x + 5, mast_y + 10,
                      mast_x - 5, mast_y + 10,
                      fill="brown")

# Рисование палки и зонта на желтой половине
umbrella_x = width // 2 + boat_width // 2
umbrella_y = mast_y
umbrella_height = height // 2 - mast_y

canvas.create_rectangle(umbrella_x - 5, umbrella_y, umbrella_x + 5, height // 2,
                        fill="orange")

canvas.create_polygon(umbrella_x, umbrella_y,
                      umbrella_x + 5, umbrella_y + 10,
                      umbrella_x - 5, umbrella_y + 10,
                      fill="orange")

# Запуск главного цикла окна
window.mainloop()
```

Теперь половины экрана синий и желтый цвета находятся друг на друге, а облако представлено кругами, расположенными близко друг к другу, чтобы создать эффект облака.
