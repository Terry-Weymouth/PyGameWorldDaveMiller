from parts.cells.sensors.Sensor import Sensor


class NearestBoundaryEastWest(Sensor):

    def __init__(self, thing):
        super().__init__(thing)

    def set_sense_value(self):
        max_value_x = self.thing.world.width / 2.0
        x = self.thing.pos[0]
        min_dist_x = min(x, (max_value_x - x))
        value = min_dist_x / max_value_x
        self.value = value
