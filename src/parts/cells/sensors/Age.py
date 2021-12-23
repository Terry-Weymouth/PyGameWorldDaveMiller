from parts.cells.sensors.Sensor import Sensor


class Age(Sensor):

    def __init__(self, thing):
        super().__init__(thing)

    def set_sense_value(self):
        return self.thing.get_normalized_age()
