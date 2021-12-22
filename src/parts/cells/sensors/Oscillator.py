from parts.cells.sensors.Sensor import Sensor


class Oscillator(Sensor):

    def __init__(self, thing):
        super().__init__(thing)

    def set_sense_value(self):
        self.value = self.thing.get_oscillator_value()
