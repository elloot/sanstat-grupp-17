import math

import numpy as np
import matplotlib.pyplot as plt

from union_find import UnionFind


b = 2 * math.pi ** (1/2) / 3 ** (1/4)
s = b * 3 ** (1/2) / 2 * (1 + math.sin(math.pi / 6))  # length from centre to vertex
h = s * (1 + math.sin(math.pi / 6))
class Triangle:
  def __init__(self, coordinates, index):
    self.coordinates = coordinates
    self.index = index

    self.vertices = [
      (coordinates[0] - s * math.cos(math.pi / 6), coordinates[1] - s * math.sin(math.pi / 6)),
      (coordinates[0] + s * math.cos(math.pi / 6), coordinates[1] - s * math.sin(math.pi / 6)),
      (coordinates[0], coordinates[1] + s),
    ]


def get_row_col(coordinates):
  (x, y) = coordinates
  if x == 0: x += 1
  if y == 0: y += 1
  return int(np.ceil(x / 2)) - 1, int(np.ceil(x / 2)) - 1


def intersects(triangle1, triangle2):
  x1, y1 = triangle1.coordinates1
  x2, y2 = triangle2.coordinates2
  if np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2) > 2 * s:
    return False

  vs2 = triangle2.vertices
  for v in triangle1.vertices:
    if not vs2[0][1] <= v[1] <= vs2[2][1]:  # if vertex is between top and bottom vertex on other
      return False

    ratio = 1 - (v[1] - vs2[0][1]) / h
    if not ratio * vs2[0][0] <= v[0] <= ratio * vs2[1][0]:  # if vertex is in the width at given height
      return False
  return True

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

  def get_intersecting_triangles(self, triangle):
    return list(filter(
      lambda triangle2: intersects(triangle, triangle2),
      self.get_adjacent_triangles(triangle.coordinates)
    ))

  def get_adjacent_triangles(self, coordinates):
    (row, col) = get_row_col(coordinates)
    row_d = [0, -1, -1, 0, 1, 1, 1, 0, -1]
    col_d = [0, 0, 1, 1, 1, 0, -1, -1, -1]
    adjacent_triangles = []
    for i in range(0, 9):
        if 0 <= row + row_d[i] < self.rows and 0 <= col + col_d[i] < self.cols:
            adjacent_triangles.extend(self.sub_area[row + row_d[i]][col + col_d[i]])
    return adjacent_triangles


class CoverageControllerTriangle:
  def __init__(self, n):
    self.n = n
    self.area = SquareArea(np.sqrt(n))
    self.triangle_unions = UnionFind(2)  # index 0 is for the left wall and 1 for the right wall.
    self.index_tracker = 2
    self.number_of_triangles = 0

  def are_walls_connected(self):
    return self.triangle_unions.is_same_set(0, 1)

  def get_random_coordinates(self):
    return np.random.uniform(0, np.sqrt(self.n)), np.random.uniform(0, np.sqrt(self.n))

  def new_triangle(self):
    triangle = Triangle(self.get_random_coordinates(), self.index_tracker)
    self.index_tracker += 1
    self.triangle_unions.add()
    for triangle2 in self.area.get_intersecting_triangles(triangle):
        self.triangle_unions.union_sets(triangle.index, triangle2.index)
    self.area.add_triangle(triangle)
    
    if triangle.vertices[0][0] <= 0:
        self.triangle_unions.union_sets(0, triangle.index)
    if triangle.vertices[1][0] >= np.sqrt(self.n) - 1:
        self.triangle_unions.union_sets(1, triangle.index)
    
    self.number_of_triangles += 1
    return triangle

  def get_triangles(self):
    while True:
      yield plt.triangle(self.new_triangle().coordinates, 1, edgecolor='black', facecolor='none')

  def run_simulation(self):
    while not self.are_walls_connected():
      self.new_triangle()
    return self.number_of_triangles
