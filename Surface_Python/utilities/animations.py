"""Generates animations such as a loading bar."""

# These get rid of annoying errors that usually mean nothing.
# Remove non-import related ones if seriously struggling

# pylint: disable=unused-import
# pylint: disable=unused-wildcard-import
# pylint: disable=wildcard-import
# pylint: disable=unexpected-keyword-arg
# pylint: disable=no-member
# pylint: disable=ungrouped-imports
# pylint: disable=undefined-variable


from Surface_Python.utilities import cursor
from Surface_Python.utilities.personal_functions import *


# def loading1(time: int = 5, message: str = "Loading:", container: str = "[ ]", length: int = 50,
#              text_colors: list | None = None, empty_symbol: str = "-", loaded_symbol: str = "#"):

#     text(message, container.split()[0], empty_symbol * length,
#          container.split()[1], mods=text_colors)

#     beginning = message + " " + container.split()[0]
#     ending = container.split()[1]
#     delta = time / length

#     for i in range(length + 1):
#         sleep(delta)
#         cursor.replace_previous()
#         text(beginning, (loaded_symbol * i) + (empty_symbol * (length - i)), ending,
#              letter_time=0, mods=text_colors)


# def loading2(time: int = 5, message: str = "Loading:", container: str = "[ ]", length: int = 50,
#              message_mods: list | None = None, bar_mods: list | None = None,
#              container_mods: list | None = None, empty_symbol: str = "-",
#              loaded_symbol: str = "#"):

#     beginning = container.split()[0]
#     start = len(message + beginning) + 2
#     ending = container.split()[1]
#     delta = time / length

#     text(message, mods=message_mods, end=" ")
#     text(beginning, mods=container_mods, end=" ")
#     text((empty_symbol * length), mods=bar_mods, end=" ")
#     text(ending, mods=container_mods, end="")

#     cursor.hide()
#     cursor.cursor_up()
#     cursor.beginning()
#     cursor.cursor_right(start)

#     for _ in range(length):
#         sleep(delta)
#         text(loaded_symbol, letter_time=0, mods=bar_mods, end="")

#     cursor.show()


def loading_v3(loading_time: int = 5, message: str = "Loading:",
               container: str = "[ ]", length: int = 50,
               message_mods: list | None = None, bar_mods: list | None = None,
               percent_mods: list | None = None, container_mods: list | None = None,
               empty_symbol: str = "-", loaded_symbol: str = "#", percent: bool = True):
    """Generate a loading bar that counts up dynamically with an optional percentage.

    Args:
        loading_time (int, optional):
            Amount of time in seconds to "load" for.
            Defaults to 5.
        message (str, optional):
            The "message", "Loading:" for example, to show in front of the percent or bar.
            Defaults to "Loading:".
        container (str, optional):
            The opening and closing brackets or symbols surrounding the bar. Split by a space.
            Defaults to "[ ]".
        length (int, optional): 
            The length of the bar.
            Defaults to 50.
        message_mods (list | None, optional):
            The color mods for the message text.
            Defaults to None.
        bar_mods (list | None, optional):
            The color mods for the bar.
            Defaults to None.
        percent_mods (list | None, optional):
            The color mods for the percentage.
            Defaults to None.
        container_mods (list | None, optional):
            The color mods for the bar container.
            Defaults to None.
        empty_symbol (str, optional):
            The symbol used to represent the unloaded part of the bar.
            Defaults to "-".
        loaded_symbol (str, optional):
            The symbol used to represent the loaded part of the bar.
            Defaults to "#".
        percent (bool, optional):
            Determines if the percentage is shown.
            Defaults to True.
    """

    beginning = container.split()[0]
    if percent:
        start = len(message + beginning) + 3 + 4
    else:
        start = len(message + beginning) + 2
    ending = container.split()[1]
    delta = loading_time / length

    text(message, mods=message_mods, end=" ")
    if percent:
        text("  0%", mods=percent_mods, end=" ")
    text(beginning, mods=container_mods, end=" ")
    text((empty_symbol * length), mods=bar_mods, end=" ")
    text(ending, mods=container_mods, end="\r")

    cursor.hide()
    cursor.cursor_up()

    for i in range(length):
        sleep(delta)

        if keybd.is_currently_pressed("esc"):
            cursor.cursor_down()
            cursor.beginning()
            break

        if percent:
            cursor.cursor_right(len(message) + 1)

            if len(str(int(((i + 1) / length) * 100))) == 1:
                text("  ", end="", letter_time=0)

            elif len(str(int(((i + 1) / length) * 100))) == 2:
                text(" ", end="", letter_time=0)

            text(rounder(((i + 1) / length) * 100),
                 letter_time=0, mods=percent_mods, end="\r")

        cursor.cursor_right(start)

        text(loaded_symbol * (i + 1), letter_time=0, mods=bar_mods, end="\r")

    cursor.show()


def drop_down(image: list, colors: dict, drop_time: int = 5,
              bottom_y: int = 20, symbol: str | None = None) -> None:
    """Drop down a text-art image from the top of the screen.

    Args:
        image (list):
            The list of lines of text to print.
        colors (dict):
            The dictionary of the colors to make each of the symbols in the image.
        drop_time (int, optional):
            The time to spend on the animation.
            Defaults to 5.
        bottom_y (int, optional):
            The distance from the top of the screen at which the image stops dropping.
            Defaults to 20.
        symbol (str | None, optional):
            The symbol to translate all non-blank symbols to.
            Defaults to None.
    """
    cursor.hide()
    cursor.clear_screen()
    colors[" "] = color.DEFAULT_COLOR

    for i in range(bottom_y):
        cursor.set_pos(0, 0)
        cursor.clear_screen()

        if keybd.is_currently_pressed("esc"):
            cursor.cursor_down()
            cursor.beginning()
            break

        for j in range(i, 0, -1):

            if j <= len(image):
                cursor.clear_line()
                line = image[-j]

                for piece in line:

                    if piece == " ":
                        text(piece, end="", letter_time=0, flush=False)
                    else:
                        if symbol is None:
                            text(piece, mods=[colors[piece]], end="", letter_time=0, flush=False)
                        else:
                            text(symbol, mods=[colors[piece]], end="", letter_time=0, flush=False)
                cursor.cursor_down()
                cursor.beginning()
            else:
                if j == len(image) + 1:
                    cursor.clear_line()
                cursor.cursor_down()

        text("", end="", flush=True)
        sleep(drop_time / bottom_y)
    cursor.show()


if __name__ == "__main__":
    logo = [
        "##########  --------  __________  ======    ......    //////  ",
        "    ##      --            __      ==    ==    ..    //        ",
        "    ##      ----          __      ======      ..      //////  ",
        "    ##      --            __      ==  ==      ..            //",
        "    ##      --------      __      ==    ==  ......    //////  "
    ]

    symbol_colors = {
        "#": color.GREEN,
        "-": color.RED,
        "_": color.ERROR,
        "=": color.BLUE,
        ".": color.YELLOW,
        "/": color.CYAN
    }

    drop_down(logo, symbol_colors, 5, 20, "█")
