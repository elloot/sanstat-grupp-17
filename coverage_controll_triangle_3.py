import numpy as np
import shapely
import math

import warnings
warnings.filterwarnings('error')

SIDE = np.sqrt(2 * np.pi / np.sqrt(1.25))
HEIGHT = np.sqrt((SIDE / 2) ** 2 + SIDE ** 2)

NUM_TRIANGLES = 1000


class Triangle:
    def __init__(self, coordinates):
        self.coordinates = coordinates
        x, y = coordinates
        self.polygon = shapely.Polygon(
            [(x - 0.5 * SIDE, y - 1 / 3 * HEIGHT), (x + 0.5 * SIDE, y - 1 / 3 * HEIGHT), (x, y + 2 / 3 * HEIGHT)])


class CoverageControllerTriangle:
    def __init__(self, n):
        self.n = n
        self.number_of_triangles = 0
        self.blob = 0
        self.square = shapely.Polygon(
            ((0, 0), (0, np.sqrt(n)), (np.sqrt(n), np.sqrt(n)), (np.sqrt(n), 0)))
        self.square_area = shapely.area(self.square)
        self.is_covered = False
        self.triangles = []
        self.errored = False

    # def opdate_area(self):
        # triangles = self.gen_triangles(NUM_TRIANGLES)
        # self.triangles.extend(triangles)
        # union = shapely.union_all(self.triangles)
        # if type(union) == shapely.geometry.polygon.Polygon:
        # self.blob = union
        # self.blobified = True

    def gen_triangles(self, num):
        coords = np.random.uniform(0, np.sqrt(self.n), (num, 2))
        triangles = []
        for x, y in coords:
            triangles.append(Triangle((x, y)).polygon)
        return triangles

    def mass_triangle(self):
        triangles = self.gen_triangles(NUM_TRIANGLES)

        if self.blob == 0:
            self.triangles.extend(triangles)
            # try:
            union = shapely.union_all(self.triangles)
            # except RuntimeWarning:
            # print(self.blob)
            # print(self.triangles)
            if type(union) == shapely.geometry.polygon.Polygon:
                self.blob = shapely.intersection(union, self.square)
            else:
                return

        tris_and_blob = []
        tris_and_blob.append(self.blob)
        tris_and_blob.extend(triangles)
        # snapshot_blob = 0
        # try:
        snapshot_blob = shapely.union_all(tris_and_blob)
        # except RuntimeWarning:
        # f = open(f'error_log_{round(np.random.uniform(1, 20))}', 'x')
        # errorstring = f'BLOB: \n\n {self.blob}\n\n TRIANGLES: \n\n {triangles}\n\n tris and blob: \n\n {tris_and_blob}'
        # f.write(errorstring)
        # f.close()
        # print(f'Length triangles {len(triangles)}')
        # print(f'Length self.triangles {len(self.triangles)}')

        # If square can be covered by the newly added triangles,
        # find the precise number of triangles that needed to be added
        # for coverage
        if shapely.area(shapely.intersection(snapshot_blob, self.square)) == self.square_area:
            final_triangle_found = False
            final_triangle_index = 0
            lower = 0
            upper = len(triangles) - 1
            pivot = math.nan
            # Binary search for finding the amount of triangles that
            # needed to be added for coverage
            while not final_triangle_found:
                if upper - lower == 1:
                    final_triangle_found = True
                    final_triangle_index = upper
                    self.is_covered = True
                    continue
                pivot = lower + math.floor((upper - lower) / 2)
                backward_tris_blob = []
                backward_tris_blob.append(self.blob)
                backward_tris_blob.extend(triangles[:pivot + 1])
                backward_blob = 0
                try:
                    backward_blob = shapely.union_all(
                        backward_tris_blob)
                except RuntimeWarning:
                    print('ass')

                if shapely.area(shapely.intersection(backward_blob, self.square)) == self.square_area:
                    upper = pivot
                    continue
                else:
                    lower = pivot
            self.number_of_triangles += final_triangle_index + 1

        # If it couldn't be covered by the newly added triangles,
        # increase the number of triangles by the amount that was added
        # and merge the new ones into the old blob
        else:
            self.blob = snapshot_blob
            self.number_of_triangles += NUM_TRIANGLES

    def run_simulation(self, index):
        while not self.is_covered:
            self.mass_triangle()
            if self.errored:
                print('fuck')
        if index % 50 == 0:
            print(f'Simulation #{index} is completed')
        return self.number_of_triangles
