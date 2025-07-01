from typing import Sequence

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.patches import Rectangle

from processing.GazeStream import GazeStream
from visualizing.configuration.GazePlotConfiguration import GazePlotConfiguration
from visualizing.VisualizationStrategy import VisualizationStrategy


class GazePlotStrategy(VisualizationStrategy[GazePlotConfiguration]):
    def __init__(self, configuration: GazePlotConfiguration) -> None:
        super().__init__(configuration)

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

        return figure, axes

    def _unpack(
        self, data: Sequence[GazeStream]
    ) -> tuple[list[float], list[float], list[float], list[int]]:
        sw = self.configuration.screen_width.value
        sh = self.configuration.screen_height.value
        xs, ys, sizes, labels = [], [], [], []
        for i, point in enumerate(data):
            cords = point.centroid()
            xs.append(cords[0] * sw)

            # NOTE: In matplolib coordinates start from bottom-left instead of top-left,
            # so we need to flip them
            ys.append(sh - cords[1] * sh)

            sizes.append(point.duration() * self.configuration.size_multiplier.value)
            labels.append(i + 1)

        return xs, ys, sizes, labels

    def _prepare_subplots(self) -> tuple[Figure, Axes]:
        sw = self.configuration.screen_width.value
        sh = self.configuration.screen_height.value
        dpi = 100  # TODO: make adjustable
        fig_w, fig_h = (
            sw / dpi,
            sh / dpi,
        )
        figure, axes = plt.subplots(figsize=(fig_w / 2, fig_h / 2), dpi=dpi)
        return figure, axes

    def _draw_screen_patch(self, axes: Axes) -> None:
        sw = self.configuration.screen_width.value
        sh = self.configuration.screen_height.value
        axes.add_patch(
            Rectangle(
                (0, 0),
                sw,
                sh,
                fill=False,
                lw=2,
                edgecolor="gray",
            )
        )

    def _set_axes(self, axes: Axes) -> None:
        sw = self.configuration.screen_width.value
        sh = self.configuration.screen_height.value
        axes.set_xlim(0, sw)
        axes.set_ylim(0, sh)
        axes.set_aspect("equal", adjustable="box")
        axes.set_xlabel("X")
        axes.set_ylabel("Y")
        axes.set_title(f"Screen Map ({sw}x{sh})")
