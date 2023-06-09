import math

import numpy as np
import matplotlib.pyplot as plt

import voronoi
from union_find import UnionFind


class Circle:
    def __init__(self, coordinates, index):
        self.coordinates = coordinates
        self.index = index


def get_row_col(coordinates):
    (x, y) = coordinates
    if x == 0:
        x += 1
    if y == 0:
        y += 1
    return int(np.ceil(x / 2)) - 1, int(np.ceil(y / 2)) - 1


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
        self.is_sub_area_covered = [
            [False for j in range(cols)] for i in range(rows)]
        self.number_of_sub_areas = rows * cols
        self.number_of_covered_sub_areas = 0

    def is_square_covered(self):
        return self.number_of_covered_sub_areas == self.number_of_sub_areas

    def test_sub_area_covered(self, row, col):
        if self.is_sub_area_covered[row][col]:
            return
        origin = (row * 2, col * 2)
        sub_area_center = (origin[0] + 1, origin[1] + 1)
        adjacent_circles_coordinates = [
            circle.coordinates for circle in self.get_adjacent_circles(sub_area_center)]
        circles = list(filter(lambda circle_center: calculate_distance(circle_center, sub_area_center) <= 2,
                              adjacent_circles_coordinates))
        if voronoi.is_covered(circles, origin=origin):
            self.is_sub_area_covered[row][col] = True
            self.number_of_covered_sub_areas += 1

    def check_new_circle(self, circle):
        (row, col) = get_row_col(circle.coordinates)
        row_d = [0, -1, -1, 0, 1, 1, 1, 0, -1]
        col_d = [0, 0, 1, 1, 1, 0, -1, -1, -1]
        for i in range(0, 9):
            if 0 <= row + row_d[i] < self.rows and 0 <= col + col_d[i] < self.cols:
                self.test_sub_area_covered(row + row_d[i], col + col_d[i])
        # print("{} of {} subareas covered".format(self.number_of_covered_sub_areas, self.number_of_sub_areas))

    def add_circle(self, circle):
        (row, col) = get_row_col(circle.coordinates)
        self.sub_area[row][col].append(circle)
        self.check_new_circle(circle)

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
                adjacent_circles.extend(
                    self.sub_area[row + row_d[i]][col + col_d[i]])
        return adjacent_circles


class CoverageController:
    def __init__(self, n):
        self.n = n
        self.area = SquareArea(np.sqrt(n))
        # index 0 is for the left wall and 1 for the right wall.
        self.circle_unions = UnionFind(2)
        self.index_tracker = 2
        self.number_of_circles = 0

    def are_walls_connected(self):
        return self.circle_unions.is_same_set(0, 1)

    def is_completely_covered(self):
        return self.area.is_square_covered()

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
        self.number_of_circles += 1
        return circle

    def get_circles(self):
        while True:
            yield plt.Circle(self.new_circle().coordinates, 1, edgecolor='black', facecolor='none')

    def run_simulation(self):
        while not self.are_walls_connected():
            self.new_circle()
        number_of_circles_for_connection = self.number_of_circles
        while not self.is_completely_covered():
            self.new_circle()
        return number_of_circles_for_connection, self.number_of_circles

"""
    def check_corners(self, new_triangle):
        x, y = new_triangle.coordinates
        # Top left corner
        if x <= SIDE / 2 and y >= np.sqrt(self.n) - 2 / 3 * HEIGHT:
            self.uf.union_sets(2, new_triangle.index)
        # Top right corner
        if x >= np.sqrt(self.n) - SIDE / 2 and y >= np.sqrt(self.n) - 2 / 3 * HEIGHT:
            self.uf.union_sets(3, new_triangle.index)
        # Bottom right corner
        if x >= np.sqrt(self.n) - SIDE / 2 and y <= 1 / 3 * HEIGHT:
            self.uf.union_sets(4, new_triangle.index)
        # Bottom left corner
        if x <= SIDE / 2 and y <= 1 / 3 * HEIGHT:
            self.uf.union_sets(5, new_triangle.index)"""