# Lunar Lander: AI-controlled play

# Instructions:
#   Land the rocket on the platform within a distance of plus/minus 20, 
#   with a horizontal and vertical speed less than 20
#
# Controlling the rocket:
#    arrows  : Turn booster rockets on and off
#    r       : Restart game
#    q / ESC : Quit

from ast import Or
from LunarLander import *
import time
import numpy as np
import matplotlib.pyplot as plt

wins = 0
losses = 0
xdist = 0

fuel_per_dist = []
frames = []
xcoord = []
fuelspent = []
render = 0

# what we actually need
sd_x = []
winrate = []
fuelspent_avg = []

frame_count = 0

# Runs track
runs_per_interval = 1000000
interval = 1
fromto = [32,33]
runs = round((fromto[1]-fromto[0])*1/interval)
currentrun = 1

env = LunarLander()
env.reset()
exit_program = False


#Speeds
center_speed = 7
outer_speed = fromto[0]
internalrun = 0

# Messages
loop1 = False

while not exit_program and outer_speed <= fromto[1]:
    if loop1 == False:
        print("Loop 1 successfully")
        loop1 = True
    if render == 1: env.render()
    frame_count += 1
    (x, y, xspeed, yspeed), reward, done = env.step((boost, left, right)) 
    
    # Process game events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit_program = True
        if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_ESCAPE, pygame.K_q]:
                exit_program = True
            if event.key == pygame.K_UP:
                boost = True
            if event.key == pygame.K_DOWN:
                boost = False
            if event.key == pygame.K_RIGHT:
                left = False if right else True
                right = False
            if event.key == pygame.K_LEFT:
                right = False if left else True
                left = False
            if event.key == pygame.K_r:
                print(f"Wins: {wins}")
                print(f"Looses: {losses}")
                print(f"Time: {frames}")
                print(f"Xcoord: {xcoord}")
                print(f"Fuel: {fuel}")
                
                boost = False        
                left = False
                right = False
                env.reset()

    # Game over events
    if env.game_over:
        framestemp = frame_count
        if not framestemp == 0:
            #print(f"{round(outer_speed / fromto[1] * 100,1)} % - Fuelspent: {100-env.rocket.fuel}, Frames: {framestemp}, XCoord: {x}, Xdist: {round(abs(env.rocket.xstart),1)}")
        
            if env.won:
                
                frames.append(framestemp)
                fuel_per_dist += [abs(env.rocket.xstart) / env.rocket.fuel]
                
                fuelspent += [100-(round(env.rocket.fuel,1))]
                wins += 1
                xcoord += [round(x,1)]

            else:
                losses = losses + 1
            boost = False        
            left = False
            right = False
            frame_count = 0
            xdist = 0
            internalrun += 1
            env.reset()
    

    if internalrun == runs_per_interval:
        #Reset values
        internalrun = 0

        # Beregn standardafvigelse
        s = 0
        for i in xcoord:
            s += 1 / (runs_per_interval - 1) * xcoord[int(i)] ** 2
        sd = np.sqrt(s)
        print(f"{round((outer_speed-fromto[0]) / (fromto[1]-fromto[0]) * 100,1)} %")

        #track data
        sd_x += [round(sd,2)]
        winrate += [round(wins/runs_per_interval,2)]
        fuelspent_avg += [round(np.mean(fuelspent),2)]

        # Set outerspeed up
        outer_speed += interval

        xcoord.clear()
        fuelspent.clear()
        wins = 0

    
    if -15 <= x <= 15:
        if xspeed < -center_speed:
            right = False
            left = True
        if xspeed > center_speed:
            right = True
            left = False
    else:
        if x > 0:
            if xspeed > -outer_speed:
                left = False
                right = True
            else:
                right = False
        if x < 0:
            if xspeed < outer_speed:
                left = True
                right = False
            else:
                left = False

    if y < 180:
        if yspeed > 13:
            boost = True
        if yspeed < 7:
            boost = False
    else:
        boost = False
else:

    
    exit_program = True
    env.close()




print(f"SD: {sd_x}")
print(f"Fuel: {fuelspent_avg}")
print(f"Winrate: {winrate}")


# Graphs

#Define intervals
speed_interval_range = [fromto[0]]
for i in range(fromto[1]-fromto[0]):
    numbertoadd = speed_interval_range[len(speed_interval_range)-1] + interval
    speed_interval_range += [numbertoadd]

# Set the figure size
plt.figure(figsize=(10, 6))

# Create the line plot for sd_x with a text label
sd_line, = plt.plot(speed_interval_range, sd_x, color='darkblue', marker='o', linestyle='-', linewidth=2)
plt.xlabel('Vertical Speed')
plt.ylabel('Standard deviation')

# Create a secondary y-axis for Winrate as a line with no y-axis labels and a text label
ax1 = plt.twinx()
ax1.set_ylim(0, 1.2)  # Set the y-axis scale for winrate
winrate_line, = ax1.plot(speed_interval_range, winrate, color='green', linestyle='-', linewidth=1, label='Winrate')  # Line without points
ax1.get_yaxis().set_visible(False)  # Hide the y-axis labels for Winrate

