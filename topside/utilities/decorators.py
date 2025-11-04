from time import time_ns
from typing import Callable


def exec_time(func: Callable) -> Callable:
    """Decorator to measure the execution time of a function.

    Args:
        func (Callable): The function to measure.

    Returns:
        Callable: The wrapped function.
    """
    def wrapper(*args, **kwargs):
        start_time = time_ns()
        result = func(*args, **kwargs)
        end_time = time_ns()
        print(f"{func.__name__} took {end_time - start_time} ns to run.")
        return result
    return wrapper
