import os
import time

fs = os.open("storage.csv", os.O_RDONLY)

time.sleep(10)

os.close(fs)
