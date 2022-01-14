from parts.cells.sensors.Sensor import Sensor


class PopulationDensityLeftRight(Sensor):

    def __init__(self, thing):
        super().__init__(thing)

    def set_sense_value(self):
        raw_value = self.thing.left_right_neighbor_count()
        return raw_value / 6.0
