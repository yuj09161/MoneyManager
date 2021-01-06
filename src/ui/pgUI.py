# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'pg.ui'
##
## Created by: Qt User Interface Compiler version 6.0.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class Ui_Pg(object):
    def setupUi(self, Pg):
        if not Pg.objectName():
            Pg.setObjectName(u"Pg")
        Pg.setFixedSize(200, 70)
        
        self.centralwidget = QWidget(Pg)
        self.centralwidget.setObjectName(u"centralwidget")
        self.vlCent = QVBoxLayout(self.centralwidget)
        self.vlCent.setObjectName(u"vlCent")
        
        self.lbStatus = QLabel(self.centralwidget)
        self.lbStatus.setObjectName(u"lbStatus")
        self.lbStatus.setAlignment(Qt.AlignCenter)
        self.vlCent.addWidget(self.lbStatus)

        self.pgPg = QProgressBar(self.centralwidget)
        self.pgPg.setObjectName(u"pgPg")
        self.pgPg.setValue(24)
        self.vlCent.addWidget(self.pgPg)

        Pg.setCentralWidget(self.centralwidget)

        self.retranslateUi(Pg)

        QMetaObject.connectSlotsByName(Pg)
    # setupUi

    def retranslateUi(self, Pg):
        Pg.setWindowTitle(QCoreApplication.translate("Pg", u"\uc9c4\ud589 \uc911", None))
        self.lbStatus.setText(QCoreApplication.translate("Pg", u"TextLabel", None))
    # retranslateUi

