from nv_NodeEditor.nodes.base_node import BaseNode
import nv_NodeEditor.socket_types as socket_types

import pymel.core as pm

class SetPosition(BaseNode):
    def __init__(self, scene, x=0, y=0):
        super(SetPosition, self).__init__(scene, x=x, y=y)
        self.change_title("[Maya] Set Position")

        self.selection_input = self.add_input(socket_types.ListSocketType(self), "selection")
        self.position_vector = self.add_input(socket_types.Vector3SocketType(self), "position")

    def compute(self):
        print "computing set pos"
        if self.selection_input.get_value() is not None:
            for transform in self.selection_input.get_value():
                transform = pm.PyNode(transform)
                print self.position_vector.get_value()
                transform.setTranslation(self.position_vector.get_value(), space="world")
