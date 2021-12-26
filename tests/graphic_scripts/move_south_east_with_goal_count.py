import pygame
from World import World
from Simulation import Simulation
from parts.Genome import Genome
from parts.Brain import Brain
from parts.BrainFactory import BrainFactory
from parts.cells.CellCollection import CellCollection
from goals.GoalSouthEastCorner import GoalSouthEastCorner
from settings import WORLD_SIZE, NUMBER_OF_THINGS


class GoalPlay:

    def main(self):
        pygame.init()
        print(WORLD_SIZE, NUMBER_OF_THINGS)
        world = World(WORLD_SIZE, 300, True)
        factory = BrainFactory()
        for thing in world.things:
            potential_cells = CellCollection(thing)
            thing.brain = self.get_south_east_brain(factory,potential_cells)
            thing.brain.clear_unused_cells()
            for con in thing.brain.connections:
                con.strength = 4.0

        goal = GoalSouthEastCorner(world)

        simulation = Simulation(world)

        # Run until the user asks to quit
        count = 0
        running = True
        while running:
            running = simulation.one_loop_step()
            count += 1
            print(goal.get_count(), count)
        pygame.quit()

    @staticmethod
    def get_south_east_brain(factory, potential_cells):
        # build - genome for connections
        genes = [
            # Nuron0 -> Actuator0
            factory.make_gene_from_settings_array([[1, 0], [0, 0], 0]),
            # Nuron1 -> Actuator3
            factory.make_gene_from_settings_array([[1, 1], [0, 3], 0])
        ]

        # make Genome with fixed genes - for testing
        genome = Genome(genes)
        brain = Brain(genome, potential_cells)
        return brain


if __name__ == '__main__':
    GoalPlay().main()
