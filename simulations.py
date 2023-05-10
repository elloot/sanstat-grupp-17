import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from coverage_controll import CoverageController


def show_coverage(n):
    fig = plt.figure(figsize=(7, 5))
    ax = fig.add_axes([0.1, 0.1, 0.8, 0.8], frameon=True)
    ax.set_title('number of circles = {}'.format(0))
    ax.set_xlim(0, np.sqrt(n)), ax.set_xticks([]), ax.set_xlabel(r'$\sqrt{n}$')
    ax.set_ylim(0, np.sqrt(n)), ax.set_yticks([]), ax.set_ylabel(r'$\sqrt{n}$', rotation=0, labelpad=10)
    ax.set_aspect('equal', adjustable='box')

    coverage_controller = CoverageController(n)

    def update(frame_number):
        if coverage_controller.are_walls_connected():
            anim.event_source.stop()
        else:
            ax.set_title('number of circles = {}'.format(coverage_controller.number_of_circles))
        yield ax.add_patch(coverage_controller.get_circles().__next__())

    anim = FuncAnimation(fig, update, interval=1, save_count=100, blit=True)
    plt.show()


def test_frequencies(n, simulations):
    results = []
    for i in range(0, simulations):
        coverage_controller = CoverageController(n)
        results.append(coverage_controller.run_simulation())

    fig = plt.figure(figsize=(7, 5))
    ax = fig.add_axes([0.1, 0.1, 0.8, 0.8], frameon=True)
    ax.set_title("n = {}, {} simulations".format(n, simulations))
    ax.set_xlabel("#circles required for connecting the walls")
    ax.set_ylabel("frequencies")
    ax.hist(results)
    plt.show()
