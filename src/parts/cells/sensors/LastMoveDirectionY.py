from parts.cells.sensors.Sensor import Sensor


class LastMoveDirectionY(Sensor):

    def __init__(self, thing):
        super().__init__(thing)

    def set_sense_value(self):
        self.value = self.thing.move_direction[1]
