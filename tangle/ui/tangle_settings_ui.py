# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'tangle_settings.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_tangle_settings(object):
    def setupUi(self, tangle_settings):
        if not tangle_settings.objectName():
            tangle_settings.setObjectName(u"tangle_settings")
        tangle_settings.setWindowModality(Qt.ApplicationModal)
        tangle_settings.resize(631, 220)
        self.gridLayout_2 = QGridLayout(tangle_settings)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.groupBox = QGroupBox(tangle_settings)
        self.groupBox.setObjectName(u"groupBox")
        self.gridLayout = QGridLayout(self.groupBox)
        self.gridLayout.setObjectName(u"gridLayout")
        self.chk_delete_nodes_with_group_node = QCheckBox(self.groupBox)
        self.chk_delete_nodes_with_group_node.setObjectName(u"chk_delete_nodes_with_group_node")

        self.gridLayout.addWidget(self.chk_delete_nodes_with_group_node, 0, 0, 1, 1)

        self.chk_show_help_text_in_node_ui = QCheckBox(self.groupBox)
        self.chk_show_help_text_in_node_ui.setObjectName(u"chk_show_help_text_in_node_ui")
        self.chk_show_help_text_in_node_ui.setChecked(True)

        self.gridLayout.addWidget(self.chk_show_help_text_in_node_ui, 1, 0, 1, 1)


        self.gridLayout_2.addWidget(self.groupBox, 0, 0, 1, 2)

        self.horizontalSpacer = QSpacerItem(527, 22, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer, 4, 0, 1, 1)

        self.btn_save = QPushButton(tangle_settings)
        self.btn_save.setObjectName(u"btn_save")

        self.gridLayout_2.addWidget(self.btn_save, 4, 1, 1, 1)

        self.line = QFrame(tangle_settings)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.gridLayout_2.addWidget(self.line, 3, 0, 1, 2)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_2.addItem(self.verticalSpacer, 2, 0, 1, 1)

        self.groupBox_2 = QGroupBox(tangle_settings)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.gridLayout_3 = QGridLayout(self.groupBox_2)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.chk_high_quality_view = QCheckBox(self.groupBox_2)
        self.chk_high_quality_view.setObjectName(u"chk_high_quality_view")
        self.chk_high_quality_view.setChecked(True)

        self.gridLayout_3.addWidget(self.chk_high_quality_view, 0, 0, 1, 1)


        self.gridLayout_2.addWidget(self.groupBox_2, 1, 0, 1, 2)


        self.retranslateUi(tangle_settings)

        QMetaObject.connectSlotsByName(tangle_settings)
    # setupUi

    def retranslateUi(self, tangle_settings):
        tangle_settings.setWindowTitle(QCoreApplication.translate("tangle_settings", u"Tangle - Settings", None))
        self.groupBox.setTitle(QCoreApplication.translate("tangle_settings", u"Nodes", None))
        self.chk_delete_nodes_with_group_node.setText(QCoreApplication.translate("tangle_settings", u"Delete nodes when group node is deleted", None))
        self.chk_show_help_text_in_node_ui.setText(QCoreApplication.translate("tangle_settings", u"Show help text in node ui", None))
        self.btn_save.setText(QCoreApplication.translate("tangle_settings", u"Save", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("tangle_settings", u"Application", None))
        self.chk_high_quality_view.setText(QCoreApplication.translate("tangle_settings", u"High quality view", None))
    # retranslateUi

