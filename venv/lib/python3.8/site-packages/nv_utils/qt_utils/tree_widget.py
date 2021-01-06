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




def get_text_from_selected_items(tree_widget, column_index):
    """
    Returns the text of the selected treeWidgetItems as a list of string

    :param tree_widget: your QTreeWidget
    :param column_index: <int> number of the column you want to ge the text from
    :return:
    """
    text_list = []
    model_indexes = tree_widget.selectedIndexes()
    for model_index in model_indexes:
        item = tree_widget.itemFromIndex(model_index)

        text_list.append(item.text(column_index))

    return text_list

def get_item_with_text(tree_widget, text, column_index):
    """
    Returns a QTreeWidgetItem that matches the selected text for the selected column

    :param tree_widget: QTreeWidget you want to search in
    :param text: <string> text
    :param column_index: <int> column number
    :return: QTreeWidgetItem if found or None if not found
    """
    try:
        iterator = QTreeWidgetItemIterator(tree_widget)
        while iterator:
            if iterator.value().text(column_index) == text:
                return iterator.value()
            iterator +=1
    except:
        return None

    return None

def remove_items(tree_widget, items=[], selected=False):
    """
    Removes the passed items from the tree widget

    :param tree_widget: QTreeWidget to remove items from
    :param items: <list> items you want to remove
    :param selected: <bool> if set to True, will remove the selected items
    :return:
    """
    if selected == True:
        items = tree_widget.selectedItems()

    root = tree_widget.invisibleRootItem()
    for item in items:
        (item.parent() or root).removeChild(item)

def set_item_background_color(tree_widget_item, q_color, columns="all"):
    """
    Sets the background color of a QTreeWidget

    :param tree_widget_item: QTreeWidget you want to color
    :param q_color: <QColor> the color as a QColor (eg: QColor(255, 0, 0, 255)
    :param columns: <string> | <list> either the string "all" to color all columns or a list of ints with specific column numbers
    :return:
    """
    if columns == "all":
        for column in range(tree_widget_item.columnCount()):
            tree_widget_item.setBackground(column, q_color)
    else:
        for column in columns:
            tree_widget_item.setBackground(column, q_color)

def resize_columns(tree_widget, columns="all"):
    """
    Sets the column size to the minimal amount needed

    :param tree_widget: QTreeWidget you want to restructure
    :param columns: <string> | <list> either the string "all" or a list with specific column numbers
    :return:
    """
    if columns == "all":
        for column in range(tree_widget.columnCount()):
            tree_widget.resizeColumnToContents(column)
    else:
        for column in columns:
            tree_widget.resizeColumnToContents(column)

def get_all_top_level_items(tree_widget):
    """
    Returns all the top level items of the QTreeWidget

    :param tree_widget: your QTreeWidget
    :return: list of QTreeWidgetItems
    """

    items = []
    for index in range(tree_widget.topLevelItemCount()):
        items.append(tree_widget.topLevelItem(index))
    return items

def get_all_under_item(item):
    """
    Returns all the children of a specific QTreeWidgetItem

    :param item: <QTreeWidgetItem>
    :return: <list> QTreeWidgetItems
    """
    items = []
    for index in range(item.childCount()):
        items.append(item.child(index))
        items.extend(get_all_under_item(item.child(index)))
    return items

def get_all_items(tree_widget):
    """
    Returns all the items of a QTreeWidget

    :param tree_widget: your QTreeWidget
    :return: <list>  QTreeWidgetItems
    """

    all_items = []
    for i in range(tree_widget.topLevelItemCount()):
        top_level_item = tree_widget.topLevelItem(i)
        all_items.append(top_level_item)
        all_items.extend(get_all_under_item(top_level_item))
    return all_items