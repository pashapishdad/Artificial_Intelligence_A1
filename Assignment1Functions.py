# written by Pasha Pishdad
# Student ID: 40042599
# Assignment 1

# Functions

import math
import shapefile as sf
import numpy as np
from graphics import *
import time


# get the threshold and grid_size from the user
def threshold_and_grid_size():
    global threshold
    global grid_size
    threshold = input("Please enter the threshold: ")
    threshold = float(threshold)
    print()
    grid_size = input("Please enter the grid size: ")
    grid_size = float(grid_size)
    print()
    l_threshold_grid_size = [threshold, grid_size]
    return l_threshold_grid_size


# get the coordinates from the shape file and make an array to store the number of points in each of its cell.
def number_crimes(file_name):
    x = []
    y = []
    # number of cells
    global n_cells
    n_cells = 0.04 / grid_size
    n_cells = int(n_cells)
    # an array to store all nodes to use it to update it with the new node if it has lower cost
    global c_f_n
    c_f_n = np.zeros((n_cells + 1, n_cells + 1, 4))
    c_f_n[:, :, 0] = 1000
    global n_crimes
    n_crimes = np.zeros((n_cells, n_cells))
    with sf.Reader(file_name, encoding='ISO-8859-1') as shape:
        ...
        shr = shape.shapeRecords()
        for i in range(len(shr)):
            x.append(shr[i].shape.__geo_interface__["coordinates"][0])
            y.append(shr[i].shape.__geo_interface__["coordinates"][1])
    # change the coordinates to be from 0 to number of cells to make it easier to manage
    # create an array to store the number of points in each cell
    for i in range(len(x)):
        rows = math.floor((x[i] + 73.590) / grid_size)
        columns = math.floor((y[i] - 45.490) / grid_size)
        n_crimes[columns][rows] += 1
    # flip the nCrimes matrix to use it on the grid GUI
    n_crimes = np.flipud(n_crimes)
    return n_crimes


# make an array out of number_crimes to define blocked cells and it will be flipped to use it in drawing.
# put the comparison of each cell to the number that we need to compare in matrix
def gridify(number_crimes):
    # flat the matrix to be able to sort it
    flatten_crimes = number_crimes.flatten()
    sorted_crimes = np.sort(flatten_crimes)[::-1]

    # find the number to compare and decide that a cell should be blocked or not based on the threshold
    n_to_compare = sorted_crimes[math.floor((n_cells*n_cells) * (1 - threshold)) - 1]
    print("Number at the given percentile(threshold), median(if threshold = 0.5): %.2f \n" % n_to_compare)
    print("Number of total crimes: %d\n" % n_crimes.sum())
    print("The average: %.2f\n" % np.average(n_crimes))
    print("The standard deviation: %.2f\n" % np.std(n_crimes))
    grid = number_crimes >= n_to_compare
    grid = grid.astype(int)

    # flip the grid array and nCrimes array to be able to draw it by the right index
    global draw
    draw = np.flipud(grid)
    return draw


# make an array out of number_crimes to store the number of crimes in each cell and it will be flipped for drawing.
def number_crimes_to_draw(number_crimes):
    draw_numbers = np.flipud(number_crimes)
    draw_numbers = draw_numbers.astype(int)
    return draw_numbers


# find the estimation of cost from a node to the end node.
def heuristic(x, y, x2, y2):
    dist = math.sqrt(((x - x2) ** 2) + ((y - y2) ** 2))
    return dist

