from pathlib import Path
from time import perf_counter
from typing import Callable

from processing.ingester import ingest_csv
from trackers.GazePoint import GazePoint


def debug_time(func: Callable):
    start = perf_counter()
    return_val = func()
    end = perf_counter()
    time = end - start
    print(f"Time taken to execute {func}: {time:.10f} seconds")
    return return_val


def ingest_sample(name: str) -> list[GazePoint]:
    current_dir = Path(__file__).parent
    csv_file = current_dir / "tests" / "integration" / "samples" / f"{name}.csv"
    return ingest_csv(csv_file)
