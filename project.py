import pygame
import sys
import time
import random

pygame.init()
screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h

font = pygame.font.Font(None, 36)

background_image = pygame.image.load("fon.png")
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

button1_image = pygame.image.load("paintlogo.jpg")
button2_image = pygame.image.load("labirint.png")
button3_image = pygame.image.load("prov.png")
button4_image = pygame.image.load("files.png")
button5_image = pygame.image.load("files.png")
button6_image = pygame.image.load("bin.png")

menu_image3 = pygame.image.load("off.png")
menu_image4 = pygame.image.load("nastroyki.png")
menu_image5 = pygame.image.load("rightmenu.png")
menu_image6 = pygame.image.load("menu.png")

GRAY = (228, 239, 250)
WHITE = (255,255,255)
RED = (255,0,0)
BLACK = (0,0,0)

drawing = False
last_pos = (0, 0)
canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill((255,255,255))

button1_rect = pygame.Rect(50, 75, 75, 75)
button2_rect = pygame.Rect(50, 200, 75, 75)
button3_rect = pygame.Rect(50, 325, 75, 75)
button4_rect = pygame.Rect(175, 75, 75, 75)

dragging_button = None
game_active = False
offset_x = 0
offset_y = 0
last_click_time = 0
click_delay = 0.5

def draw_image_button(image, rect):
    image = pygame.transform.scale(image, (rect.width, rect.height))
    screen.blit(image, (rect.x, rect.y))

def draw_text_button(text, x, y, width, height, color=GRAY):
    pygame.draw.rect(screen, color, (x, y, width, height))
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text_surface, text_rect)

