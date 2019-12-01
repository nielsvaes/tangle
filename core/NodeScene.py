import os
import sys
import importlib
import logging
logging.basicConfig(level=logging.INFO)

import re
import uuid

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import nv_utils.utils as utils
import nv_utils.io_utils as io_utils
import core.socket_types as socket_types

from .SocketConnection import SocketConnection

from core.Constants import Colors

class NodeScene(QGraphicsScene):
    def __init__(self):
        super(NodeScene, self).__init__()

    def add_node_to_view(self, class_name, module, x=0, y=0, uuid_string=None):
        node_instance = None

        if type(class_name) == str:
            module_path = ".".join(["nodes", module, class_name])
            node_module = importlib.import_module(module_path)
            importlib.reload(node_module)
            try:
                node_instance = getattr(node_module, class_name)(self, x, y)
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

    def get_node_by_name(self, name):
        for node in self.get_all_nodes():
            if node.title == name:
                return node
        return None

    def get_node_by_uuid(self, search_uuid):
        if type(search_uuid) == str:
            search_uuid = uuid.UUID(search_uuid)
        for node in self.get_all_nodes():
            if node.get_uuid() == search_uuid:
                return node
        return None

    def get_socket_by_uuid(self, search_uuid):
        if type(search_uuid) == str:
            search_uuid = uuid.UUID(search_uuid)
        for node in self.get_all_nodes():
            socket_uuid = node.get_socket_by_uuid(search_uuid)
            socket = node.get_socket_by_uuid(search_uuid)
            if socket is not None:
                return socket
        return None

    def get_view(self):
        return self.views()[0]

    def get_main_window(self):
        return self.get_view().window()

    def refresh_network(self, node=None):
        try:
            if node is None:
                for begin_node in self.get_begin_nodes():
                    print("computing begin node %s " % begin_node)
                    begin_node.set_dirty(True)
                    begin_node.compute()

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

    def open_network(self, scene_dict=None, file_path=None, with_connections=True, with_values=True, is_duplicate=False):
        offset_nodes = False
        if is_duplicate:
            offset_nodes = True

        if file_path is not None:
            scene_dict = io_utils.read_json(file_path)

        self.load_nodes(scene_dict, offset_nodes, with_values, new_socket_uuids=is_duplicate)

        if with_connections:
            self.load_connections(scene_dict)

        if not is_duplicate:
            answer = QMessageBox.question(self.get_main_window(), "Tangle", "Compute network now?", QMessageBox.No, QMessageBox.Yes)
            if answer == QMessageBox.Yes:
                self.refresh_network()

    def load_connections(self, mapped_scene):
        try:
            for connection_dict in utils.value_extract("connections", mapped_scene):
                for index, connection_list in connection_dict.items():
                    output_socket = self.get_socket_by_uuid(connection_list[0])
                    input_socket = self.get_socket_by_uuid(connection_list[1])
                    SocketConnection(output_socket, input_socket, self, auto_compute_on_connect=False)
        except Exception as err:
            utils.trace(err)

    def load_nodes(self, mapped_scene, offset_nodes, with_values, new_socket_uuids=False):
        for node_uuid, node_dict in mapped_scene.items():
            x = node_dict.get("x")
            y = node_dict.get("y")
            if offset_nodes:
                x += 20
                y += 20
            module_path = node_dict.get("module_path")
            class_name = node_dict.get("class_name")
            module_name = node_dict.get("module_name")
            node = self.add_node_to_view(class_name, module_name, x, y)

            if node is not None:
                node.load(node_dict, x=x, y=y)

                if node_dict.get("sockets") is not None:
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

                        if new_socket_uuids:
                            socket_uuid = uuid.uuid4()
                        socket.set_uuid(socket_uuid)

                        if with_values:
                            socket.set_initial_value(initial_value)
                            socket.set_value(value)
                            node.compute()

    def duplicate_nodes(self):
        try:
            for node in self.get_selected_nodes():
                node.duplicate()
        except Exception as err:
            utils.trace(err)

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

    def delete_nodes(self):
        items = self.selectedItems()
        self.clearSelection()
        for item in items:
            try:
                item.destroy_self()
            except Exception as err:
                utils.trace(err)

    def clear(self):
        for node in self.get_all_nodes():
            node.destroy_self()

    def browse_for_save_location(self, selected_nodes_only=False):
        file_path = QFileDialog.getSaveFileName(caption="Save Tangle network", filter="Tangle files (*.tngl)")[0]
        if file_path != "":
            if selected_nodes_only:
                self.save_network(selected_nodes_only=True, file_path=file_path)
            else:
                self.save_network(selected_nodes_only=False, file_path=file_path)

    def browse_for_saved_scene(self):
        file_path = QFileDialog.getOpenFileName(caption="Open Tangle Network", filter="Tangle files (*.tngl)")[0]
        if file_path != "":
            self.open_network(file_path=file_path)

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
        if event.key() == Qt.Key_Delete:
            self.delete_nodes()

        if event.key() == Qt.Key_D and event.modifiers() == Qt.ControlModifier:
            self.duplicate_nodes()

        if event.key() == Qt.Key_S and event.modifiers() == Qt.ControlModifier:
            self.browse_for_save_location()

        if event.key() == Qt.Key_O and event.modifiers() == Qt.ControlModifier:
            self.browse_for_saved_scene()

        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.refresh_network()

        if event.key() == Qt.Key_I:
            self.get_main_window().show_viewer("image")

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