# find all the possible direction of each node with the updated cost, original point, and f(n) which is the actual cost plus the heuristic function.
def graph(x, y, c=0, x2=0, y2=0):
    g = []
    # north direction
    if n_cells > x > 0 and y < n_cells and draw[y, x-1] == 0 and draw[y, x] == 0 and c_f_n[x, y+1, 0] > c+1:
        c_f_n[x, y+1] = [c+1, heuristic(x, y + 1, x2, y2) + c + 1, x, y]
        n = [x, y+1, c+1, heuristic(x, y + 1, x2, y2) + c + 1, x, y]
        g.append(n)
    elif n_cells > x > 0 and y < n_cells and ((draw[y, x-1] == 1 and draw[y, x] == 0) or (draw[y, x-1] == 0 and draw[y, x] == 1)) and c_f_n[x, y+1][0] > c+1.3:
        c_f_n[x, y + 1] = [c + 1.3, heuristic(x, y + 1, x2, y2) + c + 1.3, x, y]
        n = [x, y + 1, c+1.3, heuristic(x, y + 1, x2, y2) + c + 1.3, x, y]
        g.append(n)
    # north east direction
    if y < n_cells and x < n_cells and draw[y, x] == 0 and c_f_n[x+1, y+1][0] > c+1.5:
        c_f_n[x + 1, y + 1] = [c + 1.5, heuristic(x + 1, y + 1, x2, y2) + c + 1.5, x, y]
        ne = [x+1, y+1, c+1.5, heuristic(x + 1, y + 1, x2, y2) + c + 1.5, x, y]
        g.append(ne)
    # east direction
    if 0 < y < n_cells and x < n_cells and draw[y, x] == 0 and draw[y-1, x] == 0 and c_f_n[x+1, y][0] > c+1:
        c_f_n[x + 1, y] = [c + 1, heuristic(x + 1, y, x2, y2) + c + 1, x, y]
        e = [x + 1, y, c + 1, heuristic(x + 1, y, x2, y2) + c + 1, x, y]
        g.append(e)
    elif 0 < y < n_cells and x < n_cells and ((draw[y, x] == 1 and draw[y-1, x] == 0) or (draw[y, x] == 0 and draw[y-1, x] == 1)) and c_f_n[x+1, y][0] > c+1.3:
        c_f_n[x + 1, y] = [c + 1.3, heuristic(x + 1, y, x2, y2) + c + 1.3, x, y]
        e = [x + 1, y, c + 1.3, heuristic(x + 1, y, x2, y2) + c + 1.3, x, y]
        g.append(e)
    # south east direction
    if x < n_cells and y > 0 and draw[y-1, x] == 0 and c_f_n[x+1, y-1][0] > c+1.5:
        c_f_n[x + 1, y - 1] = [c + 1.5, heuristic(x + 1, y - 1, x2, y2) + c + 1.5, x, y]
        se = [x + 1, y - 1, c + 1.5, heuristic(x + 1, y - 1, x2, y2) + c + 1.5, x, y]
        g.append(se)
    # south direction
    if 0 < x < n_cells and y > 0 and draw[y-1, x-1] == 0 and draw[y-1, x] == 0 and c_f_n[x, y-1][0] > c+1:
        c_f_n[x, y-1] = [c + 1, heuristic(x, y-1, x2, y2) + c + 1, x, y]
        s = [x, y-1, c + 1, heuristic(x, y-1, x2, y2) + c + 1, x, y]
        g.append(s)
    elif 0 < x < n_cells and y > 0 and ((draw[y-1, x-1] == 1 and draw[y-1, x] == 0) or (draw[y-1, x-1] == 0 and draw[y-1, x] == 1)) and c_f_n[x, y-1][0] > c+1.3:
        c_f_n[x, y-1] = [c + 1.3, heuristic(x, y-1, x2, y2) + c + 1.3, x, y]
        s = [x, y-1, c + 1.3, heuristic(x, y-1, x2, y2) + c + 1.3, x, y]
        g.append(s)
    # south west direction
    if x > 0 and y > 0 and draw[y-1, x-1] == 0 and c_f_n[x-1, y-1][0] > c+1.5:
        c_f_n[x - 1, y - 1] = [c + 1.5, heuristic(x - 1, y - 1, x2, y2) + c + 1.5, x, y]
        sw = [x - 1, y - 1, c + 1.5, heuristic(x - 1, y - 1, x2, y2) + c + 1.5, x, y]
        g.append(sw)
    # west direction
    if 0 < y < n_cells and x > 0 and draw[y-1, x-1] == 0 and draw[y, x-1] == 0 and c_f_n[x-1, y][0] > c+1:
        c_f_n[x-1, y] = [c + 1, heuristic(x-1, y, x2, y2) + c + 1, x, y]
        w = [x-1, y, c + 1, heuristic(x-1, y, x2, y2) + c + 1, x, y]
        g.append(w)
    elif 0 < y < n_cells and x > 0 and ((draw[y-1, x-1] == 1 and draw[y, x-1] == 0) or (draw[y-1, x-1] == 0 and draw[y, x-1] == 1)) and c_f_n[x-1, y][0] > c+1:
        c_f_n[x - 1, y] = [c + 1.3, heuristic(x - 1, y, x2, y2) + c + 1.3, x, y]
        w = [x - 1, y, c + 1.3, heuristic(x - 1, y, x2, y2) + c + 1.3, x, y]
        g.append(w)
    # north west
    if x > 0 and y < n_cells and draw[y, x-1] == 0 and c_f_n[x-1, y+1][0] > c+1.5:
        c_f_n[x - 1, y + 1] = [c + 1.5, heuristic(x - 1, y + 1, x2, y2) + c + 1.5, x, y]
        nw = [x - 1, y + 1, c + 1.5, heuristic(x - 1, y + 1, x2, y2) + c + 1.5, x, y]
        g.append(nw)

    return g

# find the search path by putting next expandable nodes in the open list and visited nodes in the closed list.
def search_path(x1, y1, x2, y2):
    open_list = [[x1, y1, 0, heuristic(x1, y1, x2, y2)]]
    closed_list = []
    answer = False
    duration = 0
    while (len(open_list) > 0) and not answer:
        start_time = time.time()
        # to check if it would take more than 10 seconds to find the path.
        # time.sleep(12)
        if duration > 10:
            return closed_list, True, duration
        t = open_list.pop(0)
        # check if it finds the end node
        if t[0] == x2 and t[1] == y2:
            answer = True
            closed_list.append(t)
            return closed_list, False, duration
        nodes = graph(t[0], t[1], t[2], x2, y2)
        # if the nodes which is the available nodes to explore is not empty, it will add it to the open list
        if nodes:
            open_list.extend(nodes)
            open_list = sorted(open_list, key=lambda l: l[3])
        closed_list.append(t)
        elapsed_time = time.time() - start_time
        duration = duration + elapsed_time

    return closed_list, len(open_list) == 0, duration


