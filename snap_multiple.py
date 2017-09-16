from snap import snap
from time import sleep


LOOP_COUNT = 5
SLEEP_TIME = 1


def run_loop():
    """
    Run image loop and sleep.
    :return:
    """
    sleep(SLEEP_TIME)
    snap()


def run_loops():
    """
    Run multiple snaps.
    :return:
    """
    for x in range(0, LOOP_COUNT):
        run_loop()

if __name__ == '__main__':
    run_loops()
