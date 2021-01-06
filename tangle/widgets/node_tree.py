import os
import logging
logging.basicConfig(level=logging.INFO)

from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtUiTools import *

import nv_utils.file_utils as file_utils
import ez_qt as qt_utils

from ..ui import node_tree_ui

SCRIPT_FOLDER = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
UI_PATH = os.path.join(SCRIPT_FOLDER, "ui")
SETTINGS_PATH = os.path.join(SCRIPT_FOLDER, "settings", "tangle_settings.json")
ICONS_PATH = os.path.join(SCRIPT_FOLDER, "ui", "icons")
NODE_FOLDER = os.path.join(SCRIPT_FOLDER, "nodes")

class NodeTree(QTreeWidget, node_tree_ui.Ui_Form):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.load_node_tree()

        self.txt_search_nodes.textChanged.connect(self.search_node_tree)

    def search_node_tree(self):
        search_words = self.txt_search_nodes.text().lower().split(" ")

        root = self.tree_nodes.invisibleRootItem()
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
        self.tree_nodes.clear()
        for file_path in file_utils.get_files_recursively(NODE_FOLDER, filters=".py"):
            if file_path is not None and not "__" in file_path and not file_path.endswith("pyc"):
                file_name = os.path.basename(file_path)
                file_name_no_ext = os.path.splitext(file_name)[0]
                icon_path = os.path.join(ICONS_PATH, file_name_no_ext + ".png")
                complete_folder = os.path.dirname(file_path)
                folder_name = complete_folder.split(os.sep)[-1]
                parent_folder = os.sep.join(complete_folder.split(os.sep)[0:-1])
                parent_folder_name = parent_folder.split(os.sep)[-1]
                complete_path = os.path.join(complete_folder, file_name).replace("\\", "/")

                if complete_folder == NODE_FOLDER:
                    continue

                folder_item = qt_utils.tree_widget.get_item_with_text(self.tree_nodes, folder_name, 0)

                if folder_item is None:
                    folder_item = FolderItem(self.tree_nodes, [folder_name])
                    font = QFont()
                    font.setBold(True)
                    font.setPointSize(12)
                    folder_item.setFont(0, font)
                    folder_item.setExpanded(True)

                file_item = NodeItem(folder_item, [file_name_no_ext]) #, complete_path, complete_folder, folder_name])

                file_item.file_name = file_name
                file_item.file_name_no_ext = file_name_no_ext
                file_item.icon_path = icon_path
                file_item.complete_folder = complete_folder
                file_item.folder_name = folder_name
                file_item.parent_folder = parent_folder
                file_item.parent_folder_name = parent_folder_name
                file_item.complete_path = complete_path

                if os.path.isfile(icon_path):
                    file_item.setIcon(0, QIcon(icon_path))

    def get_all_node_items(self):
        return [item for item in qt_utils.tree_widget.get_all_items(self.tree_nodes) if item.item_type == "node"]

    def get_all_folder_items(self):
        return qt_utils.tree_widget.get_all_items(self.tree_nodes)


class NodeTreeItem(QTreeWidgetItem):
    def __init__(self, parent_item, columns):
        super().__init__(parent_item, columns)
        self.file_name = None
        self.file_name_no_ext = None
        self.icon_path = None
        self.complete_folder = None
        self.folder_name = None
        self.parent_folder = None
        self.parent_folder_name = None
        self.complete_path = None

class FolderItem(NodeTreeItem):
    def __init__(self, parent_item, columns):
        super().__init__(parent_item, columns)
        self.item_type = "folder"

class NodeItem(NodeTreeItem):
    def __init__(self, parent_item, columns):
        super().__init__(parent_item, columns)
        self.item_type = "node"
