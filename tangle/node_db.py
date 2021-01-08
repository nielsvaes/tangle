import os
import logging
logging.basicConfig(level=logging.INFO)

import ez_utils.io_utils as io_utils

SCRIPT_FOLDER = os.path.dirname(os.path.realpath(__file__))
UI_PATH = os.path.join(SCRIPT_FOLDER, "ui")
SETTINGS_PATH = os.path.join(SCRIPT_FOLDER, "settings", "tangle_settings.json")
NODE_INFO_DB = os.path.join(SCRIPT_FOLDER, "settings", "node_info.json")
ICONS_PATH = os.path.join(SCRIPT_FOLDER, "ui", "icons")
NODE_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), "nodes")

def generate_database(node_items, scene):
    nodes_dict_list = []
    for node_item in node_items:
        try:
            temp_node = scene.add_node_to_view(node_item.file_name_no_ext, node_item.folder_name)

            node_dict = {}
            node_dict["name"] = node_item.file_name_no_ext
            node_dict["module"] = node_item.folder_name
            node_dict["inputs"] = [socket.socket_type.name for socket in temp_node.get_all_input_sockets()]
            node_dict["outputs"] = [socket.socket_type.name for socket in temp_node.get_all_output_sockets()]

            nodes_dict_list.append(node_dict)

            temp_node.destroy_self()
        except Exception as err:
            logging.error(err)
    io_utils.write_json(nodes_dict_list, NODE_INFO_DB)

def get_node_dicts_with_input_of_type(input_type):
    node_dicts = []
    for node_dict in io_utils.read_json(NODE_INFO_DB):
        for input in node_dict.get("inputs"):
            if input == input_type:
                node_dicts.append(node_dict)
    return node_dicts

def get_node_dicts_with_output_of_type(output_type):
    node_dicts = []
    for node_dict in io_utils.read_json(NODE_INFO_DB):
        for output in node_dict.get("outputs"):
            if output == output_type:
                node_dicts.append(node_dict)
    return node_dicts

