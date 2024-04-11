import sys
from time import sleep


for i in range(10):
    print("Hello, world!")
    sleep(.5)


def clear_input_buffer():
    try:
        # For Windows platform
        import msvcrt
        while msvcrt.kbhit():
            msvcrt.getch()
    except ImportError:
        # For Linux/Unix
        import termios
        termios.tcflush(sys.stdin, termios.TCIOFLUSH)


# Call the function to clear the input buffer
clear_input_buffer()

# Print a success message
print("Input buffer cleared.")

input("Press Enter to continue...")