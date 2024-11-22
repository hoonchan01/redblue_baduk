import pygame

# 바둑판과 화면 설정
BOARD_SIZE = 19
CELL_SIZE = 30
WINDOW_SIZE = BOARD_SIZE * CELL_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BG_COLOR = (255, 255, 255)
DOT_COLOR = (0, 0, 0)

pygame.init()
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("바둑 게임")

board = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
current_player = "red"
history = []

# 바둑판 그리기
def draw_board():
    screen.fill(BG_COLOR)
    for i in range(BOARD_SIZE):
        pygame.draw.line(screen, BLACK, 
                         (CELL_SIZE // 2, i * CELL_SIZE + CELL_SIZE // 2), 
                         (WINDOW_SIZE - CELL_SIZE // 2, i * CELL_SIZE + CELL_SIZE // 2))
        pygame.draw.line(screen, BLACK, 
                         (i * CELL_SIZE + CELL_SIZE // 2, CELL_SIZE // 2), 
                         (i * CELL_SIZE + CELL_SIZE // 2, WINDOW_SIZE - CELL_SIZE // 2))
    draw_special_points()

def draw_special_points():
    center_x = BOARD_SIZE // 2
    center_y = BOARD_SIZE // 2
    pygame.draw.circle(screen, DOT_COLOR, 
                       (center_x * CELL_SIZE + CELL_SIZE // 2, center_y * CELL_SIZE + CELL_SIZE // 2), 5)
    points = [
        (3, 3), (3, 9), (3, 15),
        (9, 3), (9, 9), (9, 15),
        (15, 3), (15, 9), (15, 15)
    ]
    for x, y in points:
        pygame.draw.circle(screen, DOT_COLOR, 
                           (x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2), 5)

def draw_stones():
    for x in range(BOARD_SIZE):
        for y in range(BOARD_SIZE):
            if board[x][y] == "red":
                pygame.draw.rect(screen, RED, 
                                 (x * CELL_SIZE + 2, y * CELL_SIZE + 2, CELL_SIZE - 4, CELL_SIZE - 4))
            elif board[x][y] == "blue":
                pygame.draw.rect(screen, BLUE, 
                                 (x * CELL_SIZE + 2, y * CELL_SIZE + 2, CELL_SIZE - 4, CELL_SIZE - 4))

# 단수 처리
def remove_captured_stones():
    visited = set()
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    def find_group_and_liberties(x, y):
        stack = [(x, y)]
        group = set()
        liberties = set()
        color = board[x][y]

        while stack:
            cx, cy = stack.pop()
            if (cx, cy) in group:
                continue
            group.add((cx, cy))

            for dx, dy in directions:
                nx, ny = cx + dx, cy + dy
                if 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE:
                    if board[nx][ny] is None:
                        liberties.add((nx, ny))
                    elif board[nx][ny] == color:
                        stack.append((nx, ny))
        return group, liberties

    for x in range(BOARD_SIZE):
        for y in range(BOARD_SIZE):
            if board[x][y] is not None and (x, y) not in visited:
                group, liberties = find_group_and_liberties(x, y)
                visited.update(group)
                if not liberties:
                    for gx, gy in group:
                        board[gx][gy] = None

def undo_move():
    if history:
        last_move = history.pop()
        x, y, _ = last_move
        board[x][y] = None
        return "blue" if current_player == "red" else "red"
    return current_player

running = True
while running:
    draw_board()
    draw_stones()
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            grid_x = x // CELL_SIZE
            grid_y = y // CELL_SIZE
            
            if board[grid_x][grid_y] is None:
                board[grid_x][grid_y] = current_player
                history.append((grid_x, grid_y, current_player))
                remove_captured_stones()
                current_player = "blue" if current_player == "red" else "red"

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                current_player = undo_move()

pygame.quit()
