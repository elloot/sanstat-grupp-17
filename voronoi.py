import numpy as np
from scipy.spatial import Voronoi


def calculate_distance(coordinates1, coordinates2):
    x1, y1 = coordinates1
    x2, y2 = coordinates2
    return np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def is_covered(circles, origin=(0, 0), width=2, height=2):
    def intersects_edge(p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        k = (y2 - y1) / (x2 - x1)
        m = y1 - k * x1
        y_cutoffs = [0, height]
        for i in range(0, len(y_cutoffs)):
            y_cutoff = y_cutoffs[i]
            if max(y1, y2) > y_cutoff > min(y1, y2):
                x_intersect = (y_cutoff - m) / k
                if 0 <= x_intersect <= width:
                    return [x_intersect, y_cutoff]
        x_cutoffs = [0, width]
        for i in range(0, len(x_cutoffs)):
            x_cutoff = x_cutoffs[i]
            if max(x1, x2) > x_cutoff > min(x1, x2):
                y_intersect = x_cutoff * k + m
                if 0 <= y_intersect <= height:
                    return [x_cutoff, y_intersect]
        return [-1, -1]

    circles = [(circle[0] - origin[0], circle[1] - origin[1]) for circle in circles]
    vor = Voronoi(circles)
    extremes = list(filter(lambda c: 0 <= c[0] <= width and 0 <= c[1] <= height, vor.vertices))
    new_extremes = [[0, 0], [0, height], [width, 0], [width, height]]
    for (i1, i2) in filter(lambda p: p[0] != -1, vor.ridge_vertices):
        p1 = vor.vertices[i1]
        p2 = vor.vertices[i2]
        edge_intersection = intersects_edge(p1, p2)
        if edge_intersection != [-1, -1]:
            new_extremes.append(edge_intersection)
    extremes = np.append(extremes, new_extremes, axis=0)

    for extrema in extremes:
        covered = False
        for circle in circles:
            if covered:
                break
            if calculate_distance(extrema, circle) <= 1:
                covered = True
        if not covered:
            return False
    return True
