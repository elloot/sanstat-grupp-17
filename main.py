import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from coverage_controll import CoverageController

np.random.seed(19680801)
n = 100
c = 0

fig = plt.figure(figsize=(7, 5))
ax = fig.add_axes([0.1, 0.1, 0.8, 0.8], frameon=True)
ax.set_title('number of circles = {}'.format(c))
ax.set_xlim(0, np.sqrt(n)), ax.set_xticks([]), ax.set_xlabel(r'$\sqrt{n}$')
ax.set_ylim(0, np.sqrt(n)), ax.set_yticks([]), ax.set_ylabel(r'$\sqrt{n}$', rotation=0, labelpad=10)
ax.set_aspect('equal', adjustable='box')

coverage_controller = CoverageController(n)


def update(frame_number):
    ax.add_patch(coverage_controller.get_circles().__next__())
    if coverage_controller.are_walls_connected():
        animation.pause()
    else:
        ax.set_title('number of circles {}'.format(frame_number))
    return


animation = FuncAnimation(fig, update, interval=1, save_count=100)
plt.show()
