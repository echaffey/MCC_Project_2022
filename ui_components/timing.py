import time
import sys


class Timer:
    ''' Timer makes current thread sleep until specified Hz is reached. 
        If time is already over the Timer does nothing or prints a 
        warning if specified '''

    def __init__(self, hz, warnings=False):
        self.hz = hz
        self.wait_time = 1 / self.hz
        self.last_time = time.time()
        self.warnings = warnings

    def wait(self):
        spend_time = time.time() - self.last_time
        sleep_time = self.wait_time - spend_time

        if sleep_time < 0:
            if self.warnings:
                sys.stderr.write(
                    f'Warning: Timer delay of {round(-sleep_time, 4)} secs\n'
                )
        else:
            time.sleep(sleep_time)

        self.last_time = time.time()
