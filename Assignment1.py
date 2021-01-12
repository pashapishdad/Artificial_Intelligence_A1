# written by Pasha Pishdad
# Student ID: 40042599
# Assignment 1

import math
import shapefile as sf
import numpy as np
from graphics import *

"""
gp = gp.read_file("crime_dt.shp")
"""
threshold = 0.5

nCells = 400
x = []
y = []
p = 0
x2 = 19
y2 = 19
# cost f(n) node

test = np.zeros((20,20), dtype=bytearray)
test[0,0]=[2,1]
print("test", test[0,0][1])

c_f_n = np.zeros((20, 20), dtype=bytearray)
for i in range(20):
    for j in range(20):
        c_f_n[i,j] = [1000,0,0,0]

#r, c = 20, 20;
#nCrimes = [[0 for x in range(r)] for y in range(c)]
#nCrimes = np.array(nCrimes)

#grid = [[0 for x in range(r)] for y in range(c)]
#grid = np.array(grid)

nCrimes = np.zeros((20, 20))
grid = np.zeros((20, 20))

with sf.Reader("crime_dt.shp", encoding='ISO-8859-1') as shape:
    ...
    shr = shape.shapeRecords()
    for i in range(len(shr)):
        x.append(shr[i].shape.__geo_interface__["coordinates"][0])
        y.append(shr[i].shape.__geo_interface__["coordinates"][1])
        #list[i] = (x,y)

print(nCrimes)
for i in range(len(x)):
    rows = math.floor((x[i] + 73.590)/0.002)
    #print(rows)
    columns = math.floor((y[i] - 45.490)/0.002)
    nCrimes[columns][rows] += 1

total_crimes = np.sum(nCrimes)
print(total_crimes)

#print(nCrimes)
#print()
nCrimes = np.flipud(nCrimes)
print(nCrimes)

median = np.median(nCrimes)
print("median: ", median)

flattenCrimes = nCrimes.flatten()
print(flattenCrimes)
sortedCrimes = np.sort(flattenCrimes)[::-1]
print(sortedCrimes)

nToCompare = sortedCrimes[math.floor(nCells * (1 - threshold)) - 1]
print("number to compare", nToCompare)

grid = nCrimes >= nToCompare
grid = grid.astype(int)
print(grid)

draw = np.flipud(grid)
draw_numbers = np.flipud(nCrimes)
draw_numbers = draw_numbers.astype(int)

print("draw grid")
print(draw)
"""
test2 = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
print(test2)
test2 = np.flipud(test2)
print(test2)
test3 = test2[::-1, :]
print(test3)
"""

print(x)
print(y)

#draw lines over the plot
#axes.plot(xs, ys)
#figure.canvas.draw_idle()

#print(shapes)


#def cost_edge()
def heuristic2(x, y, x2, y2):
    dist = math.sqrt(((x - x2) ** 2) + ((y - y2) ** 2))
    return dist

print("cfn", c_f_n[1,1])


