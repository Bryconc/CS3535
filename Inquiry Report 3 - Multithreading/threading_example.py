__author__ = 'Brycon'

import threading
import time

class PrintThread(threading.Thread):
    def __init__(self, message, count, timeout):
        threading.Thread.__init__(self)
        self.message = message
        self.count_end = count
        self.count = 0
        self.timeout = timeout
        self.timer = 0

    def run(self):
        while self.count < self.count_end:
            if self.timer > 0:
                time.sleep(1)
                self.timer -= 1
            else:
                print(self.message)
                self.count += 1
                if self.count < self.count_end:
                    print("Waiting %d seconds" % self.timeout)
                self.timer = self.timeout
        else:
            print("%s finished execution." % self.getName())


def main():
    thread_one = PrintThread("Printing from Thread 1", 7, 3)
    thread_two = PrintThread("Printing from Thread 2", 3, 7)
    thread_one.setName("Thread 1")
    thread_two.setName("Thread 2")
    thread_one.start()
    thread_two.start()

if __name__ == "__main__":
    main()