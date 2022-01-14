from parts.cells.sensors.Sensor import Sensor


class PopulationDensityFoward(Sensor):

    def __init__(self, thing):
        super().__init__(thing)

    def set_sense_value(self):
        raw_value = self.thing.forward_neighbor_count()
        return raw_value / 3.0
