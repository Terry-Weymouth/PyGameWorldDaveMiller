import pygame
from goals.AbstractGoal import AbstractGoal, GOAL_COLOR
from settings import THING_SIZE

class GoalCenter(AbstractGoal):

    def satisfy_goal(self, thing):
        (x, y) = thing.pos
        center = thing.world.size/2
        rx = x - center
        ry = y - center
        r_goal = center/3
        return (rx**2 + ry**2) < r_goal**2

    def draw_goal(self, screen):
        if self.world.graphic:
            size = self.world.size * THING_SIZE
            half_way = size / 2
            center = (half_way, half_way)
            radius = half_way/3
            pygame.draw.circle(screen, GOAL_COLOR, center, radius, 1)

