import json
import urllib.request
import time
from collections import Counter
from string import ascii_lowercase

def count_letters(url, frequency: Counter):
    response = urllib.request.urlopen(url)
    txt = str(response.read())

    for l in txt:
        letter = l.lower().strip()
        frequency.update(letter)


def main():
    print()
    frequency = Counter(ascii_lowercase.strip())
    frequency.subtract(ascii_lowercase.strip())
    start = time.time()
    print("Starting to count letters")
    for i in range(1000, 1020):
        count_letters(f"https://www.rfc-editor.org/rfc/rfc{i}.txt", frequency)
    end = time.time()
    print(json.dumps(frequency.most_common(10), indent=4))
    print("Done, time taken", end - start)



main()