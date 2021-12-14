import pygame
from pygame.locals import (
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)
from settings import FPS, BACKGROUND_COLOR, DISPLAY_SIZE

pygame.init()


class Simulation:

    def __init__(self, world):
        # Set up the drawing window
        self.world = world
        self.screen = pygame.display.set_mode([DISPLAY_SIZE, DISPLAY_SIZE])
        # master clock
        self.clock = pygame.time.Clock()
        # display window
        pygame.display.set_caption("World Simulation")

    def run(self):
        print("Running: ", self)

        # Run until the user asks to quit
        running = True
        while running:
            running = self.one_loop_step()

        # Done! Time to quit.
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