def graph(x, y, c=0):
    g = []
    # north direction
    if draw[y, x-1] == 0 and draw[y, x] == 0 and c_f_n[x, y+1][0] > c+1:
        #if c_f_n[x, y+1][0] > c+1:
        c_f_n[x, y+1] = [c+1, heuristic2(x, y + 1, x2, y2) + c + 1, x, y]
        n = [x, y+1, c+1, heuristic2(x, y + 1, x2, y2) + c + 1, x, y]
        g.append(n)
        #g[x, y+1] = [c+1, heuristic2(x, y + 1, x2, y2) + c+1, x, y]

        # n = [x, y + 1, heuristic2(x, y + 1, x2, y2) + c + 1, x, y]
        # g.append(n)
    elif ((draw[y, x-1] == 1 and draw[y, x] == 0) or (draw[y, x-1] == 0 and draw[y, x] == 1)) and c_f_n[x, y+1][0] > c+1.3:
        c_f_n[x, y + 1] = [c + 1.3, heuristic2(x, y + 1, x2, y2) + c + 1.3, x, y]
        n = [x, y + 1, c+1.3, heuristic2(x, y + 1, x2, y2) + c + 1.3, x, y]
        g.append(n)
    # north east direction
    if draw[y, x] == 0 and c_f_n[x+1, y+1][0] > c+1.5:
        c_f_n[x + 1, y + 1] = [c + 1.5, heuristic2(x + 1, y + 1, x2, y2) + c + 1.5, x, y]
        ne = [x+1, y+1, c+1.5, heuristic2(x + 1, y + 1, x2, y2) + c + 1.5, x, y]
        g.append(ne)
    # east direction
    if draw[y, x] == 0 and draw[y-1, x] == 0 and c_f_n[x+1, y][0] > c+1:
        c_f_n[x + 1, y] = [c + 1, heuristic2(x + 1, y, x2, y2) + c + 1, x, y]
        e = [x + 1, y, c + 1, heuristic2(x + 1, y, x2, y2) + c + 1, x, y]
        g.append(e)
    elif ((draw[y, x] == 1 and draw[y-1, x] == 0) or (draw[y, x] == 0 and draw[y-1, x] == 1)) and c_f_n[x+1, y][0] > c+1.3:
        c_f_n[x + 1, y] = [c + 1.3, heuristic2(x + 1, y, x2, y2) + c + 1.3, x, y]
        e = [x + 1, y, c + 1.3, heuristic2(x + 1, y, x2, y2) + c + 1.3, x, y]
        g.append(e)
    # south east direction
    if draw[y-1, x] == 0 and c_f_n[x+1, y-1][0] > c+1.5:
        c_f_n[x + 1, y - 1] = [c + 1.5, heuristic2(x + 1, y - 1, x2, y2) + c + 1.5, x, y]
        se = [x + 1, y - 1, c + 1.5, heuristic2(x + 1, y - 1, x2, y2) + c + 1.5, x, y]
        g.append(se)
    # south direction
    if draw[y-1, x-1] == 0 and draw[y-1, x] == 0 and c_f_n[x, y-1][0] > c+1:
        c_f_n[x, y-1] = [c + 1, heuristic2(x, y-1, x2, y2) + c + 1, x, y]
        s = [x, y-1, c + 1, heuristic2(x, y-1, x2, y2) + c + 1, x, y]
        g.append(s)
    elif ((draw[y-1, x-1] == 1 and draw[y-1, x] == 0) or (draw[y-1, x-1] == 0 and draw[y-1, x] == 1)) and c_f_n[x, y-1][0] > c+1.3:
        c_f_n[x, y-1] = [c + 1.3, heuristic2(x, y-1, x2, y2) + c + 1.3, x, y]
        s = [x, y-1, c + 1.3, heuristic2(x, y-1, x2, y2) + c + 1.3, x, y]
        g.append(s)
    # south west direction
    if draw[y-1, x-1] == 0 and c_f_n[x-1, y-1][0] > c+1.5:
        c_f_n[x - 1, y - 1] = [c + 1.5, heuristic2(x - 1, y - 1, x2, y2) + c + 1.5, x, y]
        sw = [x - 1, y - 1, c + 1.5, heuristic2(x - 1, y - 1, x2, y2) + c + 1.5, x, y]
        g.append(sw)
    # west direction
    if draw[y-1, x-1] == 0 and draw[y, x-1] == 0 and c_f_n[x-1, y][0] > c+1:
        c_f_n[x-1, y] = [c + 1, heuristic2(x-1, y, x2, y2) + c + 1, x, y]
        w = [x-1, y, c + 1, heuristic2(x-1, y, x2, y2) + c + 1, x, y]
        g.append(w)
    elif ((draw[y-1, x-1] == 1 and draw[y, x-1] == 0) or (draw[y-1, x-1] == 0 and draw[y, x-1] == 1)) and c_f_n[x-1, y][0] > c+1:
        c_f_n[x - 1, y] = [c + 1.3, heuristic2(x - 1, y, x2, y2) + c + 1.3, x, y]
        w = [x - 1, y, c + 1.3, heuristic2(x - 1, y, x2, y2) + c + 1.3, x, y]
        g.append(w)
    # north west
    if draw[y, x-1] == 0 and c_f_n[x-1, y+1][0] > c+1.5:
        c_f_n[x - 1, y + 1] = [c + 1.5, heuristic2(x - 1, y + 1, x2, y2) + c + 1.5, x, y]
        nw = [x - 1, y + 1, c + 1.5, heuristic2(x - 1, y + 1, x2, y2) + c + 1.5, x, y]
        g.append(nw)

    return g


