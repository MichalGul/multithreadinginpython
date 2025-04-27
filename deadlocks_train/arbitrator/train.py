import random
import threading

import time

from model import Intersection

controller = threading.Condition()

def all_free(intersections_to_lock)-> bool:
    """
    return true if all intersections are ready to be used
    """
    for it in intersections_to_lock:
        if it.locked_by >= 0:
            return False

    return True




def lock_intersections_in_distance(id, reserve_start, reserve_end, crossings):
    intersections_to_lock = []
    for crossing in crossings:
        if reserve_end >= crossing.position >= reserve_start and crossing.intersection.locked_by != id:
            intersections_to_lock.append(crossing.intersection)

    # use arbitrator
    controller.acquire()

    while not all_free(intersections_to_lock):
        controller.wait() # wait for all intersections to be free Thread will wait here for notify :)


    for intersection in intersections_to_lock:
        intersection.locked_by = id
        time.sleep(0.01)

    controller.release()


def move_train(train, distance, crossings):
    while train.front < distance:
        train.front += 1
        for crossing in crossings:
            if train.front == crossing.position:
                lock_intersections_in_distance(train.uid, crossing.position, crossing.position + train.train_length, crossings)
            back = train.front - train.train_length
            if back == crossing.position:
                controller.acquire()
                crossing.intersection.locked_by = -1
                # notify waiting trains (threads)
                controller.notify_all()
                controller.release() # release usage of arbitrator
        time.sleep(0.01)
