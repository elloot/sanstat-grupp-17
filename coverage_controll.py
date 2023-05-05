import math

import numpy as np
import matplotlib.pyplot as plt

from union_find import UnionFind


class Circle:
    def __init__(self, coordinates, index):
        self.coordinates = coordinates
        self.index = index


def get_row_col(coordinates):
    (x, y) = coordinates
    if x == 0: x += 1
    if y == 0: y += 1
    return int(np.ceil(x / 2)) - 1, int(np.ceil(x / 2)) - 1


def calculate_distance(coordinates1, coordinates2):
    x1, y1 = coordinates1
    x2, y2 = coordinates2
    return np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


class SquareArea:
    def __init__(self, side_length):
        (row, col) = get_row_col((side_length, side_length))
        (rows, cols) = row + 1, col + 1
        self.rows = rows
        self.cols = cols
        self.sub_area = [[[] for j in range(cols)] for i in range(rows)]

    def add_circle(self, circle):
        (row, col) = get_row_col(circle.coordinates)
        self.sub_area[row][col].append(circle)

    def get_intersecting_circles(self, circle):
        return list(filter(lambda circle2: calculate_distance(circle.coordinates, circle2.coordinates) <= 2,
                           self.get_adjacent_circles(circle.coordinates)))

    def get_adjacent_circles(self, coordinates):
        (row, col) = get_row_col(coordinates)
        row_d = [0, -1, -1, 0, 1, 1, 1, 0, -1]
        col_d = [0, 0, 1, 1, 1, 0, -1, -1, -1]
        adjacent_circles = []
        for i in range(0, 9):
            if 0 <= row + row_d[i] < self.rows and 0 <= col + col_d[i] < self.cols:
                adjacent_circles.extend(self.sub_area[row + row_d[i]][col + col_d[i]])
        return adjacent_circles


class CoverageController:
    def __init__(self, n):
        self.n = n
        self.area = SquareArea(np.sqrt(n))
        self.circle_unions = UnionFind(2)  # index 0 is for the left wall and 1 for the right wall.
        self.index_tracker = 2
        self.number_of_circles = 0

    def are_walls_connected(self):
        return self.circle_unions.is_same_set(0, 1)

    def get_random_coordinates(self):
        return np.random.uniform(0, np.sqrt(self.n)), np.random.uniform(0, np.sqrt(self.n))

    def new_circle(self):
        circle = Circle(self.get_random_coordinates(), self.index_tracker)
        self.index_tracker += 1
        self.circle_unions.add()
        for circle2 in self.area.get_intersecting_circles(circle):
            self.circle_unions.union_sets(circle.index, circle2.index)
        self.area.add_circle(circle)
        if circle.coordinates[0] <= 1:
            self.circle_unions.union_sets(0, circle.index)
        if circle.coordinates[0] >= np.sqrt(self.n) - 1:
            self.circle_unions.union_sets(1, circle.index)
        return circle

    def get_circles(self):
        while True:
            yield plt.Circle(self.new_circle().coordinates, 1, edgecolor='black', facecolor='none')
