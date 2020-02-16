import sys
import importlib
import logging
logging.basicConfig(level=logging.INFO)

import uuid

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import nv_utils.utils as utils
import nv_utils.io_utils as io_utils
import core.socket_types as socket_types
from ez_settings.ez_settings import EasySettingsSingleton as settings

from .SocketConnection import SocketConnection
from .GroupNode import GroupNode
from nodes.base_node import BaseNode
from viewers.image_viewer import ImageViewer
from viewers.graph_viewer import GraphViewerFloat

from core.Constants import Colors
import core.SettingsConstants as sc

class NodeScene(QGraphicsScene):
    """
    The QGraphicsScene in which the Tangle network is built.
    """
    def __init__(self):
        super(NodeScene, self).__init__()

    def add_node_to_view(self, class_name, module, x=0, y=0):
        """
        Adds a new node to the scene.

        :param class_name: [string/node instance] Either the name of the node or the actual instance of the node to
        be added to the scene
        :param module: [string] name of the module the node is part of (name of parent directory)
        :param x: [int] X position of the node
        :param y: [int] Y position of the node
        :return: the newly created node instance
        """
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

    def get_all_group_nodes(self):
        """
        Returns a list of all the GroupNodes in the scene

        :return: [list] GroupNode
        """
        group_nodes = []
        for item in self.items():
            if type(item) == GroupNode:
                group_nodes.append(item)
        return group_nodes

    def get_all_nodes(self):
        """
        Returns a list of all the nodes that are currently in the scene. Nodes have to derive from BaseNode.

        :return: [list] BaseNode
        """
        nodes = []
        for item in self.items():
            if issubclass(type(item), BaseNode):
                nodes.append(item)

        return nodes

    def get_all_connections(self):
        """
        Returns a list of all the connections that are currently in the scene

        :return: [list] SocketConnection
        """
        from core.SocketConnection import SocketConnection
        connections = []
        for item in self.items():
            if type(item) == SocketConnection:
                connections.append(item)

    def get_node_by_name(self, name):
        """
        Returns the first node that has the given name as title

        :param name: [string] name to search for
        :return: [BaseNode] with the given name as title or [None]
        """
        for node in self.get_all_nodes():
            if node.title == name:
                return node
        return None

    def get_node_by_uuid(self, search_uuid):
        """
        Returns the node with the given uuid if it exists

        :param search_uuid: [string/uuid]
        :return: [BaseNode] or [None]
        """
        if type(search_uuid) == str:
            search_uuid = uuid.UUID(search_uuid)
        for node in self.get_all_nodes():
            if node.get_uuid() == search_uuid:
                return node
        return None

    def get_socket_by_uuid(self, search_uuid):
        """
        Returns the socket with the given uuid if it exists

        :param search_uuid: [string/uuid]
        :return: [NodeSocket] or [None]
        """
        if type(search_uuid) == str:
            search_uuid = uuid.UUID(search_uuid)
        for node in self.get_all_nodes():
            socket = node.get_socket_by_uuid(search_uuid)
            if socket is not None:
                return socket
        return None

    def get_view(self):
        """
        Returns the view this NodeScene is part of

        :return: [NodeView]
        """
        return self.views()[0]

    def get_main_window(self):
        """
        Returns the main Tangle window

        :return: [QMainWindow]
        """
        return self.get_view().window()

    def refresh_network(self, node=None):
        """
        Starts with all the starting nodes in the scene and computes all child nodes

        :param node: [BaseNode] if this is not None, the function will use this node as the only begin node
        :return:
        """
        try:
            if node is None:
                for begin_node in self.get_begin_nodes():
                    print("computing begin node %s " % begin_node)
                    begin_node.set_dirty(True)
                    begin_node.compute()
            else:
                node.set_dirty(True)
                node.compute()

        except Exception as err:
            utils.trace(err)

    def save_network(self, selected_nodes_only=False, to_memory=False, file_path=None):
        """
        Saves the Tangle network

        :param selected_nodes_only: [bool] will only save the selected files
        :param to_memory: [bool] will not write the file to disk, but returns a [dict] of the mapped network. If this
        is set to True, file_path is ignored
        :param file_path: [string] Location the Tangle network will be saved as a .json file with extension .tngl
        :return: [dict] if to_memory is set to True
        """
        try:
            save_dict = {}
            save_dict["nodes"] = {}
            save_dict["group_nodes"] = {}

            if selected_nodes_only:
                nodes = self.get_selected_nodes()
                group_nodes = self.get_selected_group_nodes()
            else:
                nodes = self.get_all_nodes()
                group_nodes = self.get_all_group_nodes()

            for node in nodes:
                save_dict["nodes"][node.get_uuid(as_string=True)] = node.save()

            for group_node in group_nodes:
                save_dict["group_nodes"][group_node.get_uuid(as_string=True)] = group_node.save()

            if to_memory:
                return save_dict

            if file_path is not None:
                io_utils.write_json(save_dict, file_path)

        except Exception as err:
            utils.trace(err)

    def open_network(self, scene_dict=None, file_path=None, with_connections=True, with_values=True, is_duplicate=False):
        """
        Opens a Tangle network and adds the nodes to the NodeScene

        :param scene_dict: [dict] if file_path is set to None, the function will use this dictionary to load the scene
        :param file_path: [string] location of the .tngl file
        :param with_connections: [bool] if set to True, will also connect the nodes as they were saved
        :param with_values: [bool] if set to True, will try to reset the values of all the nodes as they were saved.
        On specific node types this might cause problems and it's easier to just set the begin node to a value and let
        the network recompute
        :param is_duplicate: [bool] if set to True, new uuids will be generated so that all uuids will remain unique. Do
        not use if with_connections and/or with_values is set to True, because the network will get confused which uuids
        to use
        :return:
        """
        if file_path is not None:
            scene_dict = io_utils.read_json(file_path)

        self.load_nodes(scene_dict, with_values, is_duplicate=is_duplicate)
        m = self.get_all_nodes()
        self.load_group_nodes(scene_dict)

        if with_connections:
            self.load_connections(scene_dict)

        if not is_duplicate:
            answer = QMessageBox.question(self.get_main_window(), "Tangle", "Compute network now?", QMessageBox.No, QMessageBox.Yes)
            if answer == QMessageBox.Yes:
                self.refresh_network()

    def load_connections(self, mapped_scene):
        """
        Will recursively find all values of the key "connections" in the given dictionary

        :param mapped_scene: [dictionary] to load the connections from
        :return:
        """
        try:
            for connection_dict in utils.value_extract("connections", mapped_scene):
                for index, connection_list in connection_dict.items():
                    output_socket = self.get_socket_by_uuid(connection_list[0])
                    input_socket = self.get_socket_by_uuid(connection_list[1])
                    SocketConnection(output_socket, input_socket, self, auto_compute_on_connect=False)
        except Exception as err:
            utils.trace(err)

    def load_nodes(self, mapped_scene, with_values, is_duplicate=False):
        """
        Loads the nodes that are saved in the mapped_scene dictionary

        :param mapped_scene: [dict] that holds a saved Tangle network
        :param offset_nodes: [bool] if set to True, will add 20 pixels to the X and Y position of the node when it loads
        :param with_values: [bool] if set to True, will set the values on the sockets
        :return:
        """
        nodes_dict = mapped_scene.get("nodes")
        if nodes_dict is not None:
            for node_uuid, node_dict in nodes_dict.items():
                x = node_dict.get("x")
                y = node_dict.get("y")
                if is_duplicate:
                    x += 20
                    y += 20
                module_path = node_dict.get("module_path")
                class_name = node_dict.get("class_name")
                module_name = node_dict.get("module_name")
                node = self.add_node_to_view(class_name, module_name, x, y)

                if node is not None:
                    node.load(node_dict, is_duplicate=is_duplicate, x=x, y=y)

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

                            if is_duplicate:
                                socket_uuid = uuid.uuid4()
                            socket.set_uuid(socket_uuid)

                            if with_values:
                                socket.set_initial_value(initial_value)
                                socket.set_value(value)
                                node.compute()

    def load_group_nodes(self, mapped_scene):
        group_nodes_dict = mapped_scene.get("group_nodes")
        if group_nodes_dict is not None:
            for _, group_node_dict in group_nodes_dict.items():
                color = QColor(group_node_dict.get("color")[0],
                               group_node_dict.get("color")[1],
                               group_node_dict.get("color")[2],
                               group_node_dict.get("color")[3])
                nodes = []
                for node_uuid in group_node_dict.get("nodes"):
                    nodes.append(self.get_node_by_uuid(node_uuid))
                group_node = GroupNode(self, nodes)
                group_node.set_color(color)

    def align_selected_nodes(self, axis):
        if len(self.get_selected_nodes()) > 0:
            if axis == "horizontal_up":
                y_pos = min([node.pos().y() for node in self.get_selected_nodes()])
                for node in self.get_selected_nodes():
                    node.setPos(node.pos().x(), y_pos)
            if axis == "horizontal_down":
                y_pos = max([node.pos().y() for node in self.get_selected_nodes()])
                for node in self.get_selected_nodes():
                    node.setPos(node.pos().x(), y_pos)

            if axis == "vertical_left":
                x_pos = min([node.pos().x() for node in self.get_selected_nodes()])
                for node in self.get_selected_nodes():
                    node.setPos(x_pos, node.pos().y())
            if axis == "vertical_right":
                x_pos = max([node.pos().x() for node in self.get_selected_nodes()])
                for node in self.get_selected_nodes():
                    node.setPos(x_pos, node.pos().y())

    def duplicate_nodes(self):
        """
        Duplicates the selected nodes

        :return:
        """
        try:
            for node in self.get_selected_nodes():
                node.duplicate()
        except Exception as err:
            utils.trace(err)

    def get_begin_nodes(self):
        """
        Returns a list of all BaseNodes that have no input connections

        :return: [list]
        """
        start_nodes = []
        all_nodes = self.get_all_nodes()

        if len(all_nodes) == 1:
            return all_nodes

        if len(all_nodes) > 1:
            for node in all_nodes:
                if len(node.get_connected_output_sockets()) > 0:
                    if len(node.get_connected_input_sockets()) == 0:
                        start_nodes.append(node)

                if len(node.get_connected_input_sockets()) + len(node.get_connected_output_sockets()) == 0:
                    start_nodes.append(node)

        return start_nodes

    def get_end_nodes(self):
        """
        Returns a list of all BaseNodes that have no output connections

        :return: [list]
        """
        end_nodes = []
        all_nodes = self.get_all_nodes()

        if len(all_nodes) == 1:
            return all_nodes

        if len(all_nodes) > 1:
            for node in all_nodes:
                if len(node.get_connected_input_sockets()) > 0:
                    if len(node.get_connected_output_sockets()) == 0:
                        end_nodes.append(node)

                if len(node.get_connected_input_sockets()) + len(node.get_connected_output_sockets()) == 0:
                    end_nodes.append(node)

        return end_nodes

    def get_selected_nodes(self):
        """
        Returns all selected BaseNodes

        :return: [list]
        """
        return [item for item in self.selectedItems() if issubclass(type(item), BaseNode)]

    def get_selected_group_nodes(self):
        return [item for item in self.selectedItems() if type(item) == GroupNode]

    def delete_nodes(self):
        """
        Deletes the selected BaseNodes by calling destroy_self on them

        :return:
        """
        items = self.selectedItems()
        self.clearSelection()
        for item in items:
            try:
                item.destroy_self()
                if type(item) == GroupNode:
                    if settings().get_value(sc.GroupNodeStrings.delete_nodes_with_group_node, True) is True:
                        item.destroy_nodes()

            except Exception as err:
                utils.trace(err)

    def clear_scene(self):
        """
        Destroys all BaseNodes by calling destroy_self on them

        :return:
        """
        for node in self.get_all_nodes():
            node.destroy_self()

        for group_node in self.get_all_group_nodes():
            group_node.destroy_self()

        ImageViewer(self.get_main_window()).clear()
        GraphViewerFloat(self.get_main_window()).clear()

    def browse_for_save_location(self, selected_nodes_only=False):
        """
        Opens a QFileDialog to save the Tangle network to and then saves the network

        :param selected_nodes_only: [bool] Only saves the selected BaseNodes
        :return:
        """
        file_path = QFileDialog.getSaveFileName(caption="Save Tangle network", filter="Tangle files (*.tngl)")[0]
        if file_path != "":
            if selected_nodes_only:
                self.save_network(selected_nodes_only=True, file_path=file_path)
            else:
                self.save_network(selected_nodes_only=False, file_path=file_path)

    def browse_for_saved_scene(self):
        """
        Open a QFileDialog to open a saved Tangle network and then opens it

        :return:
        """
        file_path = QFileDialog.getOpenFileName(caption="Open Tangle Network", filter="Tangle files (*.tngl)")[0]
        if file_path != "":
            self.open_network(file_path=file_path)

    def group_nodes(self):
        try:
            for group_node in self.get_selected_group_nodes():
                group_node.destroy_self()

            group_node = GroupNode(self, self.get_selected_nodes())
            self.clearSelection()
            group_node.setSelected(True)
        except Exception as err:
            utils.trace(err)

    def dragMoveEvent(self, event):
        event.accept()

    def dropEvent(self, event):
        try:
            class_name = event.source().selectedItems()[0].text(0)
            module = event.source().selectedItems()[0].parent().text(0)

            x = event.scenePos().x()
            y = event.scenePos().y()

            dropped_node = self.add_node_to_view(class_name, module, x, y)
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

        if event.key() == Qt.Key_F5:
            self.get_main_window().show_viewer("image")

        if event.key() == Qt.Key_F6:
            self.get_main_window().show_viewer("graph")

        if event.key() == Qt.Key_G and event.modifiers() == Qt.ControlModifier:
            self.group_nodes()

        if event.key() == Qt.Key_Up and event.modifiers() == Qt.ControlModifier:
            self.align_selected_nodes("horizontal_up")

        if event.key() == Qt.Key_Down and event.modifiers() == Qt.ControlModifier:
            self.align_selected_nodes("horizontal_down")

        if event.key() == Qt.Key_Left and event.modifiers() == Qt.ControlModifier:
            self.align_selected_nodes("vertical_left")

        if event.key() == Qt.Key_Right and event.modifiers() == Qt.ControlModifier:
            self.align_selected_nodes("vertical_right")

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

