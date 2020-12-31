# -*- coding: utf-8 -*-
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


QRegExp          = QRegularExpression
QRegExpValidator = QRegularExpressionValidator

sizePolicy_EP = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
sizePolicy_EP.setHorizontalStretch(0)
sizePolicy_EP.setVerticalStretch(0)

sizePolicy_PF = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
sizePolicy_PF.setHorizontalStretch(0)
sizePolicy_PF.setVerticalStretch(0)

sizePolicy_FF = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
sizePolicy_FF.setHorizontalStretch(0)
sizePolicy_FF.setVerticalStretch(0)


class GbAddDelCate(QGroupBox):
    def __init__(self,parent):
        super().__init__(parent)
        
        self.hlMain = QHBoxLayout(self)
        self.hlMain.setObjectName(u"hlMain")
        
        
        self.widAdd = QWidget(self)
        self.widAdd.setObjectName(u"widAdd")
        sizePolicy_EP.setHeightForWidth(self.widAdd.sizePolicy().hasHeightForWidth())
        self.widAdd.setSizePolicy(sizePolicy_EP)
        
        self.hlAdd = QHBoxLayout(self.widAdd)
        self.hlAdd.setObjectName(u"hlAdd")
        
        self.lnAdd = QLineEdit(self.widAdd)
        self.lnAdd.setObjectName(u"lnAdd")
        self.hlAdd.addWidget(self.lnAdd)

        self.btnAdd = QPushButton(self.widAdd)
        self.btnAdd.setObjectName(u"btnAdd")
        self.hlAdd.addWidget(self.btnAdd)

        self.hlMain.addWidget(self.widAdd)


        self.line = QFrame(self)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.hlMain.addWidget(self.line)


        self.widDel = QWidget(self)
        self.widDel.setObjectName(u"widDel")
        sizePolicy_EP.setHeightForWidth(self.widDel.sizePolicy().hasHeightForWidth())
        self.widDel.setSizePolicy(sizePolicy_EP)
        
        self.hlDel = QHBoxLayout(self.widDel)
        self.hlDel.setObjectName(u"hlDel")
        
        self.cbDel = QComboBox(self.widDel)
        self.cbDel.setObjectName(u"cbDel")
        self.hlDel.addWidget(self.cbDel)

        self.btnDel = QPushButton(self.widDel)
        self.btnDel.setObjectName(u"btnDel")
        sizePolicy_FF.setHeightForWidth(self.btnDel.sizePolicy().hasHeightForWidth())
        self.btnDel.setSizePolicy(sizePolicy_FF)
        self.hlDel.addWidget(self.btnDel)

        self.hlMain.addWidget(self.widDel)
        
        self.retranslateUi()
    
    def retranslateUi(self):
        self.btnAdd.setText(QCoreApplication.translate("MoneyManage", u"\ucd94\uac00", None))
        self.btnDel.setText(QCoreApplication.translate("MoneyManage", u"\uc0ad\uc81c", None))


class GbSrc(GbAddDelCate):
    def __init__(self,parent):
        super().__init__(parent)
        
        self.chkCash = QCheckBox(self)
        self.hlAdd.insertWidget(1,self.chkCash)
        
        self.retranslateUi_1()
    
    def retranslateUi_1(self):
        self.chkCash.setText(QCoreApplication.translate("MoneyManage", u"\ud604\uae08\uc131\u003f", None))


class TabCate(QWidget):
    def __init__(self,parent):
        super().__init__(parent)
        
        self.setObjectName(u"tabCate")
        self.glCate = QGridLayout(self)
        self.glCate.setObjectName(u"glCate")
        
        self.gbSrc = GbSrc(self)
        self.gbSrc.setObjectName(u"gbSrc")
        self.glCate.addWidget(self.gbSrc, 0, 0, 1, 1)

        self.gbIn = GbAddDelCate(self)
        self.gbIn.setObjectName(u"gbIn")
        self.glCate.addWidget(self.gbIn, 1, 0, 1, 1)

        self.gbOut = GbAddDelCate(self)
        self.gbOut.setObjectName(u"gbOut")
        self.glCate.addWidget(self.gbOut, 2, 0, 1, 1)
        
        self.retranslateUi()
    
    def retranslateUi(self):
        self.gbSrc.setTitle(QCoreApplication.translate("MoneyManage", u"\uc6d0\ucc9c", None))
        self.gbIn.setTitle(QCoreApplication.translate("MoneyManage", u"\uc218\uc785 \uc0c1\uc138", None))
        self.gbOut.setTitle(QCoreApplication.translate("MoneyManage", u"\uc9c0\ucd9c \uc0c1\uc138(\uc0ac\uc6a9\ucc98)", None))


