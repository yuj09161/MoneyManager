# pylint: disable=attribute-defined-outside-init, line-too-long, too-many-instance-attributes
# pylint: disable=too-many-statements, too-few-public-methods, undefined-variable

from PySide6.QtCore import Qt, QCoreApplication, QSize, QMetaObject
from PySide6.QtGui import QRegularExpressionValidator, QAction, QKeySequence
from PySide6.QtWidgets import (
    QWidget, QGroupBox, QTabWidget, QScrollArea,
    QVBoxLayout, QHBoxLayout, QGridLayout,
    QSizePolicy, QSpacerItem,
    QLabel, QPushButton, QCheckBox,
    QPlainTextEdit, QLineEdit, QComboBox,
    QListView, QTreeView,
    QMenuBar, QMenu, QStatusBar, QProgressBar
)


sizePolicy_EP = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
sizePolicy_EP.setHorizontalStretch(0)
sizePolicy_EP.setVerticalStretch(0)

sizePolicy_PF = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
sizePolicy_PF.setHorizontalStretch(0)
sizePolicy_PF.setVerticalStretch(0)

sizePolicy_FF = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
sizePolicy_FF.setHorizontalStretch(0)
sizePolicy_FF.setVerticalStretch(0)

sizePolicy_EE = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
sizePolicy_EE.setHorizontalStretch(0)
sizePolicy_EE.setVerticalStretch(0)


class Ui_Txt:
    # pylint: disable=no-member

    def setupUi(self, Win, title, info_text):
        if not self.objectName():
            self.setObjectName(u"info")
        Win.setFixedSize(600, 500)
        Win.setWindowFlags(self.windowFlags() ^ Qt.WindowMinMaxButtonsHint)

        self.centralwidget = QWidget(self)
        self.centralwidget.setObjectName(u"centralwidget")

        self.vlCent = QVBoxLayout(self.centralwidget)
        self.vlCent.setObjectName(u"vlCent")


        self.pteMain = QPlainTextEdit(self.centralwidget)
        self.pteMain.setObjectName(u"pteMain")
        self.pteMain.setReadOnly(True)
        self.vlCent.addWidget(self.pteMain)


        self.widBot = QWidget(self.centralwidget)
        self.widBot.setObjectName(u"widBot")
        self.hlBot = QHBoxLayout(self.widBot)
        self.hlBot.setObjectName(u"hlBot")
        self.hlBot.setContentsMargins(0, 0, 0, 0)

        self.sp = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.hlBot.addItem(self.sp)

        self.btnExit = QPushButton(self.widBot)
        self.btnExit.setObjectName(u"btnExit")
        self.hlBot.addWidget(self.btnExit)

        self.vlCent.addWidget(self.widBot)


        self.setCentralWidget(self.centralwidget)

        self.retranslateUi(title, info_text)

    def retranslateUi(self, title, info_text):
        self.setWindowTitle(title)
        self.pteMain.setPlainText(info_text)
        self.btnExit.setText(QCoreApplication.translate("info", u"\ub2eb\uae30", None))


class Ui_Info(Ui_Txt):
    def setupUi(self, Win, title, info_text):
        super().setupUi(Win, title, info_text)

        self.btnQt = QPushButton(self.centralwidget)
        self.btnQt.setObjectName(u"btnQt")
        self.hlBot.insertWidget(0, self.btnQt)

        self.retranslateUi_1()

    def retranslateUi_1(self):
        self.btnQt.setText(QCoreApplication.translate("info", u"About Qt", None))


