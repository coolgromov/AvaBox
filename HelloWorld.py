import pygame

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

# Определение начального масштаба гифки
scale = 1.0

# Определение флага, указывающего на увеличение или уменьшение масштаба
scaling_up = True

# Основной цикл приложения
running = True
while running:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Изменение масштаба гифки
    if scaling_up:
        scale += 0.01
        if scale >= 1.5:
            scaling_up = False
    else:
        scale -= 0.01
        if scale <= 0.5:
            scaling_up = True

    # Очистка экрана
    window.fill((0, 0, 0))

    # Изменение размеров гиф-анимации с учетом масштаба
    gif_width = int(gif.get_width() * scale)
    gif_height = int(gif.get_height() * scale)
    gif_scaled = pygame.transform.scale(gif, (gif_width, gif_height))

    # Определение новых координат для отображения гифки
    gif_x = (window_width - gif_width) // 2
    gif_y = (window_height - gif_height) // 2

    # Отображение гиф-анимации
    window.blit(gif_scaled, (gif_x, gif_y))

    # Обновление экрана
    pygame.display.flip()

# Завершение работы Pygame
pygame.quit()
