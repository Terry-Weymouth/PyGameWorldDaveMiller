import pygame
from random import randint
from Thing import Thing
from ThingSprite import ThingSprite
from settings import NUMBER_OF_THINGS, WORLD_SIZE, GRID_SIZE


class World:

    def __init__(self):
        self.sprite_group = pygame.sprite.Group()
        self.things = []
        self.grid = [[None for i in range(WORLD_SIZE)] for j in range(WORLD_SIZE)]
        while len(self.things) < NUMBER_OF_THINGS:
            pos = self.find_ramdom_free_spot()
            thing = Thing(pos, self)
            (x, y) = pos
            self.grid[x][y] = thing
            self.things.append(thing)
            its_sprite = ThingSprite(thing, self)
            self.sprite_group.add(its_sprite)
        self.width = WORLD_SIZE
        self.height = WORLD_SIZE

    def one_step_all(self):
        for thing in self.things:
            thing.set_next_world_position()
        for thing in self.things:
            old_position = thing.pos
            if thing.move_to_next_world_position():
                (ox, oy) = old_position
                (nx, ny) = thing.pos  # new position
                # move in grid
                self.grid[ox][oy] = None
                self.grid[nx][ny] = thing

    def get_group(self):
        return self.sprite_group

    def find_ramdom_free_spot(self):
        x = 0
        y = 0
        free_spot = False
        while not free_spot:
            x = randint(0, WORLD_SIZE - 1)
            y = randint(0, WORLD_SIZE - 1)
            free_spot = self.is_free_grid_cell(x, y)
        return x, y

    def is_free_grid_cell(self, x, y):
        return self.grid[x][y] is None

    @staticmethod
    def is_in_bounds(x, y):
        return -1 < x < WORLD_SIZE and -1 < y < WORLD_SIZE

    @staticmethod
    def map_position(pos):
        (x, y) = pos
        nx = x * GRID_SIZE
        ny = y * GRID_SIZE
        return nx, ny
