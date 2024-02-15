import pygame
import os

# Инициализация Pygame
pygame.init()

# Установка размеров окна
window_width = 800
window_height = 600
window = pygame.display.set_mode((window_width, window_height))

# Загрузка гиф-анимации
gif_path = "путь_к_вашей_гифке.gif"
gif = pygame.image.load(gif_path)

# Определение начальных координат для отображения гифки
gif_x = (window_width - gif.get_width()) // 2
gif_y = (window_height - gif.get_height()) // 2

# Основной цикл приложения
running = True
while running:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Очистка экрана
    window.fill((0, 0, 0))

    # Отображение гиф-анимации
    window.blit(gif, (gif_x, gif_y))

    # Обновление экрана
    pygame.display.flip()

# Завершение работы Pygame
pygame.quit()
