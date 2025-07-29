from enum import Enum
from pathlib import Path
from time import perf_counter
from typing import Callable

from processing.GazeRecording import GazeRecording
from processing.GazeStream import GazeStream
from processing.ingester import ingest_csv


class Samples(Enum):
    ONE = "one_fix"
    ARS = "ars_technica"
    BALATRO = "balatro"


def debug_time(func: Callable, message: str | None = None):
    start = perf_counter()
    return_val = func()
    end = perf_counter()
    time = end - start
    print(f"\nTime taken to execute {message or func}: {time:.10f} seconds")
    return return_val


def ingest_sample(name: str) -> GazeRecording:
    current_dir = Path(__file__).parent
    csv_file = current_dir / "tests" / "integration" / "samples" / f"{name}.csv"
    return ingest_csv(csv_file)


def get_sample_image(name: str) -> Path:
    current_dir = Path(__file__).parent
    image_file = (
        current_dir / "tests" / "integration" / "samples" / "images" / f"{name}.png"
    )
    return image_file
