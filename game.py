import pygame
import random

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
COLORS = [
    (0, 255, 255),  # Cyan
    (255, 0, 0),    # Red
    (0, 255, 0),    # Green
    (0, 0, 255),    # Blue
    (255, 165, 0),  # Orange
    (255, 255, 0),  # Yellow
    (128, 0, 128)   # Purple
]

# Shapes (Tetrominoes)
SHAPES = [
    [[1, 1, 1, 1]], # I
    [[1, 1], [1, 1]], # O
    [[1, 1, 0], [0, 1, 1]], # Z
    [[0, 1, 1], [1, 1, 0]], # S
    [[1, 1, 1], [0, 1, 0]], # T
    [[1, 1, 1], [1, 0, 0]], # L
    [[1, 1, 1], [0, 0, 1]]  # J
]

class Block:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.shape = random.choice(SHAPES)
        self.color = random.choice(COLORS)
        self.rotation = 0

    def image(self):
        return self.shape

    def rotate(self):
        # Transpose and reverse rows for 90 degree clockwise rotation
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

class TetrisGame:
    def __init__(self, rows=20, cols=10, block_size=30):
        self.rows = rows
        self.cols = cols
        self.block_size = block_size
        self.grid = [[BLACK for _ in range(cols)] for _ in range(rows)]
        self.current_block = Block(3, 0)
        self.game_over = False
        self.score = 0
        self.locking = False

    def new_block(self):
        self.current_block = Block(3, 0)
        if self.check_collision():
            self.game_over = True

    def check_collision(self, offset_x=0, offset_y=0):
        shape = self.current_block.shape
        for r, row in enumerate(shape):
            for c, cell in enumerate(row):
                if cell:
                    new_x = self.current_block.x + c + offset_x
                    new_y = self.current_block.y + r + offset_y
                    if new_x < 0 or new_x >= self.cols or new_y >= self.rows:
                        return True
                    if new_y >= 0 and self.grid[new_y][new_x] != BLACK:
                        return True
        return False

    def lock_block(self):
        shape = self.current_block.shape
        for r, row in enumerate(shape):
            for c, cell in enumerate(row):
                if cell:
                    new_x = self.current_block.x + c
                    new_y = self.current_block.y + r
                    if 0 <= new_y < self.rows and 0 <= new_x < self.cols:
                        self.grid[new_y][new_x] = self.current_block.color
        self.clear_lines()
        self.new_block()

    def clear_lines(self):
        full_lines = [i for i, row in enumerate(self.grid) if all(cell != BLACK for cell in row)]
        for i in full_lines:
            del self.grid[i]
            self.grid.insert(0, [BLACK for _ in range(self.cols)])
            self.score += 100

    def move(self, dx, dy):
        if not self.game_over:
            if not self.check_collision(dx, dy):
                self.current_block.x += dx
                self.current_block.y += dy
                return True
            elif dy > 0: # Hit bottom or another block while moving down
                self.lock_block()
                return False
        return False

    def rotate(self):
        if not self.game_over:
            original_shape = self.current_block.shape
            self.current_block.rotate()
            if self.check_collision():
                self.current_block.shape = original_shape # Revert if invalid

    def draw(self, screen, start_x, start_y):
        # Draw grid
        for r in range(self.rows):
            for c in range(self.cols):
                pygame.draw.rect(screen, self.grid[r][c],
                                 (start_x + c * self.block_size, start_y + r * self.block_size,
                                  self.block_size, self.block_size), 0)
                pygame.draw.rect(screen, GRAY,
                                 (start_x + c * self.block_size, start_y + r * self.block_size,
                                  self.block_size, self.block_size), 1)

        # Draw current block
        if self.current_block:
            shape = self.current_block.shape
            for r, row in enumerate(shape):
                for c, cell in enumerate(row):
                    if cell:
                        pygame.draw.rect(screen, self.current_block.color,
                                         (start_x + (self.current_block.x + c) * self.block_size,
                                          start_y + (self.current_block.y + r) * self.block_size,
                                          self.block_size, self.block_size), 0)
                        pygame.draw.rect(screen, GRAY,
                                         (start_x + (self.current_block.x + c) * self.block_size,
                                          start_y + (self.current_block.y + r) * self.block_size,
                                          self.block_size, self.block_size), 1)

        # Draw Border
        pygame.draw.rect(screen, WHITE, (start_x, start_y, self.cols * self.block_size, self.rows * self.block_size), 2)
