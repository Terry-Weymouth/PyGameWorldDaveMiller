import pygame
from goals.AbstractGoal import AbstractGoal, GOAL_COLOR
from settings import THING_SIZE


class GoalFourCorner(AbstractGoal):

    def satisfy_goal(self, thing):
        size = self.world.size
        center_nw_pos = (0, 0)
        center_sw_pos = (0, size)
        center_ne_pos = (size, 0)
        center_se_pos = (size, size)
        goal_radius_sqr = (size/4)**2
        at_pos = thing.pos
        nw_goal = self.dist_sqr(at_pos, center_nw_pos) < goal_radius_sqr
        sw_goal = self.dist_sqr(at_pos, center_sw_pos) < goal_radius_sqr
        ne_goal = self.dist_sqr(at_pos, center_ne_pos) < goal_radius_sqr
        se_goal = self.dist_sqr(at_pos, center_se_pos) < goal_radius_sqr
        return nw_goal or sw_goal or ne_goal or se_goal

    def draw_goal(self, screen):
        if self.world.graphic:
            size = self.world.size * THING_SIZE
            center_nw_pos = (0, 0)
            center_sw_pos = (0, size)
            center_ne_pos = (size, 0)
            center_se_pos = (size, size)
            radius = size / 4
            pygame.draw.circle(screen, GOAL_COLOR, center_nw_pos, radius, 1)
            pygame.draw.circle(screen, GOAL_COLOR, center_sw_pos, radius, 1)
            pygame.draw.circle(screen, GOAL_COLOR, center_ne_pos, radius, 1)
            pygame.draw.circle(screen, GOAL_COLOR, center_se_pos, radius, 1)

    @staticmethod
    def dist_sqr(p1, p2):
        (x1, y1) = p1
        (x2, y2) = p2
        return (x1 - x2)**2 + (y1 - y2)**2
