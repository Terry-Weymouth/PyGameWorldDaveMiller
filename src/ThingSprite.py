from pygame.sprite import Sprite
from pygame import Surface
from settings import THING_SIZE, THING_COLOR


class ThingSprite(Sprite):

    def __init__(self, thing, world):
        super().__init__()
        self.world = world
        self.thing = thing
        self.image = Surface((THING_SIZE, THING_SIZE))

    def update(self):
        self.rect = self.image.get_rect()
        self.rect.topleft = self.world.map_position(self.thing.pos)

    def set_color_from_genes(self):
        color_list = [0, 0, 0]
        all_bytes = None
        for gene in self.thing.brain.genome.get_genes():
            if all_bytes:
                all_bytes += gene.get_gene_bytes()
            else:
                all_bytes = gene.get_gene_bytes()
        color_index = 0
        for byte in all_bytes:
            color_list[color_index] ^= byte
            color_index += 1
            if color_index >= len(color_list):
                color_index = 0
        self.image.fill(tuple(color_list))

