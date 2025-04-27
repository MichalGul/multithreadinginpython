import time
from threading import Thread, Lock


class StingySpendy:
    money = 100
    mutex = Lock()

    def stingy(self):
        for i in range(1000000):
            self.mutex.acquire()
            self.money += int(10) # change in python to += operator optcode somehow make it thread safe?? https://stackoverflow.com/questions/69993959/python-threads-difference-for-3-10-and-others
            self.mutex.release()
        print("Stingy Done")

    def spendy(self):
        for i in range(1000000):
            with self.mutex:
                self.money -= int(10)
        print("Spendy Done")


ss = StingySpendy()
Thread(target=ss.stingy, args=()).start()
Thread(target=ss.spendy, args=()).start()

time.sleep(5)
print("Money in the end", ss.money)