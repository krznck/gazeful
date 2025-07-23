from Ref import Ref
from visualizing.configuration.BaseConfiguration import BaseConfiguration


class FixationCountHeatmapConfiguration(BaseConfiguration):
    def _default(self) -> None:
        super()._default()
        self.opaqueness = Ref(0.9)
