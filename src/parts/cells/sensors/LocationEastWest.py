from parts.cells.sensors.Sensor import Sensor


class LocationEastWest(Sensor):

    def __init__(self, thing):
        super().__init__(thing)

    def set_sense_value(self):
        x = self.thing.pos[0]
        max_x = self.thing.world.width
        value = float(x)/max_x
        self.value = value
