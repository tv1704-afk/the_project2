import pygame
import sys
import time
import random

# Инициализация Pygame
pygame.init()

# Установка размеров окна
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))


# Загрузка изображения фона
background_image = pygame.image.load("fon.png")
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Загрузка изображений кнопок
button1_image = pygame.image.load("paintlogo.jpg")
button2_image = pygame.image.load("labirint.png")
button3_image = pygame.image.load("snake.png")

# Цвета
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
MENU_GRAY = (150, 150, 150)

# Шрифт
font = pygame.font.Font(None, 36)

# Параметры меню "Пуск"
start_menu_open = False
menu_height = 200  # Высота меню "Пуск"

# Переменные для рисования
drawing = False
last_pos = (0, 0)
canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill(WHITE)  # Начальное заполнение белым цветом

# Переменные для кнопок
button1_rect = pygame.Rect(50, 75, 100, 100)
button2_rect = pygame.Rect(50, 200, 100, 100)
button3_rect = pygame.Rect(50, 325, 100, 100)
dragging_button = None
offset_x = 0
offset_y = 0

# Время последнего нажатия для двойного клика
last_click_time = 0
click_delay = 0.5  # Время для двойного клика

# Кнопка с изображением
def draw_image_button(image, rect):
    image = pygame.transform.scale(image, (rect.width, rect.height))
    screen.blit(image, (rect.x, rect.y))

# Текстовая кнопка
def draw_text_button(text, x, y, width, height, color=GRAY):
    pygame.draw.rect(screen, color, (x, y, width, height))
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text_surface, text_rect)

# Функция для рисования
def run_paint_program():
    global drawing, last_pos
    drawing = False  # Сначала не рисуем

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                # Проверка нажатия на крестик для закрытия окна рисования
                if 760 <= mouse_x <= 790 and 10 <= mouse_y <= 40:
                    return  # Закрываем окно рисования
                if event.button == 1:  # Левый клик мыши
                    drawing = True
                    last_pos = event.pos
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Левый клик мыши
                    drawing = False
            if event.type == pygame.MOUSEMOTION:
                if drawing:
                    pygame.draw.line(canvas, BLACK, last_pos, event.pos, 5)  # Рисуем линию
                    last_pos = event.pos

        # Отображение белого холста
        screen.fill(WHITE)
        screen.blit(canvas, (0, 0))

        # Рисуем красный крестик для закрытия окна
        pygame.draw.rect(screen, RED, (760, 10, 30, 30))  # Квадрат для крестика
        pygame.draw.line(screen, WHITE, (760, 10), (790, 40), 5)  # Первая диагональ
        pygame.draw.line(screen, WHITE, (790, 10), (760, 40), 5)  # Вторая диагональ

        # Обновление экрана
        pygame.display.flip()

