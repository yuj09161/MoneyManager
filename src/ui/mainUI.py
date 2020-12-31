# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.0.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class Ui_MoneyManage(object):
    def setupUi(self, MoneyManage):
        if not MoneyManage.objectName():
            MoneyManage.setObjectName(u"MoneyManage")
        MoneyManage.resize(800, 600)
        self.acLoad = QAction(MoneyManage)
        self.acLoad.setObjectName(u"acLoad")
        self.acSave = QAction(MoneyManage)
        self.acSave.setObjectName(u"acSave")
        self.acSaveAs = QAction(MoneyManage)
        self.acSaveAs.setObjectName(u"acSaveAs")
        self.acExit = QAction(MoneyManage)
        self.acExit.setObjectName(u"acExit")
        self.acOpenLicense = QAction(MoneyManage)
        self.acOpenLicense.setObjectName(u"acOpenLicense")
        self.acLicense = QAction(MoneyManage)
        self.acLicense.setObjectName(u"acLicense")
        self.acInfo = QAction(MoneyManage)
        self.acInfo.setObjectName(u"acInfo")
        self.centralwidget = QWidget(MoneyManage)
        self.centralwidget.setObjectName(u"centralwidget")
        self.glCent = QGridLayout(self.centralwidget)
        self.glCent.setObjectName(u"glCent")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabCate = QWidget()
        self.tabCate.setObjectName(u"tabCate")
        self.glCate = QGridLayout(self.tabCate)
        self.glCate.setObjectName(u"glCate")
        self.gbSrc = QGroupBox(self.tabCate)
        self.gbSrc.setObjectName(u"gbSrc")
        self.hlSrc = QHBoxLayout(self.gbSrc)
        self.hlSrc.setObjectName(u"hlSrc")
        self.widSrcAdd = QWidget(self.gbSrc)
        self.widSrcAdd.setObjectName(u"widSrcAdd")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widSrcAdd.sizePolicy().hasHeightForWidth())
        self.widSrcAdd.setSizePolicy(sizePolicy)
        self.hlSrcAdd = QHBoxLayout(self.widSrcAdd)
        self.hlSrcAdd.setObjectName(u"hlSrcAdd")
        self.lnSrcAdd = QLineEdit(self.widSrcAdd)
        self.lnSrcAdd.setObjectName(u"lnSrcAdd")

        self.hlSrcAdd.addWidget(self.lnSrcAdd)

        self.btnSrcAdd = QPushButton(self.widSrcAdd)
        self.btnSrcAdd.setObjectName(u"btnSrcAdd")

        self.hlSrcAdd.addWidget(self.btnSrcAdd)


        self.hlSrc.addWidget(self.widSrcAdd)

        self.lineSrc = QFrame(self.gbSrc)
        self.lineSrc.setObjectName(u"lineSrc")
        self.lineSrc.setFrameShape(QFrame.VLine)
        self.lineSrc.setFrameShadow(QFrame.Sunken)

        self.hlSrc.addWidget(self.lineSrc)

        self.widSrcDel = QWidget(self.gbSrc)
        self.widSrcDel.setObjectName(u"widSrcDel")
        sizePolicy.setHeightForWidth(self.widSrcDel.sizePolicy().hasHeightForWidth())
        self.widSrcDel.setSizePolicy(sizePolicy)
        self.hlSrcDel = QHBoxLayout(self.widSrcDel)
        self.hlSrcDel.setObjectName(u"hlSrcDel")
        self.cbSrcDel = QComboBox(self.widSrcDel)
        self.cbSrcDel.setObjectName(u"cbSrcDel")

        self.hlSrcDel.addWidget(self.cbSrcDel)

        self.btnSrcDel = QPushButton(self.widSrcDel)
        self.btnSrcDel.setObjectName(u"btnSrcDel")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.btnSrcDel.sizePolicy().hasHeightForWidth())
        self.btnSrcDel.setSizePolicy(sizePolicy1)

        self.hlSrcDel.addWidget(self.btnSrcDel)


        self.hlSrc.addWidget(self.widSrcDel)


        self.glCate.addWidget(self.gbSrc, 0, 0, 1, 1)

        self.gbInDet = QGroupBox(self.tabCate)
        self.gbInDet.setObjectName(u"gbInDet")
        self.hlIn = QHBoxLayout(self.gbInDet)
        self.hlIn.setObjectName(u"hlIn")
        self.widInAdd = QWidget(self.gbInDet)
        self.widInAdd.setObjectName(u"widInAdd")
        sizePolicy.setHeightForWidth(self.widInAdd.sizePolicy().hasHeightForWidth())
        self.widInAdd.setSizePolicy(sizePolicy)
        self.hlInAdd = QHBoxLayout(self.widInAdd)
        self.hlInAdd.setObjectName(u"hlInAdd")
        self.lnInAdd = QLineEdit(self.widInAdd)
        self.lnInAdd.setObjectName(u"lnInAdd")

        self.hlInAdd.addWidget(self.lnInAdd)

        self.btnInAdd = QPushButton(self.widInAdd)
        self.btnInAdd.setObjectName(u"btnInAdd")

        self.hlInAdd.addWidget(self.btnInAdd)


        self.hlIn.addWidget(self.widInAdd)

        self.lineIn = QFrame(self.gbInDet)
        self.lineIn.setObjectName(u"lineIn")
        self.lineIn.setFrameShape(QFrame.VLine)
        self.lineIn.setFrameShadow(QFrame.Sunken)

        self.hlIn.addWidget(self.lineIn)

        self.widInDel = QWidget(self.gbInDet)
        self.widInDel.setObjectName(u"widInDel")
        sizePolicy.setHeightForWidth(self.widInDel.sizePolicy().hasHeightForWidth())
        self.widInDel.setSizePolicy(sizePolicy)
        self.hlInDel = QHBoxLayout(self.widInDel)
        self.hlInDel.setObjectName(u"hlInDel")
        self.cbInDel = QComboBox(self.widInDel)
        self.cbInDel.setObjectName(u"cbInDel")

        self.hlInDel.addWidget(self.cbInDel)

        self.btnInDel = QPushButton(self.widInDel)
        self.btnInDel.setObjectName(u"btnInDel")
        sizePolicy1.setHeightForWidth(self.btnInDel.sizePolicy().hasHeightForWidth())
        self.btnInDel.setSizePolicy(sizePolicy1)

        self.hlInDel.addWidget(self.btnInDel)


        self.hlIn.addWidget(self.widInDel)


        self.glCate.addWidget(self.gbInDet, 1, 0, 1, 1)

        self.gbOutDet = QGroupBox(self.tabCate)
        self.gbOutDet.setObjectName(u"gbOutDet")
        self.hlDel = QHBoxLayout(self.gbOutDet)
        self.hlDel.setObjectName(u"hlDel")
        self.widOutAdd = QWidget(self.gbOutDet)
        self.widOutAdd.setObjectName(u"widOutAdd")
        sizePolicy.setHeightForWidth(self.widOutAdd.sizePolicy().hasHeightForWidth())
        self.widOutAdd.setSizePolicy(sizePolicy)
        self.hlOutAdd = QHBoxLayout(self.widOutAdd)
        self.hlOutAdd.setObjectName(u"hlOutAdd")
        self.lnOutAdd = QLineEdit(self.widOutAdd)
        self.lnOutAdd.setObjectName(u"lnOutAdd")

        self.hlOutAdd.addWidget(self.lnOutAdd)

        self.btnOutAdd = QPushButton(self.widOutAdd)
        self.btnOutAdd.setObjectName(u"btnOutAdd")

        self.hlOutAdd.addWidget(self.btnOutAdd)


        self.hlDel.addWidget(self.widOutAdd)

        self.lineOut = QFrame(self.gbOutDet)
        self.lineOut.setObjectName(u"lineOut")
        self.lineOut.setFrameShape(QFrame.VLine)
        self.lineOut.setFrameShadow(QFrame.Sunken)

        self.hlDel.addWidget(self.lineOut)

        self.widOutDel = QWidget(self.gbOutDet)
        self.widOutDel.setObjectName(u"widOutDel")
        sizePolicy.setHeightForWidth(self.widOutDel.sizePolicy().hasHeightForWidth())
        self.widOutDel.setSizePolicy(sizePolicy)
        self.hlOutDel = QHBoxLayout(self.widOutDel)
        self.hlOutDel.setObjectName(u"hlOutDel")
        self.cbOutDel = QComboBox(self.widOutDel)
        self.cbOutDel.setObjectName(u"cbOutDel")

        self.hlOutDel.addWidget(self.cbOutDel)

        self.btnOutDel = QPushButton(self.widOutDel)
        self.btnOutDel.setObjectName(u"btnOutDel")
        sizePolicy1.setHeightForWidth(self.btnOutDel.sizePolicy().hasHeightForWidth())
        self.btnOutDel.setSizePolicy(sizePolicy1)

        self.hlOutDel.addWidget(self.btnOutDel)


        self.hlDel.addWidget(self.widOutDel)


        self.glCate.addWidget(self.gbOutDet, 2, 0, 1, 1)

        self.tabWidget.addTab(self.tabCate, "")
        self.tabData = QWidget()
        self.tabData.setObjectName(u"tabData")
        self.vlData = QVBoxLayout(self.tabData)
        self.vlData.setObjectName(u"vlData")
        self.treeData = QTreeWidget(self.tabData)
        self.treeData.setObjectName(u"treeData")

        self.vlData.addWidget(self.treeData)

        self.widInput = QWidget(self.tabData)
        self.widInput.setObjectName(u"widInput")
        self.glDataIn = QGridLayout(self.widInput)
        self.glDataIn.setObjectName(u"glDataIn")
        self.lnCost = QLineEdit(self.widInput)
        self.lnCost.setObjectName(u"lnCost")
        self.lnCost.setMaximumSize(QSize(75, 16777215))

        self.glDataIn.addWidget(self.lnCost, 1, 4, 1, 1)

        self.cbType = QComboBox(self.widInput)
        self.cbType.setObjectName(u"cbType")

        self.glDataIn.addWidget(self.cbType, 1, 1, 1, 1)

        self.lnDetail = QLineEdit(self.widInput)
        self.lnDetail.setObjectName(u"lnDetail")

        self.glDataIn.addWidget(self.lnDetail, 1, 5, 1, 1)

        self.lbSrc = QLabel(self.widInput)
        self.lbSrc.setObjectName(u"lbSrc")

        self.glDataIn.addWidget(self.lbSrc, 0, 2, 1, 1, Qt.AlignHCenter)

        self.lbDate = QLabel(self.widInput)
        self.lbDate.setObjectName(u"lbDate")

        self.glDataIn.addWidget(self.lbDate, 0, 0, 1, 1, Qt.AlignHCenter)

        self.lnDate = QLineEdit(self.widInput)
        self.lnDate.setObjectName(u"lnDate")
        self.lnDate.setMaximumSize(QSize(75, 16777215))

        self.glDataIn.addWidget(self.lnDate, 1, 0, 1, 1)

        self.cbDetail = QComboBox(self.widInput)
        self.cbDetail.setObjectName(u"cbDetail")

        self.glDataIn.addWidget(self.cbDetail, 1, 3, 1, 1)

        self.lbDesc = QLabel(self.widInput)
        self.lbDesc.setObjectName(u"lbDesc")

        self.glDataIn.addWidget(self.lbDesc, 0, 5, 1, 1, Qt.AlignHCenter)

        self.cbSrc = QComboBox(self.widInput)
        self.cbSrc.setObjectName(u"cbSrc")

        self.glDataIn.addWidget(self.cbSrc, 1, 2, 1, 1)

        self.lbDetail = QLabel(self.widInput)
        self.lbDetail.setObjectName(u"lbDetail")

        self.glDataIn.addWidget(self.lbDetail, 0, 3, 1, 1, Qt.AlignHCenter)

        self.lbType = QLabel(self.widInput)
        self.lbType.setObjectName(u"lbType")

        self.glDataIn.addWidget(self.lbType, 0, 1, 1, 1, Qt.AlignHCenter)

        self.lbCost = QLabel(self.widInput)
        self.lbCost.setObjectName(u"lbCost")

        self.glDataIn.addWidget(self.lbCost, 0, 4, 1, 1, Qt.AlignHCenter)

        self.btnAddData = QPushButton(self.widInput)
        self.btnAddData.setObjectName(u"btnAddData")

        self.glDataIn.addWidget(self.btnAddData, 1, 6, 1, 1)


        self.vlData.addWidget(self.widInput)

        self.tabWidget.addTab(self.tabData, "")
        self.tabSumS = QWidget()
        self.tabSumS.setObjectName(u"tabSumS")
        self.glSum = QGridLayout(self.tabSumS)
        self.glSum.setObjectName(u"glSum")
        self.treeStatS = QTreeWidget(self.tabSumS)
        self.treeStatS.setObjectName(u"treeStatS")

        self.glSum.addWidget(self.treeStatS, 0, 0, 1, 1)

        self.tabWidget.addTab(self.tabSumS, "")
        self.tabStatM = QWidget()
        self.tabStatM.setObjectName(u"tabStatM")
        self.tabWidget.addTab(self.tabStatM, "")

        self.glCent.addWidget(self.tabWidget, 0, 0, 1, 1)

        MoneyManage.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MoneyManage)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 22))
        self.fileMenu = QMenu(self.menubar)
        self.fileMenu.setObjectName(u"fileMenu")
        self.infoMenu = QMenu(self.menubar)
        self.infoMenu.setObjectName(u"infoMenu")
        MoneyManage.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MoneyManage)
        self.statusbar.setObjectName(u"statusbar")
        MoneyManage.setStatusBar(self.statusbar)

        self.menubar.addAction(self.fileMenu.menuAction())
        self.menubar.addAction(self.infoMenu.menuAction())
        self.fileMenu.addAction(self.acLoad)
        self.fileMenu.addAction(self.acSave)
        self.fileMenu.addAction(self.acSaveAs)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.acExit)
        self.infoMenu.addAction(self.acOpenLicense)
        self.infoMenu.addAction(self.acLicense)
        self.infoMenu.addSeparator()
        self.infoMenu.addAction(self.acInfo)

        self.retranslateUi(MoneyManage)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MoneyManage)
    # setupUi

    def retranslateUi(self, MoneyManage):
        MoneyManage.setWindowTitle(QCoreApplication.translate("MoneyManage", u"\uc7ac\uc0b0\uad00\ub9ac", None))
        self.acLoad.setText(QCoreApplication.translate("MoneyManage", u"\ubd88\ub7ec\uc624\uae30", None))
        self.acSave.setText(QCoreApplication.translate("MoneyManage", u"\uc800\uc7a5", None))
        self.acSaveAs.setText(QCoreApplication.translate("MoneyManage", u"\ub2e4\ub978 \uc774\ub984\uc73c\ub85c \uc800\uc7a5", None))
        self.acExit.setText(QCoreApplication.translate("MoneyManage", u"\uc885\ub8cc", None))
        self.acOpenLicense.setText(QCoreApplication.translate("MoneyManage", u"\uc624\ud508 \uc18c\uc2a4 \ub77c\uc774\uc120\uc2a4", None))
        self.acLicense.setText(QCoreApplication.translate("MoneyManage", u"\ub77c\uc774\uc120\uc2a4", None))
        self.acInfo.setText(QCoreApplication.translate("MoneyManage", u"\uc815\ubcf4", None))
        self.gbSrc.setTitle(QCoreApplication.translate("MoneyManage", u"\uc6d0\ucc9c", None))
        self.btnSrcAdd.setText(QCoreApplication.translate("MoneyManage", u"\ucd94\uac00", None))
        self.btnSrcDel.setText(QCoreApplication.translate("MoneyManage", u"\uc0ad\uc81c", None))
        self.gbInDet.setTitle(QCoreApplication.translate("MoneyManage", u"\uc218\uc785 \uc0c1\uc138", None))
        self.btnInAdd.setText(QCoreApplication.translate("MoneyManage", u"\ucd94\uac00", None))
        self.btnInDel.setText(QCoreApplication.translate("MoneyManage", u"\uc0ad\uc81c", None))
        self.gbOutDet.setTitle(QCoreApplication.translate("MoneyManage", u"\uc9c0\ucd9c \uc0c1\uc138(\uc0ac\uc6a9\ucc98)", None))
        self.btnOutAdd.setText(QCoreApplication.translate("MoneyManage", u"\ucd94\uac00", None))
        self.btnOutDel.setText(QCoreApplication.translate("MoneyManage", u"\uc0ad\uc81c", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabCate), QCoreApplication.translate("MoneyManage", u"\ubd84\ub958 \uad00\ub9ac", None))
        ___qtreewidgetitem = self.treeData.headerItem()
        ___qtreewidgetitem.setText(5, QCoreApplication.translate("MoneyManage", u"\uc124\uba85", None));
        ___qtreewidgetitem.setText(4, QCoreApplication.translate("MoneyManage", u"\uae08\uc561", None));
        ___qtreewidgetitem.setText(3, QCoreApplication.translate("MoneyManage", u"\uc0ac\uc6a9\ucc98", None));
        ___qtreewidgetitem.setText(2, QCoreApplication.translate("MoneyManage", u"\uc6d0\ucc9c", None));
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("MoneyManage", u"\uad6c\ubd84", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("MoneyManage", u"\uc77c\uc2dc", None));
        self.lbSrc.setText(QCoreApplication.translate("MoneyManage", u"\uc6d0\ucc9c", None))
        self.lbDate.setText(QCoreApplication.translate("MoneyManage", u"\uc77c\uc2dc", None))
        self.lbDesc.setText(QCoreApplication.translate("MoneyManage", u"\uc124\uba85", None))
        self.lbDetail.setText(QCoreApplication.translate("MoneyManage", u"\uc0c1\uc138", None))
        self.lbType.setText(QCoreApplication.translate("MoneyManage", u"\uad6c\ubd84", None))
        self.lbCost.setText(QCoreApplication.translate("MoneyManage", u"\uae08\uc561", None))
        self.btnAddData.setText(QCoreApplication.translate("MoneyManage", u"\ub370\uc774\ud130 \ucd94\uac00", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabData), QCoreApplication.translate("MoneyManage", u"\uae30\ub85d \ucd94\uac00/\uc218\uc815", None))
        ___qtreewidgetitem1 = self.treeStatS.headerItem()
        ___qtreewidgetitem1.setText(9, QCoreApplication.translate("MoneyManage", u"\uc774\ub3d9\uc561", None));
        ___qtreewidgetitem1.setText(8, QCoreApplication.translate("MoneyManage", u"\uc9c0\ucd9c\uc678", None));
        ___qtreewidgetitem1.setText(7, QCoreApplication.translate("MoneyManage", u"\uc218\uc785\uc678", None));
        ___qtreewidgetitem1.setText(6, QCoreApplication.translate("MoneyManage", u"\uc9c0\ucd9c", None));
        ___qtreewidgetitem1.setText(5, QCoreApplication.translate("MoneyManage", u"\uc218\uc785", None));
        ___qtreewidgetitem1.setText(4, QCoreApplication.translate("MoneyManage", u"\uc21c \uc218\uc775", None));
        ___qtreewidgetitem1.setText(3, QCoreApplication.translate("MoneyManage", u"\uc7ac\uc0b0 \ubcc0\ub3d9", None));
        ___qtreewidgetitem1.setText(2, QCoreApplication.translate("MoneyManage", u"\ud604\uae08\uc131", None));
        ___qtreewidgetitem1.setText(1, QCoreApplication.translate("MoneyManage", u"\ucd1d \uc7ac\uc0b0", None));
        ___qtreewidgetitem1.setText(0, QCoreApplication.translate("MoneyManage", u"\uc5f0\uc6d4", None));
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabSumS), QCoreApplication.translate("MoneyManage", u"\uac04\ub7b5\ud1b5\uacc4", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabStatM), QCoreApplication.translate("MoneyManage", u"\uc6d4\ubcc4\ud1b5\uacc4", None))
        self.fileMenu.setTitle(QCoreApplication.translate("MoneyManage", u"\ud30c\uc77c", None))
        self.infoMenu.setTitle(QCoreApplication.translate("MoneyManage", u"\uc815\ubcf4", None))
    # retranslateUi

