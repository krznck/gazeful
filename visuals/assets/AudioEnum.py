"""Enumeration for application audio resources."""
from enum import Enum
from pathlib import Path

from simpleaudio import WaveObject

PATH = Path(__file__).parent


def _createPath(name: str) -> str:
    """Internal helper to construct absolute paths to audio assets.

    Args:
        name: Filename of the audio asset (without extension).

    Returns:
        Absolute path as a string.
    """
    parent = Path(__file__).parent.parent.parent
    return str(parent / "assets" / "audio" / f"{name}.wav")


class AudioEnum(Enum):
    """Available audio cues in the application."""

    PIP = WaveObject.from_wave_file(_createPath("pip"))
    pass
