from goals.AbstractGoal import AbstractGoal


class GoalSouthEastCorner(AbstractGoal):

    def satisfy_goal(self, thing):
        (x, y) = thing.pos
        size = thing.world.size
        return x > size/2 and y > size/2
