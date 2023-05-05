import numpy as np
import matplotlib.pyplot as plt


class CoverageController:
    def __init__(self, n):
        self.n = n

    def get_random_coordinates(self):
        return np.random.uniform(0, np.sqrt(self.n)), np.random.uniform(0, np.sqrt(self.n))

    def get_circles(self):
        while True:
            yield plt.Circle(self.get_random_coordinates(), 1, edgecolor='black', facecolor='none')
