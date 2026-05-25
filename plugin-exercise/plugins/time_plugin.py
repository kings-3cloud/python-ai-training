NAME = "Current Time Plugin"

import datetime


def run():
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"Current date and time: {now}")