class TabData(QWidget):
    def __init__(self,parent):
        super().__init__(parent)
        
        self.setObjectName(u"tabData")
        self.vlData = QVBoxLayout(self)
        self.vlData.setObjectName(u"vlData")
        self.treeData = QTreeView(self)
        self.treeData.setObjectName(u"treeData")

        self.vlData.addWidget(self.treeData)

        self.widInput = QWidget(self)
        self.widInput.setObjectName(u"widInput")
        self.glDataIn = QGridLayout(self.widInput)
        self.glDataIn.setObjectName(u"glDataIn")
        
        self.lbDate = QLabel(self.widInput)
        self.lbDate.setObjectName(u"lbDate")
        self.glDataIn.addWidget(self.lbDate, 0, 0, 1, 1, Qt.AlignHCenter)

        self.lbType = QLabel(self.widInput)
        self.lbType.setObjectName(u"lbType")
        self.glDataIn.addWidget(self.lbType, 0, 1, 1, 1, Qt.AlignHCenter)

        self.lbSrc = QLabel(self.widInput)
        self.lbSrc.setObjectName(u"lbSrc")
        self.glDataIn.addWidget(self.lbSrc, 0, 2, 1, 1, Qt.AlignHCenter)

        self.lbDetail = QLabel(self.widInput)
        self.lbDetail.setObjectName(u"lbDetail")
        self.glDataIn.addWidget(self.lbDetail, 0, 3, 1, 1, Qt.AlignHCenter)

        self.lbCost = QLabel(self.widInput)
        self.lbCost.setObjectName(u"lbCost")
        self.glDataIn.addWidget(self.lbCost, 0, 4, 1, 1, Qt.AlignHCenter)

        self.lbDesc = QLabel(self.widInput)
        self.lbDesc.setObjectName(u"lbDesc")
        self.glDataIn.addWidget(self.lbDesc, 0, 5, 1, 1, Qt.AlignHCenter)

        self.lnDate = QLineEdit(self.widInput)
        self.lnDate.setObjectName(u"lnDate")
        self.lnDate.setAlignment(Qt.AlignCenter)
        self.lnDate.setMaximumSize(QSize(75, 16777215))
        self.glDataIn.addWidget(self.lnDate, 1, 0, 1, 1)

        self.cbType = QComboBox(self.widInput)
        self.cbType.setObjectName(u"cbType")
        self.glDataIn.addWidget(self.cbType, 1, 1, 1, 1)

        self.cbSrc = QComboBox(self.widInput)
        self.cbSrc.setObjectName(u"cbSrc")
        self.glDataIn.addWidget(self.cbSrc, 1, 2, 1, 1)

        self.cbDetail = QComboBox(self.widInput)
        self.cbDetail.setObjectName(u"cbDetail")
        self.glDataIn.addWidget(self.cbDetail, 1, 3, 1, 1)

        self.lnCost = QLineEdit(self.widInput)
        self.lnCost.setAlignment(Qt.AlignCenter)
        self.lnCost.setObjectName(u"lnCost")
        self.lnCost.setMaximumSize(QSize(75, 16777215))
        self.glDataIn.addWidget(self.lnCost, 1, 4, 1, 1)

        self.lnDetail = QLineEdit(self.widInput)
        self.lnDetail.setAlignment(Qt.AlignCenter)
        self.lnDetail.setObjectName(u"lnDetail")
        self.glDataIn.addWidget(self.lnDetail, 1, 5, 1, 1)
        
        self.btnAddData = QPushButton(self.widInput)
        self.btnAddData.setObjectName(u"btnAddData")
        self.glDataIn.addWidget(self.btnAddData, 1, 6, 1, 1)

        self.vlData.addWidget(self.widInput)
        
        self.retranslateUi()
    
    def retranslateUi(self):
        self.lbDate.setText(QCoreApplication.translate("MainWin", u"\uc77c\uc2dc", None))
        self.lbType.setText(QCoreApplication.translate("MainWin", u"\uad6c\ubd84", None))
        self.lbSrc.setText(QCoreApplication.translate("MainWin", u"\uc6d0\ucc9c", None))
        self.lbDetail.setText(QCoreApplication.translate("MainWin", u"\uc0c1\uc138", None))
        self.lbCost.setText(QCoreApplication.translate("MainWin", u"\uae08\uc561", None))
        self.lbDesc.setText(QCoreApplication.translate("MainWin", u"\uc124\uba85", None))
        self.btnAddData.setText(QCoreApplication.translate("MoneyManage", u"\ub370\uc774\ud130 \ucd94\uac00", None))
        
        self.lnDate.setInputMask(r'2\0D9-99-99;_')
        self.lnDate.setValidator(QRegExpValidator('20[1-9_][0-9_]-(0[1-9_]|1[0-2_]|__)-(0[1-9_]|[12][0-9_]|3[01_]|__)'))
        self.lnCost.setValidator(QRegExpValidator('[1-9][0-9]{0,7}'))
        self.lnDetail.setMaxLength(64)


