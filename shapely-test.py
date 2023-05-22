import shapely
from shapely.geometry import Point
import numpy as np
import matplotlib.pyplot as plt

n = 1000
num_sim = 100
circle_res = 100

square = shapely.Polygon(
    ((0, 0), (0, np.sqrt(n)), (np.sqrt(n), np.sqrt(n)), (np.sqrt(n), 0)))

# triangle creation
x, y = np.random.uniform(0, np.sqrt(n), size=2)
side = np.sqrt(2 * np.pi / np.sqrt(1.25))
height = np.sqrt((side / 2) ** 2 + side ** 2)
triangle = shapely.Polygon(
    [(x - 0.5 * side, y - 1/3 * height), (x + 0.5 * side, y - 1/3 * height), (x, y + 2/3 * height)])
x, y = triangle.exterior.xy
plt.scatter(x, y)
plt.show()

results = []

# for i in range(num_sim):
# shapes = []
# filled = False
# num_circles = 0
# blob = 0
# while not filled:
# x, y = np.random.uniform(0, np.sqrt(n), size=2)
# circle = Point(x, y).buffer(1, resolution=circle_res)
# shapes.append(circle)
# num_circles += 1
# union = shapely.union_all(shapes)
# if type(union) == shapely.geometry.polygon.Polygon:
# blob = union
# doesn't work correctly since two circles could overlap and create
# a blob, but there could be another circle farther away that then gets
# overwritten by the next line
# shapes = [blob]
# if shapely.area(shapely.intersection(blob, square)) == shapely.area(square):
# filled = True
# results.append(num_circles)


# print(sum(results) / len(results))
