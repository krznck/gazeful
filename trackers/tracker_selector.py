"""Utilities for selecting and instantiating different tracker implementations.

This module provides factory functions for creating tracker instances
and selecting the first connected hardware tracker.
"""

from enum import Enum

from recording.Recorder import Recorder
from trackers.MouseTracker import MouseTracker
from trackers.TobiiTracker import TobiiTracker
from trackers.Tracker import Tracker
from visuals.visualizer.GazeVisualizer import GazeVisualizer


class TrackersEnum(Enum):
    """Enumeration of available tracker implementations."""

    TOBII = TobiiTracker
    DUMMY = MouseTracker


DEFAULT: TrackersEnum = TrackersEnum.DUMMY


def create_tracker(
    tracker_type: TrackersEnum | str | None,
    visualizer: GazeVisualizer,
    recorder: Recorder,
) -> Tracker:
    """Factory function for creating tracker instances.

    Args:
        tracker_type: The type of tracker to create.
        visualizer: The gaze visualizer to attach to the tracker.
        recorder: The recorder to attach to the tracker.

    Returns:
        An initialized Tracker instance of the requested type.
    """
    if tracker_type is None:
        tracker_type = DEFAULT

    if isinstance(tracker_type, str):
        tracker_type = TrackersEnum[tracker_type.upper()]

    match tracker_type:
        case TrackersEnum.DUMMY:
            return MouseTracker(visualizer, recorder)
        case TrackersEnum.TOBII:
            return TobiiTracker(visualizer, recorder)


def default_to_first_connected(
    visualizer: GazeVisualizer, recorder: Recorder
) -> Tracker:
    """Selects and creates the first physically connected tracker.

    If no hardware trackers are found, it defaults to the DUMMY (mouse) tracker.

    Args:
        visualizer: The gaze visualizer to attach to the tracker.
        recorder: The recorder to attach to the tracker.

    Returns:
        The first connected Tracker instance, or the default dummy tracker.
    """
    selected = DEFAULT
    for tracker in TrackersEnum:
        if tracker.value.connected():
            selected = tracker
            break

    return create_tracker(selected, visualizer, recorder)
