from nv_utils import io_utils

MAYA_CMDS_DICT = io_utils.read_json("maya_cmds.json")


class MayaCommand(object):
    def __init__(self, command_name):
        super().__init__()

        self.command = MAYA_CMDS_DICT.get(command_name, None)


class MayaCommandArgument(object):
    def __init__(self, argument_dict):
        super().__init__()
        self.name = argument_dict.get("")

    def __fetch_argument(self):


def get_command(command_name):
    return MAYA_CMDS_DICT.get(command_name, None)

def get_arguments(command_name):
    return get_command(command_name).get("arguments", [])

def is_queryable(command_name):
    return get_command(command_name).get("queryable", None)

def is_undoable(command_name):
    return get_command(command_name).get("undoable", None)

def is_editable(command_name):
    return get_command(command_name).get("editable", None)

def get_argument_name(command_name, argument_name):

