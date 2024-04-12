"""A collection of personal functions to call.

    text(): print() alternative.
    intext(): input() alternative using text().
    intput(): Integer-specific, error-catching input() alternative using intext().
    floatput(): Float-specific, error-catching input() alternative using intext().
    boolput(): Boolean-specific, error-catching input() alternative using intext().
            Catches a string input and detects if it is positive ('yes') or negative ('no')
    rounder(): round() alternative.
    rand(): random.randrange() alternative using os.urandom().
    rand_choice(): Returns a random item from a given list using rand(). Use of a die is possible.
    die_parser(): Runs roll, but for as string input in the format of '1d4 + 5' or '2d8-2'.
    roll(): Rolls a number of dice and returns the result.
    intvert(): int() alternative but catches failures and optionally returnes a failure value.
    bound(): Combines min() and max() to make sure a value is between an upper and lower bound.
    merge(): Reverses split().
"""
import sys
import os
from time import sleep
import time

# Gets rid of an annoying and irrelevant error message

# pylint: disable=no-member
# pylint: disable=import-error

from Surface_Python.utilities import color
from Surface_Python.utilities import keyboard_input as keybd


# Input / Output


def text(*message: object, unlist_list: bool = True, letter_time: float = 0.0,
         line_delay: float = 0, sep: str = " ", end: str = "\n",
         mods: list = None, flush: bool = True) -> None:
    """Mimic print() but with more functionality and a default time delay.

    Args:
        *message (str, optional):
            A message or prompt to output to the user. NOTE: If a list or tuple is passed in,
            it will print each item in the list or tuple instead of the list or tuple itself.
            Defaults to "".
        unlist_list (bool, optional):
            If True, will print single-item lists and tuples as the contained item instead of the
            list or tuple itself. If False, will print the list or tuple as is.
            Defaults to True.
        letter_time (float, optional):
            Time delay between each letter printed.
            Defaults to 0.0.
        line_delay (int, optional):
            Additional time delay between each line printed.
            Defaults to 0.
        sep (str, optional):
            String inserted between values.
            Defaults to " ".
        end (str, optional):
            String appended after the last value.
            Defaults to "\\n".
        mods (list, optional):
            List of modifiers from the colorizer class to apply to the message.
            Defaults to [].
        flush (bool, optional):
            Determines if the text is output immediately or not.
            Defaults to True.
    """
    # Having a function have a default list is "dangerous" so this serves as an equivalent if None.
    # Otherwise, prints the markup escape codes.
    for modifier in (mods if mods is not None else []):
        print(modifier, end="")

    # Due to anything in the message slot being turned into a tuple, this checks to see if the 1st
    # item is a tuple as that usually indicates that it was passed on from intext() or one of the
    # 'put() functions. It also serves to allow for easy listing of items in a list.
    # Does not run if there's more than one argument, so adding a "" and setting sep to "" would
    # override this if you want to print a list or tuple with a single item.
    if len(message) == 1 and unlist_list:
        if isinstance(message[0], (tuple, list)):
            message = message[0]

    # The speed multiplier. Added fow using esc to speed up outputs.
    speed = 1

    if letter_time != 0:
        # Cycles through and prints each letter with delay.
        for i, item in enumerate(message):

            if i != 0:
                for letter in sep:

                    if keybd.is_currently_pressed("esc"):
                        speed = 0

                    print(letter, end='', flush=flush)
                    sleep(letter_time * speed)
            for letter in str(item):

                if keybd.is_currently_pressed("esc"):
                    speed = 0

                print(letter, end='', flush=flush)
                sleep(letter_time * speed)
    else:
        for i, item in enumerate(message):
            if i != 0:
                print(sep, end='', flush=flush)
            print(item, end='', flush=flush)

    # Cleans up and optionally waits at the end.
    sleep(line_delay * speed)
    print(color.END, end="")
    print(end=end)


