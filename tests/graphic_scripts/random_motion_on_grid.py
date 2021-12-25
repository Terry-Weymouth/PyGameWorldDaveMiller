import pygame
from World import World
from Simulation import Simulation
from parts.Genome import Genome
from parts.Brain import Brain
from parts.BrainFactory import BrainFactory
from parts.cells.CellCollection import CellCollection

MOVE_TYPE = 4  # east = 0, west = 1, north = 2, south = 3, random = 4


class RandomPlay:

    def main(self):
        pygame.init()

        world = World(graphic=True)
        factory = BrainFactory()
        for thing in world.things:
            potential_cells = CellCollection(thing)
            thing.brain = self.make_random_brain(factory,potential_cells)
            thing.brain.clear_unused_cells()
            for con in thing.brain.connections:
                con.strength = 4.0

        simulation = Simulation(world)


        # Run until the user asks to quit
        running = True
        while running:
            running = simulation.one_loop_step()
        pygame.quit()

    @staticmethod
    def make_random_brain(factory, potential_cells):
        # build - genome for connections
        genes = [
            # Nuron0 -> Actuator4
            factory.make_gene_from_settings_array([[1, 0], [0, MOVE_TYPE], 0])
        ]

        # make Genome with fixed genes - for testing
        genome = Genome(genes)
        brain = Brain(genome, potential_cells)
        return brain


if __name__ == '__main__':
    RandomPlay().main()
