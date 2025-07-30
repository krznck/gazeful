from Ref import Ref
from visualizing.configuration.BaseConfiguration import BaseConfiguration


class HeatmapConfiguration(BaseConfiguration):
    def _default(self) -> None:
        super()._default()
        self.opaqueness = Ref(0.9)
