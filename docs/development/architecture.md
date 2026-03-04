# Architecture Overview

Gazeful follows a **Model-View-Presenter (MVP)** architectural pattern to
separate concerns.

- **Views**:
  Located in [`visuals/pages/`](../reference/visuals/pages.md).
  They inherit from `Page` and focus strictly on UI layout and emitting signals.

- **Presenters**:
  Located in [`visuals/pages/presenters/`](../reference/visuals/presenters.md).
  They inherit from `PagePresenter` and contain the logic, data handling, and
  communication between the view and the rest of the application.

- **AppContext**:
  Located in [`AppContext.py`](../reference/main.md), this class acts as a
  central dependency container and state manager, holding references to the
  active tracker, recorder, and visualizer.
