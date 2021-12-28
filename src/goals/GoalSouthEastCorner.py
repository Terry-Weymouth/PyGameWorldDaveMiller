import pygame
from goals.AbstractGoal import AbstractGoal, GOAL_COLOR


class GoalSouthEastCorner(AbstractGoal):

    def satisfy_goal(self, thing):
        (x, y) = thing.pos
        size = self.world.size
        return x > size/2 and y > size/2

    def draw_goal(self, screen):
        if self.world.graphic:
            size = self.world.size * 4
            half_way = self.world.size*2
            points = [(half_way, size), (half_way, half_way), (size, half_way)]
            pygame.draw.lines(screen, GOAL_COLOR, False, points)