class TabStatS(QWidget):
    def __init__(self,parent):
        super().__init__(parent)
        self.setObjectName(u"tabStatS")
        self.glSum = QGridLayout(self)
        self.glSum.setObjectName(u"glSum")
        
        self.treeStatS = QTreeView(self)
        self.treeStatS.setObjectName(u"treeStatS")
        self.glSum.addWidget(self.treeStatS, 0, 0, 1, 1)
        self.retranslateUi()
    
    def retranslateUi(self):
        pass


class TabStatM(QWidget):
    def __init__(self,parent):
        super().__init__(parent)
        self.setupUi()
    
    def setupUi(self):
        if not self.objectName():
            self.setObjectName(u"self")
        self.setFixedSize(776,510)
        
        self.glCent = QGridLayout(self)
        self.glCent.setObjectName(u"glCent")


        self.gbMonth = QGroupBox(self)
        self.gbMonth.setObjectName(u"gbMonth")
        sizePolicy_PF.setHeightForWidth(self.gbMonth.sizePolicy().hasHeightForWidth())
        self.gbMonth.setSizePolicy(sizePolicy_PF)
        self.hlMonth = QHBoxLayout(self.gbMonth)
        self.hlMonth.setObjectName(u"hlMonth")
        
        self.lbTitleMonth = QLabel(self.gbMonth)
        self.lbTitleMonth.setObjectName(u"lbTitleMonth")
        self.lbTitleMonth.setAlignment(Qt.AlignCenter)
        self.hlMonth.addWidget(self.lbTitleMonth)

        self.cbMonth = QComboBox(self.gbMonth)
        self.cbMonth.setObjectName(u"cbMonth")
        self.hlMonth.addWidget(self.cbMonth)

        self.btnChange = QPushButton(self.gbMonth)
        self.btnChange.setObjectName(u"btnChange")
        sizePolicy_FF.setHeightForWidth(self.btnChange.sizePolicy().hasHeightForWidth())
        self.btnChange.setSizePolicy(sizePolicy_FF)
        self.hlMonth.addWidget(self.btnChange)

        self.glCent.addWidget(self.gbMonth, 0, 0, 1, 2)


        self.gbIncome = QGroupBox(self)
        self.gbIncome.setObjectName(u"gbIncome")
        self.glIncome = QGridLayout(self.gbIncome)
        self.glIncome.setObjectName(u"glIncome")
        
        self.lbTitleIncome=[]
        for x,y,w,h in ((0,0,1,2),(1,0,1,2),(1,2,1,2)):
            lb=QLabel(self.gbIncome)
            lb.setAlignment(Qt.AlignCenter)
            self.glIncome.addWidget(lb,x,y,w,h)
            self.lbTitleIncome.append(lb)

        self.lbSumIncome = QLabel(self.gbIncome)
        self.lbSumIncome.setObjectName(u"lbSumIncome")
        self.lbSumIncome.setAlignment(Qt.AlignCenter)
        self.glIncome.addWidget(self.lbSumIncome, 0, 2, 1, 2)

        self.glCent.addWidget(self.gbIncome, 1, 0, 1, 1)


        self.gbOutcome = QGroupBox(self)
        self.gbOutcome.setObjectName(u"gbOutcome")
        self.glOutcome = QGridLayout(self.gbOutcome)
        self.glOutcome.setObjectName(u"glOutcome")
        
        self.lbTitleOutcome=[]
        for x,y,w,h in ((0,0,1,2),(1,0,1,2),(1,2,1,2)):
            lb=QLabel(self.gbOutcome)
            lb.setAlignment(Qt.AlignCenter)
            self.glOutcome.addWidget(lb,x,y,w,h)
            self.lbTitleOutcome.append(lb)
        

        self.lbSumOutcome = QLabel(self.gbOutcome)
        self.lbSumOutcome.setObjectName(u"lbSumOutcome")
        self.lbSumOutcome.setAlignment(Qt.AlignCenter)
        self.glOutcome.addWidget(self.lbSumOutcome, 0, 2, 1, 2)

        self.glCent.addWidget(self.gbOutcome, 2, 0, 1, 1)


        self.gbCurrent = QGroupBox(self)
        self.gbCurrent.setObjectName(u"gbCurrent")
        self.glCurrent = QGridLayout(self.gbCurrent)
        self.glCurrent.setObjectName(u"glCurrent")

        self.lbTitleCurrent = QLabel(self.gbCurrent)
        self.lbTitleCurrent.setObjectName(u"lbTitleCurrent")
        self.lbTitleCurrent.setAlignment(Qt.AlignCenter)
        self.glCurrent.addWidget(self.lbTitleCurrent, 0, 0, 1, 1)

        self.lbSumCurrent = QLabel(self.gbCurrent)
        self.lbSumCurrent.setObjectName(u"lbSumCurrent")
        self.lbSumCurrent.setAlignment(Qt.AlignCenter)
        self.glCurrent.addWidget(self.lbSumCurrent, 0, 1, 1, 1)

        self.glCent.addWidget(self.gbCurrent, 1, 1, 1, 1)


        self.gbMove = QGroupBox(self)
        self.gbMove.setObjectName(u"gbMove")
        self.glMove = QGridLayout(self.gbMove)
        self.glMove.setObjectName(u"glMove")
        
        self.lbTitleMove=[]
        for x,y,w,h in ((0,0,1,2),(1,0,1,2),(1,2,1,2)):
            lb=QLabel(self.gbMove)
            lb.setAlignment(Qt.AlignCenter)
            self.glMove.addWidget(lb,x,y,w,h)
            self.lbTitleMove.append(lb)

        self.lbSumMove = QLabel(self.gbMove)
        self.lbSumMove.setObjectName(u"lbSumMove")
        self.lbSumMove.setAlignment(Qt.AlignCenter)
        self.glMove.addWidget(self.lbSumMove, 0, 2, 1, 2)

        self.glCent.addWidget(self.gbMove, 2, 1, 1, 1)


        self.gbStat = QGroupBox(self)
        self.gbStat.setObjectName(u"gbStat")
        sizePolicy_PF.setHeightForWidth(self.gbStat.sizePolicy().hasHeightForWidth())
        self.gbStat.setSizePolicy(sizePolicy_PF)
        self.glStat = QGridLayout(self.gbStat)
        self.glStat.setObjectName(u"glStat")
        
        self.lbTitleNet = QLabel(self.gbStat)
        self.lbTitleNet.setObjectName(u"lbTitleNet")
        sizePolicy_PF.setHeightForWidth(self.lbTitleNet.sizePolicy().hasHeightForWidth())
        self.lbTitleNet.setSizePolicy(sizePolicy_PF)
        self.lbTitleNet.setAlignment(Qt.AlignCenter)
        self.glStat.addWidget(self.lbTitleNet, 0, 0, 1, 1)

        self.lbTitleOut1 = QLabel(self.gbStat)
        self.lbTitleOut1.setObjectName(u"lbTitleOut1")
        sizePolicy_PF.setHeightForWidth(self.lbTitleOut1.sizePolicy().hasHeightForWidth())
        self.lbTitleOut1.setSizePolicy(sizePolicy_PF)
        self.lbTitleOut1.setAlignment(Qt.AlignCenter)
        self.glStat.addWidget(self.lbTitleOut1, 0, 1, 1, 1)

        self.lbTitleOut2 = QLabel(self.gbStat)
        self.lbTitleOut2.setObjectName(u"lbTitleOut2")
        sizePolicy_PF.setHeightForWidth(self.lbTitleOut2.sizePolicy().hasHeightForWidth())
        self.lbTitleOut2.setSizePolicy(sizePolicy_PF)
        self.lbTitleOut2.setAlignment(Qt.AlignCenter)
        self.glStat.addWidget(self.lbTitleOut2, 0, 2, 1, 1)

        self.lbNet = QLabel(self.gbStat)
        self.lbNet.setObjectName(u"lbNet")
        sizePolicy_PF.setHeightForWidth(self.lbNet.sizePolicy().hasHeightForWidth())
        self.lbNet.setSizePolicy(sizePolicy_PF)
        self.lbNet.setAlignment(Qt.AlignCenter)
        self.glStat.addWidget(self.lbNet, 1, 0, 1, 1)

        self.lbOut1 = QLabel(self.gbStat)
        self.lbOut1.setObjectName(u"lbOut1")
        sizePolicy_PF.setHeightForWidth(self.lbOut1.sizePolicy().hasHeightForWidth())
        self.lbOut1.setSizePolicy(sizePolicy_PF)
        self.lbOut1.setAlignment(Qt.AlignCenter)
        self.glStat.addWidget(self.lbOut1, 1, 1, 1, 1)

        self.lbOut2 = QLabel(self.gbStat)
        self.lbOut2.setObjectName(u"lbOut2")
        sizePolicy_PF.setHeightForWidth(self.lbOut2.sizePolicy().hasHeightForWidth())
        self.lbOut2.setSizePolicy(sizePolicy_PF)
        self.lbOut2.setAlignment(Qt.AlignCenter)
        self.glStat.addWidget(self.lbOut2, 1, 2, 1, 1)

        self.glCent.addWidget(self.gbStat, 3, 0, 1, 2)

        self.retranslateUi()

        QMetaObject.connectSlotsByName(self)
    # setupUi

    def retranslateUi(self):
        self.gbMonth.setTitle(QCoreApplication.translate("TabStatM", u"\ud1b5\uacc4 \uc124\uc815", None))
        self.lbTitleMonth.setText(QCoreApplication.translate("TabStatM", u"\uc5f0-\uc6d4", None))
        
        income_txt=('총액','요목별','원천별')
        self.gbIncome.setTitle(QCoreApplication.translate("TabStatM", u"\uc218\uc785", None))
        for wid,txt in zip(self.lbTitleIncome,income_txt):
            wid.setText(txt)
        
        outcome_txt=('총액','요목별','원천별')
        self.gbOutcome.setTitle(QCoreApplication.translate("TabStatM", u"\uc9c0\ucd9c", None))
        for wid,txt in zip(self.lbTitleOutcome,outcome_txt):
            wid.setText(txt)
        
        self.gbCurrent.setTitle(QCoreApplication.translate("TabStatM", u"\ud604 \uc7ac\uc0b0", None))
        self.lbTitleCurrent.setText(QCoreApplication.translate("TabStatM", u"\ucd1d \uc7ac\uc0b0", None))
        
        move_txt=('총액','이동_入','이동_出')
        self.gbMove.setTitle(QCoreApplication.translate("TabStatM", u"\uc774\ub3d9\uc561", None))
        for wid,txt in zip(self.lbTitleMove,move_txt):
            wid.setText(txt)
        
        stat_txt=('순수익','필수지출','초과지출')
        self.gbStat.setTitle(QCoreApplication.translate("TabStatM", u"\ud1b5\uacc4", None))
        for wid,txt in zip((self.lbTitleNet, self.lbTitleOut1, self.lbTitleOut2),stat_txt):
            wid.setText(txt)
        
        self.btnChange.setText(QCoreApplication.translate("TabStatM", u"\ubcc0\uacbd", None))
    # retranslateUi


