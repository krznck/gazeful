# Extending Gazeful

The following constitute a guide towards extending Gazeful with new trackers,
visualizations, or assets.

Note that Gazeful may of course be extended with more functionality.

## Adding a New Eye Tracker

Gazeful is meant to be extensible to other screen-based eye trackers.
Currently, Gazeful integrates the Tobii SDK to support devices such as the Tobii
Spark Pro.
In adding new trackers, please ensure new dependencies are added.

1. Implement the [Tracker][trackers.Tracker] interface in a new class
  within [`trackers/`][trackers].
1. Your class must inherit from
  [Tracker][trackers.Tracker] and
  implement the
  `track()`, `stop()`, and the static `connected()` methods.
1. Register your implementation in
  [tracker_selector][trackers.tracker_selector]
  by adding it to
  [TrackersEnum][trackers.tracker_selector.TrackersEnum]
  and updating the `create_tracker` factory function.

## Adding a New Visualization

1. Create a new strategy in
  [`editor/visualization/`](../reference/editor/visualization.md).
  inheriting from
  [VisualizationStrategy][editor.visualization.VisualizationStrategy]
  (or
  [BaseHeatmapVisualizationStrategy][editor.visualization.BaseHeatmapVisualizationStrategy]
  for heatmap variants).
1. Implement the abstract methods: `update()` and `_opacity_updated()`.
1. Register the new strategy in
  [VisualizationKind][editor.visualization.VisualizationKind]
  and
  [generator][editor.visualization.generator].

## Asset Management

Assets are managed through type-safe enums to avoid hardcoded paths throughout
the UI.

- **Icons**:
  Place `.svg` files in
  [`assets/icons/`](https://github.com/krznck/gazeful/tree/main/assets/icons)
  and add them to
  [IconsEnum][visuals.assets.icon_selector.IconsEnum]
  in
  [icon_selector][visuals.assets.icon_selector].
- **Audio**:
  Place `.wav` files in
  [`assets/audio/`](https://github.com/krznck/gazeful/tree/main/assets/audio)
  and add them to
  [AudioEnum][visuals.assets.AudioEnum].
