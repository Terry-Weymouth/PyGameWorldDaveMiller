from parts.cells.sensors.Sensor import Sensor


class Age(Sensor):

    def __init__(self, thing):
        super().__init__(thing)

    def set_sense_value(self):
        age = self.thing.age
        max_age = self.thing.world.max_number_of_steps
        self.value = float(age)/max_age