def error(*message: object, unlist_list: bool = True, letter_time: float = 0.0, line_delay: float = 0,
          sep: str = " ", end: str = "\n", flush: bool = True) -> None:
    """Same as text but designed for error messages.

    Args:
        *message (str, optional):
            A message or prompt to output to the user.
            Defaults to "".
        unlist_list (bool, optional):
            If True, will print single-item lists and tuples as the contained item instead of the
            list or tuple itself. If False, will print the list or tuple as is.
            Defaults to True.
        letter_time (float, optional):
            Time delay between each letter printed.
            Defaults to 0.0.
        line_delay (int, optional):
            Additional time delay between each line printed.
            Defaults to 0.
        sep (str, optional):
            String inserted between values.
            Defaults to " ".
        end (str, optional):
            String appended after the last value.
            Defaults to "\\n".
        flush (bool, optional):
            Determines if the text is output immediately or not.
            Defaults to True.
    """
    # See the equivalent in text().
    if len(message) == 1:
        if isinstance(message[0], (tuple, list)):
            message = message[0]

    # Passes through the arguments to text() and adds the error modifiers.
    text(message, unlist_list=unlist_list, letter_time=letter_time, line_delay=line_delay,
         sep=sep, end=end, flush=flush, mods=[color.ERROR, color.WARN])


def intext(*message: object, unlist_list: bool = True, letter_time: float = 0.0, line_delay: float = 0,
           sep: str = " ", end: str = " ", mods: list = None) -> str:
    """Mimic input() but use text() instead of print() and add a space at the end for convenience.

    Args:
        *message (str, optional):
            A message or prompt to output to the user.
            Defaults to "".
        unlist_list (bool, optional):
            If True, will print single-item lists and tuples as the contained item instead of the
            list or tuple itself. If False, will print the list or tuple as is.
            Defaults to True.
        letter_time (float, optional):
            Time delay between each letter printed.
            Defaults to 0.0.
        line_delay (int, optional):
            Additional time delay between each line printed.
            Defaults to 0.
        sep (str, optional):
            String inserted between values.
            Defaults to " ".
        end (str, optional):
            String appended after the last value.
            Defaults to "\\n".
        mods (list, optional):
            List of modifiers from the colorizer class to apply to the message.
            Defaults to [].

    Returns:
        str: The string value of the user's input.
    """
    # See the equivalent in text().
    if len(message) == 1:
        if isinstance(message[0], (tuple, list)):
            message = message[0]

    # Passes through the arguments to text() and returns the input.
    text(message, unlist_list=unlist_list, letter_time=letter_time, sep=sep,
         line_delay=line_delay, end=end, mods=mods)
    return input()


def intput(*message: object, unlist_list: bool = True, letter_time: int = 0.0, line_delay: int = 0,
           sep: str = " ", end: str = " ", fail_message: str =
           ("⚠  That's not an integer within acceptable bounds. ⚠  " +
            "Please enter an integer within bounds:"), fail_mods: list = None, mods: list = None,
           auto_bound: bool = False, minimum: int | None = None, maximum: int | None = None) -> int:
    """Get an integer input from the user or loop if invalid.

    Args:
        *message (str, optional):
            A message or prompt to output to the user.
            Defaults to "".
        unlist_list (bool, optional):
            If True, will print single-item lists and tuples as the contained item instead of the
            list or tuple itself. If False, will print the list or tuple as is.
            Defaults to True.
        letter_time (float, optional):
            Time delay between each letter printed.
            Defaults to 0.0.
        line_delay (int, optional):
            Additional time delay between each line printed.
            Defaults to 0.
        sep (str, optional):
            String inserted between values.
            Defaults to " ".
        end (str, optional):
            String appended after the last value.
            Defaults to "\\n".
        mods (list, optional):
            List of modifiers from the colorizer class to apply to the message.
            Defaults to [].
        fail_mods (str, optional):
            The message to give if the original input is invalid.
            Defaults to [color.ERROR]
        fail_message (str, optional):
            The message to give if the original input is invalid.
            Defaults to "That's not an integer. Please enter an integer:"
        auto_bound (bool, optional):
            If True, will automatically bound the input to the given minimum and maximum.
            Defaults to False.
        minimum (int, optional):
            The minimum value the input can be if auto_bound is True.
            Defaults to None.
        maximum (int, optional):
            The maximum value the input can be if auto_bound is True.
            Defaults to None.

    Returns:
        int: The integer value of the user's input within any specified bounds.
    """

    # Having a function have a default list is "dangerous" so this serves as an equivalent if None.
    fail_mods = [color.ERROR] if fail_mods is None else fail_mods

    # Attempts to get an input and loops until it is valid.
    # Changes the message and mods after the 1st attempt.
    msg = message
    while True:
        try:
            num = int(intext(msg, unlist_list=unlist_list, letter_time=letter_time, sep=sep,
                             line_delay=line_delay, end=end, mods=mods))
            if auto_bound:
                return bound(num, minimum, maximum)
            if not (minimum is None or maximum is None):
                if not minimum < num < maximum:
                    raise ValueError
            return num
        except ValueError:
            msg = fail_message if len(fail_message) > 0 else msg
            mods = fail_mods