def run_paint_program(screen, canvas):
    global WIDTH
    drawing = False
    eraser_mode = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos

                if WIDTH-40 <= mouse_x <= WIDTH-10 and 10 <= mouse_y <= 40:
                    return

                if WIDTH//2-80 <= mouse_x <= WIDTH//2 and 10 <= mouse_y <= 40:
                    eraser_mode = not eraser_mode
                    continue

                if event.button == 1:
                    drawing = True
                    last_pos = event.pos
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    drawing = False
            if event.type == pygame.MOUSEMOTION:
                if drawing:
                    color = WHITE if eraser_mode else BLACK
                    pygame.draw.line(canvas, color, last_pos, event.pos, 5)
                    last_pos = event.pos

        screen.fill(WHITE)
        screen.blit(canvas, (0, 0))

        pygame.draw.rect(screen, RED, (WIDTH-40, 10, 30, 30))
        pygame.draw.line(screen, WHITE, (WIDTH-35, 15), (WIDTH-15, 35), 3)
        pygame.draw.line(screen, WHITE, (WIDTH-15, 15), (WIDTH-35, 35), 3)

        pygame.draw.rect(screen, (0, 0, 0), (WIDTH//2-80, 10, 80, 30))
        font = pygame.font.Font(None, 24)
        text = font.render("ластик" if eraser_mode else "карандаш", True, WHITE)
        screen.blit(text, (WIDTH//2-75, 15))

        pygame.display.flip()


def run_maze_game():

    global dragging_button

    CELL_SIZE = 20
    MAZE_WIDTH = WIDTH // CELL_SIZE
    MAZE_HEIGHT = HEIGHT // CELL_SIZE

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)

    def generate_maze(width, height):
        maze = [[1 for _ in range(width)] for _ in range(height)]
        start_x, start_y = 1, 1
        maze[start_y][start_x] = 0
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
                maze[(y + ny) // 2][(x + nx) // 2] = 0
                maze[ny][nx] = 0
                stack.append((nx, ny))
            else:
                stack.pop()

        maze[MAZE_HEIGHT - 2][MAZE_WIDTH - 2] = 0
        return maze

    def draw_maze(maze, player_pos):
        for y in range(len(maze)):
            for x in range(len(maze[0])):
                color = WHITE if maze[y][x] == 0 else BLACK
                pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        pygame.draw.rect(screen, GREEN, (player_pos[0] * CELL_SIZE, player_pos[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(screen, RED, ((MAZE_WIDTH - 2) * CELL_SIZE, (MAZE_HEIGHT - 2) * CELL_SIZE, CELL_SIZE, CELL_SIZE))


    maze = generate_maze(MAZE_WIDTH, MAZE_HEIGHT)
    pygame.mouse.set_pos(25,25)
    player_pos = [1, 1]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        mouse_x, mouse_y = pygame.mouse.get_pos()
        new_player_pos = [mouse_x // CELL_SIZE, mouse_y // CELL_SIZE]

        if maze[new_player_pos[1]][new_player_pos[0]] == 0:
            player_pos = new_player_pos
        else:
            # Логика проигрыша
            screen.fill(WHITE)
            font = pygame.font.Font(None, 74)
            text = font.render("Вы проиграли", True, BLACK)
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(text, text_rect)
            pygame.display.flip()
            pygame.time.delay(1000)
            return

        if player_pos == [MAZE_WIDTH - 2, MAZE_HEIGHT - 2]:
            return

        screen.fill(BLACK)
        draw_maze(maze, player_pos)
        pygame.display.flip()

file_system = {
    "home": {
        "Documents": {
            "file1.txt": "Содержимое файла 1",
            "file2.txt": "Содержимое файла 2",
        },
        "Pictures": {
            "image1.png": "Изображение 1",
            "image2.jpg": "Изображение 2",
        },
        "Music": {},
        "Videos": {},
    }
}
def run_file_explorer_simulator(start_directory="home"):
    global file_system
    # Настройки
    WIDTH, HEIGHT = screen.get_size()
    BACKGROUND_COLOR = (230, 230, 230)
    TEXT_COLOR = (0, 0, 0)
    FONT_SIZE = 24
    ITEM_PADDING = 10
    BUTTON_COLOR = (100, 150, 255)
    BUTTON_HOVER_COLOR = (150, 200, 255)
    SELECTION_COLOR = (0, 191, 255, 100)  # Полупрозрачный голубой цвет

    # Начальная директория
    current_path = start_directory.split('/')  # Разделяем путь на части
    selected_items = []
    clipboard = []  # Буфер обмена для копирования/вырезания
    last_click_time = 0
    is_selecting = False
    selection_start = None

    # Функция для получения текущего уровня файловой системы
    def get_current_directory():
        directory = file_system
        for folder in current_path:
            if folder in directory:  # Проверяем, существует ли папка
                directory = directory[folder]
            else:
                print(f"Директория '{folder}' не найдена. Открывается домашняя директория.")
                return file_system["home"]  # Возвращаем домашнюю директорию, если путь не найден
        return directory

    # Функция для отрисовки кнопки
    def draw_button(rect, text, hover=False):
        color = BUTTON_HOVER_COLOR if hover else BUTTON_COLOR
        pygame.draw.rect(screen, color, rect)
        text_surface = font.render(text, True, TEXT_COLOR)
        text_rect = text_surface.get_rect(center=rect.center)
        screen.blit(text_surface, text_rect)

    # Функция для отображения мини-меню
    def draw_context_menu(x, y):
        menu_items = ["Копировать", "Вырезать", "Вставить"]
        menu_rects = []
        for index, item in enumerate(menu_items):
            rect = pygame.Rect(x, y + index * (FONT_SIZE + ITEM_PADDING), 150, FONT_SIZE + ITEM_PADDING)
            menu_rects.append(rect)
            pygame.draw.rect(screen, BUTTON_COLOR, rect)
            text_surface = font.render(item, True, TEXT_COLOR)

            text_rect = text_surface.get_rect(center=rect.center)
            screen.blit(text_surface, text_rect)
        return menu_rects

    def perform_action(action, selected_elements):
        global clipboard, selected_items

        current_directory = get_current_directory()  # Получаем текущую директорию
        selected_elements = list(selected_elements)  # Выделенные элементы

        if action == "Копировать":
            clipboard = []
            for item in selected_elements:
                if item in current_directory:
                    # Проверяем, является ли элемент папкой
                    if isinstance(current_directory[item], dict):
                        # Копируем содержимое папки
                        clipboard.append({item: current_directory[item]})
                    else:
                        clipboard.append(item)  # Копируем файл
            print("Элементы скопированы в буфер:", clipboard)

        elif action == "Вырезать":
            clipboard = []
            for item in selected_elements:
                if item in current_directory:
                    # Проверяем, является ли элемент папкой
                    if isinstance(current_directory[item], dict):
                        # Вырезаем содержимое папки
                        clipboard.append({item: current_directory[item]})
                        del current_directory[item]  # Удаляем папку из текущей директории
                    else:
                        clipboard.append(item)  # Вырезаем файл
                        del current_directory[item]  # Удаляем файл из текущей директории
            print("Элементы вырезаны и скопированы в буфер:", clipboard)

        elif action == "Вставить":
            if clipboard:
                for item in clipboard:
                    if isinstance(item, dict):  # Если это папка с содержимым
                        folder_name = list(item.keys())[0]
                        if folder_name not in current_directory:
                            current_directory[folder_name] = item[folder_name]  # Вставляем папку
                        else:
                            print(f"Папка {folder_name} уже существует в директории!")
                    else:  # Если это файл
                        if item not in current_directory:
                            current_directory[item] = "Содержимое вставленного элемента"  # Добавляем файл из буфера
                        else:
                            print(f"Элемент {item} уже существует в директории!")
                print("Элементы вставлены из буфера:", clipboard)
            else:
                print("Буфер обмена пуст!")


    # Основной цикл
    running = True
    context_menu_visible = False
    context_menu_pos = (0, 0)
    menu_rects = []  # Инициализация переменной
    font = pygame.font.Font(None, 23)
    back_button_rect = pygame.Rect(WIDTH - 370, HEIGHT - 80, 150, 50)
    exit_button_rect = pygame.Rect(WIDTH - 170, HEIGHT - 80, 150, 50)

    while running:
        screen.fill(BACKGROUND_COLOR)

        # Получаем текущую директорию
        current_directory = get_current_directory()
        items = list(current_directory.keys())

        # Отображаем файлы и папки
        items_per_row = 5  # Количество элементов в строке
        item_width = 100    # Ширина элемента
        item_height = 100   # Высота элемента
        ITEM_PADDING = 20   # Отступ между элементами

        for index, item in enumerate(items):
            # Рассчитываем позицию элемента
            item_x = 20 + (index % items_per_row) * (item_width + ITEM_PADDING)  # Позиция по оси X
            item_y = 20 + (index // items_per_row) * (item_height + ITEM_PADDING)  # Позиция по оси Y

            # Создаем квадратную область для каждого элемента
            item_rect = pygame.Rect(item_x, item_y, item_width, item_height)

            # Отображаем выделение, если элемент выбран
            if item in selected_items:
                pygame.draw.rect(screen, SELECTION_COLOR, item_rect)

            # Отображаем изображение, соответствующее элементу
            # Убедитесь, что button4_image имеет правильные размеры
            scaled_image = pygame.transform.scale(button4_image, (item_width, item_height))
            screen.blit(scaled_image, (item_x, item_y))

            # Отображаем текст под изображением
            item_surface = font.render(item, True, TEXT_COLOR)
            text_rect = item_surface.get_rect(center=(item_x + item_width // 2, item_y + item_height + 5))
            screen.blit(item_surface, text_rect)  # Центрируем текст под изображением



        # Отображаем текущий путь
        path_surface = font.render(f"Текущий путь: {'/'.join(current_path)}", True, TEXT_COLOR)
        screen.blit(path_surface, (20, HEIGHT - 60))

        # Создаем кнопки
        back_button_rect = pygame.Rect(WIDTH - 370, HEIGHT - 80, 150, 50)
        exit_button_rect = pygame.Rect(WIDTH - 170, HEIGHT - 80, 150, 50)

        # Проверка наведения мыши на кнопки
        mouse_x, mouse_y = pygame.mouse.get_pos()
        back_button_hover = back_button_rect.collidepoint(mouse_x, mouse_y)
        exit_button_hover = exit_button_rect.collidepoint(mouse_x, mouse_y)

        # Отрисовка кнопок
        draw_button(back_button_rect, "Назад", back_button_hover)
        draw_button(exit_button_rect, "Выход", exit_button_hover)

        # Отображение контекстного меню
        if context_menu_visible:
            menu_rects = draw_context_menu(context_menu_pos[0], context_menu_pos[1])  # Обновляем menu_rects

                # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos

                if context_menu_visible:  # Игнорируем клики, если меню активно
                    for index, rect in enumerate(menu_rects):
                        if rect.collidepoint(mouse_pos):
                            perform_action(["Копировать", "Вырезать", "Вставить"][index], selected_items)
                            context_menu_visible = False  # Закрываем меню после выбора
                    continue  # Пропускаем остальные действия

                if event.button == 1:  # Левый клик
                    clicked_item = None

                    # Проверка клика по элементам
                    for index, item in enumerate(items):
                        item_rect = pygame.Rect(20 + (index % items_per_row) * (item_width + ITEM_PADDING),
                         20 + (index // items_per_row) * (item_height + ITEM_PADDING),
                         item_width,
                         item_height)
                        if item_rect.collidepoint(mouse_pos):
                            clicked_item = item
                            break

                    # Если кликнули в пустое место, очищаем выделение и закрываем меню
                    if clicked_item is None:
                        selected_items.clear()
                        context_menu_visible = False  # Закрываем контекстное меню
                    else:
                        # Очистка выделения перед добавлением нового
                        selected_items.clear()
                        selected_items.append(clicked_item)

                    # Двойной клик для открытия папки
                    current_time = pygame.time.get_ticks()
                    if clicked_item and current_time - last_click_time < 300:  # Проверка на двойной клик
                        if not context_menu_visible:
                            if isinstance(current_directory[clicked_item], dict):  # Если это папка
                                current_path.append(clicked_item)  # Переход внутрь папки
                            last_click_time = 0  # Сброс таймера
                    else:
                        last_click_time = current_time

                    # Проверка нажатия кнопок
                    if back_button_rect.collidepoint(mouse_pos):
                        if not context_menu_visible:
                            if current_path:
                                current_path.pop()  # Возврат на уровень вверх
                    if exit_button_rect.collidepoint(mouse_pos):
                        running = False

                elif event.button == 3:  # Правый клик
                    context_menu_visible = True  # Открываем меню
                    context_menu_pos = event.pos

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Левый клик
                    is_selecting = False

            if event.type == pygame.MOUSEMOTION:
                if event.buttons[0]:  # Если левая кнопка мыши нажата
                    if not is_selecting:
                        is_selecting = True
                        selection_start = event.pos

                    # Логика выделения
                    selection_rect = pygame.Rect(selection_start, (event.pos[0] - selection_start[0], event.pos[1] - selection_start[1]))

                    for index, item in enumerate(items):
                        item_rect = pygame.Rect(20, 20 + index * (FONT_SIZE + ITEM_PADDING), WIDTH - 40, FONT_SIZE + ITEM_PADDING)
                        if selection_rect.colliderect(item_rect):
                            if item not in selected_items:
                                selected_items.append(item)  # Добавляем элемент в выделенные
                        else:
                            if item in selected_items:
                                selected_items.remove(item)  # Убираем элемент из выделенных

        # Обновляем экран
        pygame.display.flip()
    font = pygame.font.Font(None, 36)

menu_active = False

def draw_menu():

    global HEIGHT, menu_active
    if menu_active == False:
        menu_x, menu_y = 0,HEIGHT
    else:
        menu_x, menu_y = 0,HEIGHT-695

    BACKGROUND_COLOR = (200, 230, 250)
    BUTTON_COLOR = (200, 230, 250)
    TEXT_COLOR = (0, 0, 0)
    MENU_WIDTH, MENU_HEIGHT = 600, 650

    font = pygame.font.SysFont("Arial", 20)

    button_size = 20

    buttons = [("", (menu_x + 10, MENU_HEIGHT - button_size * 2 * 2 + menu_y)),
               ("", (menu_x + 10, MENU_HEIGHT - button_size * 2 + menu_y))]

    programs = [("paint", (10, 0)), ("лабиринт", (10, 0)),
                ("проводник", (10, 0)), ("file2", (10, 0)),
                ("file3", (10, 0)), ("bin", (10, 0))]

    app_icons = [button1_image, button2_image, button3_image, button4_image, button5_image, button6_image]
    app_icons = [pygame.transform.scale(icon, (40, 40)) for icon in app_icons]  # Изменяем размер иконок

    button_images = [menu_image4, menu_image3]
    button_images = [pygame.transform.scale(img, (button_size, button_size)) for img in button_images]

    program_images = [button1_image, button2_image, button3_image, button4_image, button5_image, button6_image]
    program_images = [pygame.transform.scale(img, (30, 30)) for img in program_images]

    app_bgs = [pygame.Surface((80, 80)) for _ in range(6)]
    for bg in app_bgs:
        bg.fill((240, 250, 250))

    pygame.draw.rect(screen, BACKGROUND_COLOR, (menu_x, menu_y, MENU_WIDTH, MENU_HEIGHT))

    left_column_width = 50
    pygame.draw.rect(screen, BUTTON_COLOR, (menu_x, menu_y, left_column_width, MENU_HEIGHT - button_size * 2))

    button_rects = []
    for i, (button_text, (x, y)) in enumerate(buttons):
        rect = pygame.Rect(x, y, button_size, button_size)
        button_rects.append(rect)
        screen.blit(button_images[i], (x, y))
        button_label = font.render(button_text, True, TEXT_COLOR)
        screen.blit(button_label, (x + 5, y + 5))

    central_column_x = left_column_width + menu_x
    central_column_width = 250
    program_list_y = 60 + menu_y

    program_header = font.render("Список программ", True, TEXT_COLOR)
    screen.blit(program_header, (central_column_x + 10, 10 + menu_y))

    program_rects = []
    for i, (program_name, _) in enumerate(programs):
        rect = pygame.Rect(central_column_x, program_list_y + i * 40, central_column_width, 38)
        program_rects.append(rect)
        pygame.draw.rect(screen, BUTTON_COLOR, rect)
        screen.blit(program_images[i], (central_column_x, program_list_y + i * 40 + 4))
        program_text = font.render(program_name, True, TEXT_COLOR)
        screen.blit(program_text, (central_column_x + 40, program_list_y + i * 40 + 8))

    right_column_x = central_column_x + central_column_width + 20

    training_header = font.render("Обучение", True, TEXT_COLOR)
    screen.blit(training_header, (right_column_x + 10, 10 + menu_y))
    app_rects = []
    for i, bg in enumerate(app_bgs):
        x_position = right_column_x + (i % 3) * 90
        y_position = 60 + (i // 3) * 90 + menu_y
        screen.blit(bg, (x_position, y_position))

        rect = pygame.Rect(x_position, y_position, 80, 80)
        app_rects.append(rect)

    for i, icon in enumerate(app_icons):
        x_position = right_column_x + (i % 3) * 90 + 20
        y_position = 60 + (i // 3) * 90 + menu_y + 20
        screen.blit(icon, (x_position, y_position))

    mouse_pos = pygame.mouse.get_pos()
    mouse_click = pygame.mouse.get_pressed()

    if mouse_click[0]:
        if button_rects[1].collidepoint(mouse_pos):
            pygame.quit()
            exit()

    if mouse_click[0]:
        for i, rect in enumerate(app_rects):
            if rect.collidepoint(mouse_pos):
                if i == 0:
                    run_paint_program(screen,canvas)
                elif i == 1:
                    run_maze_game()
                elif i == 2:
                    run_file_explorer_simulator()
                elif i == 3:
                    run_file_explorer_simulator("home/Documents")
                elif i == 4:
                    run_file_explorer_simulator("home/Pictures")
                elif i == 5:
                    run_file_explorer_simulator()

    if mouse_click[0]:
        for i, rect in enumerate(program_rects):
            if rect.collidepoint(mouse_pos):
                if i == 0:
                    run_paint_program(screen,canvas)
                elif i == 1:
                    run_maze_game()
                elif i == 2:
                    run_file_explorer_simulator()
                elif i == 3:
                    run_file_explorer_simulator("home/Documents")
                elif i == 4:
                    run_file_explorer_simulator("home/Pictures")
                elif i == 5:
                    run_file_explorer_simulator()

    pygame.display.flip()

def main():
    global dragging_button, offset_x, offset_y, last_click_time, menu_active, HEIGHT, WIDTH, game_active

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos

                if 10 <= mouse_x <= 90 and HEIGHT - 40 <= mouse_y <= HEIGHT - 10:
                    menu_active = not menu_active
                elif mouse_x > 650 or mouse_y < HEIGHT - 695:
                    menu_active = False

                if not menu_active:
                    if game_active == False:
                        game_active = True
                        if button1_rect.collidepoint(event.pos):
                            current_time = time.time()
                            if current_time - last_click_time < click_delay:
                                run_paint_program(screen, canvas)
                            last_click_time = current_time
                        elif button2_rect.collidepoint(event.pos):
                            current_time = time.time()
                            if current_time - last_click_time < click_delay:
                                run_maze_game()
                            last_click_time = current_time
                        elif button3_rect.collidepoint(event.pos):
                            current_time = time.time()
                            if current_time - last_click_time < click_delay:
                                run_file_explorer_simulator()
                            last_click_time = current_time
                        elif button4_rect.collidepoint(event.pos):
                            current_time = time.time()
                            if current_time - last_click_time < click_delay:
                                run_file_explorer_simulator()
                            last_click_time = current_time

                if event.button == 1:
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
                    elif button4_rect.collidepoint(mouse_x, mouse_y):
                        dragging_button = button4_rect
                        offset_x = button4_rect.x - mouse_x
                        offset_y = button4_rect.y - mouse_y

            if event.type == pygame.MOUSEMOTION:
                if game_active == False:
                    if dragging_button:  # Если кнопка перетаскивается
                        new_x = event.pos[0] + offset_x  # Новые координаты
                        new_y = event.pos[1] + offset_y

                        # Проверка границ
                        if new_x < 0:
                            new_x = 0
                        elif new_x + dragging_button.width > WIDTH:
                            new_x = WIDTH - dragging_button.width

                        if new_y < 0:
                            new_y = 0
                        elif new_y + dragging_button.height > HEIGHT - 45:
                            new_y = HEIGHT - 45 - dragging_button.height

                        # Обновляем позицию кнопки
                        dragging_button.x = new_x
                        dragging_button.y = new_y

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Если кнопка мыши отпущена
                    dragging_button = None  # Сбросить состояние перетаскивания

        screen.blit(background_image, (0, 0))

        pygame.draw.rect(screen, GRAY, (0, HEIGHT - 45, WIDTH, 45))
        draw_image_button(menu_image5, pygame.Rect(WIDTH - 270, HEIGHT - 45, 270, 45))
        draw_image_button(menu_image6, pygame.Rect(0, HEIGHT - 45, 45, 45))

        draw_image_button(button1_image, button1_rect)
        draw_image_button(button2_image, button2_rect)
        draw_image_button(button3_image, button3_rect)
        draw_image_button(button6_image, button4_rect)

        draw_menu()
        game_active = False
        pygame.display.flip()

if __name__ == "__main__":
    main()

