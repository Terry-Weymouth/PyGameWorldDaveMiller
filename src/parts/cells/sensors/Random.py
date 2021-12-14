from parts.cells.sensors.Sensor import Sensor


class Random(Sensor):

    def __init__(self, thing):
        super().__init__(thing)

    def set_sense_value(self):
        self.value = self.thing.world.get_random_value_for_sensor()