def floatput(*message: str, unlist_list: bool = True, sep: str = " ", letter_time: float = 0.0,
             line_delay: float = 0, end: str = " ", fail_message: str =
             "⚠  That's not a floating point value within acceptable bounds. ⚠  " +
             "Please enter a floating point value within bounds:",
             fail_mods: list = None, mods: list = None,
             auto_bound: bool = False, minimum: int | None = None,
             maximum: int | None = None) -> float:
    """Get a floating point input from the user or loop if invalid.

    Args:
        *message (str, optional):
            A message or prompt to output to the user.
            Defaults to "".
        unlist_list (bool, optional):
            If True, will print single-item lists and tuples as the contained item instead of the
            list or tuple itself. If False, will print the list or tuple as is.
            Defaults to True.
        letter_time (float, optional):
            Time delay between each letter printed.
            Defaults to 0.0.
        line_delay (int, optional):
            Additional time delay between each line printed.
            Defaults to 0.
        sep (str, optional):
            String inserted between values.
            Defaults to " ".
        end (str, optional):
            String appended after the last value.
            Defaults to "\\n".
        mods (list, optional):
            List of modifiers from the colorizer class to apply to the message.
            Defaults to [].
        fail_message (str, optional):
            The message to give if the original input is invalid.
            Defaults to "That's not a floating point value. Please enter a floating point value:"
        fail_mods (str, optional):
            The message to give if the original input is invalid.
            Defaults to [color.ERROR]
        auto_bound (bool, optional):
            If True, will automatically bound the input to the given minimum and maximum.
            Defaults to False.
        minimum (int, optional):
            The minimum value the input can be if auto_bound is True.
            Defaults to None.
        maximum (int, optional):
            The maximum value the input can be if auto_bound is True.
            Defaults to None.

    Returns:
        float: The floating point value of the user's input within any specified bounds.
    """

    # Having a function have a default list is "dangerous" so this serves as an equivalent if None.
    fail_mods = [color.ERROR] if fail_mods is None else fail_mods

    # Attempts to get an input and loops until it is valid.
    # Changes the message and mods after the 1st attempt.
    msg = message
    while True:
        try:
            num = float(intext(msg, unlist_list=unlist_list, letter_time=letter_time, sep=sep,
                               line_delay=line_delay, end=end, mods=mods))
            if auto_bound:
                return bound(num, minimum, maximum)
            if not (minimum is None or maximum is None):
                if not minimum < num < maximum:
                    raise ValueError
            return num
        except ValueError:
            msg = fail_message if len(fail_message) > 0 else msg
            mods = fail_mods


