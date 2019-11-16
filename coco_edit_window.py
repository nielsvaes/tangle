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

import qtmodern.styles
import qtmodern.windows

import nv_utils.file_utils as file_utils
import nv_utils.qt_utils as qutils
import nv_utils.utils as utils
from utils import image as im_utils

from core.NodeScene import NodeScene
from core.NodeView import NodeView
from core.Constants import ss, IO


class TangleWindow(QMainWindow):
    def __init__(self):
        super(TangleWindow, self).__init__()
        self.SCRIPT_FOLDER = os.path.dirname(os.path.realpath(__file__))
        self.UI_PATH = os.path.join(self.SCRIPT_FOLDER, "ui")
        self.ICONS_PATH = os.path.join(self.SCRIPT_FOLDER, "ui", "icons")
        self.NODE_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), "nodes")

        uic.loadUi(os.path.join(self.UI_PATH, "coco_edit.ui"), self)

        self.build_ui()
        self.load_nodes()

        self.pixmap = QPixmap()

        self.keep_pixmap_on_empty_selection = False

        self.show()

        self.setWindowTitle("Tangle")

        #load_node = self.scene.add_node_to_view("LoadImage", "io", 100, 100)
        # load_node.load_image(r"D:\Google Drive\Tools\CocoEdit\its-a-me_4.jpg")
        # load_node.set_dirty(True)

    def build_ui(self):
        self.setBaseSize(QSize(1920, 1080))

        self.scene = NodeScene()
        self.scene.setObjectName('Scene')
        self.scene.setSceneRect(0, 0, 50000, 28000)

        self.view = NodeView(self.scene, self)
        self.main_vertical_layout.addWidget(self.view)

        for i in range(1, 4):
            self.tree_nodes.setColumnHidden(i, True)

        self.lbl_pixmap.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)

        self.horizontal_splitter.setSizes([500, 400])
        self.vertical_splitter.setSizes([500, 400, 400])

        self.scene.selectionChanged.connect(self.load_values_ui)
        self.horizontal_splitter.splitterMoved.connect(self.resize_pixmap)
        self.vertical_splitter.splitterMoved.connect(self.resize_pixmap)

    def normal_node_start(self):
        for node in self.scene.get_begin_nodes():
            pass

    def load_nodes(self):
        for file_path in file_utils.get_files_recursively(self.NODE_FOLDER, filters=".py"):
            if file_path is not None and not "__" in file_path and not "base_node" in file_path and not file_path.endswith(
                    "pyc") and not "image_node" in file_path:

                file_name = os.path.basename(file_path)
                file_name_no_ext = os.path.splitext(file_name)[0]
                icon_path = os.path.join(self.ICONS_PATH, file_name_no_ext + ".png")
                complete_folder = os.path.dirname(file_path)
                folder_name = complete_folder.split(os.sep)[-1]
                complete_path = os.path.join(complete_folder, file_name).replace("\\", "/")

                folder_item = qutils.get_item_with_text_from_tree_widget(self.tree_nodes, folder_name, 0)

                if folder_item is None:
                    folder_item = QTreeWidgetItem(self.tree_nodes, [folder_name])
                    font = QFont()
                    font.setBold(True)
                    font.setPointSize(12)
                    folder_item.setFont(0, font)
                    folder_item.setExpanded(True)

                file_item = QTreeWidgetItem(folder_item,
                                            [file_name_no_ext, complete_path, complete_folder, folder_name])

                if os.path.isfile(icon_path):
                    file_item.setIcon(0, QIcon(icon_path))


    def load_values_ui(self):
        from nodes.base_node import BaseNode
        qutils.clear_layout(self.values_layout)

        selected_items = self.scene.selectedItems()
        if len(selected_items) > 0:
            for node in selected_items:
                if issubclass(type(node), BaseNode):
                    node.refresh()

                    title_label = TitleLabel()
                    title_label.setText(node.name)
                    title_label.setStyleSheet(ss.values_title)
                    title_label.setAlignment(Qt.AlignCenter)
                    title_label.node = node

                    title_label.textChanged.connect(partial(self.change_node_title, title_label))
                    title_label.returnPressed.connect(title_label.node.reposition_title)

                    self.values_layout.insertWidget(self.values_layout.count(), title_label)
                    widget = node.get_ui()

                    self.values_layout.insertWidget(self.values_layout.count() + 1, widget)

                    try:
                        self.pixmap = node.get_pixmap()
                        if self.pixmap is not None:
                            self.set_pixmap(self.pixmap)
                    except AttributeError as err:
                        pass
                        # utils.trace(err)

        else:
            if not self.keep_pixmap_on_empty_selection:
                self.lbl_pixmap.clear()

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

    def resize_pixmap(self):
        try:
            self.lbl_pixmap.setPixmap(self.pixmap.scaled(self.lbl_pixmap.width(), self.lbl_pixmap.height(),
                                                          Qt.KeepAspectRatio, Qt.SmoothTransformation))
        except AttributeError as err:
            utils.trace(err)

    def set_pixmap(self, pixmap):
        self.pixmap = pixmap
        self.lbl_pixmap.setPixmap(self.pixmap)
        self.resize_pixmap()

    def resizeEvent(self, event):
        self.resize_pixmap()
        super(TangleWindow, self).resizeEvent(event)



class TitleLabel(QLineEdit):
    def __init__(self):
        super(TitleLabel, self).__init__()

        self.node = None

    def delete_ui(self):
        self.setParent(None)
        self.deleteLater()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    qtmodern.styles.dark(app)


    splash_pixmap = QPixmap(os.path.join(os.path.dirname(os.path.realpath(__file__)), "ui", "icons", "splashscreen.png"))
    splash_screen = QSplashScreen(splash_pixmap)

    splash_screen.show()

    app.processEvents()

    tangle_window = TangleWindow()

    # modern_window = qtmodern.windows.ModernWindow(tangle_window)
    # modern_window.show()

    tangle_window.show()
    splash_screen.finish(tangle_window)


    app.exec_()
