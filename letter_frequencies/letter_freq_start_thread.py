import json
import urllib.request
import time
from collections import Counter
from string import ascii_lowercase
from threading import Thread, Lock

finished_count = 0

def count_letters(url, frequency: Counter, mutex: Lock):
    response = urllib.request.urlopen(url)
    txt = str(response.read())

    mutex.acquire()

    for l in txt:
        letter = l.lower().strip()
        frequency.update(letter)
    global finished_count
    finished_count += int(1)

    mutex.release()


def main():
    print()
    mutex = Lock()
    frequency = Counter(ascii_lowercase.strip())
    frequency.subtract(ascii_lowercase.strip())
    start = time.time()
    print("Starting to count letters")
    for i in range(1000, 1020):
        th = Thread(target=count_letters, args=(f"https://www.rfc-editor.org/rfc/rfc{i}.txt", frequency, mutex))
        th.start()

    while True:
        mutex.acquire()
        if finished_count == 20:
            break
        mutex.release()
        time.sleep(0.5)
    end = time.time()
    print(json.dumps(frequency.most_common(10), indent=4))
    print("Done, time taken", end - start)



main()