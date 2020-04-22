import os
import sys
from functools import partial
import logging
logging.basicConfig(level=logging.INFO)

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic

try:
    import qtmodern.styles
    import qtmodern.windows
    modern = True
except:
    logging.warning("Can't find qtmodern!")
    modern = False

from ez_settings.ez_settings import EasySettingsSingleton as settings

import nv_utils.qt_utils as qt_utils
import nv_utils.io_utils as io_utils

from core.NodeScene import NodeScene
from core.NodeView import NodeView
from core.Constants import sc

from widgets.node_tree import NodeTree
from widgets.about import AboutDialog
import node_db

from viewers.image_viewer import ImageViewer
from viewers.graph_viewer import GraphViewerFloat, GraphViewerDate

SCRIPT_FOLDER = os.path.dirname(os.path.realpath(__file__))
UI_PATH = os.path.join(SCRIPT_FOLDER, "ui")
SETTINGS_PATH = os.path.join(SCRIPT_FOLDER, "settings", "tangle_settings.json")
NODE_INFO_DB = os.path.join(SCRIPT_FOLDER, "settings", "node_info.json")
ICONS_PATH = os.path.join(SCRIPT_FOLDER, "ui", "icons")
NODE_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), "nodes")

TANGLE_VERSION = 1.0

settings(SETTINGS_PATH)
settings().set_value(sc.version, TANGLE_VERSION)

class TangleWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        uic.loadUi(os.path.join(UI_PATH, "tangle.ui"), self)
        self.setWindowTitle("Tangle")

        self.build_ui()
        self.show()
        
        self.set_help_text("Testing!")

    def build_ui(self):
        self.scene = NodeScene()
        self.scene.setObjectName('Scene')
        self.scene.setSceneRect(0, 0, 50000, 28000)

        self.view = NodeView(self.scene, self)
        self.main_vertical_layout.addWidget(self.view)

        self.node_tree = NodeTree()
        self.node_tree_layout.addWidget(self.node_tree)

        self.setWindowIcon(QIcon(os.path.join(ICONS_PATH, "logo.png")))

        for i in range(1, 4):
            self.node_tree.ui.tree_nodes.setColumnHidden(i, True)

        self.connect_ui_elements()

    def connect_ui_elements(self):
        self.action_show_about.triggered.connect(self.show_about)

        self.action_save_scene.triggered.connect(self.scene.browse_for_save_location)
        self.action_load.triggered.connect(self.scene.browse_for_saved_scene)
        self.action_clear_scene.triggered.connect(self.scene.clear_scene)
        self.action_recompute_entire_network.triggered.connect(self.scene.refresh_network)

        self.action_save_selected_nodes.triggered.connect(partial(self.scene.browse_for_save_location, True))
        self.action_duplicate_nodes.triggered.connect(self.scene.duplicate_nodes)
        self.action_group_ungroup_nodes.triggered.connect(self.scene.group_nodes)
        self.action_delete_nodes.triggered.connect(self.scene.delete_nodes)
        self.action_align_selected_nodes_horizontally.triggered.connect(partial(self.scene.align_selected_nodes, "horizontal_up"))
        self.action_align_selected_nodes_vertically.triggered.connect(partial(self.scene.align_selected_nodes, "vertical_left"))

        self.action_reload_nodes.triggered.connect(self.node_tree.ui.load_node_tree)
        self.action_generate_node_database.triggered.connect(self.generate_node_database)
        self.action_show_image_viewer.triggered.connect(partial(self.show_viewer, "image"))
        self.action_show_graph_viewer.triggered.connect(partial(self.show_viewer, "graph_float"))
        self.action_show_graph_viewer_date.triggered.connect(partial(self.show_viewer, "graph_date"))

        self.scene.selectionChanged.connect(self.load_values_ui)

        self.horizontal_splitter.setSizes([500, 100])
        self.vertical_splitter.setSizes([500, 200])

    def show_viewer(self, viewer_type):
        if viewer_type == "image":
            ImageViewer(self).show()
        if viewer_type == "graph_float":
            GraphViewerFloat(self).show()
        if viewer_type == "graph_date":
            GraphViewerDate(self).show()

    def load_values_ui(self):
        from nodes.base_node import BaseNode
        from core.GroupNode import GroupNode
        qt_utils.clear_layout(self.values_layout)

        selected_items = self.scene.selectedItems()
        if len(selected_items) > 0:
            for node in selected_items:
                if issubclass(type(node), BaseNode) or type(node) == GroupNode:
                    node.refresh()
                    widget = node.get_ui()
                    self.values_layout.insertWidget(self.values_layout.count() + 1, widget)

    def generate_node_database(self):
        node_db.generate_database(self.node_tree.get_all_node_items(), self.scene)

    def show_about(self):
        dialog = AboutDialog()
        dialog.exec_()

    def set_help_text(self, text, timeout=0):
        self.statusbar.showMessage(text, timeout)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_F5:
            self.show_viewer("image")
        if event.key() == Qt.Key_F6:
            self.show_viewer("graph_float")
        if event.key() == Qt.Key_F7:
            self.show_viewer("graph_date")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    if modern:
        qtmodern.styles.dark(app)

    splash_pixmap = QPixmap(os.path.join(os.path.dirname(os.path.realpath(__file__)), "ui", "icons", "splashscreen.png"))
    splash_screen = QSplashScreen(splash_pixmap)

    splash_screen.show()

    app.processEvents()

    tangle_window = TangleWindow()

    # tangle_window.showMaximized()
    tangle_window.show()
    splash_screen.finish(tangle_window)

    app.exec_()
