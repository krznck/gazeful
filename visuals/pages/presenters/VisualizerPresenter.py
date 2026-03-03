"""Presenter for the Visualizer page, managing animations and opacity settings."""
from AppContext import AppContext

from visuals.pages.presenters.PagePresenter import PagePresenter
from visuals.pages.VisualizerPage import VisualizerPage


class VisualizerPresenter(PagePresenter[VisualizerPage]):
    """Presenter managing the configuration of the real-time gaze visualizer."""

    def __init__(self, view: VisualizerPage, context: AppContext) -> None:
        """Initializes the visualizer presenter.

        Args:
            view: The VisualizerPage view.
            context: The application context.
        """
        super().__init__(view, context)
        self._connect_signals()

    def _connect_signals(self) -> None:
        """Connects signals from the view's widgets to the presenter's slots."""
        v = self._view
        v.animation_toggle.clicked.connect(self._on_animation_toggle_click)
        v.opacity_slider.valueChanged.connect(self._on_opacity_slider_value_changed)

    def _on_animation_toggle_click(self) -> None:
        """Slot triggered to enable/disable visualizer animations."""
        v, c = self._view, self._context

        on = v.animation_toggle.isChecked()
        text = "Animations: On" if on else "Animations: Off"
        v.animation_toggle.setText(text)
        c.visualizer.toggle_animations(on)

    def _on_opacity_slider_value_changed(self) -> None:
        """Slot triggered when the visualizer opacity slider is moved."""
        v, c = self._view, self._context
        c.visualizer.set_opacity(v.opacity_slider.value())
