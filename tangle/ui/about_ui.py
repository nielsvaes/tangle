# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'about.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_tangle_about(object):
    def setupUi(self, tangle_about):
        if not tangle_about.objectName():
            tangle_about.setObjectName(u"tangle_about")
        tangle_about.setWindowModality(Qt.ApplicationModal)
        tangle_about.resize(276, 475)
        self.gridLayout = QGridLayout(tangle_about)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.lbl_logo = QLabel(tangle_about)
        self.lbl_logo.setObjectName(u"lbl_logo")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_logo.sizePolicy().hasHeightForWidth())
        self.lbl_logo.setSizePolicy(sizePolicy)
        self.lbl_logo.setMinimumSize(QSize(256, 256))
        self.lbl_logo.setMaximumSize(QSize(256, 256))
        font = QFont()
        font.setFamily(u"Verdana")
        font.setPointSize(60)
        self.lbl_logo.setFont(font)
        self.lbl_logo.setScaledContents(True)
        self.lbl_logo.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.lbl_logo)

        self.lbl_title = QLabel(tangle_about)
        self.lbl_title.setObjectName(u"lbl_title")
        font1 = QFont()
        font1.setFamily(u"Verdana")
        font1.setPointSize(40)
        self.lbl_title.setFont(font1)
        self.lbl_title.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.lbl_title)

        self.lbl_version = QLabel(tangle_about)
        self.lbl_version.setObjectName(u"lbl_version")
        font2 = QFont()
        font2.setFamily(u"Verdana")
        font2.setPointSize(10)
        self.lbl_version.setFont(font2)
        self.lbl_version.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.verticalLayout.addWidget(self.lbl_version)

        self.lbl_logo_2 = QLabel(tangle_about)
        self.lbl_logo_2.setObjectName(u"lbl_logo_2")
        self.lbl_logo_2.setFont(font2)
        self.lbl_logo_2.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.verticalLayout.addWidget(self.lbl_logo_2)

        self.lbl_logo_3 = QLabel(tangle_about)
        self.lbl_logo_3.setObjectName(u"lbl_logo_3")
        self.lbl_logo_3.setFont(font2)
        self.lbl_logo_3.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.verticalLayout.addWidget(self.lbl_logo_3)

        self.lbl_website = QLabel(tangle_about)
        self.lbl_website.setObjectName(u"lbl_website")
        self.lbl_website.setFont(font2)
        self.lbl_website.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.verticalLayout.addWidget(self.lbl_website)


        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 2)

        self.btn_close = QPushButton(tangle_about)
        self.btn_close.setObjectName(u"btn_close")

        self.gridLayout.addWidget(self.btn_close, 2, 1, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 2, 0, 1, 1)

        self.line = QFrame(tangle_about)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.gridLayout.addWidget(self.line, 1, 0, 1, 2)


        self.retranslateUi(tangle_about)

        QMetaObject.connectSlotsByName(tangle_about)
    # setupUi

    def retranslateUi(self, tangle_about):
        tangle_about.setWindowTitle(QCoreApplication.translate("tangle_about", u"Tangle - About", None))
        self.lbl_logo.setText("")
        self.lbl_title.setText(QCoreApplication.translate("tangle_about", u"Tangle", None))
        self.lbl_version.setText(QCoreApplication.translate("tangle_about", u"0.0", None))
        self.lbl_logo_2.setText(QCoreApplication.translate("tangle_about", u"Niels Vaes", None))
        self.lbl_logo_3.setText(QCoreApplication.translate("tangle_about", u"nielsvaes@gmail.com", None))
        self.lbl_website.setText(QCoreApplication.translate("tangle_about", u"www.nielsvaes.be", None))
        self.btn_close.setText(QCoreApplication.translate("tangle_about", u"Close", None))
    # retranslateUi

