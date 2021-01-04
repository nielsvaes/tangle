from ez_settings.ez_settings import EasySettingsBase
from ...core.Constants import Colors
from .nodes.plot_node import PlotNode

class StockNode(PlotNode):
    def __init__(self, scene, title="unnamed_node", title_background_color=Colors.node_selected_border, x=0, y=0):
        super().__init__(scene, title, title_background_color, x, y)

        self.key = EasySettingsBase().get_value("alpha_vantage_api")



