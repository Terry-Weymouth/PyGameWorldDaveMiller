from random import randint, random

from parts.Brain import Brain
from parts.Genome import Genome
from World import World
from Simulation import Simulation
from goals.GoalSouthEastCorner import GoalSouthEastCorner
from parts.cells.CellCollection import CellCollection

if __name__ == '__main__':

    mutation_rate = 0.005
    generation_size = 100
    number_of_steps = 128  # per generation
    number_of_generations = 101

    world = World(128, generation_size, True)
    for thing in world.things:
        potential_cells = CellCollection(thing)
        thing.brain = Brain(Genome(), potential_cells)  # random bits
        thing.brain.clear_unused_cells()

    goal = GoalSouthEastCorner(world)

    generation = 0
    graphic = True
    for _ in range(number_of_generations):

        generation += 1

        if graphic:
            simulation = Simulation(world)
            simulation.run(number_of_steps)
        else:
            for _ in range(number_of_steps):
                world.one_step_all()

        genome_list = []
        for thing in world.things:
            if goal.satisfy_goal(thing):
                genome_list.append(thing.brain.genome)

        new_genomes = []
        for genome in genome_list:
            if random() < mutation_rate:
                new_genomes.append(genome.create_mutant_genome_single_bit())
        genome_list += new_genomes

        unique_genome_list = []
        for genome in genome_list:
            if genome not in unique_genome_list:
                unique_genome_list.append(genome)

        print("generation {}: {} survivers; {} unique; {} mutant".format(
            generation, len(genome_list), len(unique_genome_list), len(new_genomes)))

        graphic = generation % 10 == 0
        world = World(128, generation_size, graphic)

        for thing in world.things:
            potential_cells = CellCollection(thing)
            random_index = randint(0, len(genome_list) - 1)
            genome = genome_list[random_index]
            thing.brain = Brain(genome, potential_cells)
            thing.brain.clear_unused_cells()
            for cell in thing.brain.all_cells:
                cell.value = 0.0