# Create a separate y-axis for the Fuel variable (fuelspent_avg) on the right with a text label
ax2 = ax1.twinx()
ax2.spines['right'].set_position(('outward', 0))  # Adjust the position of the Fuel axis to the right
fuelspent_line, = ax2.plot(speed_interval_range, fuelspent_avg, color='darkorange', marker='o', linestyle='-', linewidth=2, label='Fuel')

# Create a custom legend for SD
custom_legend = plt.Line2D([], [], color='darkblue', marker='o', linestyle='-', linewidth=2, label='SD')
plt.legend(handles=[custom_legend, winrate_line, fuelspent_line], loc='upper right')

# Add a green dashed line to correspond to where 100% is
ax1.axhline(y=1.0, color='green', linestyle='--')
ax1.annotate('100%', (speed_interval_range[5], 1.05), color='green')
plt.title('Line chart of sd, Fuel, and Winrate against v_speed')
plt.show()


# Find the index of the lowest sd_x where winrate is 100%
lowest_sd_index = None
lowest_sd_value = float('inf')  # Initialize with a high value

for i, (sd_value, winrate_value) in enumerate(zip(sd_x, winrate)):
    if winrate_value == 1.0 and sd_value < lowest_sd_value:
        lowest_sd_index = i
        lowest_sd_value = sd_value

# Check if there is a valid lowest value
if lowest_sd_index is not None:
    lowest_speed_interval = speed_interval_range[lowest_sd_index]  # Get the speed_interval_range number
    print(f"Lowest sd_x with 100% winrate: {lowest_sd_value} at index {lowest_sd_index}")
    print(f"Speed Interval Range corresponding to lowest SD: {lowest_speed_interval}")

    env = LunarLander()
    env.reset()
    exit_program = False
    boost = False        
    left = False
    right = False
    env.reset()

    xcoord_second = []
    runsamount = runs_per_interval
    runnow = 0

    while runnow <= runsamount:
        outer_speed = lowest_speed_interval
        #print(runnow/runsamount*100)
        if render == 1: env.render()
        (x, y, xspeed, yspeed), reward, done = env.step((boost, left, right)) 
        
        # Process game events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_program = True
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_ESCAPE, pygame.K_q]:
                    exit_program = True
                if event.key == pygame.K_UP:
                    boost = True
                if event.key == pygame.K_DOWN:
                    boost = False
                if event.key == pygame.K_RIGHT:
                    left = False if right else True
                    right = False
                if event.key == pygame.K_LEFT:
                    right = False if left else True
                    left = False
                if event.key == pygame.K_r:
                    boost = False        
                    left = False
                    right = False
                    env.reset()

        # Game over events
        if env.game_over:
            print("have won")
            if env.won:
                xcoord_second += [round(x,1)]
            else:
                losses = losses + 1
            boost = False        
            left = False
            right = False
            runnow += 1
            env.reset()

        
        if -15 <= x <= 15:
            if xspeed < -center_speed:
                right = False
                left = True
            if xspeed > center_speed:
                right = True
                left = False
        else:
            if x > 0:
                if xspeed > -outer_speed:
                    left = False
                    right = True
                else:
                    right = False
            if x < 0:
                if xspeed < outer_speed:
                    left = True
                    right = False
                else:
                    left = False

        if y < 180:
            if yspeed > 13:
                boost = True
            if yspeed < 7:
                boost = False
        else:
            boost = False
    else:
        # Define the number of bins for the histogram
        xbins_value = 30

        # Create the histogram for xcoord_second
        x_hist, x_bins = np.histogram(xcoord_second, bins=xbins_value)
        print(len(fuelspent))
        print(lowest_sd_index)
        # Create the plot for the histogram
        plt.figure(figsize=(8, 6))
        plt.hist(xcoord_second, bins=xbins_value, edgecolor='black')
        plt.title(f'Xspeed = {outer_speed}, SD = {sd_x[lowest_sd_index]}, Fuelspent = {fuelspent_avg[lowest_sd_index]}, WR = {winrate[lowest_sd_index]*100} %')
        plt.xlabel('X')
        plt.ylabel('Frequency')

        # Show the histogram
        plt.show()
        exit_program = True
        env.close()

else:
    print("No 100% winrate found in the data")




# Find the index of the highest sd_x
highest_sd_index = None
highest_sd_value = float('-inf')  # Initialize with a low value

for i, sd_value in enumerate(sd_x):
    if sd_value > highest_sd_value:
        highest_sd_index = i
        highest_sd_value = sd_value

