import pygame
from random import randint, random
from Thing import Thing
from ThingSprite import ThingSprite
from settings import NUMBER_OF_THINGS, WORLD_SIZE, GRID_SIZE, MAX_NUMBER_OF_STEPS


class World:

    def __init__(self, size=WORLD_SIZE, number_of_things=NUMBER_OF_THINGS, graphic=False):
        self.graphic = graphic
        self.size = size
        if self.graphic:
            self.sprite_group = pygame.sprite.Group()
        self.things = []
        self.grid = [[None for _ in range(self.size)] for _ in range(self.size)]
        while len(self.things) < number_of_things:
            pos = self.find_ramdom_free_spot()
            thing = Thing(pos, self)
            self.add_thing_to_world(thing)
        self.width = self.size
        self.height = self.size
        self.max_number_of_steps = MAX_NUMBER_OF_STEPS

    def one_step_all(self):
        for thing in self.things:
            thing.set_sensors()
            thing.brain.propagate()
            thing.setup_next_step_from_actions()
        # for motion of things
        for thing in self.things:
            old_pos = thing.pos
            check_pos = thing.next_pos
            (x, y) = check_pos
            if self.is_in_bounds(x, y) and self.is_free_grid_cell(x, y):
                if thing.move_to_next_world_position():
                    (ox, oy) = old_pos
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
            x = randint(0, self.size - 1)
            y = randint(0, self.size - 1)
            free_spot = self.is_free_grid_cell(x, y)
        return x, y

    def add_thing_to_world(self, thing):
        (x, y) = thing.pos
        self.grid[x][y] = thing
        self.things.append(thing)
        if self.graphic:
            its_sprite = ThingSprite(thing, self)
            self.sprite_group.add(its_sprite)

    def get_random_value_for_sensor(self):
        return random()

    def is_free_grid_cell(self, x, y):
        return self.grid[x][y] is None

    def thing_at(self, pos):
        (x, y) = pos
        return self.grid[x][y]

    def is_in_bounds(self, x, y):
        return -1 < x < self.size and -1 < y < self.size

    @staticmethod
    def map_position(pos):  # position of lower_right corner in graphic display
        (x, y) = pos
        nx = x * GRID_SIZE
        ny = y * GRID_SIZE
        return nx, ny

    def color_all_sprites(self, all_cells):
        if self.graphic:
            for s in self.sprite_group:
                s.set_color_from_thing_genome(all_cells)