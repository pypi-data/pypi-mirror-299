import sys

from pynput.mouse import Controller
import time
from tossnturn.gui import main as gui


def main():
    if len(sys.argv) == 1:
        gui()
    elif sys.argv[1] == "cli":
        cli()
    else:
        raise Exception("Invalid command given")


def cli():
    eps = 1
    timeout = 280
    mouse = Controller()
    while True:
        mouse.move(eps, 0)
        mouse.move(-eps, 0)
        time.sleep(timeout)
