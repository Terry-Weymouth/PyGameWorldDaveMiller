from random import randint, random
from parts.Brain import Brain
from parts.Genome import Genome
from World import World
from Simulation import Simulation
from goals.GoalSouthEastCorner import GoalSouthEastCorner
from goals.GoalCenter import GoalCenter
from goals.GoalFourCorner import GoalFourCorner
from goals.GoalEast import GoalEast
from goals.GoalSplitEastWest import GoalSplitEastWest
from parts.cells.CellCollection import CellCollection
from settings import NUMBER_OF_THINGS


if __name__ == '__main__':

    world_size = 128
    mutation_rate = 0.01
    crossover_rate = 0.05
    generation_size = 300
    number_of_steps = 200  # per generation
    number_of_generations = 100001
    goal_choice = 2

    graphic_interval = 5

    generation = 0
    graphic = True
    show_goal_survive = False
    good_world_count = 0
    world = None

    goal_class = {
        0: GoalSouthEastCorner,
        1: GoalCenter,
        2: GoalFourCorner,
        3: GoalEast,
        4: GoalSplitEastWest
    }[goal_choice]

    print(goal_class)

    # initial genome list (random)
    genome_list = []
    for _ in range(NUMBER_OF_THINGS):
        genome_list.append(Genome())

    for _ in range(number_of_generations):
        generation += 1
        graphic = generation % graphic_interval == 0
        world = World(world_size, generation_size, graphic)

        goal = goal_class(world)

        # add mutations and crossovers
        mutant_genomes = []
        crossover_genomes = []
        for genome in genome_list:
            if random() < mutation_rate:
                mutant_genomes.append(genome.create_mutant_genome_single_bit())
            if random() < crossover_rate:
                random_index = randint(0, len(genome_list) - 1)
                mate = genome_list[random_index]
                crossover_genomes.append(genome.create_crossover(mate))
        genome_list += (mutant_genomes + crossover_genomes)

        # set up things
        for thing in world.things:
            potential_cells = CellCollection(thing)
            random_index = randint(0, len(genome_list) - 1)
            genome = genome_list[random_index]
            thing.brain = Brain(genome, potential_cells)
            thing.brain.clear_unused_cells()

        if graphic:
            simulation = Simulation(world, goal)
            simulation.run(number_of_steps, show_goal = show_goal_survive)

        else:
            for _ in range(number_of_steps):
                world.one_step_all()

        # determine survivors
        genome_list = []
        for thing in world.things:
            if goal.satisfy_goal(thing):
                genome_list.append(thing.brain.genome)

        unique_genome_list = []
        for genome in genome_list:
            if genome not in unique_genome_list:
                unique_genome_list.append(genome)

        survival_ratio = float(len(genome_list)) / float(len(world.things))
        ratio_string = ""
        if survival_ratio > 0.95:
            good_world_count += 1
            ratio_string = " - *: {}".format(good_world_count)

        total = len(world.things)
        print(("generation {}: {} survivers ({:3.1f}%); {} unique;" +
              " {} mutants; {} crossovers{}").format(
            generation, len(genome_list), (len(genome_list)*100.0)/total,
            len(unique_genome_list),
            len(mutant_genomes), len(crossover_genomes),
            ratio_string
        ))

        if good_world_count > 5:
            break

    # show survivors
    print("Found good world - five times")
