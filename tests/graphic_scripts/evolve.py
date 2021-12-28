from random import randint, random

from parts.Brain import Brain
from parts.Genome import Genome
from World import World
from Simulation import Simulation
from goals.GoalSouthEastCorner import GoalSouthEastCorner
from goals.GoalCenter import GoalCenter
from parts.cells.CellCollection import CellCollection

if __name__ == '__main__':

    world_size = 128
    mutation_rate = 0.01
    generation_size = 1000
    number_of_steps = 128  # per generation
    number_of_generations = 100001
    goal_choice = 1

    genome_list = []
    generation = 0
    graphic = True
    good_world_count = 0

    for _ in range(number_of_generations):
        graphic = generation % 10 == 0

        generation += 1

        world = World(world_size, generation_size, graphic)

        goal = GoalSouthEastCorner(world)
        if goal_choice == 1:
            goal = GoalCenter(world)

        if genome_list:
            for thing in world.things:
                potential_cells = CellCollection(thing)
                random_index = randint(0, len(genome_list) - 1)
                genome = genome_list[random_index]
                thing.brain = Brain(genome, potential_cells)
                thing.brain.clear_unused_cells()
        else:
            for thing in world.things:
                potential_cells = CellCollection(thing)
                thing.brain = Brain(Genome(), potential_cells)  # random bits
                thing.brain.clear_unused_cells()

        if graphic:
            simulation = Simulation(world, goal)
            simulation.run(number_of_steps)
        else:
            for _ in range(number_of_steps):
                world.one_step_all()

        genome_list = []
        for thing in world.things:
            if goal.satisfy_goal(thing):
                genome_list.append(thing.brain.genome)

        last_genome_list = genome_list

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

        if float(len(genome_list)) / float(len(world.things)) > 0.95:
            good_world_count += 1

        if good_world_count > 5:
            break
