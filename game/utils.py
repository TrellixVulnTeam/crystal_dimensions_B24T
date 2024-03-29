#!/bin/python3
# Code by Nathaniel Ashford
# Date: 22 September 2019
# RPG game design by Rudy Ashford

import sys
import os
import time

clear = lambda: os.system("clear")


def spinning_cursor(timeout):
    # Spinning cursor
    timeout_start = time.time()
    while time.time() < timeout_start + timeout:
        for cursor in "\\|/-":
            time.sleep(0.1)
            # Use '\r' to move cursor back to line beginning
            # Or use '\b' to erase the last character
            sys.stdout.write("\r{}".format(cursor))
            # Force Python to write data into terminal.
            sys.stdout.flush()


def progress_bar():
    # Progress bar
    for i in range(100):
        time.sleep(0.1)
        sys.stdout.write("\r{:02d}: {}".format(i, "#" * (i / 2)))
        sys.stdout.flush()


def chunks(l, n):
    # break a list into chunks of n size:
    # For item i in a range that is a length of l,
    for i in range(0, len(l), n):
        # Create an index range for l of n items:
        yield l[i : i + n]
