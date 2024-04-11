import threading

class TerminalListener:
    def __init__(self, main_system):
        self.main_system = main_system

        self.input_value = None
        self.input_received = False
        self.lock = threading.Lock()

    def start_listening(self) -> None:
        """Start listening for input in a separate thread."""
        threading.Thread(target=self._listen_for_input).start()

    def _listen_for_input(self) -> None:
        """Listens for user input from the terminal and updates the input value.

        This method runs in a loop until the `run` flag of the `main_system` is set to False.
        """
        while self.main_system.run:
            user_input = input(">> ")
            with self.lock:
                self.input_value = user_input
                self.input_received = True


    def check_for_input(self) -> bool:
        """Check if an input value is available from the terminal listener.

        Returns:
            bool: True if an input value is available, False otherwise.
        """
        with self.lock:
            return self.input_value is not None

    def get_input_value(self) -> str | None:
        """Retrieves the input value from the terminal listener.

        Returns:
            str: The input value from the terminal listener, or None if no input value is available.
        """
        with self.lock:
            if self.check_for_input is None:
                return None

            # Reset the variable to None after retrieving the value.
            value = self.input_value + ""
            self.input_value = None

            return value
