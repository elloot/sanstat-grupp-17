from timeit import default_timer as timer

if __name__ == '__main__':
    import multiprocessing as mp
    from coverage_controll_triangle_3 import CoverageControllerTriangle

    cc = CoverageControllerTriangle(10000)

    pool = mp.Pool(mp.cpu_count() - 1)

    start = timer()

    result = pool.map(cc.run_simulation, [i for i in range(1, 1000 + 1)])

    pool.close()

    stop = timer()

    print(f'{sum(result) / len(result)}, took {round(stop - start)} s')
