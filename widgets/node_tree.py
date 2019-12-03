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

import nv_utils.file_utils as file_utils
import nv_utils.qt_utils as qutils
import nv_utils.utils as utils

SCRIPT_FOLDER = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
UI_PATH = os.path.join(SCRIPT_FOLDER, "ui")
SETTINGS_PATH = os.path.join(SCRIPT_FOLDER, "settings", "tangle_settings.json")
ICONS_PATH = os.path.join(SCRIPT_FOLDER, "ui", "icons")
NODE_FOLDER = os.path.join(SCRIPT_FOLDER, "nodes")

form, base = uic.loadUiType(os.path.join(UI_PATH, "node_tree.ui"))

class NodeTree(form, base):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.ui = uic.loadUi(os.path.join(UI_PATH, "node_tree.ui"), self)
        self.load_node_tree()

        self.ui.txt_search_nodes.textChanged.connect(self.search_node_tree)

    def search_node_tree(self):
        # if self.txt_search_nodes.text()
        search_words = self.ui.txt_search_nodes.text().lower().split(" ")

        root = self.ui.tree_nodes.invisibleRootItem()
        folder_count = root.childCount()
        for i in range(folder_count):
            folder = root.child(i)
            item_count = folder.childCount()
            for j in range(item_count):
                item = folder.child(j)

                hidden = False
                for word in search_words:
                    if not word in item.text(0).lower():
                        hidden = True

                item.setHidden(hidden)

    def load_node_tree(self):
        self.ui.tree_nodes.clear()
        self.loaded_nodes_info_dict = {}
        for file_path in file_utils.get_files_recursively(NODE_FOLDER, filters=".py"):
            if file_path is not None and not "__" in file_path and not "base_node" in file_path and not file_path.endswith(
                    "pyc") and not "image_node" in file_path:

                file_name = os.path.basename(file_path)
                file_name_no_ext = os.path.splitext(file_name)[0]
                icon_path = os.path.join(ICONS_PATH, file_name_no_ext + ".png")
                complete_folder = os.path.dirname(file_path)
                folder_name = complete_folder.split(os.sep)[-1]
                parent_folder = os.sep.join(complete_folder.split(os.sep)[0:-1])
                parent_folder_name = parent_folder.split(os.sep)[-1]
                complete_path = os.path.join(complete_folder, file_name).replace("\\", "/")

                folder_item = qutils.get_item_with_text_from_tree_widget(self.ui.tree_nodes, folder_name, 0)

                if folder_item is None:
                    folder_item = QTreeWidgetItem(self.ui.tree_nodes, [folder_name])
                    font = QFont()
                    font.setBold(True)
                    font.setPointSize(12)
                    folder_item.setFont(0, font)
                    folder_item.setExpanded(True)

                file_item = QTreeWidgetItem(folder_item,
                                            [file_name_no_ext, complete_path, complete_folder, folder_name])

                if os.path.isfile(icon_path):
                    file_item.setIcon(0, QIcon(icon_path))

