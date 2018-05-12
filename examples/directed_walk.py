
from random import randint, choice, shuffle


# Ugly hack to fix s.a imports
import sys
sys.path.append(sys.path[0] + "/..")
sys.path.append(sys.path[0] + "/../..")

from simulated_agency.world import World
from simulated_agency.location import Location
from simulated_agency.agent import Agent
from simulated_agency import states
 

# Initialise world
world = World()

# Constants
NUM_WALKERS = int(world.width * world.height * 0.1)

# Add some locations to the world - specifically, a simple grid
Location.world = world
for x in range(0, world.width):
    for y in range(0, world.height):
        world.locations[x, y] = Location(x, y)

# A Walker is identical to the Agent class (for now)
Walker = Agent

# Specify the World the Walkers live in
Walker.world = world

# Specify an initial target
x = int(world.width / 4)
y = int(world.height / 4)
location = world.locations[x, y]
# A static target is the same thing as a "Dead" walker
Static = states.Dead
Static.colour = 'cyan'
target = Walker(location, Static)

# Add some walkers to the world
for _ in range(0, NUM_WALKERS):
    x = randint(0, world.width - 1)
    y = randint(0, world.height -1)
    location = world.locations[x, y]
    Walker(location, states.MovingTowards, target=target)
            


while True:
    '''
    Event loop
    '''

    # Counter for image frame numbers
    world.counter += 1
    
    # Clear the canvas
    world.canvas.delete('all')

    # Change the target from time to time
    change_target = False
    dice_roll = randint(1, 30)
    if dice_roll == 1:
        change_target = True
        x = randint(0, world.width - 1)
        y = randint(0, world.height - 1)
        target.location = world.locations[x, y]
    
    # Go through the list of agents and tell each of them to do something
    shuffle(world.agents)
    for agent in world.agents:
        if change_target:
            # Don't change the state of our target
            if agent is target:
                continue
            agent.set_state(states.MovingTowards, target=target)
        # Tell the agent to act
        agent.state.execute()
        world.draw(agent)

    # Draw the target last
    world.draw(target)

    # Update the canvas
    world.canvas.after(20)
    world.canvas.update()

    # Save images
    if world.record_video:
        world.save_image('directed_walk')
        

world.window.mainloop()