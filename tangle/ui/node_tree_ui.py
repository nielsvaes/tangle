# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'node_tree.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(544, 722)
        self.gridLayout = QGridLayout(Form)
        self.gridLayout.setObjectName(u"gridLayout")
        self.txt_search_nodes = QLineEdit(Form)
        self.txt_search_nodes.setObjectName(u"txt_search_nodes")

        self.gridLayout.addWidget(self.txt_search_nodes, 0, 0, 1, 1)

        self.tree_nodes = QTreeWidget(Form)
        self.tree_nodes.setObjectName(u"tree_nodes")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tree_nodes.sizePolicy().hasHeightForWidth())
        self.tree_nodes.setSizePolicy(sizePolicy)
        self.tree_nodes.setMinimumSize(QSize(150, 0))
        self.tree_nodes.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree_nodes.setStyleSheet(u"font: 9pt \"MS Shell Dlg 2\";")
        self.tree_nodes.setDragEnabled(True)
        self.tree_nodes.setAlternatingRowColors(False)
        self.tree_nodes.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tree_nodes.setSortingEnabled(True)
        self.tree_nodes.setAnimated(True)
        self.tree_nodes.setHeaderHidden(False)
        self.tree_nodes.header().setVisible(True)

        self.gridLayout.addWidget(self.tree_nodes, 1, 0, 1, 1)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.txt_search_nodes.setPlaceholderText(QCoreApplication.translate("Form", u"Search node", None))
        ___qtreewidgetitem = self.tree_nodes.headerItem()
        ___qtreewidgetitem.setText(3, QCoreApplication.translate("Form", u"ParentFolder", None));
        ___qtreewidgetitem.setText(2, QCoreApplication.translate("Form", u"FolderName", None));
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("Form", u"CompletePath", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("Form", u"Nodes", None));
    # retranslateUi

