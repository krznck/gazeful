from typing import Sequence

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.lines import Line2D

from processing.GazeStream import GazeStream
from visualizing.configuration.GazePlotConfiguration import GazePlotConfiguration
from visualizing.VisualizationStrategy import VisualizationStrategy

SCALING_FACTOR = 0.5


class GazePlotStrategy(VisualizationStrategy[GazePlotConfiguration]):
    def __init__(self, configuration: GazePlotConfiguration) -> None:
        super().__init__(configuration)

    def visualize(self, data: Sequence[GazeStream]) -> tuple[Figure, Axes]:
        xs, ys, sizes = self._interpret(data)

        figure, axes = self._prepare_subplots()

        self._draw_background(axes)

        self._draw_lines(axes, xs, ys)

        for i, (x, y, size) in enumerate(zip(xs, ys, sizes)):
            self._draw_point(axes, i, x, y, size)
            self._draw_label(axes, i, x, y, size)

        self._set_axes(axes)
        self._set_legend(axes)

        return figure, axes

    def _draw_background(self, axes: Axes):
        if self.configuration.background_image.value is None:
            return

        sw = self.configuration.screen_width.value
        sh = self.configuration.screen_height.value
        image = plt.imread(self.configuration.background_image.value)
        axes.imshow(image, extent=(0, sw, 0, sh))

    def _prepare_subplots(self) -> tuple[Figure, Axes]:
        figure, axes = plt.subplots(figsize=(10, 8), dpi=150)
        return figure, axes

    def _draw_lines(self, ax: Axes, x_cords: list[float], y_cords: list[float]) -> None:
        # NOTE: Lines not as important as points - looks better with a low zorder
        ax.plot(
            x_cords,
            y_cords,
            linestyle="-",
            color="blue",
            linewidth=1,
            alpha=self.configuration.opaqueness.value,
            zorder=0,
        )

    def _draw_point(self, axes: Axes, number: int, x: float, y: float, size: float):
        axes.plot(
            x,
            y,
            marker="o",
            markersize=(size**SCALING_FACTOR),
            markerfacecolor="blue",
            markeredgecolor="black",
            linestyle="None",
            zorder=number * 2,
            alpha=self.configuration.opaqueness.value,
        )

    def _draw_label(self, axes: Axes, number: int, x: float, y: float, size: float):
        axes.text(
            x,
            y,
            str(number + 1),
            ha="center",
            va="center",
            fontsize=self._calculate_font_size(size),
            weight="bold",
            color="white",
            zorder=number * 2 + 1,
            alpha=self.configuration.opaqueness.value,
        )

    def _calculate_font_size(self, size: float) -> float:
        scaling_factor = 0.4
        min_font_size = 4
        font_size = scaling_factor * (size**SCALING_FACTOR)
        return max(font_size, min_font_size)

    def _interpret(
        self, data: Sequence[GazeStream]
    ) -> tuple[list[float], list[float], list[float]]:
        sw = self.configuration.screen_width.value
        sh = self.configuration.screen_height.value
        xs, ys, sizes = [], [], []
        for stream in data:
            cords = stream.centroid()
            xs.append(cords[0] * sw)

            # NOTE: In matplolib coordinates start from bottom-left instead of top-left,
            # so we need to flip them
            ys.append(sh - cords[1] * sh)

            sizes.append(stream.duration() * self.configuration.size_multiplier.value)

        return xs, ys, sizes

    def _set_axes(self, axes: Axes) -> None:
        sw = self.configuration.screen_width.value
        sh = self.configuration.screen_height.value
        axes.set_xlim(0, sw)
        axes.set_ylim(0, sh)
        axes.set_aspect("equal", adjustable="box")
        axes.set_title(f"Gaze Sequence Map ({sw}x{sh})")

        # coordinate ticks aren't all that relevant for these
        axes.set_xticks([])
        axes.set_yticks([])

    def _set_legend(self, axes: Axes) -> None:
        example_durations = [0.25, 0.5, 0.75]
        size_mult = self.configuration.size_multiplier.value

        legend_elements = [
            Line2D([0], [0], color="blue", lw=1, label="saccade"),
            Line2D(
                [0],
                [0],
                marker="None",
                color="None",
                label="fixation duration:",
                markersize=0,
            ),
        ]

        for duration in example_durations:
            marker_size = (duration * size_mult) ** SCALING_FACTOR
            legend_elements.append(
                Line2D(
                    [0],
                    [0],
                    marker="o",
                    color="black",
                    label=f"{int(duration*1000)} ms",
                    lw=0,
                    markerfacecolor="blue",
                    markeredgecolor="black",
                    markersize=marker_size,
                    linestyle=None,
                )
            )

        axes.legend(
            handles=legend_elements,
            bbox_to_anchor=(1, 1),
            loc="upper left",
            labelspacing=1.6,
            borderpad=1.0,
            fontsize="x-small",
        )
