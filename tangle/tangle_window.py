import os
import sys
from functools import partial
import logging
logging.basicConfig(level=logging.INFO)

from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtUiTools import *

from ez_settings.ez_settings import EZSettings as ez_settings

import ez_qt as qt_utils

from .ui import tangle_ui

from .core.NodeScene import NodeScene
from .core.NodeView import NodeView
from .core.Constants import sc

from .nodes.base_node import BaseNode
from .core.GroupNode import GroupNode

from .widgets.node_tree import NodeTree
from .widgets.about import AboutDialog
from .widgets.settings_dialog import SettingsDialog
from . import node_db

from .viewers.image_viewer import ImageViewer
from .viewers.graph_viewer import GraphViewerFloat #, GraphViewerDate

SCRIPT_FOLDER = os.path.dirname(os.path.realpath(__file__))
UI_PATH = os.path.join(SCRIPT_FOLDER, "ui")
SETTINGS_PATH = os.path.join(SCRIPT_FOLDER, "settings", "tangle_settings.json")
NODE_INFO_DB = os.path.join(SCRIPT_FOLDER, "settings", "node_info.json")
ICONS_PATH = os.path.join(SCRIPT_FOLDER, "ui", "icons")
NODE_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), "nodes")

TANGLE_VERSION = 1.0

print(SETTINGS_PATH)
ez_settings(SETTINGS_PATH)
ez_settings().set(sc.version, TANGLE_VERSION)


class TangleWindow(QMainWindow, tangle_ui.Ui_tangle_window):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Tangle")

        self.build_ui()
        self.show()
        
        self.set_help_text("Testing!")
        self.__image_viewer = ImageViewer(parent=self)

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
            self.node_tree.tree_nodes.setColumnHidden(i, True)

        self.connect_ui_elements()

    def connect_ui_elements(self):
        self.action_show_about.triggered.connect(self.show_about)

        self.action_save_scene.triggered.connect(self.scene.browse_for_save_location)
        self.action_load.triggered.connect(partial(self.scene.browse_for_saved_scene, True))
        self.action_clear_scene.triggered.connect(self.scene.clear_scene)
        self.action_recompute_entire_network.triggered.connect(self.scene.refresh_network)

        self.action_save_selected_nodes.triggered.connect(partial(self.scene.browse_for_save_location, True))
        self.action_duplicate_nodes.triggered.connect(self.scene.duplicate_nodes)
        self.action_group_ungroup_nodes.triggered.connect(self.scene.group_nodes)
        self.action_delete_nodes.triggered.connect(self.scene.delete_nodes)
        self.action_import_nodes_from_file.triggered.connect(partial(self.scene.browse_for_saved_scene, False))
        self.action_align_selected_nodes_horizontally.triggered.connect(partial(self.scene.align_selected_nodes, "horizontal_up"))
        self.action_align_selected_nodes_vertically.triggered.connect(partial(self.scene.align_selected_nodes, "vertical_left"))

        self.action_reload_nodes.triggered.connect(self.node_tree.load_node_tree)
        self.action_generate_node_database.triggered.connect(self.generate_node_database)
        self.action_settings.triggered.connect(self.show_settings)
        self.action_show_image_viewer.triggered.connect(partial(self.show_viewer, "image"))
        self.action_show_graph_viewer.triggered.connect(partial(self.show_viewer, "graph_float"))
        self.action_show_graph_viewer_date.triggered.connect(partial(self.show_viewer, "graph_date"))

        self.scene.selectionChanged.connect(self.load_values_ui)

        self.horizontal_splitter.setSizes([500, 100])
        self.vertical_splitter.setSizes([500, 200])

    def get_image_viewer(self):
        return self.__image_viewer

    def show_viewer(self, viewer_type):
        if viewer_type == "image":
            self.__image_viewer.show()
        if viewer_type == "graph_float":
            GraphViewerFloat(self).show()
        if viewer_type == "graph_date":
            GraphViewerDate(self).show()

    def load_values_ui(self):
        self.clear_values_ui()

        selected_items = self.scene.selectedItems()
        if len(selected_items) > 0:
            for node in selected_items:
                if issubclass(type(node), BaseNode) or type(node) == GroupNode:
                    node.refresh()
                    widget = node.get_ui()
                    widget.setVisible(True)
                    self.values_layout.addWidget(widget)
                    # self.values_layout.insertWidget(self.values_layout.count() + 1, widget)

    def clear_values_ui(self):
        for i in reversed(range(self.values_layout.count())):
            widgetToRemove = self.values_layout.itemAt(i).widget()
            # remove it from the layout list
            self.values_layout.removeWidget(widgetToRemove)
            # remove it from the gui
            widgetToRemove.setParent(None)

    def generate_node_database(self):
        node_db.generate_database(self.node_tree.get_all_node_items(), self.scene)

    def show_about(self):
        dialog = AboutDialog()
        dialog.exec_()

    def show_settings(self):
        dialog = SettingsDialog()
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
