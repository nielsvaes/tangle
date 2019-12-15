import os
import sys
from functools import partial
import time
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

from ez_settings.ez_settings import EasySettingsBase


import nv_utils.file_utils as file_utils
import nv_utils.qt_utils as qutils
import nv_utils.utils as utils

from core.NodeScene import NodeScene
from core.NodeView import NodeView
from core.Constants import ss, IO

from widgets.node_tree import NodeTree

from viewers.image_viewer import ImageViewer
from viewers.graph_viewer import GraphViewer

SCRIPT_FOLDER = os.path.dirname(os.path.realpath(__file__))
UI_PATH = os.path.join(SCRIPT_FOLDER, "ui")
SETTINGS_PATH = os.path.join(SCRIPT_FOLDER, "settings", "tangle_settings.json")
ICONS_PATH = os.path.join(SCRIPT_FOLDER, "ui", "icons")
NODE_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), "nodes")


class TangleWindow(QMainWindow):
    def __init__(self):
        super(TangleWindow, self).__init__()

        uic.loadUi(os.path.join(UI_PATH, "tangle.ui"), self)
        self.setWindowTitle("Tangle")

        EasySettingsBase(SETTINGS_PATH)

        self.build_ui()
        self.show()

    def build_ui(self):
        self.scene = NodeScene()
        self.scene.setObjectName('Scene')
        self.scene.setSceneRect(0, 0, 50000, 28000)

        self.view = NodeView(self.scene, self)
        self.main_vertical_layout.addWidget(self.view)

        self.node_tree = NodeTree()
        self.node_tree_layout.addWidget(self.node_tree)

        for i in range(1, 4):
            self.node_tree.ui.tree_nodes.setColumnHidden(i, True)

        self.connect_ui_elements()

    def connect_ui_elements(self):
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
        self.action_show_image_viewer.triggered.connect(partial(self.show_viewer, "image"))
        self.action_show_graph_viewer.triggered.connect(partial(self.show_viewer, "graph"))

        self.scene.selectionChanged.connect(self.load_values_ui)

        self.horizontal_splitter.setSizes([500, 100])
        self.vertical_splitter.setSizes([500, 200])


    def show_viewer(self, viewer_type):
        if viewer_type == "image":
            ImageViewer(self).show()

        if viewer_type == "graph":
            GraphViewer(self).show()


    def load_values_ui(self):
        from nodes.base_node import BaseNode
        from core.GroupNode import GroupNode
        qutils.clear_layout(self.values_layout)

        selected_items = self.scene.selectedItems()
        if len(selected_items) > 0:
            for node in selected_items:
                if issubclass(type(node), BaseNode) or type(node) == GroupNode:
                    node.refresh()

                    # title_label = TitleLabel()
                    # title_label.setText(node.name)
                    # title_label.setStyleSheet(ss.values_title)
                    # title_label.setAlignment(Qt.AlignCenter)
                    # title_label.node = node
                    #
                    # title_label.textChanged.connect(partial(self.change_node_title, title_label))
                    # title_label.returnPressed.connect(title_label.node.reposition_title)

                    # self.values_layout.insertWidget(self.values_layout.count(), title_label)
                    widget = node.get_ui()

                    self.values_layout.insertWidget(self.values_layout.count() + 1, widget)

    def clear_values_layout(self):
        for i in reversed(range(self.values_layout.count())):
            self.values_layout.takeAt(i).widget().setParent(None)

    def change_node_title(self, title_label, text):
        text = text.replace(" ", "_")
        title_label.setText(text)
        title_label.node.change_title(text)

    def compute(self):
        for node in self.scene.selectedItems():
            node.compute()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_F5:
            self.show_viewer("image")
        if event.key() == Qt.Key_F6:
            self.show_viewer("graph")


class TitleLabel(QLineEdit):
    def __init__(self):
        super(TitleLabel, self).__init__()

        self.node = None

    def delete_ui(self):
        self.setParent(None)
        self.deleteLater()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    if modern:
        qtmodern.styles.dark(app)

    splash_pixmap = QPixmap(os.path.join(os.path.dirname(os.path.realpath(__file__)), "ui", "icons", "splashscreen.png"))
    splash_screen = QSplashScreen(splash_pixmap)

    splash_screen.show()

    app.processEvents()

    tangle_window = TangleWindow()

    # modern_window = qtmodern.windows.ModernWindow(tangle_window)
    # modern_window.show()

    tangle_window.showMaximized()
    splash_screen.finish(tangle_window)


    app.exec_()