# Check if there is a valid highest value
if highest_sd_index is not None:
    highest_speed_interval = speed_interval_range[highest_sd_index]  # Get the speed_interval_range number
    print(f"Highest sd_x value: {highest_sd_value} at index {highest_sd_index}")
    print(f"Speed Interval Range corresponding to highest SD: {highest_speed_interval}")
    
    env = LunarLander()
    env.reset()
    exit_program = False
    boost = False        
    left = False
    right = False
    env.reset()

    xcoord_second = []
    runsamount = runs_per_interval
    runnow = 0

    while runnow <= runsamount:
        outer_speed = highest_speed_interval
        #print(runnow/runsamount*100)
        if render == 1: env.render()
        (x, y, xspeed, yspeed), reward, done = env.step((boost, left, right)) 
        
        # Process game events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_program = True
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_ESCAPE, pygame.K_q]:
                    exit_program = True
                if event.key == pygame.K_UP:
                    boost = True
                if event.key == pygame.K_DOWN:
                    boost = False
                if event.key == pygame.K_RIGHT:
                    left = False if right else True
                    right = False
                if event.key == pygame.K_LEFT:
                    right = False if left else True
                    left = False
                if event.key == pygame.K_r:
                    boost = False        
                    left = False
                    right = False
                    env.reset()

        # Game over events
        if env.game_over:
            print("have won")
            if env.won:
                xcoord_second += [round(x,1)]
            else:
                losses = losses + 1
            boost = False        
            left = False
            right = False
            runnow += 1
            env.reset()

        
        if -15 <= x <= 15:
            if xspeed < -center_speed:
                right = False
                left = True
            if xspeed > center_speed:
                right = True
                left = False
        else:
            if x > 0:
                if xspeed > -outer_speed:
                    left = False
                    right = True
                else:
                    right = False
            if x < 0:
                if xspeed < outer_speed:
                    left = True
                    right = False
                else:
                    left = False

        if y < 180:
            if yspeed > 13:
                boost = True
            if yspeed < 7:
                boost = False
        else:
            boost = False
    else:
        # Define the number of bins for the histogram
        xbins_value = 30

        # Create the histogram for xcoord_second
        x_hist, x_bins = np.histogram(xcoord_second, bins=xbins_value)

        # Create the plot for the histogram
        plt.figure(figsize=(8, 6))
        plt.hist(xcoord_second, bins=xbins_value, edgecolor='black')
        plt.title(f'Xspeed = {outer_speed}, SD = {sd_x[highest_sd_index]}, Fuelspent = {fuelspent_avg[highest_sd_index]}, WR = {winrate[highest_sd_index]*100} %')
        plt.xlabel('X')
        plt.ylabel('Frequency')

        # Show the histogram
        plt.show()
        exit_program = True
        env.close()

else:
    print("No data found in sd_x or all values are negative")


#print(f"minimumsd: {min()}")


# ## HISTOGRAMS ###

#     # Define the number of bins for each histogram
#     xbins_value = 30
#     fuel_bins_value = 30
#     frame_bins_value = 15
#     fuel_per_dist_bins_value = 30  # Define the number of bins for fuel_per_dist

#     # Create histograms for xcoord, fuel, frames, and fuel_per_dist
#     x_hist, x_bins = np.histogram(xcoord, bins=xbins_value)
#     fuel_hist, fuel_bins = np.histogram(fuel, bins=fuel_bins_value)
#     frame_hist, frame_bins = np.histogram(frames, bins=frame_bins_value)
#     fuel_per_dist_hist, fuel_per_dist_bins = np.histogram(fuel_per_dist, bins=fuel_per_dist_bins_value)

#     # Create subplots with 2 rows and 2 columns
#     fig, axs = plt.subplots(2, 2, figsize=(12, 8))  # Adjust the figsize as needed

#     # Plot the first histogram (XCoord) on the first subplot
#     axs[0, 0].hist(xcoord, bins=xbins_value, edgecolor='black')
#     axs[0, 0].set_title('XCoord - Histogram')
#     axs[0, 0].set_xlabel('X')
#     axs[0, 0].set_ylabel('Frequency')

#     # Plot the second histogram (Fuel) on the second subplot
#     axs[0, 1].hist(fuel, bins=fuel_bins_value, edgecolor='black')
#     axs[0, 1].set_title('Fuel - Histogram')
#     axs[0, 1].set_xlabel('Fuel')
#     axs[0, 1].set_ylabel('Frequency')

#     # Plot the third histogram (Frames) on the third subplot
#     axs[1, 0].hist(frames, bins=frame_bins_value, edgecolor='black')
#     axs[1, 0].set_title('Frames - Histogram')
#     axs[1, 0].set_xlabel('Frames')
#     axs[1, 0].set_ylabel('Frequency')

#     # Plot the fourth histogram (Fuel_per_Dist) on the fourth subplot
#     axs[1, 1].hist(fuel_per_dist, bins=fuel_per_dist_bins_value, edgecolor='black')
#     axs[1, 1].set_title('Fuel per Distance - Histogram')
#     axs[1, 1].set_xlabel('Fuel per Distance')
#     axs[1, 1].set_ylabel('Frequency')

#     # Adjust spacing between subplots
#     plt.tight_layout()

#     # Show the subplots
#     plt.show()