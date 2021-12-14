from parts.cells.sensors.Sensor import Sensor


class NearestBoundary(Sensor):

    def __init__(self, thing):
        super().__init__(thing)

    def set_sense_value(self):
        max_value_x = self.thing.world.width / 2.0
        max_value_y = self.thing.world.height / 2.0
        x = self.thing.pos[0]
        y = self.thing.pos[1]
        min_dist_x = min(x, (max_value_x - x))
        min_dist_y = min(y, (max_value_y - y))
        value = min_dist_x / max_value_x
        if min_dist_y < min_dist_x:
            value = min_dist_y / max_value_y
        self.value = value
