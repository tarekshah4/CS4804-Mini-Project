import pygame
import random
from enum import Enum
from collections import namedtuple
import numpy as np

pygame.init()
font = pygame.font.SysFont('arial', 25)

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

Point = namedtuple('Point', 'x, y')

# rgb colors
WHITE = (255, 255, 255)
RED = (200,0,0)
BLUE = (0, 0, 255)
BLACK = (0,0,0)

SQUARE_SIZE = 30
SPEED = 60

class Snake:

    def __init__(self):
        self.w = 600
        self.h = 600
        # init display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()
        self.reset()


    def reset(self):
        # init game state
        self.direction = Direction.RIGHT

        self.head = Point(self.w/2, self.h/2)
        self.snake = [self.head,
                      Point(self.head.x-SQUARE_SIZE, self.head.y),
                      Point(self.head.x-(2*SQUARE_SIZE), self.head.y)]

        self.score = 0
        self.food = None
        self._put_food()
        self.frame_iteration = 0


    def _put_food(self):
        x = random.randint(0, (self.w-SQUARE_SIZE )//SQUARE_SIZE )*SQUARE_SIZE
        y = random.randint(0, (self.h-SQUARE_SIZE )//SQUARE_SIZE )*SQUARE_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._put_food()


    def play_step(self, action):
        self.frame_iteration += 1
        # collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        # move
        self._move(action) # update the head
        self.snake.insert(0, self.head)
        
        # check if game over
        reward = 0
        game_over = False
        if self.is_collision() or self.frame_iteration > 100*len(self.snake):
            game_over = True
            reward = -10
            return reward, game_over, self.score

        # place new food or just move
        if self.head == self.food:
            self.score += 1
            reward = 10
            self._put_food()
        else:
            self.snake.pop()
        
        # update ui and clock
        self._update_ui()
        self.clock.tick(SPEED)
        # return game over and score
        return reward, game_over, self.score


    def is_collision(self, pt=None):
        if pt is None:
            pt = self.head
        if pt.x > self.w - SQUARE_SIZE or pt.x < 0 or pt.y > self.h - SQUARE_SIZE or pt.y < 0:
            return True
        if pt in self.snake[1:]:
            return True

        return False


    def _update_ui(self):
        self.display.fill(BLACK)

        for pt in self.snake:
            pygame.draw.rect(self.display, BLUE, pygame.Rect(pt.x, pt.y, SQUARE_SIZE, SQUARE_SIZE))

        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, SQUARE_SIZE, SQUARE_SIZE))

        text = font.render("Curent Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()


    def _move(self, action):
        # [straight, right, left]

        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clock_wise.index(self.direction)

        if np.array_equal(action, [1, 0, 0]):
            new_dir = clock_wise[idx]
        elif np.array_equal(action, [0, 1, 0]):
            next_idx = (idx + 1) % 4
            new_dir = clock_wise[next_idx]
        else:
            next_idx = (idx - 1) % 4
            new_dir = clock_wise[next_idx]

        self.direction = new_dir

        x = self.head.x
        y = self.head.y
        if self.direction == Direction.RIGHT:
            x += SQUARE_SIZE
        elif self.direction == Direction.LEFT:
            x -= SQUARE_SIZE
        elif self.direction == Direction.DOWN:
            y += SQUARE_SIZE
        elif self.direction == Direction.UP:
            y -= SQUARE_SIZE

        self.head = Point(x, y)