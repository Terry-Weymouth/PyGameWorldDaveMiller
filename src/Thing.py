from random import randint
from pygame.sprite import Sprite
from pygame import Surface
from util import add_points
from settings import THING_SIZE, THING_COLOR


class Thing(Sprite):

    def __init__(self, start_pos, world):
        Sprite.__init__(self)
        self.world = world
        self.image = Surface((THING_SIZE, THING_SIZE))
        self.image.fill(THING_COLOR)
        self.pos = start_pos
        self.next_pos = self.pos
        self.age = 0
        self.update()

    def desired_move(self):
        # sense environment
        # cycle brain
        # read out actions
        # effect world - random motion only for now
        dx = randint(0, 3) - 1
        dy = randint(0, 3) - 1
        return add_points(self.pos, (dx, dy))

    def set_next_world_position(self):
        check_pos = self.desired_move()
        (x, y) = check_pos
        if self.world.is_in_bounds(x, y) and self.world.is_free_grid_cell(x, y):
            self.next_pos = check_pos

    def move_to_next_world_position(self):
        (x, y) = self.next_pos
        # in case it can't move
        self.next_pos = self.pos
        # multiple Things may be trying to move into the free cell
        # so, check is another Thing has already made the move
        if self.world.is_free_grid_cell(x, y):
            self.pos = (x, y)
            # reset next_pos
            self.next_pos = self.pos
            return True
        return False

    def update(self):
        self.rect = self.image.get_rect()
        self.rect.topleft = self.world.map_position(self.pos)

    def get_pos(self):
        return self.rect.center
