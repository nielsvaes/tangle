import os

from collections import OrderedDict
import pickle

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import nv_utils.utils as utils

from pydoc import locate

from core.Constants import Colors
from core.NodeItem import NodeItem

class NodeScene(QGraphicsScene):
    refreshed = pyqtSignal()

    def __init__(self):
        super(NodeScene, self).__init__()
        self.__set_colors_computed()


    def add_node_to_view(self, class_name, module, x=0, y=0):
        node_instance = None

        if type(class_name) == str:
            class_path = ".".join([os.path.basename(self.get_main_window().SCRIPT_FOLDER), "nodes", module, class_name, class_name])
            print(class_path)
            node_class = locate(class_path)
            try:
                node_instance = node_class(self, x, y)
            except TypeError as err:
                utils.trace(err)
        else:
            node_instance = class_name.__class__(self, x, y)

        if node_instance is not None:
            # for socket_type in node_instance.get_all_socket_types():
            #     socket_type.is_dirty.connect(self.set_colors_dirty)

            node_instance.dirty_signal.signal.connect(self.set_colors_dirty)
            return node_instance


    def get_all_nodes(self):
        from nodes.base_node import BaseNode
        nodes = []
        for item in self.items():
            if issubclass(type(item), BaseNode):
                nodes.append(item)

        return nodes

    # def get_all_nodes(self):
    #     from nodes.base_node import BaseNode
    #     nodes = []
    #     for node in self.items():
    #         if issubclass(type(node), BaseNode):
    #             if not node.is_executing_node():
    #                 nodes.append(node)
    #
    #     return nodes

    def get_nonexisting_name(self, name):
        for node in self.get_all_nodes():
            if name == node.name:
                pass
            #TODO: generate unique name, now battlefield

    def get_node_by_name(self, name):
        for node in self.get_all_nodes():
            if node.title == name:
                return node
        return None

    def get_node_by_uuid(self, uuid):
        for node in self.get_all_nodes():
            if node.uuid == uuid:
                return node
        return None

    def get_view(self):
        return self.views()[0]

    def get_main_window(self):
        return self.get_view().window()

    def refresh_network(self, node=None):
        try:
            if node is None:
                for begin_node in self.get_begin_nodes():
                    if begin_node.is_dirty():
                        begin_node.compute()

                    child_nodes_are_dirty = False
                    for connected_node in begin_node.get_connected_output_nodes_recursive():
                        if child_nodes_are_dirty:
                            print("is a child node, needs computing: ", connected_node.title)
                            connected_node.compute()
                            continue
                        if connected_node.is_dirty():
                            print("is dirty, needs computing: ", connected_node.title)
                            connected_node.compute()
                            child_nodes_are_dirty = True

            self.__set_colors_computed()

        except Exception as err:
            utils.trace(err)

    def map_network(self):
        node_dict = OrderedDict()
        for begin_node in self.get_begin_nodes():
            for attribute in vars(begin_node):
            # for index, attribute in enumerate(begin_node.__dict__):
                node_dict[begin_node.get_uuid(as_string=True)] = {}
                node_dict[begin_node.get_uuid(as_string=True)][attribute] = getattr(begin_node, attribute)

        for key, value in enumerate(node_dict):
            print(key)
            print(value)

    def get_begin_nodes(self):
        start_nodes = []
        non_executing_nodes = self.get_all_nodes()

        if len(non_executing_nodes) == 1:
            return non_executing_nodes

        if len(non_executing_nodes) > 1:
            for node in non_executing_nodes:
                if len(node.get_connected_output_sockets()) > 0:
                    if len(node.get_connected_input_sockets()) == 0:
                        start_nodes.append(node)

                if len(node.get_connected_input_sockets()) + len(node.get_connected_output_sockets()) == 0:
                    start_nodes.append(node)

        return start_nodes

    def get_end_nodes(self):
        end_nodes = []
        non_executing_nodes = self.get_all_nodes()

        if len(non_executing_nodes) == 1:
            return non_executing_nodes

        if len(non_executing_nodes) > 1:
            for node in non_executing_nodes:
                if len(node.get_connected_input_sockets()) > 0:
                    if len(node.get_connected_output_sockets()) == 0:
                        end_nodes.append(node)

                if len(node.get_connected_input_sockets()) + len(node.get_connected_output_sockets()) == 0:
                    end_nodes.append(node)

        return end_nodes

    # def is_cyclical(self):
    #     try:
    #         self.get_begin_executing_node()
    #         return False
    #     except:
    #         pass
    #
    #     result = True
    #     for node in self.get_all_executing_nodes():
    #         if not node.is_execution_output_connected() or not node.is_execution_input_connected:
    #             result = False
    #
    #     return result

    def save(self, file_path=None):
        if file_path is None:
            file_path = QFileDialog.getSaveFileName(caption="Save Network", filter="Coco Edit Network Files(*.json)")[0]


    def duplicate_nodes(self, nodes=None):
        from nodes.base_node import BaseNode
        if nodes is None:
            nodes = [item for item in self.selectedItems() if issubclass(type(item), BaseNode)]

        self.clearSelection()

        for node in nodes:
            x = node.scenePos().x() + 20
            y = node.scenePos().y() + 20

            new_node = self.add_node_to_view(node, None, x, y)

    def dragMoveEvent(self, event):
        event.accept()

    def dropEvent(self, event):
        try:
            class_name = event.source().selectedItems()[0].text(0)
            module = event.source().selectedItems()[0].parent().text(0)

            x = event.scenePos().x()
            y = event.scenePos().y()

            self.add_node_to_view(class_name, module, x, y)
        except Exception as err:
            utils.trace(err)

    def keyPressEvent(self, event):
        #from nodes.base_node import BaseNode
        if event.key() == Qt.Key_Delete:
            selected_nodes = self.selectedItems()
            self.clearSelection()
            for item in selected_nodes:
                try:
                    item.destroy_self()
                except Exception as err:
                    utils.trace(err)
            if len(self.items()) == 0:
                self.__set_colors_computed()

        if event.key() == Qt.Key_D and event.modifiers() == Qt.ControlModifier:
            self.duplicate_nodes()

        if event.key() == Qt.Key_S and event.modifiers() == Qt.ControlModifier:
            self.map_network()

        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.refresh_network()

    def set_colors_dirty(self):
        dirty_node_exists = False
        for node in self.get_all_nodes():
            if node.is_dirty():
                dirty_node_exists = True
                break
        if dirty_node_exists:
            brush = QBrush()
            brush.setStyle(Qt.SolidPattern)
            brush.setColor(Colors.node_scene_dirty)
            self.setBackgroundBrush(brush)

    def __set_colors_computed(self):
        brush = QBrush()
        brush.setStyle(Qt.SolidPattern)
        brush.setColor(Colors.node_scene_computed)
        self.setBackgroundBrush(brush)

