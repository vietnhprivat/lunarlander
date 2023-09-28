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
fuel = []
fuel_per_dist = []
frames = []
xcoord = []

v_speed = 37

frame_count = 0

runs = 1000000
run = 1

env = LunarLander()
env.reset()
exit_program = False
while not exit_program and wins < runs:
    #env.render()
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
            run += 1
            print(f"{round(run / runs * 100,1)} % - Fuel: {env.rocket.fuel}, Frames: {framestemp}, XCoord: {x}, Xdist: {round(abs(env.rocket.xstart),1)}")
        
            if env.won:
                wins += 1
                fuel += [(round(env.rocket.fuel,1))]
                frames.append(framestemp)
                xcoord += [round(x,1)]
                fuel_per_dist += [abs(env.rocket.xstart) / env.rocket.fuel]
            else:
                losses = losses + 1
            boost = False        
            left = False
            right = False
            frame_count = 0
            xdist = 0
            env.reset()
    
    if -15 <= x <= 15:
        if xspeed < -7:
            right = False
            left = True
        if xspeed > 7:
            right = True
            left = False
    else:
        if x > 4:
            if xspeed > -v_speed:
                left = False
                right = True
            else:
                right = False
        if x < 4:
            if xspeed < v_speed:
                left = True
                right = False
            else:
                left = False

    if y < 177:
        if yspeed > 13:
            boost = True
        if yspeed < 7:
            boost = False
    else:
        boost = False
    
    
    # Modify and add more if-statements to make the rocket land safely
    # END OF YOUR CODE
else:
    print(f"Wins: {wins}")
    print(f"Looses: {losses}")
    
    # print(xcoord)
    # print(fuel)

    
    average_fuel = round(np.mean(fuel), 2)
    sd = round(np.std(xcoord), 2)
    
    #print(f"Time: {frames}")
    #print(f"Fuel per dist: {fuel_per_dist}")
    #print(f"Xcoord: {xcoord}")
    #print(f"Fuel: {fuel}")
        # Define the number of bins for the histogram
    xbins_value = 30
    # Create the histogram for xcoord_second
    x_hist, x_bins = np.histogram(xcoord, bins=xbins_value)
    #print(len(fuelspent))
    #print(lowest_sd_index)
    # Create the plot for the histogram
    plt.figure(figsize=(12, 9))
    plt.hist(xcoord, bins=xbins_value, edgecolor='black')
    plt.title(f'Xspeed = {v_speed}, SD = {3.39}, Fuelspent = {100-average_fuel}, WR = {(1*100)} %')
    plt.xlabel('X')
    plt.ylabel('Frequency')

    # Show the histogram
    plt.show()

    
    # # Define the number of bins for each histogram
    # xbins_value = 30
    # fuel_bins_value = 30
    # frame_bins_value = 15
    # fuel_per_dist_bins_value = 30  # Define the number of bins for fuel_per_dist

    # # Create histograms for xcoord, fuel, frames, and fuel_per_dist
    # x_hist, x_bins = np.histogram(xcoord, bins=xbins_value)
    # fuel_hist, fuel_bins = np.histogram(fuel, bins=fuel_bins_value)
    # frame_hist, frame_bins = np.histogram(frames, bins=frame_bins_value)
    # fuel_per_dist_hist, fuel_per_dist_bins = np.histogram(fuel_per_dist, bins=fuel_per_dist_bins_value)

    # # Create subplots with 2 rows and 2 columns
    # fig, axs = plt.subplots(2, 2, figsize=(12, 8))  # Adjust the figsize as needed

    # # Plot the first histogram (XCoord) on the first subplot
    # axs[0, 0].hist(xcoord, bins=xbins_value, edgecolor='black')
    # axs[0, 0].set_title('XCoord - Histogram')
    # axs[0, 0].set_xlabel('X')
    # axs[0, 0].set_ylabel('Frequency')

    # # Plot the second histogram (Fuel) on the second subplot
    # axs[0, 1].hist(fuel, bins=fuel_bins_value, edgecolor='black')
    # axs[0, 1].set_title('Fuel - Histogram')
    # axs[0, 1].set_xlabel('Fuel')
    # axs[0, 1].set_ylabel('Frequency')

    # # Plot the third histogram (Frames) on the third subplot
    # axs[1, 0].hist(frames, bins=frame_bins_value, edgecolor='black')
    # axs[1, 0].set_title('Frames - Histogram')
    # axs[1, 0].set_xlabel('Frames')
    # axs[1, 0].set_ylabel('Frequency')

    # # Plot the fourth histogram (Fuel_per_Dist) on the fourth subplot
    # axs[1, 1].hist(fuel_per_dist, bins=fuel_per_dist_bins_value, edgecolor='black')
    # axs[1, 1].set_title('Fuel per Distance - Histogram')
    # axs[1, 1].set_xlabel('Fuel per Distance')
    # axs[1, 1].set_ylabel('Frequency')

    # # Adjust spacing between subplots
    # plt.tight_layout()

    # # Show the subplots
    # plt.show()


    # print(xcoord)
    # print(fuel)


    exit_program = True
    env.close()

    
env.close()

