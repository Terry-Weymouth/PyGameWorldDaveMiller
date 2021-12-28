import pygame
from pygame.locals import (
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)
from settings import FPS, BACKGROUND_COLOR, DISPLAY_SIZE

pygame.init()


class Simulation:

    def __init__(self, world, goal):
        # Set up the drawing window
        self.world = world
        self.goal = goal
        self.screen = pygame.display.set_mode([DISPLAY_SIZE, DISPLAY_SIZE])
        # master clock
        self.clock = pygame.time.Clock()
        # display window
        pygame.display.set_caption("World Simulation")

    def run(self, number_of_steps=None):

        # Run until the user asks to quit
        running = True
        steps = 0
        while running:
            running = self.one_loop_step()
            if number_of_steps:
                steps += 1
                running = running & (steps < number_of_steps)
        pygame.quit()

    def one_loop_step(self):
        running = True

        # keep loop running at the right speed
        self.clock.tick(FPS)

        # Process input (events) - quite click or ESCAPE key
        for event in pygame.event.get():
            if self.is_quit_event(event):
                running = False

        if running:
            self.world.one_step_all()
            self.world.sprite_group.update()

            # Fill the background
            self.screen.fill(BACKGROUND_COLOR)

            # Draw updated things
            self.world.sprite_group.draw(self.screen)

            # draw the goal
            self.goal.draw_goal(self.screen)

            # Flip the display
            pygame.display.flip()

        return running

    @staticmethod
    def is_quit_event(event):
        # Did the user hit a key?
        if event.type == KEYDOWN:
            # Was it the Escape key? If so, stop the loop.
            if event.key == K_ESCAPE:
                return True
        # Did the user click the window close button? If so, stop the loop.
        if event.type == QUIT:
            return True
        return False

    def show_current_state(self, title):
        running = True

        # keep loop running at the right speed
        self.clock.tick(FPS)
        pygame.display.set_caption(title)

        while running:

            # Process input (events) - quite click or ESCAPE key
            for event in pygame.event.get():
                if self.is_quit_event(event):
                    running = False
            if not running:
                print("Quit event received")

            if running:
                self.world.sprite_group.update()

                # Fill the background
                self.screen.fill(BACKGROUND_COLOR)

                # Draw updated things
                self.world.sprite_group.draw(self.screen)

                # draw the goal
                self.goal.draw_goal(self.screen)

                # Flip the display
                pygame.display.flip()

        pygame.quit()

