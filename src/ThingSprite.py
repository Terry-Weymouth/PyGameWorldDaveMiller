from pygame.sprite import Sprite
from pygame import Surface
from settings import THING_SIZE

class ThingSprite(Sprite):

    def __init__(self, thing, world):
        super().__init__()
        self.world = world
        self.thing = thing
        self.image = Surface((THING_SIZE, THING_SIZE))

    def update(self):
        self.rect = self.image.get_rect()
        self.rect.topleft = self.world.map_position(self.thing.pos)

    def set_color_from_thing_genome(self, cell_collection):
        color = self.thing.brain.genome.get_color(cell_collection)
        self.image.fill(color)

