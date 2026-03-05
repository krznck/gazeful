"""Enumeration for application audio resources."""
from enum import Enum
from pathlib import Path

from simpleaudio import WaveObject

from assets.resources import get_resource_path

AUDIO_DIR = Path("assets/audio")


def _createPath(name: str) -> str:
    """Internal helper to construct absolute paths to audio assets.

    Args:
        name: Filename of the audio asset (without extension).

    Returns:
        Absolute path as a string.
    """
    path = get_resource_path(AUDIO_DIR / f"{name}.wav")
    return str(path)


class AudioEnum(Enum):
    """Available audio cues in the application."""

    PIP = WaveObject.from_wave_file(_createPath("pip"))
