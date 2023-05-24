import numpy as np
import shapely
from matplotlib import pyplot as plt
from timeit import default_timer as timer
import math

from union_find import UnionFind

SIDE = np.sqrt(2 * np.pi / np.sqrt(1.25))
HEIGHT = np.sqrt((SIDE / 2) ** 2 + SIDE ** 2)

HAS_RAN = False

START = 0
STOP = 0

NUM_TRIANGLES = 1000


def flatten(l):
    return [(l_element for l_element in sub_list) for sub_list in l]


class Triangle:
    def __init__(self, coordinates, index):
        self.coordinates = coordinates
        self.index = index
        x, y = coordinates
        self.polygon = shapely.Polygon(
            [(x - 0.5 * SIDE, y - 1 / 3 * HEIGHT), (x + 0.5 * SIDE, y - 1 / 3 * HEIGHT), (x, y + 2 / 3 * HEIGHT)])


def get_row_col(coordinates):
    (x, y) = coordinates
    if x == 0:
        x += 1
    if y == 0:
        y += 1
    return int(np.ceil(x / SIDE)) - 1, int(np.ceil(y / SIDE)) - 1


class SquareArea:
    def __init__(self, side_length):
        (row, col) = get_row_col((side_length, side_length))
        (rows, cols) = row + 1, col + 1
        self.rows = rows
        self.cols = cols
        self.sub_area = [[[] for j in range(cols)] for i in range(rows)]

    def add_triangle(self, triangle):
        (row, col) = get_row_col(triangle.coordinates)
        self.sub_area[row][col].append(triangle)

    def get_intersecting_triangle(self, triangle):
        return list(filter(lambda triangle2: shapely.intersects(triangle.polygon, triangle2.polygon),
                           self.get_adjacent_triangles(triangle.coordinates)))

    def get_adjacent_triangles(self, coordinates):
        (row, col) = get_row_col(coordinates)
        row_d = [0, -1, -1, 0, 1, 1, 1, 0, -1]
        col_d = [0, 0, 1, 1, 1, 0, -1, -1, -1]
        adjacent_triangles = []
        for i in range(0, 9):
            if 0 <= row + row_d[i] < self.rows and 0 <= col + col_d[i] < self.cols:
                adjacent_triangles.extend(
                    self.sub_area[row + row_d[i]][col + col_d[i]])
        return adjacent_triangles

    def get_all_triangles(self):
        triangles = []
        for r in range(0, self.rows):
            for c in range(0, self.cols):
                triangles.extend(self.sub_area[r][c])
        return triangles


