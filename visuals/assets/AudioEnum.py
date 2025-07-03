from enum import Enum
from pathlib import Path

from simpleaudio import WaveObject

PATH = Path(__file__).parent


def _createPath(name: str) -> str:
    parent = Path(__file__).parent.parent.parent
    return str(parent / "assets" / "audio" / f"{name}.wav")


class AudioEnum(Enum):
    PIP = WaveObject.from_wave_file(_createPath("pip"))
    pass
