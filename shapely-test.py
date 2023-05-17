import shapely
from shapely.geometry import Point
import numpy as np

n = 1000
num_sim = 100
circle_res = 100

square = shapely.Polygon(
    ((0, 0), (0, np.sqrt(n)), (np.sqrt(n), np.sqrt(n)), (np.sqrt(n), 0)))


results = []

for i in range(num_sim):
    shapes = []
    filled = False
    num_circles = 0
    blob = 0
    while not filled:
        x, y = np.random.uniform(0, np.sqrt(n), size=2)
        circle = Point(x, y).buffer(1, resolution=circle_res)
        shapes.append(circle)
        num_circles += 1
        union = shapely.union_all(shapes)
        if type(union) == shapely.geometry.polygon.Polygon:
            blob = union
            shapes = [blob]
        if shapely.area(shapely.intersection(blob, square)) == shapely.area(square):
            filled = True
    results.append(num_circles)

print(sum(results) / len(results))
