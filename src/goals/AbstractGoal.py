class AbstractGoal:

    def __init__(self, world):
        self.world = world

    def get_count(self):
        count = 0
        for thing in self.world.things:
            if self.satisfy_goal(thing):
                count += 1
        return count

    def satisfy_goal(self, thing):
        raise NotImplementedError
