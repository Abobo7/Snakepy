import sys
import pygame
import random
from pygame.locals import *

# 设置游戏参数
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
CELL_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // CELL_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // CELL_SIZE

# 颜色定义
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# 方向定义
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


def main():
    pygame.init()
    global GAME_WIN, BASIC_FONT

    # 初始化 Pygame 窗口
    GAME_WIN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Snake Game')
    BASIC_FONT = pygame.font.Font(None, 18)

    while True:
        run_game()
        show_gameover()


def run_game():
    start_x = random.randint(5, GRID_WIDTH - 6)
    start_y = random.randint(5, GRID_HEIGHT - 6)
    snake_coords = [{'x': start_x, 'y': start_y},
                    {'x': start_x - 1, 'y': start_y},
                    {'x': start_x - 2, 'y': start_y}]
    direction = RIGHT

    # 生成苹果
    apple = create_new_apple()

    # 游戏主循环
    while True:
        for event in pygame.event.get():  # 检查是否退出游戏
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if (event.key == K_UP or event.key == K_w) and direction != DOWN:
                    direction = UP
                elif (event.key == K_DOWN or event.key == K_s) and direction != UP:
                    direction = DOWN
                elif (event.key == K_LEFT or event.key == K_a) and direction != RIGHT:
                    direction = LEFT
                elif (event.key == K_RIGHT or event.key == K_d) and direction != LEFT:
                    direction = RIGHT

        # 移动蛇头
        snake_head = {'x': snake_coords[0]['x'] + direction[0], 'y': snake_coords[0]['y'] + direction[1]}

        # 检查蛇头是否撞到边界或自身
        if snake_head['x'] < 0 or snake_head['x'] >= GRID_WIDTH or snake_head['y'] < 0 or snake_head['y'] >= GRID_HEIGHT or snake_head in snake_coords[:-1]:
            return

        # 更新蛇的坐标
        snake_coords.insert(0, snake_head)

        # 检查蛇头是否碰到苹果
        if snake_head == apple:
            apple = create_new_apple()  # 生成新苹果
        else:
            # 移动蛇身体
            snake_coords.pop()

        # 更新游戏画面
        GAME_WIN.fill(WHITE)
        draw_grid()
        draw_snake(snake_coords)
        draw_apple(apple)
        pygame.display.update()
        pygame.time.Clock().tick(10)


def create_new_apple():
    return {'x': random.randint(0, GRID_WIDTH - 1), 'y': random.randint(0, GRID_HEIGHT - 1)}


def draw_grid():
    for x in range(0, WINDOW_WIDTH, CELL_SIZE):
        pygame.draw.line(GAME_WIN, (200, 200, 200), (x, 0), (x, WINDOW_HEIGHT))
    for y in range(0, WINDOW_HEIGHT, CELL_SIZE):
        pygame.draw.line(GAME_WIN, (200, 200, 200), (0, y), (WINDOW_WIDTH, y))


def draw_snake(snake_coords):
    for coord in snake_coords:
        x = coord['x'] * CELL_SIZE
        y = coord['y'] * CELL_SIZE
        snake_rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(GAME_WIN, GREEN, snake_rect)
        snake_inner_rect = pygame.Rect(x + 4, y + 4, CELL_SIZE - 8, CELL_SIZE - 8)
        pygame.draw.rect(GAME_WIN, GREEN, snake_inner_rect)


def draw_apple(coord):
    x = coord['x'] * CELL_SIZE
    y = coord['y'] * CELL_SIZE
    apple_rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(GAME_WIN, RED, apple_rect)


def show_gameover():
    gameover_surf = BASIC_FONT.render('Game Over', True, RED)
    gameover_rect = gameover_surf.get_rect()
    gameover_rect.midtop = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 50)
    GAME_WIN.blit(gameover_surf, gameover_rect)

    presskey_surf = BASIC_FONT.render('Press any key to continue', True, GREEN)
    presskey_rect = presskey_surf.get_rect()
    presskey_rect.midtop = (WINDOW_WIDTH / 2, gameover_rect.height + gameover_rect.top + 25)
    GAME_WIN.blit(presskey_surf, presskey_rect)

    pygame.display.update()

    # 等待一段时间
    wait_time = 500
    pygame.time.wait(wait_time)

    check_for_keypress()


def check_for_keypress():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:  # 按下 Esc 键退出
                    terminate()
                return


def terminate():
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()