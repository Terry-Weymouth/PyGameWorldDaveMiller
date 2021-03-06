from enum import Enum

BLUE = (0, 0, 255)
LIGHT_GREY = (180, 180, 180)
DARK_GREY = (80, 80, 80)
RED = (255, 0, 0)

THING_SIZE = 4
THING_COLOR = BLUE

NUMBER_OF_THINGS = 300
NUMBER_OF_GENES_IN_GENOME = 20
NUMBER_OF_NEURONS = 10
WORLD_SIZE = 128
GRID_SIZE = 4
DISPLAY_SIZE = WORLD_SIZE * GRID_SIZE

MAX_NUMBER_OF_STEPS = 1000  # how many steps to a generation (should be in Simulation - which is not now)

BACKGROUND_COLOR = DARK_GREY
FPS = 30


class GeneCellType(Enum):
    SENSOR = 1
    NEURON = 2
    ACTUATOR = 3

    @classmethod
    def source_type_by_index(cls, type_index):
        cell_type = GeneCellType.SENSOR
        if type_index is 1:
            cell_type = GeneCellType.NEURON
        return cell_type

    @classmethod
    def sink_type_by_index(cls, type_index):
        cell_type = GeneCellType.ACTUATOR
        if type_index is 1:
            cell_type = GeneCellType.NEURON
        return cell_type
