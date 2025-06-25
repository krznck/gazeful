from time import perf_counter
from typing import Callable


def debug_time(func: Callable):
    start = perf_counter()
    return_val = func()
    end = perf_counter()
    time = end - start
    print(f"Time taken to execute {func}: {time:.10f} seconds")
    return return_val
