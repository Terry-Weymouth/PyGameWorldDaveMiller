from parts.cells.sensors.Sensor import Sensor


class PopulationDensityNeighborhood(Sensor):

    def __init__(self, thing):
        super().__init__(thing)

    def set_sense_value(self):
        raw_value = self.thing.neighbor_count()
        self.value = raw_value/8.0
