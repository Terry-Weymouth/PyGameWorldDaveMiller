from parts.cells.sensors.Sensor import Sensor


class LocationNorthSouth(Sensor):

    def __init__(self, thing):
        super().__init__(thing)

    def set_sense_value(self):
        y = self.thing.pos[1]
        max_y = self.thing.world.height
        value = float(y)/max_y
        self.value = value
