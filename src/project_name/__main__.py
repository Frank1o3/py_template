import sys
import time


def noice_print(text: str, term_line: int = 1, duration: float = 1.0) -> None:
    """Nice typing print in the terminal

    Args:
        text (str): the string you want to print
        term_line (int, optional): the line the text will get printed at. Defaults to 1.
        duration (float, optional): the duration the writing animation will take. Defaults to 1.0.
    """
    delay = duration / max(len(text), 1)

    # Move cursor to the target line, column 0, clear it
    sys.stdout.write(f"\033[{term_line};0H\033[2K")
    sys.stdout.flush()

    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)


def main() -> None:
    # Clear screen and hide cursor before animating
    sys.stdout.write("\033[2J\033[?25l")
    sys.stdout.flush()

    try:
        noice_print("This is a Template!", term_line=1, duration=1.0)
        noice_print("Made by Frank1o3...", term_line=2, duration=1.0)
        noice_print("Comes with niche updates/fixes..", term_line=3, duration=1.0)

        # Move cursor below the last line when done
        sys.stdout.write("\033[4;0H")
        sys.stdout.flush()
    finally:
        # Always restore cursor even if interrupted
        sys.stdout.write("\033[?25h")
        sys.stdout.flush()


if __name__ == "__main__":
    main()