def boolput(*message: str, unlist_list: bool = True, sep: str = " ", letter_time: float = 0.0,
            line_delay: float = 0, end: str = " ", add_true: list = None,
            add_false: list = None, mods: list = None) -> bool:
    """Get a boolean input from the user.

    Args:
        *message (str, optional):
            A message or prompt to output to the user.
            Defaults to "".
        unlist_list (bool, optional):
            If True, will print single-item lists and tuples as the contained item instead of the
            list or tuple itself. If False, will print the list or tuple as is.
            Defaults to True.
        letter_time (float, optional):
            Time delay between each letter printed.
            Defaults to 0.0.
        line_delay (int, optional):
            Additional time delay between each line printed.
            Defaults to 0.
        sep (str, optional):
            String inserted between values.
            Defaults to " ".
        end (str, optional):
            String appended after the last value.
            Defaults to "\\n".
        mods (list, optional):
            List of modifiers from the colorizer class to apply to the message.
            Defaults to [].
        add_true (list, optional):
            Additional answers to be considered as True.
            Defaults to [].
        add_false (list, optional):
            Additional answers to be considered as False.
            Defaults to [].

    Returns:
        bool: The boolean value of the user's input.
    """

    # Having a function have a default list is "dangerous" so this serves as an equivalent if None.
    if add_true is None:
        add_true = []
    if add_false is None:
        add_false = []

    # I listed every reasonable (and one or two unreasonable) affirmative and negative word I could
    # think of and added the ability to add more.
    positive_answers = (['ok', 'okay', 'yes', 'y', 'sure', '1', 'true', 'affirmative',
                         'alright', 't', 'yeah', 'yup', 'ye', 'yea'] + add_true)
    negative_answers = (['no', 'nope', 'negative', 'nein', '0',
                         'n', 'false', 'nah', 'nay', 'negatory'] + add_false)

    # Gets the response and checks it against both lists.
    # If there are no matches, it simply casts to bool.
    reply = intext(message, unlist_list=unlist_list, letter_time=letter_time, sep=sep,
                   line_delay=line_delay, end=end, mods=mods).lower()

    answer = None
    for i in positive_answers:
        if i in reply:
            answer = True
    for i in negative_answers:
        if i in reply:
            answer = False
    if answer is None:
        answer = bool(reply)

    return answer


# Math


def rounder(num: float) -> int:
    """Round a number better than the default function because default rounds down on .5 sometimes.

    Args:
        num (float):
            The number you wish to round.

    Returns:
        int: The input rounded to the nearest whole number.
    """
    # Truncates then checks if adding .5 is still lower that or equal to the original.
    # If true, outputs the truncated number + 1. Otherwise, passes on the truncated number.
    # Example 1: 1.4 in -> 1 + 0.5 </= 1.5 -> 1 out
    # Example 2: 1.6 in -> 1 + 0.5 <= 1.5 -> 1 + 1 out
    # Example 3: 1.5 in -> 1 + 0.5 <= 1.5 -> 1 + 1 out
    if int(num) + 0.5 <= num:
        return int(num) + 1
    return int(num)


def rand(num1: int, num2: int = None) -> int:
    """Given one value, generates a random number from 0 to num1 - 1.\n
    Given two values, generates a random number from num1 to num2 - 1.

    Args:
        num1 (int):
            If one number given, num1 is the upper limit. If two, it's the lower limit.
        num2 (int, optional):
            Upper limit (if given).
            Defaults to None.

    Returns:
        int: A random number within the given range.
    """
    # Generates a 128-bit number, then depending on the number of inputs,
    # finds a number in the given range.
    random = int.from_bytes(os.urandom(128), sys.byteorder)
    if num2 is None:
        return random % num1
    return random % (num2 - num1) + num1


def rand_choice(options: list, die: str | None = None) -> object | None:
    """Choose a random item from the given list. Use dice if desired.

    Args:
        options (list):
            The list to choose an item from randomly.
        die (str | None, optional):
            The die to use to determine the item chosen. Example: "5d12"

            Warning: Do not use modifiers; They will be overridden.
            It is recommended that the sum of the options is equal to the range of the die roll.
            None may be returned if this is not true and an out-of-bounds option is chosen.
            Defaults to None.

    Returns:
        object: A random choice from the list given.
        None: None if out of bounds of the list (only returned if a die is used).
    """
    # If no die is given:
    if die is None:
        return options[rand(len(options))]

    # Else:
    try:
        return options[die_parser(die, True)]
    except IndexError:
        return None


def die_parser(command: str, option_chooser: bool = False) -> int | None:
    """Run the die roll command and return the result.

    Args:
        command (str):
            The die to be parsed and rolled. Format: '1d4 + 2', '2d8-4', or '3d36'
        option_chooser (bool, optional):
            This is for a specific function. Should not be used.

    Returns:
        int: The result of the rolled die.
    """
    try:
        # Split off the die number and remainder.
        arg1, part2 = command.rsplit("d")

        # Split part2 into a die and mod if the mod exists.
        if "+" in command:
            arg2 = part2.rsplit("+")[0].strip()
            arg3 = part2.rsplit("+")[1].strip()
        elif "-" in command:
            arg2 = part2.rsplit("-")[0].strip()
            arg3 = "-" + part2.rsplit("-")[1].strip()
        else:
            arg2 = part2.strip()
            arg3 = "0"

        number = intvert(arg1, "The number of dice is not a number!") if len(
            arg1) >= 1 else 1
        die = intvert(arg2, "That's no die type!")
        mod = intvert(arg3, "That's no mod!")

        if option_chooser:
            mod = -abs(die)

        result = []
        num = 0
        for _ in range(number):
            result.append(roll(1, die, 0))
            num += result[-1]
        num += mod

        return num

    except ValueError:
        print(f"Pretty sure something in {command} wasn't a number when it should have been... " +
              "Try again?")
        return None


