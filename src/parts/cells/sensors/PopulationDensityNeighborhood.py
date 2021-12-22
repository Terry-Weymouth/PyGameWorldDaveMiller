from parts.cells.sensors.Sensor import Sensor


class PopulationDensityNeighborhood(Sensor):

    def __init__(self, thing):
        super().__init__(thing)

    def set_sense_value(self):
        raw = float(sum(self.thing.neighborhood_cache))
        self.value = raw/8.0