class Ui_MainWin:
    def setupUi(self, MainWin):
        if not MainWin.objectName():
            MainWin.setObjectName(u"MainWin")
        MainWin.resize(800, 600)
        
        
        self.acLoad = QAction(MainWin)
        self.acLoad.setObjectName(u"acLoad")
        self.acSave = QAction(MainWin)
        self.acSave.setObjectName(u"acSave")
        self.acSaveAs = QAction(MainWin)
        self.acSaveAs.setObjectName(u"acSaveAs")
        self.acImport = QAction(MainWin)
        self.acImport.setObjectName(u"acImport")
        self.acExport = QAction(MainWin)
        self.acExport.setObjectName(u"acExport")
        self.acExit = QAction(MainWin)
        self.acExit.setObjectName(u"acExit")
        
        self.acOpenLicense = QAction(MainWin)
        self.acOpenLicense.setObjectName(u"acOpenLicense")
        self.acLicense = QAction(MainWin)
        self.acLicense.setObjectName(u"acLicense")
        self.acInfo = QAction(MainWin)
        self.acInfo.setObjectName(u"acInfo")
        
        self.menubar = QMenuBar(MainWin)
        self.menubar.setObjectName(u"menubar")
        
        self.fileMenu = QMenu(self.menubar)
        self.fileMenu.setObjectName(u"fileMenu")
        self.fileMenu.addAction(self.acLoad)
        self.fileMenu.addAction(self.acSave)
        self.fileMenu.addAction(self.acSaveAs)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.acImport)
        self.fileMenu.addAction(self.acExport)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.acExit)
        self.menubar.addAction(self.fileMenu.menuAction())
        
        self.infoMenu = QMenu(self.menubar)
        self.infoMenu.setObjectName(u"infoMenu")
        self.infoMenu.addAction(self.acOpenLicense)
        self.infoMenu.addAction(self.acLicense)
        self.infoMenu.addSeparator()
        self.infoMenu.addAction(self.acInfo)
        self.menubar.addAction(self.infoMenu.menuAction())

        MainWin.setMenuBar(self.menubar)
        
        
        self.statusbar = QStatusBar(MainWin)
        self.statusbar.setObjectName(u"statusbar")
        MainWin.setStatusBar(self.statusbar)
        
        
        self.centralwidget = QWidget(MainWin)
        self.centralwidget.setObjectName(u"centralwidget")
        self.glCent = QGridLayout(self.centralwidget)
        self.glCent.setObjectName(u"glCent")
        MainWin.setCentralWidget(self.centralwidget)
        
        
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        
        self.tabCate = TabCate(self)
        self.tabWidget.addTab(self.tabCate, u"\ubd84\ub958 \uad00\ub9ac")
        
        self.tabData = TabData(self)
        self.tabWidget.addTab(self.tabData, u"\uae30\ub85d \ucd94\uac00/\uc218\uc815")
        
        self.tabStatS = TabStatS(self)
        self.tabWidget.addTab(self.tabStatS, u"\uac04\ub7b5\ud1b5\uacc4")
        
        self.tabStatM = TabStatM(self)
        self.tabWidget.addTab(self.tabStatM, u"\uc6d4\ubcc4\ud1b5\uacc4")
        
        self.glCent.addWidget(self.tabWidget, 0, 0, 1, 1)


        self.retranslateUi(MainWin)
        QMetaObject.connectSlotsByName(MainWin)
    # setupUi

    def retranslateUi(self, MainWin):
        MainWin.setWindowTitle(QCoreApplication.translate("MainWin", u"\uc7ac\uc0b0\uad00\ub9ac", None))
        
        self.fileMenu.setTitle(QCoreApplication.translate("MainWin", u"\ud30c\uc77c", None))
        self.infoMenu.setTitle(QCoreApplication.translate("MainWin", u"\uc815\ubcf4", None))
        
        self.acLoad.setText(QCoreApplication.translate("MainWin", u"\ubd88\ub7ec\uc624\uae30", None))
        self.acSave.setText(QCoreApplication.translate("MainWin", u"\uc800\uc7a5", None))
        self.acSaveAs.setText(QCoreApplication.translate("MainWin", u"\ub2e4\ub978 \uc774\ub984\uc73c\ub85c \uc800\uc7a5", None))
        self.acImport.setText(QCoreApplication.translate("MainWin", u'\uac00\uc838\uc624\uae30', None))
        self.acExport.setText(QCoreApplication.translate("MainWin", u'\ub0b4\ubcf4\ub0b4\uae30', None))
        self.acExit.setText(QCoreApplication.translate("MainWin", u"\uc885\ub8cc", None))
        
        self.acOpenLicense.setText(QCoreApplication.translate("MainWin", u"\uc624\ud508 \uc18c\uc2a4 \ub77c\uc774\uc120\uc2a4", None))
        self.acLicense.setText(QCoreApplication.translate("MainWin", u"\ub77c\uc774\uc120\uc2a4", None))
        self.acInfo.setText(QCoreApplication.translate("MainWin", u"\uc815\ubcf4", None))
        # retranslateUi

