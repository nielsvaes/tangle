import traceback
import os
import logging

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic


from pydoc import locate

from core.Constants import Colors

class NodeScene(QGraphicsScene):
    refreshed = pyqtSignal()

    def __init__(self):
        super(NodeScene, self).__init__()
        self.__set_colors_computed()


    def add_node_to_view(self, class_name, module, x=0, y=0):
        if type(class_name) == str:
            class_path = ".".join(["CocoEdit", "nodes", module, class_name, class_name])
            node_class = locate(class_path)
            node_instance = node_class(self, x, y)
        else:
            node_instance = class_name.__class__(self, x, y)

        for socket_type in node_instance.get_all_socket_types():
            socket_type.is_dirty.connect(self.__set_colors_dirty)

        self.__set_colors_dirty()

        return node_instance


    def get_all_nodes(self):
        from nodes.base_node import BaseNode
        nodes = []
        for item in self.items():
            if issubclass(type(item), BaseNode):
                nodes.append(item)

        return nodes

    def get_all_non_executing_nodes(self):
        from nodes.base_node import BaseNode
        nodes = []
        for node in self.items():
            if issubclass(type(node), BaseNode):
                if not node.is_executing_node():
                    nodes.append(node)

        return nodes

    def get_all_executing_nodes(self):
        executing_nodes = []
        for node in self.get_all_nodes():
            if node.is_executing_node():
                executing_nodes.append(node)

        return executing_nodes

    def get_nonexisting_name(self, name):
        for node in self.get_all_nodes():
            if name == node.name:
                pass
            #TODO: generate unique name, now battlefield

    def get_view(self):
        return self.views()[0]

    def refresh_network(self, node=None):
        try:
            if node is None:
                for begin_node in self.get_begin_nodes():
                    begin_node.compute()

                    for connected_node in begin_node.get_connected_output_nodes():
                        self.refresh_network(node=connected_node)
            else:
                # node.is_computed.connect(self.__set_colors_computed)
                node.refresh()
                for connected_node in node.get_connected_output_nodes():
                    self.refresh_network(node=connected_node)

                    for socket_type in connected_node.get_all_socket_types():
                        socket_type.is_dirty.connect(self.__set_colors_dirty)
                        socket_type.get_ui()

            self.__set_colors_computed()
            self.refreshed.emit()
        except Exception as err:
            logging.debug(traceback.format_exc(5))

    def get_begin_nodes(self):
        start_nodes = []
        non_executing_nodes = self.get_all_non_executing_nodes()

        if len(non_executing_nodes) == 1:
            return non_executing_nodes

        if len(non_executing_nodes) > 1:
            for node in non_executing_nodes:
                if len(node.get_connected_output_sockets()) > 0:
                    if len(node.get_connected_input_sockets()) == 0:
                        start_nodes.append(node)

        return start_nodes

    def get_begin_executing_node(self):
        start_nodes = []

        executing_nodes = self.get_all_executing_nodes()
        if len(executing_nodes) == 1:
            return executing_nodes[0]

        if len(executing_nodes) > 1:
            for node in executing_nodes:
                try:
                    if node.is_execution_connected():
                        if node.is_execution_output_connected() and not node.is_execution_input_connected():
                            start_nodes.append(node)
                    else:
                        start_nodes.append(node)
                except AttributeError as err:
                    pass

            if len(start_nodes) == 1:
                return start_nodes[0]

        if len(executing_nodes) == 0:
            raise RuntimeError("There is no executing node in the scene!")


        raise RuntimeError("There are multiple nodes that have their out ExecutionSocket connected but not their input ExecutionSocket. This is invalid for the graph!\nPotential invalid nodes are: %s" % [start_node.name for start_node in start_nodes])

    def is_cyclical(self):
        try:
            self.get_begin_executing_node()
            return False
        except:
            pass

        result = True
        for node in self.get_all_executing_nodes():
            if not node.is_execution_output_connected() or not node.is_execution_input_connected:
                result = False

        return result

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
        class_name = event.source().selectedItems()[0].text(0)
        module = event.source().selectedItems()[0].parent().text(0)

        x = event.scenePos().x()
        y = event.scenePos().y()

        self.add_node_to_view(class_name, module, x, y)

    def keyPressEvent(self, event):
        #from nodes.base_node import BaseNode
        if event.key() == Qt.Key_Delete:
            selected_nodes = self.selectedItems()
            self.clearSelection()
            for item in selected_nodes:
                try:
                    item.destroy_self()
                except Exception as err:
                    pass
            if len(self.items()) == 0:
                self.__set_colors_computed()

        if event.key() == Qt.Key_D and event.modifiers() == Qt.ControlModifier:
            self.duplicate_nodes()

        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.refresh_network()
            # print "enter"
            # for item in self.items():
            #     if issubclass(type(item), BaseNode):
            #         try:
            #
            #         except StandardError, err:
            #             print "Can't refresh network"
            #             print err
            #             pass
        # else:
        #     super(NodeScene, self).keyPressEvent(event)

    def __set_colors_dirty(self):
        brush = QBrush()
        brush.setStyle(Qt.SolidPattern)
        brush.setColor(Colors.node_scene_dirty)
        self.setBackgroundBrush(brush)

    def __set_colors_computed(self):
        brush = QBrush()
        brush.setStyle(Qt.SolidPattern)
        brush.setColor(Colors.node_scene_computed)
        self.setBackgroundBrush(brush)

