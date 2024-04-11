"""A series of cursor moving commands:

    cursor_up(): Moves the cursor up a given number of lines (Default: 1).
    cursor_down(): Moves the cursor down a given number of lines (Default: 1).
    cursor_left(): Moves the cursor left a given number of lines (Default: 1).
    cursor_right(): Moves the cursor right a given number of lines (Default: 1).

    beginning(): Moves the cursor to the beginning of the current line.

    clear_line_after(): Clear the current line after the cursor.
    clear_line_before(): Clear the current line before the cursor.
    clear_line(): Clear the current line from the beginning.

    clear_screen_after(): Clear the screen after the cursor.
    clear_screen_before(): Clear the screen before the cursor.
    clear_screen(): Clear the entire screen.

    replace_current(): Identical to clear_line() but with a different name.
    replace_previous(): Move the curser to the previous line and clears it to allow overwriting.

    save(): Save the current position of the cursor. Can be loaded again using load().
    load(): Load the previously saved cursor position. Position can be saved with save().

    set_pos(): Set the position of the cursor to specific coordinates.
"""

import time


# Cursor Movement


def cursor_up(num: int = 1):
    """Move the cursor a number of spaces up.

    Args:
        num (int, optional):
            The number of spaces to move.
            Defaults to 1.
    """
    print(f"\033[{num}A", end="")

def cursor_down(num: int = 1):
    """Move the cursor a number of spaces down.

    Args:
        num (int, optional):
            The number of spaces to move.
            Defaults to 1.
    """
    print(f"\033[{num}B", end="")

def cursor_right(num: int = 1):
    """Move the cursor a number of spaces right.

    Args:
        num (int, optional):
            The number of spaces to move.
            Defaults to 1.
    """
    print(f"\033[{num}C", end="")

def cursor_left(num: int = 1):
    """Move the cursor a number of spaces left.

    Args:
        num (int, optional):
            The number of spaces to move.
            Defaults to 1.
    """
    print(f"\033[{num}D", end="")



# Go to line position

def beginning():
    """Move the cursor to the beginning of the current line."""
    print("\r", end="")

def _ending():
    """Move the cursor to the end of the current line.
    Work In Progress, DOES NOT WORK!!!"""
    cursor_down()
    beginning()
    cursor_left()



# Clearing single lines

def clear_line_after():
    """Clear the current line after the cursor."""
    print("\033[K", end="")

def clear_line_before():
    """Clear the current line before the cursor.
    Effectively replaces the preceding text with blank spaces."""
    print("\033[1K", end="")

def clear_line():
    """Clear the current line from the beginning."""
    print("\033[2K", end="")



# Clearing screens

def clear_screen_after():
    """Clear the screen after the cursor."""
    print("\033[J", end="")

def clear_screen_before():
    """Clear the screen before the cursor."""
    print("\033[1J", end="")

def clear_screen():
    """Clear the entire screen."""
    print("\033[2J", end="")



# Prep to replace previous text

def replace_current():
    """Alternative wording to clear_line(). Literally just calls that function.
    Used in preparation to print there again."""
    clear_line()

def replace_previous():
    """Move the cursor back one line and clears it in preparation to print on it again."""
    print("\033[F\033[K", end="")



# Save and load cursor position

def save():
    """Save the current position of the cursor. Can be loaded again using load()."""
    print("\033[s", end="")

def load():
    """Load the previously saved cursor position. Position can be saved with save()."""
    print("\033[u", end="")



# Set cursor position

def set_pos(line: int = 0, column: int = 0):
    """Set the position of the cursor to specific coordinates.

    Args:
        line (int, optional):
            The line or y-axis to set the position of the cursor to.
            Defaults to 0. (The top of the screen)
        column (int, optional): 
            The column or x-axis to set the position of the cursor to.
            Defaults to 0. (The left side of the screen)
    """
    print(f"\033[{line};{column}H", end="")



# Hide and show cursor

def hide():
    """Makes the cursor invisible. Can be undone with show()."""
    print("\033[?25l")

def show():
    """Makes the cursor visible. Inverse of hide()."""
    print("\033[?25h")



# Save and load screen

def load_screen():
    """Restores the screen after it has been wiped by save_screen() and re-saves it.
    This hides anything done between these points.
    """
    print("\033[?47l")
    save_screen()

def save_screen():
    """Saves the screen and clears it. Can be undone by load_screen().
    Anything done between the save and the load will be hidden.
    """
    print("\033[?47h")



# Testing
if __name__ == "__main__":
    print("Hello"*5, end="", flush=True)
    time.sleep(3)
    cursor_left(10)
    print("Hi", end="")
    _ending()
    print("Pizza")
