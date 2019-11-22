import os
import importlib

import re

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import nv_utils.utils as utils
import nv_utils.io as io_utils

from pydoc import locate

from core.Constants import Colors
from core.Node import Node

class NodeScene(QGraphicsScene):
    refreshed = pyqtSignal()

    def __init__(self):
        super(NodeScene, self).__init__()
        self.__set_colors_computed()


    def add_node_to_view(self, class_name, module, x=0, y=0):
        node_instance = None

        if type(class_name) == str:
            print(class_name)
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
                node_instance = class_name.__class__(self, x, y)
            except:
                utils.trace("Can't create node of type %s" % class_name)
                return None

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

    def get_all_connections(self):
        from core.SocketConnection import SocketConnection
        connections = []
        for item in self.items():
            if type(item) == SocketConnection:
                connections.append(item)

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

    def save_network(self):
        # print("Saving scene")
        # path = r"C:/deleteme/mapped_scene.json"
        # mapped_scene = {}
        # for node in self.get_all_nodes():
        #     node_dict = node.save()
        #
        #     mapped_scene[node.get_uuid(as_string=True)] = node_dict
        # #
        # # with open(path, "wb") as out:
        # #     pickle.dump(mapped_scene, out)
        #
        # with open(path, "w") as out:
        #     json.dump(mapped_scene, out, indent=4)

        path = r"C:/deleteme/mapped_scene.json"

        save_dict = {}

        for node in self.get_all_nodes():
            save_dict[node.get_uuid(as_string=True)] = node.save()

        io_utils.write_json(save_dict, path)




    def open_network(self, path):
        mapped_scene = io_utils.read_json(r"C:/deleteme/mapped_scene.json")

        for node_uuid, node_dict in mapped_scene.items():
            type_string = node_dict.get("node_type")
            print(type(type_string))
            other = re.findall(r"'(.*?)'", type_string, re.DOTALL)[0]
            class_name = other.split(".")[-1]
            print(class_name)



        # node_dict = OrderedDict()
        # for begin_node in self.get_begin_nodes():
        #     for attribute in vars(begin_node):
        #     # for index, attribute in enumerate(begin_node.__dict__):
        #         node_dict[begin_node.get_uuid(as_string=True)] = {}
        #         node_dict[begin_node.get_uuid(as_string=True)][attribute] = getattr(begin_node, attribute)
        #
        # for key, value in enumerate(node_dict):
        #     print(key)
        #     print(value)

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

    # def drawBackground(self, painter, rect):
    #     super().drawBackground(painter, rect)
    #     grid_size = 20
    #
    #     left = int(rect.left()) - (int(rect.left()) % grid_size)
    #     top = int(rect.top()) - (int(rect.top()) % grid_size)
    #
    #     for x in range(left,

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
        self.refresh_network()

        if event.key() == Qt.Key_D and event.modifiers() == Qt.ControlModifier:
            self.duplicate_nodes()

        if event.key() == Qt.Key_S and event.modifiers() == Qt.ControlModifier:
            self.save_network()


        if event.key() == Qt.Key_O and event.modifiers() == Qt.ControlModifier:
            self.open_network("D:/mapped_scene")

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

