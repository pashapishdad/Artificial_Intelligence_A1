# written by Pasha Pishdad
# Student ID: 40042599
# Assignment 1

# Driver

from Assignment1Functions import *


if __name__ == "__main__":

    run = True
    while run:
        # calling the function threshold_and_grid_size() to get the threshold and grid size
        threshold_and_grid_size()

        # calling the function number_crimes("crime_dt.shp") to create coordinates based on the shape file
        n_crimes = number_crimes("crime_dt.shp")

        # calling the function gridify(n_crimes) to make the initial grid
        gridify(n_crimes)

        # calling the function solve() to find the shortest path
        solve()

        # check to see if the user want to exit or continue
        running = input("Press 'Y' or 'y' to continue, press any other key to exit: \n")
        run = running.upper() == 'Y'

