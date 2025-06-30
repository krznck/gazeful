from typing import Sequence

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.patches import Rectangle

from processing.GazeStream import GazeStream
from visualizing.VisualizationStrategy import VisualizationStrategy


class GazePlotStrategy(VisualizationStrategy):
    def __init__(self) -> None:
        self._screen_w, self._screen_h = 1920, 1200  # TODO: make this adjustable
        super().__init__()

    def visualize(self, data: Sequence[GazeStream]) -> tuple[Figure, Axes]:
        xs, ys, sizes, labels = self._unpack(data)

        figure, axes = self._prepare_subplots()

        self._draw_screen_patch(axes)

        axes.plot(xs, ys, linestyle="-", color="blue", linewidth=1, alpha=1)

        axes.scatter(xs, ys, s=sizes, alpha=1, edgecolor="black", facecolor="blue")

        for x, y, label in zip(xs, ys, labels):
            axes.text(
                x,
                y,
                str(label),
                ha="center",
                va="center",
                fontsize=6,
                weight="bold",
                color="white",
            )

        self._set_axes(axes)

        figure.patch.set_alpha(0.0)
        axes.patch.set_alpha(0.0)
        return figure, axes

    def _unpack(
        self, data: Sequence[GazeStream]
    ) -> tuple[list[float], list[float], list[float], list[int]]:
        xs, ys, sizes, labels = [], [], [], []
        for i, point in enumerate(data):
            cords = point.centroid()
            xs.append(cords[0] * self._screen_w)
            ys.append(cords[1] * self._screen_h)
            sizes.append(point.duration() * 500)  # TODO: make adjustable as well
            labels.append(i + 1)

        return xs, ys, sizes, labels

    def _prepare_subplots(self) -> tuple[Figure, Axes]:
        dpi = 100  # TODO: make adjustable
        fig_w, fig_h = self._screen_w / dpi, self._screen_h / dpi
        figure, axes = plt.subplots(figsize=(fig_w / 2, fig_h / 2), dpi=dpi)
        return figure, axes

    def _draw_screen_patch(self, axes: Axes) -> None:
        axes.add_patch(
            Rectangle(
                (0, 0),
                self._screen_w,
                self._screen_h,
                fill=False,
                lw=2,
                edgecolor="gray",
            )
        )

    def _set_axes(self, axes: Axes) -> None:
        axes.set_xlim(0, self._screen_w)
        # NOTE: matplotlib's coordinate system starts at bottom-left, not top-left
        axes.set_ylim(self._screen_h, 0)
        axes.set_aspect("equal", adjustable="box")
        axes.set_xlabel("X")
        axes.set_ylabel("Y")
        axes.set_title(f"Screen Map ({self._screen_w}x{self._screen_h})")
