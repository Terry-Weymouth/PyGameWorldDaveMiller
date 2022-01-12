from random import randint, random
import pygame
from parts.Brain import Brain
from parts.Genome import Genome
from World import World
from Simulation import Simulation
from goals.GoalSouthEastCorner import GoalSouthEastCorner
from goals.GoalCenter import GoalCenter
from goals.GoalFourCorner import GoalFourCorner
from parts.cells.CellCollection import CellCollection


def print_stats(stats_genome_list, stats_unique_genome_list):

    counts = []
    for stats_genome in stats_unique_genome_list:
        count = 0
        for candidate in stats_genome_list:
            if stats_genome is candidate:
                count += 1
        counts.append(count)

    for i in range(len(counts)):
        stats_genome = stats_genome_list[i]
        count = counts[i]
        signature = []
        for gene in stats_genome.get_genes():
            signature.append(gene.parse())
        print(count, signature)


def freeze_frame(title, frame_world, frame_goal_class):
    keep_things = frame_world.things
    frame_world = World(world_size, generation_size, True)
    frame_goal = frame_goal_class(frame_world)

    frame_world.sprite_group = pygame.sprite.Group()
    frame_world.things = []
    for frame_thing in keep_things:
        frame_world.add_thing_to_world(frame_thing)

    for sprite in frame_world.sprite_group:
        if frame_goal.satisfy_goal(sprite.thing):
            sprite.image.fill((255, 0, 0))
    frame_simulation = Simulation(frame_world, frame_goal)
    frame_simulation.show_current_state(title)


if __name__ == '__main__':

    world_size = 128
    mutation_rate = 0.01
    crossover_rate = 0.05
    generation_size = 300
    number_of_steps = 200  # per generation
    number_of_generations = 100001
    goal_choice = 1

    graphic_interval = 5
    snapshot_interval = 10000

    genome_list = []
    generation = 0
    graphic = True
    good_world_count = 0
    world = None

    goal_class = {
        0: GoalSouthEastCorner,
        1: GoalCenter,
        2: GoalFourCorner
    }[goal_choice]

    print("Goal class = {}".format(goal_class))

    for _ in range(number_of_generations):
        generation += 1
        graphic = generation % graphic_interval == 0
        world = World(world_size, generation_size, graphic)

        goal = goal_class(world)

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

        unique_genome_list = []
        for genome in genome_list:
            if genome not in unique_genome_list:
                unique_genome_list.append(genome)

        total = len(world.things)
        print(("generation {}: {} survivers ({:3.1f}%); {} unique;" +
              " {} mutants; {} crossovers").format(
                  generation, len(genome_list), (len(genome_list)*100.0)/total,
                  len(unique_genome_list),
                  len(mutant_genomes), len(crossover_genomes)))

        if graphic:
            dummy_thing = world.things[0]
            collection = CellCollection(dummy_thing)

        if float(len(genome_list)) / float(len(world.things)) > 0.95:
            good_world_count += 1
        else:
            good_world_count = 0

        if good_world_count > 5:
            break

        if generation % snapshot_interval == 0:
            # print_stats(genome_list, unique_genome_list)
            freeze_frame("Snapshot", world, goal_class)

    # show survivors
    print("Found good world - five times in a row")

    freeze_frame("Final Run", world, goal_class)
