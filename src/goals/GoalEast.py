import pygame
from goals.AbstractGoal import AbstractGoal, GOAL_COLOR


class GoalEast(AbstractGoal):

    def satisfy_goal(self, thing):
        (x, y) = thing.pos
        size = self.world.size
        return x > size * (2 / 3)

    def draw_goal(self, screen):
        if self.world.graphic:
            top = 0
            bottom = self.world.size * 4
            goal_line = (self.world.size * 4) * (2 / 3)
            points = [(goal_line, top), (goal_line, bottom)]
            pygame.draw.lines(screen, GOAL_COLOR, False, points)
