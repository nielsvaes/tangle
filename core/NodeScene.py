import os
import sys
import importlib
import logging
logging.basicConfig(level=logging.INFO)

import re

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import nv_utils.utils as utils
import nv_utils.io_utils as io_utils
import core.socket_types as socket_types

from pydoc import locate

from core.Constants import Colors
from core.Node import Node

path = os.path.join(os.path.dirname(os.path.basename(os.path.realpath(__file__))), "saved_network.json")

class NodeScene(QGraphicsScene):
    refreshed = pyqtSignal()

    def __init__(self):
        super(NodeScene, self).__init__()

    def add_node_to_view(self, class_name, module, x=0, y=0, uuid_string=None):
        node_instance = None

        if type(class_name) == str:
            module_path = ".".join(["nodes", module, class_name])
            node_module = importlib.import_module(module_path)
            importlib.reload(node_module)
            # class_path = ".".join([os.path.basename(self.get_main_window().SCRIPT_FOLDER), "nodes", module, class_name, class_name])
            # node_class = locate(class_path)
            try:
                node_instance = getattr(node_module, class_name)(self, x, y)
                # node_instance = node_class(self, x, y)
            except TypeError as err:
                utils.trace(err)
        else:
            try:
                module_file_path = sys.modules[class_name.__module__].__file__
                module_path = utils.get_clean_module_path(module_file_path, "nodes")
                node_instance = class_name.__class__(self, x, y)
            except:
                utils.trace("Can't create node of type %s" % class_name)
                return None

        if node_instance is not None:
            node_instance.set_module_path(module_path)
            return node_instance


    def get_all_nodes(self):
        from nodes.base_node import BaseNode
        nodes = []
        for item in self.items():
            if issubclass(type(item), BaseNode):
                nodes.append(item)

        return nodes

    def get_all_connections(self):
        from core.SocketConnection import SocketConnection
        connections = []
        for item in self.items():
            if type(item) == SocketConnection:
                connections.append(item)

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
                        if connected_node.is_dirty():
                            logging.info("is dirty, needs computing: %s" % connected_node.title)
                            connected_node.compute()
                            child_nodes_are_dirty = True
                        if child_nodes_are_dirty:
                            logging.info("is a child node, needs computing: %s" % connected_node.title)
                            connected_node.compute()
                            continue

            self.__set_colors_computed()

        except Exception as err:
            utils.trace(err)

    def save_network(self, selected_nodes_only=False, to_memory=False, file_path=None):
        try:
            save_dict = {}

            if selected_nodes_only:
                nodes = self.get_selected_nodes()
            else:
                nodes = self.get_all_nodes()

            for node in nodes:
                save_dict[node.get_uuid(as_string=True)] = node.save()

            if to_memory:
                return save_dict

            if file_path is not None:
                io_utils.write_json(save_dict, file_path)

        except Exception as err:
            utils.trace(err)


    def open_network(self, save_dict=None, file_path=None, with_values=True):
        if save_dict is not None:
            mapped_scene = save_dict
        else:
            if file_path is not None:
                mapped_scene = io_utils.read_json(file_path)

        for node_uuid, node_dict in mapped_scene.items():
            x = node_dict.get("x")
            y = node_dict.get("y")
            if save_dict:
                x += 20
                y += 20
            module_path = node_dict.get("module_path")
            class_name = node_dict.get("class_name")
            module_name = node_dict.get("module_name")
            node = self.add_node_to_view(class_name, module_name, x, y)

            if node is not None:
                node.set_uuid(node_uuid)

                for socket_uuid, socket_dict in node_dict.get("sockets").items():
                    label = socket_dict.get("label")
                    io = socket_dict.get("io")
                    value = socket_dict.get("value")
                    initial_value = socket_dict.get("initial_value")
                    socket_type_name = socket_dict.get("socket_type")
                    socket_type = getattr(socket_types, socket_type_name)(node)

                    socket = node.get_socket(label, io)

                    if socket is None:
                        if io == "output":
                            socket = node.add_output(socket_type, label)
                        elif io == "input":
                            socket = node.add_input(socket_type, label)

                    socket.set_uuid(socket_uuid)

                    if with_values:
                        socket.set_initial_value(initial_value)
                        socket.set_value(value)
                        node.compute()

    def duplicate_nodes(self):
        save_dict = self.save_network(selected_nodes_only=True, to_memory=True)
        self.open_network(save_dict=save_dict, with_values=True)

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

    def get_selected_nodes(self):
        from nodes.base_node import BaseNode
        return [item for item in self.selectedItems() if issubclass(type(item), BaseNode)]


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
        #self.refresh_network()

        if event.key() == Qt.Key_D and event.modifiers() == Qt.ControlModifier:
            self.duplicate_nodes()

        if event.key() == Qt.Key_S and event.modifiers() == Qt.ControlModifier:
            print("saving_network")
            self.save_network(file_path=path)


        if event.key() == Qt.Key_O and event.modifiers() == Qt.ControlModifier:
            self.open_network(path)

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

