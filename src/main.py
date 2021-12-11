from Simulation import Simulation
from World import World

if __name__ == '__main__':
    world = World()
    sim = Simulation(world)
    sim.run()