# this fuction will use the closed list and backtrack to find the optimal path by finding the next node that has minimum actual cost.
def shortest_path(closed_list):
    s_path = [closed_list[-1][:2]]
    source = closed_list.pop(0)[:2]
    last_point = closed_list.pop(-1)
    total_cost = last_point[2]
    t_sorted = sorted(closed_list, key=lambda l: l[2])
    i = 0
    while last_point[-2:] != source:
        current_point = t_sorted[i]
        if last_point[-2:] == current_point[:2]:
            t_sorted.pop(i)
            i = 0
            s_path.append(last_point[-2:])
            last_point = current_point
        else:
            i += 1
    s_path.append(source[:2])
    s_path.reverse()
    return s_path, total_cost


# this function will draw the grid and the final path
def solve():
    draw_numbers = number_crimes_to_draw(n_crimes)
    t_g = "Threshold = %.2f\tGrid size = %.3f" %(threshold, grid_size)
    win = GraphWin(t_g, 500, 500, autoflush=False)
    win.setCoords(0.0, 0.0, n_cells, n_cells)
    win.setBackground("black")

    # filling the cells with color and number
    for i in range(n_cells):
        for j in range(n_cells):
            if draw[i, j]:
                square = Rectangle(Point(j, i), Point(j+1, i+1))
                square.setFill("yellow")
                square.draw(win)
                text = Text(Point(j+0.5, i+0.5), draw_numbers[i, j])
                text.draw(win)
            else:
                square = Rectangle(Point(j, i), Point(j + 1, i + 1))
                square.setFill("purple")
                square.draw(win)
                text = Text(Point(j + 0.5, i + 0.5), draw_numbers[i, j])
                text.draw(win)

    # getting the point from the user by clicking on the map
    p1 = win.getMouse()
    p2 = win.getMouse()

    # finding the search path by calling the search_path function
    searchpath, invalid_flag, duration = search_path(math.floor(p1.x), math.floor(p1.y), math.floor(p2.x), math.floor(p2.y))

    # displaying proper message
    if duration > 10:
        print("Time is up. The optimal path is not found.")
        return
    if invalid_flag:
        print("Due to blocks, no path is found. Please change the map and try again.\n")
        return

    # finding the solution path by calling the shortest_path function
    shortestpath, total_cost = shortest_path(searchpath)

    print("It took %.8f seconds to calculate the path.\n" % duration)

    p1x, p1y, p2x, p2y = math.floor(p1.x), math.floor(p1.y), math.floor(p2.x), math.floor(p2.y)
    point1x, point1y, point2x, point2y = (p1x * grid_size) - 73.590, (p1y * grid_size) + 45.490, (p2x * grid_size) - 73.590, (p2y * grid_size) + 45.490
    print("starting point x: %.3f y: %.3f -- or -- x: %.3f y: %.3f\n\nend point x: %.3f y: %.3f -- or -- x: %.3f y: %.3f\n" % (point1x, point1y, p1x, p1y, point2x, point2y, p2x, p2y))
    print("Total cost for this path is: %.1f\n" % total_cost)
    print("This is the path: \n", shortestpath)

    # drawing the solution path on the map
    for i in range(len(shortestpath)):
        if i + 1 >= len(shortestpath):
            break
        # cir = Circle(Point(shortestpath[i][0], shortestpath[i][1]), 0.1)
        # cir.setWidth(3)
        # cir.setFill("green")
        # if not i:
        #     cir.draw(win)
        line = Line(Point(shortestpath[i][0], shortestpath[i][1]), Point(shortestpath[i+1][0], shortestpath[i+1][1]))
        if i == 0:
            size = 0.15
        elif i < len(shortestpath) - 2:
            size = 0.2
        elif i == len(shortestpath) - 2:
            # drawing the last point
            cir_final = Circle(Point(shortestpath[i + 1][0], shortestpath[i + 1][1]), 0.3)
            # to just fill the circles with color without border
            cir_final.setWidth(0)
            cir_final.setFill("red")
        cir = Circle(Point(shortestpath[i][0], shortestpath[i][1]), size)
        # to just fill the circles with color without border
        cir.setWidth(0)
        cir.setFill("red")
        line.setFill("black")
        line.setWidth(3)
        line.draw(win)
        cir.draw(win)
        if i == len(shortestpath) - 2:
            cir_final.draw(win)


    # to close byclicking on the map after showing the solution path
    t3 = win.getMouse()

    win.close()
