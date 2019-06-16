from nv_NodeEditor.nodes.base_node import BaseNode
import nv_NodeEditor.socket_types as socket_types

import pymel.core as pm

class Selection(BaseNode):
    def __init__(self, scene, x=0, y=0):
        super(Selection, self).__init__(scene, x=x, y=y)
        self.change_title("[Maya] Selection")

        self.output = self.add_output(socket_types.ListSocketType(self), "selection")
        self.output.set_initial_value([])

    def compute(self):
        if len(pm.selected()) > 0:
            objects = [node.name() for node in pm.selected()]
            self.output.set_value(objects)
        else:
            self.set_value([])

        print self.output.get_value()