def search_path(x1, y1, x2, y2):
    open_list = [[x, y, 0, heuristic(x1, y1, x2, y2)]]
    closed_list = []
    #oList = []
    answer = False
    while (len(open_list) > 0) and not answer:
        t = open_list.pop(0)
        if t[0] == x2 and t[1] == y2:
            answer = True
            return closed_list
        print(t[0],"--", t[1],"--", t[2])
        nodes = graph(t[0], t[1], t[2])
        if not nodes:
            open_list.append(nodes)
            open_list = sorted(open_list, key=lambda l: l[3])
        closed_list.append(t)
        #paths = graph()
        return closed_list
        print()


def main():
    win = GraphWin('Floor', 500, 525, autoflush=False)
    win.setCoords(0.0, 0.0, 20.0, 21.0)
    win.setBackground("black")

    for i in range(20):
        for j in range(20):
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
    t = win.getMouse()
    point = Text(Point(10, 20.5), t)
    point.setFill("white")
    point.draw(win)
    t2 = win.getMouse()
    print()

    """
    win = GraphWin('Floor', 500, 500)

    win.setCoords(0.0, 0.0, 10.0, 10.0)
    win.setBackground("yellow")

    # draw grid
    for x in range(10):
        for y in range(10):
            win.plotPixel(x * 50, y * 50, "blue")

    square = Rectangle(Point(5, 5), Point(6, 6))
    square.draw(win)
    square.setFill("black")
    """
    #square = Rectangle(Point(5,5), Point(6,6))
    #square.draw(win)
    #square.setFill("yellow")

    #t = win.getMouse()
    print(t)
    p = t
    directions = graph(math.floor(p.x), math.floor(p.y))
    print(directions)
    print(draw[math.floor(p.y), math.floor(p.x)])
    print(draw_numbers[math.floor(p.y), math.floor(p.x)])
    win.close()

main()


#directions = a_star(math.floor(p.x), math.floor(p.y))
#print(directions)
#print(draw[5, 2])
#print(draw_numbers[2, 5])

def heuristic(x, y, x2, y2):
    dist = math.sqrt(((x - x2) ** 2) + ((y - y2) ** 2))
    return dist


print(heuristic(1, 1, 1, 6))

def a_star(x, y, x2, y2):
    oList = []
    answer = False
    while oList != [] or answer == False:

        print()


search_path(1, 1, 3, 3)

"""
open_list = [[1, 1, 0, heuristic(1, 1, 3, 3)]]
print("open list:", open_list)
#e = open_list.pop(0)
#print("open list pop 0", e)
closed_list = []
    #oList = []
answer = False
while (len(open_list) > 0) and not answer:
    print("check again", open_list)
    t = open_list.pop(0)
    if t[0] == x2 and t[1] == y2:
        answer = True
        print(closed_list)
    print(t[0],"--", t[1],"--", t[2])
    nodes = graph(t[0], t[1], t[2])
    if not nodes:
        open_list.append(nodes)
        open_list = sorted(open_list, key=lambda l: l[3])
        closed_list.append(t)
        #paths = graph()
    print(closed_list)
    print()
"""
"""
plot = gp.plot()
plt.show()
(p, bins, patches) = plt.hist(p, bins=20, label='hst')
print(p)

# generate some uniformly distributed data
x = np.random.rand(1000)

# create the histogram
(n, bins, patches) = plt.hist(x, bins=10, label='hst')

plt.show()

# inspect the counts in each bin
print(n)

# and we see that the bins are approximately uniformly filled.
# create a second histogram with more bins (but same input data)
(n2, bins2, patches) = plt.hist(x, bins=20, label='hst')

print(n2)


# bins are uniformly filled but obviously with fewer in each bin.
"""