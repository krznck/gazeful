# Development Guide

<!--toc:start-->
- [Development Guide](#development-guide)
  - [Recommended Tools](#recommended-tools)
  - [Architecture Overview](#architecture-overview)
  - [Extending Gazeful](#extending-gazeful)
    - [Adding a New Eye Tracker](#adding-a-new-eye-tracker)
    - [Adding a New Visualization](#adding-a-new-visualization)
  - [Asset Management](#asset-management)
  - [Static Typing and Type Annotation](#static-typing-and-type-annotation)
  - [Commit Guidelines](#commit-guidelines)
<!--toc:end-->

The following document outlines recommended practices for contributing to
Gazeful.

## Environment Setup

For installation instructions, refer to
[Getting Started](./README.md#getting-started).

### Development Tools

The following are a list of tools meant to be used when contributing to Gazeful.

- [black](https://pypi.org/project/black/):
  A Python code formatter.

- [isort](https://pypi.org/project/isort/):
  A utility to sort Python imports alphabetically.

- [markdownlint](https://github.com/DavidAnson/markdownlint):
  A style checker and lint tool for Markdown files.

- [pyright](https://github.com/microsoft/pyright):
  A static type checker for Python.

## Architecture Overview

Gazeful follows a **Model-View-Presenter (MVP)** architectural pattern to
separate concerns.

- **Views**:
  Located in [`visuals/pages/`](./visuals/pages/). They inherit from
  [`Page`](./visuals/pages/Page.py) and focus strictly on UI layout and emitting
  signals.

- **Presenters**:
  Located in [`visuals/pages/presenters/`](./visuals/pages/presenters/).
  They inherit from
  [`PagePresenter`](./visuals/pages/presenters/PagePresenter.py) and contain
  the logic, data handling, and communication between the view and the rest of
  the application.

- **AppContext**:
  Located in [`AppContext.py`](./AppContext.py), this class acts as a central
  dependency container and state manager, holding references to the active
  tracker, recorder, and visualizer.

## Data Interchange

Gazeful produces and reads eye-tracked data via `.csv` files in the following
format.
Note that samples of recorded gaze
[can be found here](./tests/samples/).

```csv
#1920x1200
x,y,timestamp
0.2854602783918381,0.15251591056585312,0.0
0.2863858789205551,0.1512339562177658,0.030999999999039574
0.2857642024755478,0.15045832842588425,0.046999999998661224
0.28722967207431793,0.14983608573675156,0.06199999999989814
NA,NA,0.07799999999951979
NA,NA,0.09399999999914144
NA,NA,0.10899999999855936
NA,NA,0.125
0.2894028425216675,0.1486806944012642,0.13999999999941792
0.288333460688591,0.150211863219738,0.15599999999903957
0.28788837790489197,0.1548076942563057,0.17199999999866122
0.28981468081474304,0.15458183735609055,0.18699999999989814
```

The first line should be the resolution of the target screen.
The second line should be the column declaration, `x,y,timestamp`.
Values should be written in floating point format.
When eyes are closed or undetected, the `x` and `y` values should be marked as
`NA`.

### Adding a New Eye Tracker

Gazeful is meant to be extensible to other screen-based eye trackers.
Currently, Gazeful integrates the Tobii SDK to support devices such as the Tobii
Spark Pro.
In adding new trackers, please ensure new dependencies are added.

1. Implement the [`Tracker`](./trackers/Tracker.py) interface in a new class
  within [`trackers/`](./trackers/).
1. Your class must inherit from [`Tracker`](./trackers/Tracker.py) and implement
  the `track()`, `stop()`, and the static `connected()` methods.
1. Register your implementation in
  [`tracker_selector`](./trackers/tracker_selector.py) by adding it
  to `TrackersEnum` and updating the `create_tracker` factory function.

### Adding a New Visualization

1. Create a new strategy in [`editor/visualization/`](./editor/visualization/)
  inheriting from
  [`VisualizationStrategy`](./editor/visualization/VisualizationStrategy.py)
  (or
  [`BaseHeatmapVisualizationStrategy`](./editor/visualization/BaseHeatmapVisualizationStrategy.py)
  for heatmap variants).
1. Implement the abstract methods: `update()` and `_opacity_updated()`.
1. Register the new strategy in
  [`VisualizationKind`](./editor/visualization/VisualizationKind.py) and
  [`generator`](./editor/visualization/generator.py).

## Asset Management

Assets are managed through type-safe enums to avoid hardcoded paths throughout
the UI.

- **Icons**:
  Place `.svg` files in [`assets/icons/`](./assets/icons/) and add
  them to `IconsEnum` in [`icon_selector`](./visuals/assets/icon_selector.py).
- **Audio**:
  Place `.wav` files in [`assets/audio/`](./assets/audio/) and add
  them to [`AudioEnum`](./visuals/assets/AudioEnum.py).

## Static Typing and Type Annotation

The entire codebase is written with heavy use of type annotation, and any
contributions should keep this style.
All code should pass `pyright` checks.

## Commit Guidelines

Commit messages should roughly follow the
[Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/)
specification.
