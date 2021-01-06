# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'login.ui'
##
## Created by: Qt User Interface Compiler version 6.0.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class Ui_Login(object):
    def setupUi(self, Login):
        if not Login.objectName():
            Login.setObjectName(u"Login")
        Login.resize(400, 100)
        
        self.centralwidget = QWidget(Login)
        self.centralwidget.setObjectName(u"centralwidget")
        self.glCent = QGridLayout(self.centralwidget)
        self.glCent.setObjectName(u"glCent")
        
        self.lbTitlePath = QLabel(self.centralwidget)
        self.lbTitlePath.setObjectName(u"lbTitlePath")
        self.lbTitlePath.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.glCent.addWidget(self.lbTitlePath, 2, 0, 1, 1)

        self.lbTitlePass = QLabel(self.centralwidget)
        self.lbTitlePass.setObjectName(u"lbTitlePass")
        self.lbTitlePass.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.glCent.addWidget(self.lbTitlePass, 0, 2, 1, 1)

        self.lnPath = QLineEdit(self.centralwidget)
        self.lnPath.setObjectName(u"lnPath")
        self.glCent.addWidget(self.lnPath, 2, 1, 1, 3)

        self.lnPass = QLineEdit(self.centralwidget)
        self.lnPass.setObjectName(u"lnPass")
        self.lnPass.setEchoMode(QLineEdit.Password)
        self.glCent.addWidget(self.lnPass, 0, 3, 1, 1)

        self.lbTitleUser = QLabel(self.centralwidget)
        self.lbTitleUser.setObjectName(u"lbTitleUser")
        self.lbTitleUser.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.glCent.addWidget(self.lbTitleUser, 0, 0, 1, 1)

        self.lnUser = QLineEdit(self.centralwidget)
        self.lnUser.setObjectName(u"lnUser")
        self.glCent.addWidget(self.lnUser, 0, 1, 1, 1)

        self.widBot = QWidget(self.centralwidget)
        self.widBot.setObjectName(u"widBot")
        self.hlBot = QHBoxLayout(self.widBot)
        self.hlBot.setObjectName(u"hlBot")
        self.hlBot.setContentsMargins(0, 0, 0, 0)
        self.chkEnc = QCheckBox(self.widBot)
        self.chkEnc.setObjectName(u"chkEnc")


        self.hlBot.addWidget(self.chkEnc)

        self.sp = QSpacerItem(196, 21, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.hlBot.addItem(self.sp)

        self.btnConnect = QPushButton(self.widBot)
        self.btnConnect.setObjectName(u"btnConnect")
        self.hlBot.addWidget(self.btnConnect)

        self.glCent.addWidget(self.widBot, 3, 0, 1, 4)


        Login.setCentralWidget(self.centralwidget)

        self.retranslateUi(Login)

        QMetaObject.connectSlotsByName(Login)
    # setupUi

    def retranslateUi(self, Login):
        Login.setWindowTitle(QCoreApplication.translate("Login", u"\uc11c\ubc84 \ub85c\uadf8\uc778", None))
        self.lbTitlePath.setText(QCoreApplication.translate("Login", u"\uc11c\ubc84 \uc8fc\uc18c: ", None))
        self.lbTitlePass.setText(QCoreApplication.translate("Login", u"\uc554\ud638: ", None))
        self.lnPath.setPlaceholderText(QCoreApplication.translate("Login", u"/data.json", None))
        self.lnPass.setPlaceholderText(QCoreApplication.translate("Login", u"hys.moneymanage", None))
        self.lbTitleUser.setText(QCoreApplication.translate("Login", u"\uc0ac\uc6a9\uc790\uba85: ", None))
        self.lnUser.setPlaceholderText(QCoreApplication.translate("Login", u"anonymous", None))
        self.chkEnc.setText(QCoreApplication.translate("Login", u"\uc554\ud638\ud654?", None))
        self.btnConnect.setText(QCoreApplication.translate("Login", u"\uc5f0\uacb0", None))
    # retranslateUi

