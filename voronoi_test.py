import numpy as np
from matplotlib import patches
from scipy.spatial import Voronoi, voronoi_plot_2d
import matplotlib.pyplot as plt

from voronoi import is_covered

# np.random.seed(123)


circles = np.array([(np.random.uniform(-1, 3), np.random.uniform(-1, 3)) for i in range(0, 15)])

plt.xlim([-1, 3]), plt.ylim([-1, 3])
rect = patches.Rectangle((0, 0), 2, 2, linewidth=2, edgecolor='black', facecolor='none')
for circle in circles:
    plt.gca().add_patch(plt.Circle(circle, 1, edgecolor='none', facecolor='blue'))
plt.gca().add_patch(rect)

plt.title(is_covered(circles))
plt.gca().set_aspect('equal')
plt.show()

"""

points = np.array([(np.random.uniform(-1, 3), np.random.uniform(-1, 3)) for i in range(0, 50)])
# points = np.array([[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2], [2, 0], [2, 1], [2, 2]])
points = np.append(points, [[10, 10], [-10, 10], [10, -10], [-10, -10]], axis=0)

vor = Voronoi(points)


def calculate_distance(coordinates1, coordinates2):
    x1, y1 = coordinates1
    x2, y2 = coordinates2
    return np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def scatter_array(coordinates):
    plt.scatter([coordinates[i][0] for i in range(0, len(coordinates))],
                [coordinates[i][1] for i in range(0, len(coordinates))])


def line_between_points(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    plt.plot([x1, x2], [y1, y2], color="green")


#scatter_array(points)

extrema = list(filter(lambda c: 0 <= c[0] <= 2 and 0 <= c[1] <= 2, vor.vertices))


def intersects_edge(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    k = (y2 - y1) / (x2 - x1)
    m = y1 - k * x1
    y_cutoffs = [0, 2]
    for i in range(0, len(y_cutoffs)):
        y_cutoff = y_cutoffs[i]
        if max(y1, y2) > y_cutoff > min(y1, y2):
            x_intersect = (y_cutoff - m) / k
            if 0 <= x_intersect <= 2:
                return [x_intersect, y_cutoff]
    x_cutoffs = [0, 2]
    for i in range(0, len(x_cutoffs)):
        x_cutoff = x_cutoffs[i]
        if max(x1, x2) > x_cutoff > min(x1, x2):
            y_intersect = x_cutoff * k + m
            if 0 <= y_intersect <= 2:
                return [x_cutoff, y_intersect]
    return [-1, -1]


new_extrema = [[0, 0], [0, 2], [2, 0], [2, 2]]
for (i1, i2) in filter(lambda p: p[0] != -1, vor.ridge_vertices):
    p1 = vor.vertices[i1]
    p2 = vor.vertices[i2]
    edge_intersection = intersects_edge(p1, p2)
    if edge_intersection != [-1, -1]:
        new_extrema.append(edge_intersection)
    #line_between_points(p1, p2)
extrema = np.append(extrema, new_extrema, axis=0)
#scatter_array(extrema)

# fig = voronoi_plot_2d(vor)
plt.xlim([-1, 3]), plt.ylim([-1, 3])
rect = patches.Rectangle((0, 0), 2, 2, linewidth=2, edgecolor='black', facecolor='none')
for point in points:
    plt.gca().add_patch(plt.Circle(point, 1, edgecolor='none', facecolor='blue'))
plt.gca().add_patch(rect)


def is_covered(circles, control_points):
    for control_point in control_points:
        covered = False
        for circle in circles:
            if covered:
                break
            if calculate_distance(control_point, circle) <= 1:
                covered = True
        if not covered:
            return False
    return True


plt.title(is_covered(points, extrema))
plt.gca().set_aspect('equal')
plt.show()
"""
