from AppContext import AppContext
from visuals.pages.VisualizerPage import VisualizerPage
from visuals.pages.presenters.PagePresenter import PagePresenter


class VisualizerPresenter(PagePresenter[VisualizerPage]):
    def __init__(self, view: VisualizerPage, context: AppContext) -> None:
        super().__init__(view, context)
        self._connect_signals()

    def _connect_signals(self) -> None:
        v = self._view
        v.animation_toggle.clicked.connect(self._on_animation_toggle_click)
        v.opacity_slider.valueChanged.connect(self._on_opacity_slider_value_changed)

    def _on_animation_toggle_click(self) -> None:
        v, c = self._view, self._context

        on = v.animation_toggle.isChecked()
        text = "Animations: On" if on else "Animations: Off"
        v.animation_toggle.setText(text)
        c.visualizer.toggle_animations(on)

    def _on_opacity_slider_value_changed(self) -> None:
        v, c = self._view, self._context
        c.visualizer.set_opacity(v.opacity_slider.value())
