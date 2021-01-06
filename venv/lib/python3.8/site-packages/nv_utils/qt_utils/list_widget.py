try:
    from PySide2.QtCore import *
    from PySide2.QtUiTools import *
    from PySide2.QtGui import *
    from PySide2.QtWidgets import *
except:
    from PyQt5.QtCore import *
    from PyQt5.QtUiTools import *
    from PyQt5.QtGui import *
    from PyQt5.QtWidgets import *


def add_items(list_widget, items, duplicates_allowed=False, string_split_character=None, clear=False):
    """
    Convenience function to add items to your list widget

    :param list_widget: your QListWidget
    :param items: <string> | <list> a single string item ("option"), a list (["option_1", "option_2"]), or a string that can be split on a character like a comma separated string ("option_1, option_2")
    :param duplicates_allowed: <bool> >whether or not to allow duplicates
    :param string_split_character: <string> split the string on this character (eg: ","), the result is the list of items that get added to the list widget
    :param clear: <bool> whether or not to clear the listWidget first
    :return:
    """
    if not isinstance(items, (list, tuple)):
        if isinstance(items, str) and string_split_character is not None and string_split_character in items:
            tmp_list = [part.strip() for part in items.split(string_split_character)]
            items = tmp_list
        elif isinstance(items, str) and items == "":
            return
        else:
            items = [items]

    if clear is True:
        list_widget.clear()

    for item in items:
        if duplicates_allowed is True:
            list_widget.addItem(item)
        else:
            if len(list_widget.findItems(item, Qt.MatchExactly)) == 0 and item is not None:
                list_widget.addItem(item)

def remove_items(list_widget, items=None, selected=False, string_split_character=None):
    """
    Convenience function to remove items from a listWidget

    :param list_widget: your QListWidget
    :param items: <string> | <list> a single string item ("option"), a list (["option_1", "option_2"]), or a string that can be split on a character like a comma separated string ("option_1, option_2")
    :param string_split_character: <string> split the string on this character (eg: ","), the result is the list of items that get added to the listWidget
    :param selected: <bool> if set to true, the deletion will only happen in the listWidgetItems that are currently selected
    :return:
    """
    if items is not None:
        if not isinstance(items, (list, tuple)):
            if isinstance(items, str) and string_split_character is not None and string_split_character in items:
                tmpList = [part.strip() for part in items.split(string_split_character)]
                items = tmpList
            else:
                items = [items]

    if selected:
        items = list_widget.selectedItems()

    for item in items:
        list_widget.takeItem(list_widget.row(item))

def get_all_items(list_widget, as_string=True):
    """
    Gets all the items in a listWidget as a list

    :param list_widget: your QListWidget
    :param as_string: <bool> if set to true, will return the text of the item. If set to false will return the actual QListWidgetItem
    :return: items of your QListWidget
    """
    items = []

    if as_string is True:
        for item in [list_widget.item(i).text() for i in
                     range(list_widget.count())]:
            if item is not None:
                items.append(item)
    else:
        for item in range(list_widget.count()):
            items.append(item)

    return items
