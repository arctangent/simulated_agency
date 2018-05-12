
from random import randint, choice, shuffle


# Ugly hack to fix s.a imports
import sys
sys.path.append(sys.path[0] + "/..")
sys.path.append(sys.path[0] + "/../..")

from simulated_agency.simulation import Simulation
from simulated_agency.location import Location
from simulated_agency.agents import Agent
from simulated_agency.states import *
 

# Initialise simulation
simulation = Simulation(cell_size=8)
Location.simulation = simulation

# Constants
NUM_WALKERS = int(simulation.width * simulation.height * 0.1)

# A Walker is identical to the Agent class (for now)
Walker = Agent
Walker.state_machine = StateMachine([Dead, Waiting, MovingTowardsLocation])
Walker.simulation = simulation

# Create a target location
target_location = simulation.random_location()

# Add some walkers to the simulation
for _ in range(0, NUM_WALKERS):
    Walker(simulation.random_location(), MovingTowardsLocation, target_location=target_location)
            


def loop():
    '''
    Event loop
    '''

    # Counter for image frame numbers
    simulation.counter += 1
    
    # Clear the canvas
    simulation.canvas.delete('all')

    # Change the target location from time to time
    change_target = False
    dice_roll = randint(1, 30)
    if dice_roll == 1:
        change_target = True
        target_location = simulation.random_location()
    
    # Go through the list of agents and tell each of them to do something
    shuffle(Walker.objects)
    for agent in Walker.objects:
        if change_target:
            agent.set_state(MovingTowardsLocation, target_location=target_location)
        # Tell the agent to act
        agent.execute()
        simulation.draw(agent)

    # Save images
    if simulation.record_video:
        simulation.save_image('directed_walk')

    simulation.canvas.after(20, loop)
        
loop()
simulation.window.mainloop()