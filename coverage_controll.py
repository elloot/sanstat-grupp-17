import math

import numpy as np
import matplotlib.pyplot as plt


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
        self.sub_area = [[[] for j in range(cols)] for i in range(rows)]

    def add_circle(self, coordinates):
        (row, col) = get_row_col(coordinates)
        self.sub_area[row][col].append(coordinates)

    def get_intersecting_circles(self, coordinates):
        return list(filter(lambda coordinates2: calculate_distance(coordinates, coordinates2) <= 2,
                           self.get_adjacent_circles(coordinates)))

    def get_adjacent_circles(self, coordinates):
        (row, col) = get_row_col(coordinates)
        row_d = [0, -1, -1, 0, 1, 1, 1, 0, -1]
        col_d = [0, 0, 1, 1, 1, 0, -1, -1, -1]
        adjacent_circles = []
        for i in range(0, 9):
            adjacent_circles.extend(self.sub_area[row + row_d[i]][col + col_d[i]])
        return adjacent_circles


square = SquareArea(np.sqrt(64))
square.add_circle((0, 0))
square.add_circle((0.1, 0.1))
print(square.get_intersecting_circles((2.05, 0)))


class CoverageController:
    def __init__(self, n):
        self.n = n
        self.x_max = np.sqrt(n)
        self.y_max = np.sqrt(n)

    def get_random_coordinates(self):
        return np.random.uniform(0, np.sqrt(self.n)), np.random.uniform(0, np.sqrt(self.n))

    def get_circles(self):
        while True:
            yield plt.Circle(self.get_random_coordinates(), 1, edgecolor='black', facecolor='none')
