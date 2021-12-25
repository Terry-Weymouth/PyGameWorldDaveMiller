"""
This module contains all of the necessary PyGame components for
running a simplified game loop, based on PyGame-related code.
Copied from https://gist.github.com/MarquisLP/b534c95e4a11efaf376e
Written by Mark Padilla, https://gist.github.com/MarquisLP

It have been modified to run a one-generation loop of the
evolutionary simulation represented in this project.
See the top-level Readme file.

Modified: Dec 2021
"""
import sys
import pygame
from pygame.locals import *
# Import additional modules here.
from Simulation import Simulation
from World import World
from settings import NUMBER_OF_THINGS, WORLD_SIZE


def pygame_modules_have_loaded():
    success = True

    if not pygame.display.get_init:
        success = False
    if not pygame.font.get_init():
        success = False
    if not pygame.mixer.get_init():
        success = False

    return success


pygame.init()

if not pygame_modules_have_loaded():
    print("Load of pygame elements, and/or initialization failed")
    pygame.quit()
else:
    pygame.display.set_caption('Test')
    clock = pygame.time.Clock()

    def declare_globals():
        # The class(es) that will be tested should be declared and initialized
        # here with the global keyword.
        # Yes, globals are evil, but for a confined test script they will make
        # everything much easier. This way, you can access the class(es) from
        # all three of the methods provided below.
        pass

    def prepare_test():
        # Add in any code that needs to be run before the game loop starts.
        pass

    def handle_input(key_name):
        # Add in code for input handling.
        # key_name provides the String name of the key that was pressed.
        pass

    def update(screen, time):
        # Add in code to be run during each update cycle.
        # screen provides the PyGame Surface for the game window.
        # time provides the seconds elapsed since the last update.
        pygame.display.update()

    # Add additional methods here.

    def main():
        print("Not currently working - needs to be Refactored to take into accounts updates in Thing, Brain, and World")
#        declare_globals()
#        prepare_test()

#        world = World(WORLD_SIZE, NUMBER_OF_THINGS, True)
#        simulation = Simulation(world)

        # Run until the user asks to quit
#        running = True
#        while running:
#            running = simulation.one_loop_step()

        # Done! Time to quit.
        pygame.quit()

    main()
