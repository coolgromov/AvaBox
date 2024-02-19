Хорошо! Давайте решим каждое из заданий по порядку, используя библиотеку Matplotlib.

Задание 18: Построение графика функции x^2 на отрезке x ∈ [-2, 2] с шагом выборки данных 0.1.

```python
import matplotlib.pyplot as plt
import numpy as np

# Генерация данных
x = np.arange(-2, 2, 0.1)
y = x ** 2

# Построение графика
plt.plot(x, y)

# Добавление подписей
plt.xlabel('x')
plt.ylabel('y')
plt.title('График функции y = x^2')

# Отображение графика
plt.show()
```

Задание 19: Изменение цвета линии, типа линии и маркеров, а также шага выборки данных. Добавление сетки и сохранение графика в разных форматах.

```python
import matplotlib.pyplot as plt
import numpy as np

# Генерация данных
x = np.arange(-2, 2, 0.05)  # Изменим шаг выборки на 0.05
y = x ** 2

# Построение графика с изменениями
plt.plot(x, y, color='r', linestyle='--', marker='o', markersize=3)

# Добавление подписей
plt.xlabel('x')
plt.ylabel('y')
plt.title('График функции y = x^2')

# Добавление сетки
plt.grid(True)

# Сохранение графика в разных форматах
plt.savefig('graph.png')
plt.savefig('graph.pdf')
plt.savefig('graph.jpg')
plt.savefig('graph.eps')

# Отображение графика
plt.show()
```

Задание 20: Построение семейства функций на одном графике различными цветами.

```python
import matplotlib.pyplot as plt
import numpy as np

# Генерация данных
x = np.linspace(-1, 1, 100)  # Увеличим количество точек для более плавного графика

# Степенные многочлены с целыми степенями от 1 до 6
for power in range(1, 7):
    y = x ** power
    plt.plot(x, y, label=f'x^{power}')

# Синусоиды y = sin(ωt) с различными частотами
frequencies = np.arange(2, 9) * np.pi
for freq in frequencies:
    y = np.sin(freq * x)
    plt.plot(x, y, label=f'sin({freq:.1f}t)')

# Синусоиды y = sin(2πt + φ0) с различными начальными фазами
initial_phases = np.arange(0, np.pi + np.pi / 6, np.pi / 6)
for phase in initial_phases:
    y = np.sin(2 * np.pi * x + phase)
    plt.plot(x, y, label=f'sin(2πt + {phase:.2f})')

# Логарифмические функции log2(x), ln(x) и log10(x)
y = np.log2(x)
plt.plot(x, y, label='log2(x)')

y = np.log(x)
plt.plot(x, y, label='ln(x)')

y = np.log10(x)
plt.plot(x, y, label='log10(x)')

# Гиперболические функции sh(x), ch(x) и th(x)
y = np.sinh(x)
plt.plot(x, y, label='sh(x)')

y = np.cosh(x)
plt.plot(x, y, label='ch(x)')

y = np.tanh(x)
plt.plot(x, y, label='th(x)')

# Добавление подписей
plt.xlabel('x')
plt.ylabel('y')
plt.title('Семейство функций')

# Добавление легенды
plt.legend()

# Отображение графика
plt.show()
```

Надеюсь, это поможет вам выполнить задания с использованием библиотеки Matplotlib в Python!
