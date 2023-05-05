import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

np.random.seed(19680801)
n = 100
c = 0

fig = plt.figure(figsize=(7, 5))
ax = fig.add_axes([0.1, 0.1, 0.8, 0.8], frameon=True)
ax.set_title('number of circles = {}'.format(c))
ax.set_xlim(0, np.sqrt(n)), ax.set_xticks([]), ax.set_xlabel(r'$\sqrt{n}$')
ax.set_ylim(0, np.sqrt(n)), ax.set_yticks([]), ax.set_ylabel(r'$\sqrt{n}$', rotation=0, labelpad=10)
ax.set_aspect('equal', adjustable='box')


def get_random_coordinates():
    return np.random.uniform(0, np.sqrt(n)), np.random.uniform(0, np.sqrt(n))


def get_circle():
    return plt.Circle(get_random_coordinates(), 1, edgecolor='black', facecolor='none')


def update(frame_number):
    ax.add_patch(get_circle())
    ax.set_title('number of circles {}'.format(frame_number))
    return


animation = FuncAnimation(fig, update, interval=100, save_count=100)
plt.show()
