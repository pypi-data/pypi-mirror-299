import sys
from time import sleep

from tqdm import tqdm


def timer() -> None:
    """A simple timer function that uses tqdm to display a progress bar."""

    user_input = sys.argv[1] if len(sys.argv) > 1 else input("Enter the number of seconds: ")
    try:
        seconds = float(user_input)
    except ValueError:
        print("Invalid input. Please enter a number.")
        return

    for _ in tqdm(range(1000), desc="Remaining time", unit="ms"):
        sleep(seconds / 1000.0)


if __name__ == "__main__":
    timer()