class Ui_Login:
    def setupUi(self, Login):
        if not Login.objectName():
            Login.setObjectName(u"Login")
        Login.resize(400, 100)
        Login.setWindowFlags(Qt.Dialog)

        self.centralwidget = QWidget(Login)
        self.centralwidget.setObjectName(u"centralwidget")
        self.glCent = QGridLayout(self.centralwidget)
        self.glCent.setObjectName(u"glCent")

        self.lbTitleUser = QLabel(self.centralwidget)
        self.lbTitleUser.setObjectName(u"lbTitleUser")
        self.lbTitleUser.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)
        self.glCent.addWidget(self.lbTitleUser, 0, 0, 1, 1)

        self.lbTitlePass = QLabel(self.centralwidget)
        self.lbTitlePass.setObjectName(u"lbTitlePass")
        self.lbTitlePass.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)
        self.glCent.addWidget(self.lbTitlePass, 0, 2, 1, 1)

        self.lbTitlePath = QLabel(self.centralwidget)
        self.lbTitlePath.setObjectName(u"lbTitlePath")
        self.lbTitlePath.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)
        self.glCent.addWidget(self.lbTitlePath, 2, 0, 1, 1)

        self.lnUser = QLineEdit(self.centralwidget)
        self.lnUser.setObjectName(u"lnUser")
        self.glCent.addWidget(self.lnUser, 0, 1, 1, 1)

        self.lnPass = QLineEdit(self.centralwidget)
        self.lnPass.setObjectName(u"lnPass")
        self.lnPass.setEchoMode(QLineEdit.Password)
        self.glCent.addWidget(self.lnPass, 0, 3, 1, 1)

        self.lnPath = QLineEdit(self.centralwidget)
        self.lnPath.setObjectName(u"lnPath")
        self.glCent.addWidget(self.lnPath, 2, 1, 1, 3)

        self.widBot = QWidget(self.centralwidget)
        self.widBot.setObjectName(u"widBot")
        self.hlBot = QHBoxLayout(self.widBot)
        self.hlBot.setObjectName(u"hlBot")
        self.hlBot.setContentsMargins(0, 0, 0, 0)

        self.chkSave = QCheckBox(self.widBot)
        self.chkSave.setObjectName(u"chkSave")
        self.hlBot.addWidget(self.chkSave)

        self.btnFile = QPushButton(self.widBot)
        self.btnFile.setObjectName(u"btnFile")
        self.hlBot.addWidget(self.btnFile)

        self.sp = QSpacerItem(196, 21, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.hlBot.addItem(self.sp)

        self.chkEnc = QCheckBox(self.widBot)
        self.chkEnc.setObjectName(u"chkEnc")
        self.hlBot.addWidget(self.chkEnc)

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
        self.lbTitleUser.setText(QCoreApplication.translate("Login", u"\uc0ac\uc6a9\uc790\uba85: ", None))
        self.lbTitlePass.setText(QCoreApplication.translate("Login", u"\uc554\ud638: ", None))
        self.lbTitlePath.setText(QCoreApplication.translate("Login", u"\uc11c\ubc84 \uc8fc\uc18c: ", None))
        self.chkSave.setText(QCoreApplication.translate("Login", u"\uacc4\uc815 \uc800\uc7a5?", None))
        self.btnFile.setText(QCoreApplication.translate("Login", u"\ud30c\uc77c \uc120\ud0dd", None))
        self.chkEnc.setText(QCoreApplication.translate("Login", u"\uc554\ud638\ud654?", None))
        self.btnConnect.setText(QCoreApplication.translate("Login", u"\uc5f0\uacb0", None))
    # retranslateUi


class Ui_Pg:
    def setupUi(self, Pg):
        if not Pg.objectName():
            Pg.setObjectName(u"Pg")
        Pg.setFixedSize(200, 70)
        Pg.setWindowFlags(Qt.SplashScreen)

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
        self.pgPg.setRange(0, 0)
        self.pgPg.setTextVisible(False)
        self.vlCent.addWidget(self.pgPg)

        Pg.setCentralWidget(self.centralwidget)

        QMetaObject.connectSlotsByName(Pg)
    # setupUi


class Ui_GbAddDelCate:
    def setupUi(self, GbAddDelCate):
        self.vlMain = QVBoxLayout(GbAddDelCate)
        self.vlMain.setObjectName(u"vlMain")

        self.lvOrd = QListView(GbAddDelCate)
        self.lvOrd.setEditTriggers(QListView.NoEditTriggers)
        self.lvOrd.setDragDropMode(QListView.InternalMove)
        self.vlMain.addWidget(self.lvOrd)

        self.widAdd = QWidget(GbAddDelCate)
        self.widAdd.setObjectName(u"widAdd")
        sizePolicy_EP.setHeightForWidth(self.widAdd.sizePolicy().hasHeightForWidth())
        self.widAdd.setSizePolicy(sizePolicy_EP)

        self.glEdit = QGridLayout(self.widAdd)
        self.glEdit.setObjectName(u"glEdit")
        self.glEdit.setContentsMargins(0, 7, 0, 7)

        self.lnAdd = QLineEdit(self.widAdd)
        self.lnAdd.setObjectName(u"lnAdd")
        self.lnAdd.setAlignment(Qt.AlignCenter)
        self.lnAdd.setMaxLength(10)
        self.glEdit.addWidget(self.lnAdd, 0, 0, 1, 1)

        self.btnAdd = QPushButton(self.widAdd)
        self.btnAdd.setObjectName(u"btnAdd")
        self.glEdit.addWidget(self.btnAdd, 0, 1, 1, 1)

        self.btnApply = QPushButton(self.widAdd)
        self.btnApply.setObjectName(u"btnApply")
        self.btnApply.hide()
        self.glEdit.addWidget(self.btnApply, 0, 1, 1, 1)

        self.btnCancel = QPushButton(self.widAdd)
        self.btnCancel.setObjectName(u"btnCancel")
        self.btnCancel.hide()
        self.glEdit.addWidget(self.btnCancel, 1, 1, 1, 1)

        self.vlMain.addWidget(self.widAdd)

        self.retranslateUi()

    def retranslateUi(self):
        self.btnAdd.setText(QCoreApplication.translate("MoneyManage", u"\ucd94\uac00", None))
        self.btnApply.setText(QCoreApplication.translate("MoneyManage", u"\uc218\uc815", None))
        self.btnCancel.setText(QCoreApplication.translate("MoneyManage", u"\ucde8\uc18c", None))


class Ui_GbAddDelChk(Ui_GbAddDelCate):
    def setupUi(self, GbAddDelChk, chk_txt):  # pylint: disable=arguments-differ
        super().setupUi(GbAddDelChk)

        self.chk = QCheckBox(GbAddDelChk)
        self.glEdit.addWidget(self.chk, 1, 0, 1, 1)

        self.glEdit.removeWidget(self.btnAdd)
        self.glEdit.addWidget(self.btnAdd, 0, 1, 2, 1)

        self.chk.setText(QCoreApplication.translate("MoneyManage", chk_txt, None))


class Ui_TabCate:
    def setupUi(self, TabCate):
        TabCate.setObjectName(u"tabCate")
        self.glCate = QGridLayout(TabCate)
        self.glCate.setObjectName(u"glCate")

        TabCate.gbSrc.setObjectName(u"gbSrc")
        self.glCate.addWidget(TabCate.gbSrc, 0, 0, 1, 1)

        TabCate.gbIn.setObjectName(u"gbIn")
        self.glCate.addWidget(TabCate.gbIn, 0, 1, 1, 1)

        TabCate.gbOut.setObjectName(u"gbOut")
        self.glCate.addWidget(TabCate.gbOut, 0, 2, 1, 1)

        self.retranslateUi(TabCate)

    def retranslateUi(self, TabCate):
        TabCate.gbSrc.setTitle(QCoreApplication.translate("MoneyManage", u"\uc6d0\ucc9c", None))
        TabCate.gbIn.setTitle(QCoreApplication.translate("MoneyManage", u"\uc218\uc785 \uc0c1\uc138", None))
        TabCate.gbOut.setTitle(QCoreApplication.translate("MoneyManage", u"\uc9c0\ucd9c \uc0c1\uc138(\uc0ac\uc6a9\ucc98)", None))


class Ui_TabData:
    def setupUi(self, TabData):
        TabData.setObjectName(u"tabData")
        self.vlData = QVBoxLayout(TabData)
        self.vlData.setObjectName(u"vlData")

        self.treeData = QTreeView(TabData)
        self.treeData.setObjectName(u"treeData")
        self.treeData.setEditTriggers(QListView.NoEditTriggers)
        self.vlData.addWidget(self.treeData)

        self.widInput = QWidget(TabData)
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

        self.btnCancel = QPushButton(self.widInput)
        self.btnCancel.setObjectName(u"btnCancel")
        self.btnCancel.hide()
        self.glDataIn.addWidget(self.btnCancel, 0, 6, 1, 1)

        self.btnUp = QPushButton(self.widInput)
        self.btnUp.setObjectName(u"btnUp")
        self.btnUp.hide()
        self.btnUp.setMaximumWidth(25)
        self.glDataIn.addWidget(self.btnUp, 0, 7, 1, 1)

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
        self.cbSrc.setMinimumSize(QSize(100, 1))
        self.glDataIn.addWidget(self.cbSrc, 1, 2, 1, 1)

        self.cbDetail = QComboBox(self.widInput)
        self.cbDetail.setObjectName(u"cbDetail")
        self.cbDetail.setMinimumSize(QSize(100, 1))
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

        self.btnEdit = QPushButton(self.widInput)
        self.btnEdit.setObjectName(u"btnEdit")
        self.btnEdit.hide()
        self.glDataIn.addWidget(self.btnEdit, 1, 6, 1, 1)

        self.btnDown = QPushButton(self.widInput)
        self.btnDown.setObjectName(u"btnDown")
        self.btnDown.hide()
        self.btnDown.setMaximumWidth(25)
        self.glDataIn.addWidget(self.btnDown, 1, 7, 1, 1)

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
        self.btnEdit.setText(QCoreApplication.translate("MoneyManage", u"\uc218\uc815", None))
        self.btnCancel.setText(QCoreApplication.translate("MoneyManage", u"\ucde8\uc18c", None))
        self.btnUp.setText(QCoreApplication.translate("MoneyManage", u"\u25b2", None))
        self.btnDown.setText(QCoreApplication.translate("MoneyManage", u"\u25bc", None))

        self.lnDate.setInputMask(r'2\0D9-99-99;_')
        self.lnDate.setValidator(QRegularExpressionValidator('20[1-9_][0-9_]-(0[1-9_]|1[0-2_]|__)-(0[1-9_]|[12][0-9_]|3[01_]|__)'))
        self.lnCost.setValidator(QRegularExpressionValidator('[1-9][0-9]{0,7}'))
        self.lnDetail.setMaxLength(64)


class Ui_TabStatS:
    def setupUi(self, TabStatS):
        TabStatS.setObjectName(u"tabStatS")
        self.glSum = QGridLayout(TabStatS)
        self.glSum.setObjectName(u"glSum")

        self.treeStatS = QTreeView(TabStatS)
        self.treeStatS.setObjectName(u"treeStatS")
        self.treeStatS.setEditTriggers(QTreeView.NoEditTriggers)
        self.glSum.addWidget(self.treeStatS, 0, 0, 1, 1)


class Ui_TabStatM:
    def setupUi(self, TabStatM):
        if not TabStatM.objectName():
            TabStatM.setObjectName(u"TabStatM")

        self.glCent = QGridLayout(TabStatM)
        self.glCent.setContentsMargins(0, 0, 0, 0)

        self.scCent = QScrollArea(TabStatM)
        self.scCent.setWidgetResizable(True)
        self.scCent.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scCent.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.glCent.addWidget(self.scCent, 0, 0)

        self.widCent = QWidget(self.scCent)
        sizePolicy_EE.setHeightForWidth(self.widCent.sizePolicy().hasHeightForWidth())
        self.widCent.setSizePolicy(sizePolicy_EE)
        self.glCent = QGridLayout(self.widCent)
        self.glCent.setObjectName(u"glCent")


        ###############################################
        #                Groupbox order               #
        # Month, Income, Outcome, Current, Move, Stat #
        ###############################################


        # Month groupbox
        self.gbMonth = QGroupBox(self.widCent)
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

        self.glCent.addWidget(self.gbMonth, 0, 0, 1, 2)
        # end Month


        # Income groupbox
        self.gbIncome = QGroupBox(self.widCent)
        self.gbIncome.setObjectName(u"gbIncome")
        self.glIncome = QGridLayout(self.gbIncome)
        self.glIncome.setObjectName(u"glIncome")

        self.lbTitleIncome = []
        for x, y, w, h in ((0, 0, 1, 2), (1, 0, 1, 2), (1, 2, 1, 2)):
            lb = QLabel(self.gbIncome)
            lb.setAlignment(Qt.AlignCenter)
            lb.setObjectName(f'lbTitleIncome{x+1}{y+1}')
            self.glIncome.addWidget(lb, x, y, w, h)
            self.lbTitleIncome.append(lb)

        self.lbSumIncome = QLabel(self.gbIncome)
        self.lbSumIncome.setObjectName(u"lbSumIncome")
        self.lbSumIncome.setAlignment(Qt.AlignCenter)
        self.glIncome.addWidget(self.lbSumIncome, 0, 2, 1, 2)

        self.glCent.addWidget(self.gbIncome, 3, 0, 1, 1)
        # end Income


        # Outcome groupbox
        self.gbOutcome = QGroupBox(self.widCent)
        self.gbOutcome.setObjectName(u"gbOutcome")
        self.glOutcome = QGridLayout(self.gbOutcome)
        self.glOutcome.setObjectName(u"glOutcome")

        self.lbTitleOutcome = []
        for x, y, w, h in ((0, 0, 1, 2), (1, 0, 1, 2), (1, 2, 1, 2)):
            lb = QLabel(self.gbOutcome)
            lb.setAlignment(Qt.AlignCenter)
            lb.setObjectName(f'lbTitleOutcome{x+1}{y+1}')
            self.glOutcome.addWidget(lb, x, y, w, h)
            self.lbTitleOutcome.append(lb)

        self.lbSumOutcome = QLabel(self.gbOutcome)
        self.lbSumOutcome.setObjectName(u"lbSumOutcome")
        self.lbSumOutcome.setAlignment(Qt.AlignCenter)
        self.glOutcome.addWidget(self.lbSumOutcome, 0, 2, 1, 2)

        self.glCent.addWidget(self.gbOutcome, 2, 1, 1, 1)
        # end Outcome


        # Current groupbox
        self.gbCurrent = QGroupBox(self.widCent)
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

        self.lbTitleCash = QLabel(self.gbCurrent)
        self.lbTitleCash.setObjectName(u"lbTitleCash")
        self.lbTitleCash.setAlignment(Qt.AlignCenter)
        self.glCurrent.addWidget(self.lbTitleCash, 1, 0, 1, 1)

        self.lbSumCash = QLabel(self.gbCurrent)
        self.lbSumCash.setObjectName(u"lbSumCash")
        self.lbSumCash.setAlignment(Qt.AlignCenter)
        self.glCurrent.addWidget(self.lbSumCash, 1, 1, 1, 1)

        self.glCent.addWidget(self.gbCurrent, 2, 0, 1, 1)
        # end Current


        # Move groupbox
        self.gbMove = QGroupBox(self.widCent)
        self.gbMove.setObjectName(u"gbMove")
        self.glMove = QGridLayout(self.gbMove)
        self.glMove.setObjectName(u"glMove")

        self.lbTitleMove = []
        for x, y, w, h in ((0, 0, 1, 2), (1, 0, 1, 2), (1, 2, 1, 2)):
            lb = QLabel(self.gbMove)
            lb.setAlignment(Qt.AlignCenter)
            lb.setObjectName(f'lbTitleMove{x+1}{y+1}')
            self.glMove.addWidget(lb, x, y, w, h)
            self.lbTitleMove.append(lb)

        self.lbSumMove = QLabel(self.gbMove)
        self.lbSumMove.setObjectName(u"lbSumMove")
        self.lbSumMove.setAlignment(Qt.AlignCenter)
        self.glMove.addWidget(self.lbSumMove, 0, 2, 1, 2)

        self.glCent.addWidget(self.gbMove, 3, 1, 1, 1)
        # end Move


        # Stat groupbox
        self.gbStat = QGroupBox(self.widCent)
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

        self.glCent.addWidget(self.gbStat, 1, 0, 1, 2)
        # end Stat


        self.scCent.setWidget(self.widCent)

        self.retranslateUi()

        QMetaObject.connectSlotsByName(self)
    # setupUi

    def retranslateUi(self):
        self.gbMonth.setTitle(QCoreApplication.translate("TabStatM", u"\ud1b5\uacc4 \uc124\uc815", None))
        self.lbTitleMonth.setText(QCoreApplication.translate("TabStatM", u"\uc5f0-\uc6d4", None))

        income_txt = ('총액', '요목별', '원천별')
        self.gbIncome.setTitle(QCoreApplication.translate("TabStatM", u"\uc218\uc785", None))
        for wid, txt in zip(self.lbTitleIncome, income_txt):
            wid.setText(txt)

        outcome_txt = ('총액', '요목별', '원천별')
        self.gbOutcome.setTitle(QCoreApplication.translate("TabStatM", u"\uc9c0\ucd9c", None))
        for wid, txt in zip(self.lbTitleOutcome, outcome_txt):
            wid.setText(txt)

        self.gbCurrent.setTitle(QCoreApplication.translate("TabStatM", u"\ud604 \uc7ac\uc0b0", None))
        self.lbTitleCurrent.setText(QCoreApplication.translate("TabStatM", u"\ucd1d \uc7ac\uc0b0", None))
        self.lbTitleCash.setText(QCoreApplication.translate("TabStatM", u"\ud604\uae08\uc131", None))

        move_txt = ('총액', '이동_出', '이동_入')
        self.gbMove.setTitle(QCoreApplication.translate("TabStatM", u"\uc774\ub3d9\uc561", None))
        for wid, txt in zip(self.lbTitleMove, move_txt):
            wid.setText(txt)

        stat_txt = ('순수익', '필수지출', '초과지출')
        self.gbStat.setTitle(QCoreApplication.translate("TabStatM", u"\ud1b5\uacc4", None))
        for wid, txt in zip((self.lbTitleNet, self.lbTitleOut1, self.lbTitleOut2), stat_txt):
            wid.setText(txt)
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
        self.acSave.setShortcut(QKeySequence("Ctrl+S"))
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

        self.netMenu = self.fileMenu.addMenu('네트워크')
        self.acGet = self.netMenu.addAction('다운로드')
        self.acPut = self.netMenu.addAction('업로드')

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
