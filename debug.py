"""Diagnostic and debugging utilities for gaze data ingestion."""
from enum import Enum
from pathlib import Path
from time import perf_counter
from typing import Callable

from assets.resources import get_resource_path
from processing.GazeRecording import GazeRecording
from processing.ingester import ingest_csv

SAMPLES_DIR = Path("tests/samples")


class Samples(Enum):
    """Enumeration of available sample gaze data files."""

    ONE = "one_fix"
    ARS = "ars_technica"
    BALATRO = "balatro"


def debug_time(func: Callable, message: str | None = None):
    """Measures and prints the execution time of a function.

    Args:
        func: The callable to measure.
        message: Optional custom message to print with the duration.

    Returns:
        The return value of the executed function.
    """
    start = perf_counter()
    return_val = func()
    end = perf_counter()
    time = end - start
    print(f"\nTime taken to execute {message or func}: {time:.10f} seconds")
    return return_val


def ingest_sample(name: str) -> GazeRecording:
    """Loads a gaze recording from the project's sample directory.

    Args:
        name: Filename of the sample (without extension).

    Returns:
        A GazeRecording instance of the sample data.
    """
    csv_file = get_resource_path(SAMPLES_DIR / f"{name}.csv")
    return ingest_csv(csv_file)


def get_sample_image(name: str) -> Path:
    """Retrieves the path to a sample background image.

    Args:
        name: Filename of the sample image (without extension).

    Returns:
        A Path object pointing to the image.
    """
    image_file = get_resource_path(SAMPLES_DIR / "images" / f"{name}.png")
    return image_file
