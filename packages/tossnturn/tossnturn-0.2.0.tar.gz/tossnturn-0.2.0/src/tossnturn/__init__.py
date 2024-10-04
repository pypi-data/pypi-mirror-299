from pynput.mouse import Controller
import time

def cli():
    eps = 1
    timeout = 280
    mouse = Controller()
    while True:
        mouse.move(eps,0)
        mouse.move(-eps,0)
        time.sleep(timeout)


