from pygame.sprite import Sprite
from pygame import Surface
from settings import THING_SIZE, THING_COLOR


class ThingSprite(Sprite):

    def __init__(self, thing, world):
        super().__init__()
        self.image = Surface((THING_SIZE, THING_SIZE))
        self.image.fill(THING_COLOR)
        self.world = world
        self.thing = thing

    def update(self):
        self.rect = self.image.get_rect()
        self.rect.topleft = self.world.map_position(self.thing.pos)

