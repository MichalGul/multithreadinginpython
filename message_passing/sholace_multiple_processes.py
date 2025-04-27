import re
import time
from multiprocessing import Process, Queue


# (45,11),(41,15),(36,20)

PTS_REGEX = "\((\d*),(\d*)\)"
TOTAL_PROCESSES = 4

def find_area(points_queue: Queue):
    points_str  = points_queue.get()

    while points_str is not None: # stop on None
        points = []
        area = 0.0
        for xy in re.finditer(PTS_REGEX, points_str):
            points.append((int(xy.group(1)), int(xy.group(2))))

        for i in range(len(points)):
            a, b = points[i], points[(i + 1) % len(points)]
            area += a[0] * b[1] - a[1] * b[0]
        area = abs(area) / 2.0
        print(area)

        points_str = points_queue.get()


if __name__ == "__main__":
    data_queue = Queue(maxsize=1000)
    processes = []
    for i in range(TOTAL_PROCESSES):
        p = Process(target=find_area, args=(data_queue,))
        processes.append(p)
        p.start()
    f = open("polygons.txt", "r")
    lines = f.read().splitlines()
    start = time.time()

    for line in lines:
        data_queue.put(line)

    # Closing work
    for _ in range(TOTAL_PROCESSES):# need do this 4 time to stop all processes
        data_queue.put(None)

    for p in processes:
        p.join()

    end = time.time()

    print("Time taken", end - start)
