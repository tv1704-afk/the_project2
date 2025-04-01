import pygame
import sys
import time
import random

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))


background_image = pygame.image.load("fon.png")
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

button1_image = pygame.image.load("paintlogo.jpg")
button2_image = pygame.image.load("labirint.png")
button3_image = pygame.image.load("snake.png")

GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
MENU_GRAY = (150, 150, 150)

start_menu_open = False
menu_height = 200  # Высота меню "Пуск"

drawing = False
last_pos = (0, 0)
canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill(WHITE) 

button1_rect = pygame.Rect(50, 75, 100, 100)
button2_rect = pygame.Rect(50, 200, 100, 100)
button3_rect = pygame.Rect(50, 325, 100, 100)
dragging_button = None
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

def run_paint_program():
    global drawing, last_pos
    drawing = False 

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if 760 <= mouse_x <= 790 and 10 <= mouse_y <= 40:
                    return 
                if event.button == 1: 
                    drawing = True
                    last_pos = event.pos
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1: 
                    drawing = False
            if event.type == pygame.MOUSEMOTION:
                if drawing:
                    pygame.draw.line(canvas, BLACK, last_pos, event.pos, 5) 
                    last_pos = event.pos

        screen.fill(WHITE)
        screen.blit(canvas, (0, 0))

        pygame.draw.rect(screen, RED, (760, 10, 30, 30)) 
        pygame.draw.line(screen, WHITE, (760, 10), (790, 40), 5)  
        pygame.draw.line(screen, WHITE, (790, 10), (760, 40), 5) 
        pygame.display.flip()

def run_maze_game():


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

        maze[MAZE_HEIGHT - 2][MAZE_WIDTH - 2] = 0  # Проход
        return maze
        
    def draw_maze(maze, player_pos, hit_count):
        for y in range(len(maze)):
            for x in range(len(maze[0])):
                color = WHITE if maze[y][x] == 0 else BLACK
                pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        pygame.draw.rect(screen, GREEN, (player_pos[0] * CELL_SIZE, player_pos[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        pygame.draw.rect(screen, RED, ((MAZE_WIDTH - 2) * CELL_SIZE, (MAZE_HEIGHT - 2) * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        font = pygame.font.Font(None, 36)
        text = font.render(f"Счётчик стен: {hit_count}", True, RED)
        screen.blit(text, (10, 10))

    maze = generate_maze(MAZE_WIDTH, MAZE_HEIGHT)
    player_pos = [1, 1]  
    hit_count = 0
    
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
            hit_count += 1  

        if player_pos == [MAZE_WIDTH - 2, MAZE_HEIGHT - 2]:
            in_maze_game = False 
            return  
 
        screen.fill(BLACK)
        draw_maze(maze, player_pos, hit_count)  
        pygame.display.flip() 


def main():
    global dragging_button, offset_x, offset_y, last_click_time, start_menu_open

    start_menu_open = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos

                if 10 <= mouse_x <= 90 and HEIGHT - 40 <= mouse_y <= HEIGHT - 10:
                    start_menu_open = not start_menu_open  

                if button1_rect.collidepoint(event.pos):
                    current_time = time.time()
                    if current_time - last_click_time < click_delay: 
                        run_paint_program() 
                    last_click_time = current_time
                elif button2_rect.collidepoint(event.pos):
                    current_time = time.time()
                    if current_time - last_click_time < click_delay:  
                        run_maze_game()
                    last_click_time = current_time
                elif button3_rect.collidepoint(event.pos):
                    current_time = time.time()
                    if current_time - last_click_time < click_delay: 
                        print("Запуск программы 3")
                    last_click_time = current_time

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
                if event.button == 1: 
                    dragging_button = None

            if event.type == pygame.MOUSEMOTION:
                if dragging_button:
                    dragging_button.x = event.pos[0] + offset_x
                    dragging_button.y = event.pos[1] + offset_y

        screen.blit(background_image, (0, 0))

        draw_image_button(button1_image, button1_rect)
        draw_image_button(button2_image, button2_rect)
        draw_image_button(button3_image, button3_rect)

        pygame.draw.rect(screen, GRAY, (0, HEIGHT - 40, WIDTH, 40))
        pygame.draw.rect(screen, BLACK, (10, HEIGHT - 40, 80, 30)) 
        draw_text_button("Пуск", 10, HEIGHT - 40, 80, 30, color=WHITE)
        
        if start_menu_open:
            pygame.draw.rect(screen, MENU_GRAY, (0, HEIGHT - menu_height, WIDTH//3.5, menu_height))
            draw_text_button("Программы", 10, HEIGHT - menu_height + 20, 200, 40)
            draw_text_button("Выключение", 10, HEIGHT - menu_height + 70, 200, 40)
            draw_text_button("Настройки", 10, HEIGHT - menu_height + 120, 200, 40)

        pygame.display.flip()

if __name__ == "__main__":
    main()