def roll(number=1, die=6, mod=0):
    """Roll a number of any type of dice with any modifier.

    Args:
        number (int, optional):
            Number of dice.
            Defaults to 1.
        die (int, optional):
            Number of sides on the die.
            Defaults to 6.
        mod (int, optional):
            Modifier to add.
            Defaults to 0.

    Returns:
        int: The sum of the rolls.
    """
    num = 0
    for _ in range(number):
        num += rand(0, die) + 1
    return num + mod


def intvert(string: str, fail_message: str = None,
            fail_return: int | None = None, throw: bool = False) -> int:
    """Convert a string to an int and catch any ValueErrors.

    Args:
        string (str):
            The string to convert to an integer.
        fail_message (str, optional):
            The message to output if the conversion fails.
            Defaults to None.
        fail_return (int | None, optional):
            The value to return if the conversion fails.
            Defaults to None.
        throw (bool, optional):
            If true, throws an error upon a failure to convert.
            Defaults to False.

    Returns:
        int: The integer value of the input string.
    """
    try:
        return int(string)
    except ValueError as ex:
        if fail_message is not None:
            text(fail_message)
        if throw:
            raise ex
        return fail_return


def bound(num: int | float, minimum: int | float = 0,
          maximum: int | float = 2_000_000_000) -> int | float:
    """If num is out of bounds, replace it with the nearer bound.

    Args:
        num (int | float):
            The number to check the bounds of.
        minimum (int | float, optional):
            The minimum value of the returned number.
            Defaults to 0.
        maximum (int | float, optional):
            The maximum value of the returned number.
            Defaults to 2_000_000_000.

    Returns:
        int | float: A number within the given or default bounds.
    """
    return min(max(num, minimum), maximum)


def factorial(num: int) -> int:
    """Generate the factorial of a given number. (factorial(5) = 1*2*3*4*5 = 120)

    Args:
        num (int):
            The number to get the factorial of.

    Returns:
        int: The factorial.
    """
    result = 1
    for i in range(1, num):
        result *= i + 1
    return result


# Lists


def merge(message: list, sep: str = " ") -> str:
    """Invert the split function. Merge lines of text into a string with a given seperator.

    Args:
        message (list):
            The list of strings or numbers to merge into a string
        sep (str, optional):
            The seperator to place between the elements of the list.
            Defaults to " ".

    Returns:
        str: The string form of the list with elements seperated by sep.
    """
    output_message = ""
    for i, section in enumerate(message):
        if not i == 0:
            output_message += sep
        output_message += str(section)
    return output_message


def shuffle(array: list, depth: int) -> list:
    """Create a shuffled version of the list.

    Args:
        array (list):
            The list to shuffle.
        depth (int):
            The number of times to move a card.

    Returns:
        list: A scrambled version o f the inputted list.
    """
    second_array = array[:]

    for _ in range(depth):
        item = rand_choice(array)
        second_array.remove(item)
        second_array.append(item)

    return second_array


def pause_nanoseconds(nanoseconds: int) -> None:
    """Sleep for a specified amount of nanoseconds.\n
    NOTE: Kinda sucks, don't use it in important code.

    Args:
        nanoseconds (int):
            The amount of time in billionths of a second to pause.
    """
    start_time = time.monotonic_ns()
    end_time = start_time + bound(nanoseconds)
    while time.monotonic_ns() < end_time:
        pass


# Other


def _tester():
    """Test various modifications or new functions easily.
    Used entirely for prototyping purposes."""

    text(f"{color.WARN} WARNING!!! {color.WARN.strip()}",
         mods=[color.ERROR, color.BOLD])


if __name__ == "__main__":
    _tester()