class CoverageControllerTriangle:
    def __init__(self, n):
        self.n = n
        self.area = SquareArea(np.sqrt(n))
        # index 0 is for the left wall and 1 for the right wall. 2, 3, 4, 5 for the corners
        self.uf = UnionFind(6)
        self.index_tracker = 6
        self.number_of_triangles = 0
        self.is_one_set = False
        self.blob = 0
        self.square = shapely.Polygon(
            ((0, 0), (0, np.sqrt(n)), (np.sqrt(n), np.sqrt(n)), (np.sqrt(n), 0)))
        self.square_area = shapely.area(self.square)
        self.is_covered = False
        self.triangles = []
        self.blobified = False

    def are_walls_connected(self):
        return self.uf.is_same_set(0, 1)

    def get_random_coordinates(self):
        return np.random.uniform(0, np.sqrt(self.n)), np.random.uniform(0, np.sqrt(self.n))

    def update_area(self, new_triangle):
        # global HAS_RAN, START, STOP
        # if not HAS_RAN:
        # START = timer()
        # HAS_RAN = True

        if not self.is_one_set:
            if self.uf.number_of_sets >= 2:
                return
        if not self.is_one_set:
            self.blob = shapely.union_all(
                [triangle.polygon for triangle in self.area.get_all_triangles()])
            self.is_one_set = True
            print('Link complete')
            # STOP = timer()
            # print(f'Took {STOP - START} s for link')

        else:
            self.blob = shapely.union_all([self.blob, new_triangle.polygon])
            if shapely.area(shapely.intersection(self.blob, self.square)) == shapely.area(self.square):
                self.is_covered = True

    def check_corners(self, new_triangle):
        # Top left corner
        if new_triangle.polygon.contains(shapely.geometry.Point(0, np.sqrt(self.n))):
            self.uf.union_sets(2, new_triangle.index)
        # Top right corner
        if new_triangle.polygon.contains(shapely.geometry.Point(np.sqrt(self.n), np.sqrt(self.n))):
            self.uf.union_sets(3, new_triangle.index)
        # Bottom right corner
        if new_triangle.polygon.contains(shapely.geometry.Point(np.sqrt(self.n), 0)):
            self.uf.union_sets(4, new_triangle.index)
        # Bottom left corner
        if new_triangle.polygon.contains(shapely.geometry.Point(0, 0)):
            self.uf.union_sets(5, new_triangle.index)

    def new_triangle(self):
        triangle = Triangle(self.get_random_coordinates(), self.index_tracker)
        self.index_tracker += 1
        self.uf.add()
        for triangle2 in self.area.get_intersecting_triangle(triangle):
            self.uf.union_sets(triangle.index, triangle2.index)
        self.area.add_triangle(triangle)
        if triangle.coordinates[0] <= SIDE / 2:
            self.uf.union_sets(0, triangle.index)
        if triangle.coordinates[0] >= np.sqrt(self.n) - SIDE / 2:
            self.uf.union_sets(1, triangle.index)
        self.number_of_triangles += 1
        if self.uf.number_of_sets >= 2:
            self.check_corners(triangle)
        self.update_area(triangle)
        return triangle

    def opdate_area(self):
        triangles = self.gen_tonsa_triangles()
        self.triangles.extend(triangles)
        union = shapely.union_all(self.triangles)
        if type(union) == shapely.geometry.polygon.Polygon:
            self.blob = union
            self.blobified = True

    def gen_tonsa_triangles(self):
        coords = np.random.uniform(0, np.sqrt(self.n), (NUM_TRIANGLES, 2))
        triangles = []
        for x, y in coords:
            triangles.append(Triangle((x, y), self.index_tracker).polygon)
            self.index_tracker += 1
        return triangles

    def mass_triangle(self):
        triangles = self.gen_tonsa_triangles()
        tris_and_blob = []
        tris_and_blob.append(self.blob)
        tris_and_blob.extend(triangles)
        snapshot_blob = shapely.union_all(tris_and_blob)

        # If square can be covered by the newly added triangles,
        # find the precise number of triangles that needed to be added
        # for coverage
        loopstart, loopstop = 0, 0
        if shapely.area(shapely.intersection(snapshot_blob, self.square)) == self.square_area:
            final_triangle_found = False
            final_triangle_index = 0
            lower = 0
            upper = len(triangles) - 1
            pivot = math.nan
            # Binary search for finding the amount of triangles that
            # needed to be added for coverage
            # loopstart = timer()
            # print('Starting loop')
            while not final_triangle_found:
                if upper - lower == 1:
                    final_triangle_found = True
                    final_triangle_index = upper
                    # self.blob = shapely.union_all([self.blob].extend(
                    # triangles[:final_triangle_index + 1]))
                    self.is_covered = True
                    continue
                pivot = lower + math.floor((upper - lower) / 2)
                backward_tris_blob = []
                backward_tris_blob.append(self.blob)
                backward_tris_blob.extend(triangles[:pivot + 1])
                backward_blob = shapely.union_all(
                    backward_tris_blob)

                if shapely.area(shapely.intersection(backward_blob, self.square)) == self.square_area:
                    upper = pivot
                    continue
                else:
                    lower = pivot
                # elif shapely.area(shapely.intersection(forward_blob, self.square)) == self.square_area:
                    # bot_index = top_index
                    # top_index = top_index + math.ceil(top_index / 2)
            self.number_of_triangles += final_triangle_index + 1
            # loopstop = timer()
            # print(f'Finito, took {loopstop - loopstart} s')

        # If it couldn't be covered by the newly added triangles,
        # increase the number of triangles by the amount that was added
        # and merge the new ones into the old blob
        else:
            self.blob = snapshot_blob
            self.number_of_triangles += NUM_TRIANGLES

    def get_triangles(self):
        while True:
            yield plt.patch.Polygon(self.new_triangle().polygon.exterior.xy, edgecolor='black', facecolor='none')

    def run_simulation(self, index):
        # while not self.are_walls_connected():
        # self.new_triangle()
        number_of_triangles_for_connection = self.number_of_triangles
        while not self.is_covered:
            if not self.blobified:
                self.opdate_area()
            else:
                self.mass_triangle()
        if index % 50 == 0:
            print(f'Simulation #{index} is completed')
        return self.number_of_triangles
        # return number_of_triangles_for_connection, self.number_of_triangles