def run_maze_game():


    # Настройки
    CELL_SIZE = 20
    MAZE_WIDTH = WIDTH // CELL_SIZE
    MAZE_HEIGHT = HEIGHT // CELL_SIZE

    # Цвета
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)  # Цвет для выхода

    # Алгоритм генерации лабиринта
    def generate_maze(width, height):
        maze = [[1 for _ in range(width)] for _ in range(height)]
        start_x, start_y = 1, 1
        maze[start_y][start_x] = 0  # Проход
        stack = [(start_x, start_y)]

        while stack:
            x, y = stack[-1]
            neighbors = []

            for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
                nx, ny = x + dx, y + dy
                if 0 < nx < width and 0 < ny < height and maze[ny][nx] == 1:
                    neighbors.append((nx, ny))

            if neighbors:
                nx, ny = random.choice(neighbors)
                maze[(y + ny) // 2][(x + nx) // 2] = 0  # Удаляем стену
                maze[ny][nx] = 0  # Делаем проход
                stack.append((nx, ny))  # Добавляем в стек
            else:
                stack.pop()  # Если нет соседей, возвращаемся назад

        # Устанавливаем выход в правом нижнем углу
        maze[MAZE_HEIGHT - 2][MAZE_WIDTH - 2] = 0  # Проход
        return maze

    # Функция для отрисовки лабиринта
    def draw_maze(maze, player_pos, hit_count):
        for y in range(len(maze)):
            for x in range(len(maze[0])):
                color = WHITE if maze[y][x] == 0 else BLACK
                pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        # Рисуем игрока
        pygame.draw.rect(screen, GREEN, (player_pos[0] * CELL_SIZE, player_pos[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        # Рисуем выход
        pygame.draw.rect(screen, RED, ((MAZE_WIDTH - 2) * CELL_SIZE, (MAZE_HEIGHT - 2) * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        # Отображаем счётчик
        font = pygame.font.Font(None, 36)
        text = font.render(f"Счётчик стен: {hit_count}", True, RED)
        screen.blit(text, (10, 10))

    # Генерация лабиринта
    maze = generate_maze(MAZE_WIDTH, MAZE_HEIGHT)
    player_pos = [1, 1]  # Начальная позиция игрока
    hit_count = 0  # Счётчик столкновений с стенами

    # Основной игровой цикл
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Получаем позицию мыши и переводим в координаты лабиринта
        mouse_x, mouse_y = pygame.mouse.get_pos()
        new_player_pos = [mouse_x // CELL_SIZE, mouse_y // CELL_SIZE]

        # Проверяем, не упал ли игрок в стену
        if maze[new_player_pos[1]][new_player_pos[0]] == 0:
            player_pos = new_player_pos  # Обновляем позицию игрока
        else:
            hit_count += 1  # Увеличиваем счётчик, если игрок задел стену

        # Проверка на выход
        if player_pos == [MAZE_WIDTH - 2, MAZE_HEIGHT - 2]:
            in_maze_game = False  # Сбрасываем флаг после выхода
            return  # Выход из игры
        # Очищаем экран
        screen.fill(BLACK)
        draw_maze(maze, player_pos, hit_count)  # Отрисовываем лабиринт
        pygame.display.flip()  # Обновляем экран

# Основная функция
def main():
    global dragging_button, offset_x, offset_y, last_click_time, start_menu_open

    # Инициализация переменной для состояния меню
    start_menu_open = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos

                # Проверка нажатия кнопки "Пуск"
                if 10 <= mouse_x <= 90 and HEIGHT - 40 <= mouse_y <= HEIGHT - 10:
                    start_menu_open = not start_menu_open  # Переключаем состояние меню "Пуск"

                # Проверка нажатия на кнопки
                if button1_rect.collidepoint(event.pos):
                    current_time = time.time()
                    if current_time - last_click_time < click_delay:  # Двойной клик
                        run_paint_program()  # Запускаем программу рисования
                    last_click_time = current_time
                elif button2_rect.collidepoint(event.pos):
                    current_time = time.time()
                    if current_time - last_click_time < click_delay:  # Двойной клик
                        run_maze_game()
                    last_click_time = current_time
                elif button3_rect.collidepoint(event.pos):
                    current_time = time.time()
                    if current_time - last_click_time < click_delay:  # Двойной клик
                        print("Запуск программы 3")  # Здесь можно добавить код для запуска другой программы
                    last_click_time = current_time

                # Проверка нажатия для перемещения кнопок
                if event.button == 1:  # Левый клик мыши
                    if button1_rect.collidepoint(mouse_x, mouse_y):
                        dragging_button = button1_rect
                        offset_x = button1_rect.x - mouse_x
                        offset_y = button1_rect.y - mouse_y
                    elif button2_rect.collidepoint(mouse_x, mouse_y):
                        dragging_button = button2_rect
                        offset_x = button2_rect.x - mouse_x
                        offset_y = button2_rect.y - mouse_y
                    elif button3_rect.collidepoint(mouse_x, mouse_y):
                        dragging_button = button3_rect
                        offset_x = button3_rect.x - mouse_x
                        offset_y = button3_rect.y - mouse_y

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Левый клик мыши
                    dragging_button = None

            if event.type == pygame.MOUSEMOTION:
                if dragging_button:
                    dragging_button.x = event.pos[0] + offset_x
                    dragging_button.y = event.pos[1] + offset_y

        # Отрисовка фона
        screen.blit(background_image, (0, 0))

        # Отрисовка кнопок
        draw_image_button(button1_image, button1_rect)
        draw_image_button(button2_image, button2_rect)
        draw_image_button(button3_image, button3_rect)

        # Отрисовка нижней панели
        pygame.draw.rect(screen, GRAY, (0, HEIGHT - 40, WIDTH, 40))  # Нижняя панель
        pygame.draw.rect(screen, BLACK, (10, HEIGHT - 40, 80, 30))  # Кнопка "Пуск"
        draw_text_button("Пуск", 10, HEIGHT - 40, 80, 30, color=WHITE)

        # Отображение меню "Пуск", если оно открыто
        if start_menu_open:
            pygame.draw.rect(screen, MENU_GRAY, (0, HEIGHT - menu_height, WIDTH//3.5, menu_height))
            draw_text_button("Программы", 10, HEIGHT - menu_height + 20, 200, 40)
            draw_text_button("Выключение", 10, HEIGHT - menu_height + 70, 200, 40)
            draw_text_button("Настройки", 10, HEIGHT - menu_height + 120, 200, 40)

        # Обновление экрана
        pygame.display.flip()

# Запуск программы
if __name__ == "__main__":
    main()

