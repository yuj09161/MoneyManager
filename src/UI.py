# pylint: disable=attribute-defined-outside-init, line-too-long, too-many-instance-attributes
# pylint: disable=too-many-statements, too-few-public-methods, undefined-variable

from PySide6.QtCore import Qt, Signal, QCoreApplication, QSize, QMetaObject
from PySide6.QtGui import QRegularExpressionValidator, QAction, QKeySequence
from PySide6.QtWidgets import (
    QWidget, QGroupBox, QTabWidget, QScrollArea,
    QVBoxLayout, QHBoxLayout, QGridLayout,
    QSizePolicy, QSpacerItem,
    QLabel, QPushButton, QRadioButton, QCheckBox,
    QPlainTextEdit, QLineEdit, QComboBox, QCalendarWidget,
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

sizePolicy_EF = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
sizePolicy_EF.setHorizontalStretch(0)
sizePolicy_EF.setVerticalStretch(0)

sizePolicy_EE = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
sizePolicy_EE.setHorizontalStretch(0)
sizePolicy_EE.setVerticalStretch(0)


class EscapeLineEdit(QLineEdit):
    escapePressed = Signal()

    def keyPressEvent(self, event):
        if event == QKeySequence.Cancel:
            self.escapePressed.emit()
        else:
            super().keyPressEvent(event)


class Ui_Txt:
    # pylint: disable=no-member

    def setupUi(self, Win, title, info_text):
        if not self.objectName():
            self.setObjectName("info")
        Win.setFixedSize(600, 500)
        Win.setWindowFlags(self.windowFlags() ^ Qt.WindowMinMaxButtonsHint)

        self.centralwidget = QWidget(self)
        self.centralwidget.setObjectName("centralwidget")

        self.vlCent = QVBoxLayout(self.centralwidget)
        self.vlCent.setObjectName("vlCent")


        self.pteMain = QPlainTextEdit(self.centralwidget)
        self.pteMain.setObjectName("pteMain")
        self.pteMain.setReadOnly(True)
        self.vlCent.addWidget(self.pteMain)


        self.widBot = QWidget(self.centralwidget)
        self.widBot.setObjectName("widBot")
        self.hlBot = QHBoxLayout(self.widBot)
        self.hlBot.setObjectName("hlBot")
        self.hlBot.setContentsMargins(0, 0, 0, 0)

        self.sp = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.hlBot.addItem(self.sp)

        self.btnExit = QPushButton(self.widBot)
        self.btnExit.setObjectName("btnExit")
        self.hlBot.addWidget(self.btnExit)

        self.vlCent.addWidget(self.widBot)


        self.setCentralWidget(self.centralwidget)

        self.retranslateUi(title, info_text)

    def retranslateUi(self, title, info_text):
        self.setWindowTitle(title)
        self.pteMain.setPlainText(info_text)
        self.btnExit.setText(QCoreApplication.translate("info", "\ub2eb\uae30", None))


class Ui_Info(Ui_Txt):
    def setupUi(self, Win, title, info_text):
        super().setupUi(Win, title, info_text)

        self.btnQt = QPushButton(self.centralwidget)
        self.btnQt.setObjectName("btnQt")
        self.hlBot.insertWidget(0, self.btnQt)

        self.retranslateUi_1()

    def retranslateUi_1(self):
        self.btnQt.setText(QCoreApplication.translate("info", "About Qt", None))


class Ui_Login:
    def setupUi(self, Login):
        if not Login.objectName():
            Login.setObjectName("Login")
        Login.resize(400, 100)
        Login.setWindowFlags(Qt.Dialog)

        self.centralwidget = QWidget(Login)
        self.centralwidget.setObjectName("centralwidget")
        self.glCent = QGridLayout(self.centralwidget)
        self.glCent.setObjectName("glCent")

        self.lbTitleUser = QLabel(self.centralwidget)
        self.lbTitleUser.setObjectName("lbTitleUser")
        self.lbTitleUser.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)
        self.glCent.addWidget(self.lbTitleUser, 0, 0, 1, 1)

        self.lbTitlePass = QLabel(self.centralwidget)
        self.lbTitlePass.setObjectName("lbTitlePass")
        self.lbTitlePass.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)
        self.glCent.addWidget(self.lbTitlePass, 0, 2, 1, 1)

        self.lbTitlePath = QLabel(self.centralwidget)
        self.lbTitlePath.setObjectName("lbTitlePath")
        self.lbTitlePath.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)
        self.glCent.addWidget(self.lbTitlePath, 2, 0, 1, 1)

        self.lnUser = QLineEdit(self.centralwidget)
        self.lnUser.setObjectName("lnUser")
        self.glCent.addWidget(self.lnUser, 0, 1, 1, 1)

        self.lnPass = QLineEdit(self.centralwidget)
        self.lnPass.setObjectName("lnPass")
        self.lnPass.setEchoMode(QLineEdit.Password)
        self.glCent.addWidget(self.lnPass, 0, 3, 1, 1)

        self.lnPath = QLineEdit(self.centralwidget)
        self.lnPath.setObjectName("lnPath")
        self.glCent.addWidget(self.lnPath, 2, 1, 1, 3)

        self.widBot = QWidget(self.centralwidget)
        self.widBot.setObjectName("widBot")
        self.hlBot = QHBoxLayout(self.widBot)
        self.hlBot.setObjectName("hlBot")
        self.hlBot.setContentsMargins(0, 0, 0, 0)

        self.chkSave = QCheckBox(self.widBot)
        self.chkSave.setObjectName("chkSave")
        self.hlBot.addWidget(self.chkSave)

        self.btnFile = QPushButton(self.widBot)
        self.btnFile.setObjectName("btnFile")
        self.hlBot.addWidget(self.btnFile)

        self.sp = QSpacerItem(196, 21, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.hlBot.addItem(self.sp)

        self.chkEnc = QCheckBox(self.widBot)
        self.chkEnc.setObjectName("chkEnc")
        self.hlBot.addWidget(self.chkEnc)

        self.btnConnect = QPushButton(self.widBot)
        self.btnConnect.setObjectName("btnConnect")
        self.hlBot.addWidget(self.btnConnect)

        self.glCent.addWidget(self.widBot, 3, 0, 1, 4)

        Login.setCentralWidget(self.centralwidget)

        self.retranslateUi(Login)

        QMetaObject.connectSlotsByName(Login)
    # setupUi

    def retranslateUi(self, Login):
        Login.setWindowTitle(QCoreApplication.translate("Login", "\uc11c\ubc84 \ub85c\uadf8\uc778", None))
        self.lbTitleUser.setText(QCoreApplication.translate("Login", "\uc0ac\uc6a9\uc790\uba85: ", None))
        self.lbTitlePass.setText(QCoreApplication.translate("Login", "\uc554\ud638: ", None))
        self.lbTitlePath.setText(QCoreApplication.translate("Login", "\uc11c\ubc84 \uc8fc\uc18c: ", None))
        self.chkSave.setText(QCoreApplication.translate("Login", "\uacc4\uc815 \uc800\uc7a5?", None))
        self.btnFile.setText(QCoreApplication.translate("Login", "\ud30c\uc77c \uc120\ud0dd", None))
        self.chkEnc.setText(QCoreApplication.translate("Login", "\uc554\ud638\ud654?", None))
        self.btnConnect.setText(QCoreApplication.translate("Login", "\uc5f0\uacb0", None))
    # retranslateUi


class Ui_Pg:
    def setupUi(self, Pg):
        if not Pg.objectName():
            Pg.setObjectName("Pg")
        Pg.setFixedSize(200, 70)
        Pg.setWindowFlags(Qt.SplashScreen)

        self.centralwidget = QWidget(Pg)
        self.centralwidget.setObjectName("centralwidget")
        self.vlCent = QVBoxLayout(self.centralwidget)
        self.vlCent.setObjectName("vlCent")

        self.lbStatus = QLabel(self.centralwidget)
        self.lbStatus.setObjectName("lbStatus")
        self.lbStatus.setAlignment(Qt.AlignCenter)
        self.vlCent.addWidget(self.lbStatus)

        self.pgPg = QProgressBar(self.centralwidget)
        self.pgPg.setObjectName("pgPg")
        self.pgPg.setRange(0, 0)
        self.pgPg.setTextVisible(False)
        self.vlCent.addWidget(self.pgPg)

        Pg.setCentralWidget(self.centralwidget)

        QMetaObject.connectSlotsByName(Pg)
    # setupUi


class Ui_GbAddDelCate:
    def setupUi(self, GbAddDelCate):
        self.vlMain = QVBoxLayout(GbAddDelCate)
        self.vlMain.setObjectName("vlMain")

        self.lvOrd = QListView(GbAddDelCate)
        self.lvOrd.setEditTriggers(QListView.NoEditTriggers)
        self.lvOrd.setDragDropMode(QListView.InternalMove)
        self.vlMain.addWidget(self.lvOrd)

        self.widAdd = QWidget(GbAddDelCate)
        self.widAdd.setObjectName("widAdd")
        sizePolicy_EP.setHeightForWidth(self.widAdd.sizePolicy().hasHeightForWidth())
        self.widAdd.setSizePolicy(sizePolicy_EP)

        self.glEdit = QGridLayout(self.widAdd)
        self.glEdit.setObjectName("glEdit")
        self.glEdit.setContentsMargins(0, 7, 0, 7)

        self.lnAdd = QLineEdit(self.widAdd)
        self.lnAdd.setObjectName("lnAdd")
        self.lnAdd.setAlignment(Qt.AlignCenter)
        self.lnAdd.setMaxLength(10)
        self.glEdit.addWidget(self.lnAdd, 0, 0, 1, 1)

        self.btnAdd = QPushButton(self.widAdd)
        self.btnAdd.setObjectName("btnAdd")
        self.glEdit.addWidget(self.btnAdd, 0, 1, 1, 1)

        self.btnApply = QPushButton(self.widAdd)
        self.btnApply.setObjectName("btnApply")
        self.btnApply.hide()
        self.glEdit.addWidget(self.btnApply, 0, 1, 1, 1)

        self.btnCancel = QPushButton(self.widAdd)
        self.btnCancel.setObjectName("btnCancel")
        self.btnCancel.hide()
        self.glEdit.addWidget(self.btnCancel, 1, 1, 1, 1)

        self.vlMain.addWidget(self.widAdd)

        self.retranslateUi()

    def retranslateUi(self):
        self.btnAdd.setText(QCoreApplication.translate("MoneyManage", "\ucd94\uac00", None))
        self.btnApply.setText(QCoreApplication.translate("MoneyManage", "\uc218\uc815", None))
        self.btnCancel.setText(QCoreApplication.translate("MoneyManage", "\ucde8\uc18c", None))


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
        TabCate.setObjectName("tabCate")
        self.glCate = QGridLayout(TabCate)
        self.glCate.setObjectName("glCate")

        TabCate.gbSrc.setObjectName("gbSrc")
        self.glCate.addWidget(TabCate.gbSrc, 0, 0, 1, 1)

        TabCate.gbIn.setObjectName("gbIn")
        self.glCate.addWidget(TabCate.gbIn, 0, 1, 1, 1)

        TabCate.gbOut.setObjectName("gbOut")
        self.glCate.addWidget(TabCate.gbOut, 0, 2, 1, 1)

        self.retranslateUi(TabCate)

    def retranslateUi(self, TabCate):
        TabCate.gbSrc.setTitle(QCoreApplication.translate("MoneyManage", "\uc6d0\ucc9c", None))
        TabCate.gbIn.setTitle(QCoreApplication.translate("MoneyManage", "\uc218\uc785 \uc0c1\uc138", None))
        TabCate.gbOut.setTitle(QCoreApplication.translate("MoneyManage", "\uc9c0\ucd9c \uc0c1\uc138(\uc0ac\uc6a9\ucc98)", None))


class Ui_TabData:
    def setupUi(self, TabData):
        TabData.setObjectName("TabData")
        self.vlData = QVBoxLayout(TabData)
        self.vlData.setObjectName("vlData")

        self.treeData = QTreeView(TabData)
        self.treeData.setObjectName("treeData")
        self.treeData.setEditTriggers(QListView.NoEditTriggers)
        self.vlData.addWidget(self.treeData)

        self.widInput = QWidget(TabData)
        self.widInput.setObjectName("widInput")
        self.glDataIn = QGridLayout(self.widInput)
        self.glDataIn.setObjectName("glDataIn")

        self.lbDate = QLabel(self.widInput)
        self.lbDate.setObjectName("lbDate")
        self.glDataIn.addWidget(self.lbDate, 0, 0, 1, 1, Qt.AlignHCenter)

        self.lbType = QLabel(self.widInput)
        self.lbType.setObjectName("lbType")
        self.glDataIn.addWidget(self.lbType, 0, 1, 1, 1, Qt.AlignHCenter)

        self.lbSrc = QLabel(self.widInput)
        self.lbSrc.setObjectName("lbSrc")
        self.glDataIn.addWidget(self.lbSrc, 0, 2, 1, 1, Qt.AlignHCenter)

        self.lbDetail = QLabel(self.widInput)
        self.lbDetail.setObjectName("lbDetail")
        self.glDataIn.addWidget(self.lbDetail, 0, 3, 1, 1, Qt.AlignHCenter)

        self.lbCost = QLabel(self.widInput)
        self.lbCost.setObjectName("lbCost")
        self.glDataIn.addWidget(self.lbCost, 0, 4, 1, 1, Qt.AlignHCenter)

        self.lbDesc = QLabel(self.widInput)
        self.lbDesc.setObjectName("lbDesc")
        self.glDataIn.addWidget(self.lbDesc, 0, 5, 1, 1, Qt.AlignHCenter)

        self.btnCancel = QPushButton(self.widInput)
        self.btnCancel.setObjectName("btnCancel")
        self.btnCancel.hide()
        self.glDataIn.addWidget(self.btnCancel, 0, 6, 1, 1)

        self.btnUp = QPushButton(self.widInput)
        self.btnUp.setObjectName("btnUp")
        self.btnUp.hide()
        self.btnUp.setMaximumWidth(25)
        self.glDataIn.addWidget(self.btnUp, 0, 7, 1, 1)

        self.lnDate = EscapeLineEdit(self.widInput)
        self.lnDate.setObjectName("lnDate")
        self.lnDate.setAlignment(Qt.AlignCenter)
        self.lnDate.setMaximumSize(QSize(75, 16777215))
        self.glDataIn.addWidget(self.lnDate, 1, 0, 1, 1)

        self.cbType = QComboBox(self.widInput)
        self.cbType.setObjectName("cbType")
        self.glDataIn.addWidget(self.cbType, 1, 1, 1, 1)

        self.cbSrc = QComboBox(self.widInput)
        self.cbSrc.setObjectName("cbSrc")
        self.cbSrc.setMinimumSize(QSize(125, 1))
        self.cbSrc.setMaximumSize(QSize(125, 16777215))
        self.glDataIn.addWidget(self.cbSrc, 1, 2, 1, 1)

        self.cbDetail = QComboBox(self.widInput)
        self.cbDetail.setObjectName("cbDetail")
        self.cbDetail.setMinimumSize(QSize(125, 1))
        self.cbDetail.setMaximumSize(QSize(125, 16777215))
        self.glDataIn.addWidget(self.cbDetail, 1, 3, 1, 1)

        self.lnCost = QLineEdit(self.widInput)
        self.lnCost.setAlignment(Qt.AlignCenter)
        self.lnCost.setObjectName("lnCost")
        self.lnCost.setMaximumSize(QSize(75, 16777215))
        self.glDataIn.addWidget(self.lnCost, 1, 4, 1, 1)

        self.lnDetail = QLineEdit(self.widInput)
        self.lnDetail.setObjectName("lnDetail")
        self.lnDetail.setAlignment(Qt.AlignCenter)
        self.lnDetail.setMaxLength(60)
        self.glDataIn.addWidget(self.lnDetail, 1, 5, 1, 1)

        self.btnAddData = QPushButton(self.widInput)
        self.btnAddData.setObjectName("btnAddData")
        self.glDataIn.addWidget(self.btnAddData, 1, 6, 1, 1)

        self.btnEdit = QPushButton(self.widInput)
        self.btnEdit.setObjectName("btnEdit")
        self.btnEdit.hide()
        self.glDataIn.addWidget(self.btnEdit, 1, 6, 1, 1)

        self.btnDown = QPushButton(self.widInput)
        self.btnDown.setObjectName("btnDown")
        self.btnDown.hide()
        self.btnDown.setMaximumWidth(25)
        self.glDataIn.addWidget(self.btnDown, 1, 7, 1, 1)

        self.vlData.addWidget(self.widInput)

        self.retranslateUi()

    def retranslateUi(self):
        self.lbDate.setText(QCoreApplication.translate("MainWin", "\uc77c\uc2dc", None))
        self.lbType.setText(QCoreApplication.translate("MainWin", "\uad6c\ubd84", None))
        self.lbSrc.setText(QCoreApplication.translate("MainWin", "\uc6d0\ucc9c", None))
        self.lbDetail.setText(QCoreApplication.translate("MainWin", "\uc0c1\uc138", None))
        self.lbCost.setText(QCoreApplication.translate("MainWin", "\uae08\uc561", None))
        self.lbDesc.setText(QCoreApplication.translate("MainWin", "\uc124\uba85", None))

        self.btnAddData.setText(QCoreApplication.translate("MoneyManage", "\ub370\uc774\ud130 \ucd94\uac00", None))
        self.btnEdit.setText(QCoreApplication.translate("MoneyManage", "\uc218\uc815", None))
        self.btnCancel.setText(QCoreApplication.translate("MoneyManage", "\ucde8\uc18c", None))
        self.btnUp.setText(QCoreApplication.translate("MoneyManage", "\u25b2", None))
        self.btnDown.setText(QCoreApplication.translate("MoneyManage", "\u25bc", None))

        self.lnDate.setInputMask(r'2\0D9-99-99;_')
        self.lnDate.setValidator(QRegularExpressionValidator('20[1-9_][0-9_]-(0[1-9_]|1[0-2_]|__)-(0[1-9_]|[12][0-9_]|3[01_]|__)'))
        self.lnCost.setValidator(QRegularExpressionValidator('[1-9][0-9]{0,7}'))


class Ui_TabStatS:
    def setupUi(self, TabStatS):
        TabStatS.setObjectName("tabStatS")
        self.glSum = QGridLayout(TabStatS)
        self.glSum.setObjectName("glSum")

        self.treeStatS = QTreeView(TabStatS)
        self.treeStatS.setObjectName("treeStatS")
        self.treeStatS.setEditTriggers(QTreeView.NoEditTriggers)
        self.glSum.addWidget(self.treeStatS, 0, 0, 1, 1)


class Ui_TabStatM:
    def setupUi(self, TabStatM):
        if not TabStatM.objectName():
            TabStatM.setObjectName("TabStatM")

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
        self.glCent.setObjectName("glCent")


        ######################
        # Groupbox positions #
        #      Interval      #
        #        Stat        #
        # Current || Outcome #
        # Income  ||  Move   #
        ######################


        # Interval groupbox
        self.gbInterval = QGroupBox(self.widCent)
        self.gbInterval.setObjectName("gbInterval")
        sizePolicy_PF.setHeightForWidth(self.gbInterval.sizePolicy().hasHeightForWidth())
        self.gbInterval.setSizePolicy(sizePolicy_PF)
        self.glInterval = QGridLayout(self.gbInterval)
        self.glInterval.setObjectName("glInterval")

        self.widIntvIn = QWidget(self.gbInterval)
        sizePolicy_EF.setHeightForWidth(self.widIntvIn.sizePolicy().hasHeightForWidth())
        self.widIntvIn.setSizePolicy(sizePolicy_EF)
        self.hlIntvIn = QHBoxLayout(self.widIntvIn)
        self.hlIntvIn.setContentsMargins(0, 0, 0, 0)

        self.rbMonthly = QRadioButton(self.gbInterval)
        self.rbMonthly.setObjectName('rbMonthly')
        sizePolicy_FF.setHeightForWidth(self.rbMonthly.sizePolicy().hasHeightForWidth())
        self.rbMonthly.setSizePolicy(sizePolicy_FF)
        self.hlIntvIn.addWidget(self.rbMonthly)

        self.rbWeekly = QRadioButton(self.gbInterval)
        self.rbWeekly.setObjectName('rbWeekly')
        sizePolicy_FF.setHeightForWidth(self.rbWeekly.sizePolicy().hasHeightForWidth())
        self.rbWeekly.setSizePolicy(sizePolicy_FF)
        self.hlIntvIn.addWidget(self.rbWeekly)

        self.rbDaily = QRadioButton(self.gbInterval)
        self.rbDaily.setObjectName('rbDaily')
        sizePolicy_FF.setHeightForWidth(self.rbDaily.sizePolicy().hasHeightForWidth())
        self.rbDaily.setSizePolicy(sizePolicy_FF)
        self.hlIntvIn.addWidget(self.rbDaily)

        self.glInterval.addWidget(self.widIntvIn, 0, 0, 1, 1)

        self.cbMonth = QComboBox(self.gbInterval)
        self.cbMonth.setObjectName("cbMonth")
        sizePolicy_EF.setHeightForWidth(self.cbMonth.sizePolicy().hasHeightForWidth())
        self.cbMonth.setSizePolicy(sizePolicy_EF)
        self.glInterval.addWidget(self.cbMonth, 0, 1, 1, 1)

        self.calInterval = QCalendarWidget(self.gbInterval)
        self.calInterval.setObjectName("calInterval")
        sizePolicy_EF.setHeightForWidth(self.calInterval.sizePolicy().hasHeightForWidth())
        self.calInterval.setSizePolicy(sizePolicy_EF)
        self.calInterval.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)
        self.calInterval.setGridVisible(True)
        self.calInterval.hide()
        self.glInterval.addWidget(self.calInterval, 0, 1, 1, 1)

        self.glCent.addWidget(self.gbInterval, 0, 0, 1, 2)
        # end Interval


        # Stat groupbox
        self.gbStat = QGroupBox(self.widCent)
        self.gbStat.setObjectName("gbStat")
        sizePolicy_PF.setHeightForWidth(self.gbStat.sizePolicy().hasHeightForWidth())
        self.gbStat.setSizePolicy(sizePolicy_PF)
        self.glStat = QGridLayout(self.gbStat)
        self.glStat.setObjectName("glStat")

        self.lbTitleInStat = QLabel(self.gbStat)
        self.lbTitleInStat.setObjectName("lbTitleInStat")
        sizePolicy_PF.setHeightForWidth(self.lbTitleInStat.sizePolicy().hasHeightForWidth())
        self.lbTitleInStat.setSizePolicy(sizePolicy_PF)
        self.lbTitleInStat.setAlignment(Qt.AlignCenter)
        self.glStat.addWidget(self.lbTitleInStat, 0, 0, 1, 1)

        self.lbTitleOutStat = QLabel(self.gbStat)
        self.lbTitleOutStat.setObjectName("lbTitleOutStat")
        sizePolicy_PF.setHeightForWidth(self.lbTitleOutStat.sizePolicy().hasHeightForWidth())
        self.lbTitleOutStat.setSizePolicy(sizePolicy_PF)
        self.lbTitleOutStat.setAlignment(Qt.AlignCenter)
        self.glStat.addWidget(self.lbTitleOutStat, 0, 1, 1, 1)

        self.lbTitleNet = QLabel(self.gbStat)
        self.lbTitleNet.setObjectName("lbTitleNet")
        sizePolicy_PF.setHeightForWidth(self.lbTitleNet.sizePolicy().hasHeightForWidth())
        self.lbTitleNet.setSizePolicy(sizePolicy_PF)
        self.lbTitleNet.setAlignment(Qt.AlignCenter)
        self.glStat.addWidget(self.lbTitleNet, 0, 2, 1, 1)

        self.lbTitleOut1 = QLabel(self.gbStat)
        self.lbTitleOut1.setObjectName("lbTitleOut1")
        sizePolicy_PF.setHeightForWidth(self.lbTitleOut1.sizePolicy().hasHeightForWidth())
        self.lbTitleOut1.setSizePolicy(sizePolicy_PF)
        self.lbTitleOut1.setAlignment(Qt.AlignCenter)
        self.glStat.addWidget(self.lbTitleOut1, 0, 3, 1, 1)

        self.lbTitleOut2 = QLabel(self.gbStat)
        self.lbTitleOut2.setObjectName("lbTitleOut2")
        sizePolicy_PF.setHeightForWidth(self.lbTitleOut2.sizePolicy().hasHeightForWidth())
        self.lbTitleOut2.setSizePolicy(sizePolicy_PF)
        self.lbTitleOut2.setAlignment(Qt.AlignCenter)
        self.glStat.addWidget(self.lbTitleOut2, 0, 4, 1, 1)

        self.lbInStat = QLabel(self.gbStat)
        self.lbInStat.setObjectName("lbInStat")
        sizePolicy_PF.setHeightForWidth(self.lbInStat.sizePolicy().hasHeightForWidth())
        self.lbInStat.setSizePolicy(sizePolicy_PF)
        self.lbInStat.setAlignment(Qt.AlignCenter)
        self.glStat.addWidget(self.lbInStat, 1, 0, 1, 1)

        self.lbOutStat = QLabel(self.gbStat)
        self.lbOutStat.setObjectName("lbOutStat")
        sizePolicy_PF.setHeightForWidth(self.lbOutStat.sizePolicy().hasHeightForWidth())
        self.lbOutStat.setSizePolicy(sizePolicy_PF)
        self.lbOutStat.setAlignment(Qt.AlignCenter)
        self.glStat.addWidget(self.lbOutStat, 1, 1, 1, 1)

        self.lbNet = QLabel(self.gbStat)
        self.lbNet.setObjectName("lbNet")
        sizePolicy_PF.setHeightForWidth(self.lbNet.sizePolicy().hasHeightForWidth())
        self.lbNet.setSizePolicy(sizePolicy_PF)
        self.lbNet.setAlignment(Qt.AlignCenter)
        self.glStat.addWidget(self.lbNet, 1, 2, 1, 1)

        self.lbOut1 = QLabel(self.gbStat)
        self.lbOut1.setObjectName("lbOut1")
        sizePolicy_PF.setHeightForWidth(self.lbOut1.sizePolicy().hasHeightForWidth())
        self.lbOut1.setSizePolicy(sizePolicy_PF)
        self.lbOut1.setAlignment(Qt.AlignCenter)
        self.glStat.addWidget(self.lbOut1, 1, 3, 1, 1)

        self.lbOut2 = QLabel(self.gbStat)
        self.lbOut2.setObjectName("lbOut2")
        sizePolicy_PF.setHeightForWidth(self.lbOut2.sizePolicy().hasHeightForWidth())
        self.lbOut2.setSizePolicy(sizePolicy_PF)
        self.lbOut2.setAlignment(Qt.AlignCenter)
        self.glStat.addWidget(self.lbOut2, 1, 4, 1, 1)

        self.glCent.addWidget(self.gbStat, 1, 0, 1, 2)
        # end Stat


        # Current groupbox
        self.gbCurrent = QGroupBox(self.widCent)
        self.gbCurrent.setObjectName("gbCurrent")
        self.glCurrent = QGridLayout(self.gbCurrent)
        self.glCurrent.setObjectName("glCurrent")

        self.lbTitleCurrent = QLabel(self.gbCurrent)
        self.lbTitleCurrent.setObjectName("lbTitleCurrent")
        self.lbTitleCurrent.setAlignment(Qt.AlignCenter)
        self.glCurrent.addWidget(self.lbTitleCurrent, 0, 0, 1, 1)

        self.lbSumCurrent = QLabel(self.gbCurrent)
        self.lbSumCurrent.setObjectName("lbSumCurrent")
        self.lbSumCurrent.setAlignment(Qt.AlignCenter)
        self.glCurrent.addWidget(self.lbSumCurrent, 0, 1, 1, 1)

        self.lbTitleCash = QLabel(self.gbCurrent)
        self.lbTitleCash.setObjectName("lbTitleCash")
        self.lbTitleCash.setAlignment(Qt.AlignCenter)
        self.glCurrent.addWidget(self.lbTitleCash, 1, 0, 1, 1)

        self.lbSumCash = QLabel(self.gbCurrent)
        self.lbSumCash.setObjectName("lbSumCash")
        self.lbSumCash.setAlignment(Qt.AlignCenter)
        self.glCurrent.addWidget(self.lbSumCash, 1, 1, 1, 1)

        self.glCent.addWidget(self.gbCurrent, 2, 0, 1, 1)
        # end Current


        # Income groupbox
        self.gbIncome = QGroupBox(self.widCent)
        self.gbIncome.setObjectName("gbIncome")
        self.glIncome = QGridLayout(self.gbIncome)
        self.glIncome.setObjectName("glIncome")

        self.lbTitleIncome = []
        for x, y, w, h in ((0, 0, 1, 2), (1, 0, 1, 2), (1, 2, 1, 2)):
            lb = QLabel(self.gbIncome)
            lb.setAlignment(Qt.AlignCenter)
            lb.setObjectName(f'lbTitleIncome{x+1}{y+1}')
            self.glIncome.addWidget(lb, x, y, w, h)
            self.lbTitleIncome.append(lb)

        self.lbSumIncome = QLabel(self.gbIncome)
        self.lbSumIncome.setObjectName("lbSumIncome")
        self.lbSumIncome.setAlignment(Qt.AlignCenter)
        self.glIncome.addWidget(self.lbSumIncome, 0, 2, 1, 2)

        self.glCent.addWidget(self.gbIncome, 3, 0, 1, 1)
        # end Income


        # Outcome groupbox
        self.gbOutcome = QGroupBox(self.widCent)
        self.gbOutcome.setObjectName("gbOutcome")
        self.glOutcome = QGridLayout(self.gbOutcome)
        self.glOutcome.setObjectName("glOutcome")

        self.lbTitleOutcome = []
        for x, y, w, h in ((0, 0, 1, 2), (1, 0, 1, 2), (1, 2, 1, 2)):
            lb = QLabel(self.gbOutcome)
            lb.setAlignment(Qt.AlignCenter)
            lb.setObjectName(f'lbTitleOutcome{x+1}{y+1}')
            self.glOutcome.addWidget(lb, x, y, w, h)
            self.lbTitleOutcome.append(lb)

        self.lbSumOutcome = QLabel(self.gbOutcome)
        self.lbSumOutcome.setObjectName("lbSumOutcome")
        self.lbSumOutcome.setAlignment(Qt.AlignCenter)
        self.glOutcome.addWidget(self.lbSumOutcome, 0, 2, 1, 2)

        self.glCent.addWidget(self.gbOutcome, 2, 1, 1, 1)
        # end Outcome


        # Move groupbox
        self.gbMove = QGroupBox(self.widCent)
        self.gbMove.setObjectName("gbMove")
        self.glMove = QGridLayout(self.gbMove)
        self.glMove.setObjectName("glMove")

        self.lbTitleMove = []
        for x, y, w, h in ((0, 0, 1, 2), (1, 0, 1, 2), (1, 2, 1, 2)):
            lb = QLabel(self.gbMove)
            lb.setAlignment(Qt.AlignCenter)
            lb.setObjectName(f'lbTitleMove{x+1}{y+1}')
            self.glMove.addWidget(lb, x, y, w, h)
            self.lbTitleMove.append(lb)

        self.lbSumMove = QLabel(self.gbMove)
        self.lbSumMove.setObjectName("lbSumMove")
        self.lbSumMove.setAlignment(Qt.AlignCenter)
        self.glMove.addWidget(self.lbSumMove, 0, 2, 1, 2)

        self.glCent.addWidget(self.gbMove, 3, 1, 1, 1)
        # end Move


        self.scCent.setWidget(self.widCent)

        self.retranslateUi()

        QMetaObject.connectSlotsByName(self)
    # setupUi

    def retranslateUi(self):
        self.gbInterval.setTitle(QCoreApplication.translate("TabStatM", "\uae30\uac04 \uc124\uc815", None))
        self.rbMonthly.setText(QCoreApplication.translate("TabStatM", "\uc6d4\uac04", None))
        self.rbWeekly.setText(QCoreApplication.translate("TabStatM", "\uc8fc\uac04", None))
        self.rbDaily.setText(QCoreApplication.translate("TabStatM", "\uc77c\uac04", None))
        self.rbMonthly.setChecked(True)

        income_txt = ('총액', '요목별', '원천별')
        self.gbIncome.setTitle(QCoreApplication.translate("TabStatM", "\uc218\uc785", None))
        for wid, txt in zip(self.lbTitleIncome, income_txt):
            wid.setText(txt)

        outcome_txt = ('총액', '요목별', '원천별')
        self.gbOutcome.setTitle(QCoreApplication.translate("TabStatM", "\uc9c0\ucd9c", None))
        for wid, txt in zip(self.lbTitleOutcome, outcome_txt):
            wid.setText(txt)

        self.gbCurrent.setTitle(QCoreApplication.translate("TabStatM", "\ud604 \uc7ac\uc0b0", None))
        self.lbTitleCurrent.setText(QCoreApplication.translate("TabStatM", "\ucd1d \uc7ac\uc0b0", None))
        self.lbTitleCash.setText(QCoreApplication.translate("TabStatM", "\ud604\uae08\uc131", None))

        move_txt = ('총액', '이동_出', '이동_入')
        self.gbMove.setTitle(QCoreApplication.translate("TabStatM", "\uc774\ub3d9\uc561", None))
        for wid, txt in zip(self.lbTitleMove, move_txt):
            wid.setText(txt)

        stat_txt = ('수익', '지출', '순수익', '필수지출', '초과지출')
        self.gbStat.setTitle(QCoreApplication.translate("TabStatM", "\ud1b5\uacc4", None))
        for wid, txt in zip(
            (
                self.lbTitleInStat,
                self.lbTitleOutStat,
                self.lbTitleNet,
                self.lbTitleOut1,
                self.lbTitleOut2
            ),
            stat_txt
        ):
            wid.setText(txt)
    # retranslateUi


class Ui_MainWin:
    def setupUi(self, MainWin):
        if not MainWin.objectName():
            MainWin.setObjectName("MainWin")
        MainWin.resize(800, 600)

        # Menubar
        self.menubar = QMenuBar(MainWin)
        self.menubar.setObjectName("menubar")

        # File menu
        self.fileMenu = QMenu(self.menubar)
        self.fileMenu.setObjectName("fileMenu")

        self.acLoad = QAction(MainWin)
        self.acLoad.setObjectName("acLoad")
        self.fileMenu.addAction(self.acLoad)

        self.acSave = QAction(MainWin)
        self.acSave.setObjectName("acSave")
        self.acSave.setShortcut(QKeySequence("Ctrl+S"))
        self.fileMenu.addAction(self.acSave)

        self.acSaveAs = QAction(MainWin)
        self.acSaveAs.setObjectName("acSaveAs")
        self.fileMenu.addAction(self.acSaveAs)

        self.fileMenu.addSeparator()

        self.acImport = QAction(MainWin)
        self.acImport.setObjectName("acImport")
        self.fileMenu.addAction(self.acImport)

        self.acExport = QAction(MainWin)
        self.acExport.setObjectName("acExport")
        self.fileMenu.addAction(self.acExport)

        self.fileMenu.addSeparator()

        self.netMenu = self.fileMenu.addMenu('네트워크')
        self.acGet = self.netMenu.addAction('다운로드')
        self.acPut = self.netMenu.addAction('업로드')

        self.fileMenu.addSeparator()

        self.acExit = QAction(MainWin)
        self.acExit.setObjectName("acExit")
        self.fileMenu.addAction(self.acExit)

        self.menubar.addAction(self.fileMenu.menuAction())
        # end File

        # Setting menu
        self.settingMenu = QMenu(self.menubar)
        self.settingMenu.setObjectName("settingMenu")

        self.acHangulInputEnable = QAction(MainWin)
        self.acHangulInputEnable.setObjectName("acHangulInputEnable")
        self.acHangulInputEnable.setCheckable(True)
        self.settingMenu.addAction(self.acHangulInputEnable)

        self.menubar.addAction(self.settingMenu.menuAction())
        # end Setting

        # Info menu
        self.infoMenu = QMenu(self.menubar)
        self.infoMenu.setObjectName("infoMenu")

        self.acOpenLicense = QAction(MainWin)
        self.acOpenLicense.setObjectName("acOpenLicense")
        self.infoMenu.addAction(self.acOpenLicense)

        self.acLicense = QAction(MainWin)
        self.acLicense.setObjectName("acLicense")
        self.infoMenu.addAction(self.acLicense)

        self.infoMenu.addSeparator()

        self.acInfo = QAction(MainWin)
        self.acInfo.setObjectName("acInfo")
        self.infoMenu.addAction(self.acInfo)

        self.menubar.addAction(self.infoMenu.menuAction())
        # end Info

        MainWin.setMenuBar(self.menubar)
        # End menubar


        self.centralwidget = QWidget(MainWin)
        self.centralwidget.setObjectName("centralwidget")
        self.glCent = QGridLayout(self.centralwidget)
        self.glCent.setObjectName("glCent")
        MainWin.setCentralWidget(self.centralwidget)

        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")

        self.glCent.addWidget(self.tabWidget, 0, 0, 1, 1)


        self.statusbar = QStatusBar(MainWin)
        self.statusbar.setObjectName("statusbar")
        MainWin.setStatusBar(self.statusbar)


        self.retranslateUi(MainWin)
    # setupUi

    def retranslateUi(self, MainWin):
        MainWin.setWindowTitle(QCoreApplication.translate("MainWin", "\uc7ac\uc0b0\uad00\ub9ac", None))

        self.fileMenu.setTitle(QCoreApplication.translate("MainWin", "\ud30c\uc77c", None))
        self.acLoad.setText(QCoreApplication.translate("MainWin", "\ubd88\ub7ec\uc624\uae30", None))
        self.acSave.setText(QCoreApplication.translate("MainWin", "\uc800\uc7a5", None))
        self.acSaveAs.setText(QCoreApplication.translate("MainWin", "\ub2e4\ub978 \uc774\ub984\uc73c\ub85c \uc800\uc7a5", None))
        self.acImport.setText(QCoreApplication.translate("MainWin", '\uac00\uc838\uc624\uae30', None))
        self.acExport.setText(QCoreApplication.translate("MainWin", '\ub0b4\ubcf4\ub0b4\uae30', None))
        self.acExit.setText(QCoreApplication.translate("MainWin", "\uc885\ub8cc", None))

        self.settingMenu.setTitle(QCoreApplication.translate("MainWin", "\uc124\uc815", None))
        self.acHangulInputEnable.setText(QCoreApplication.translate("MainWin", "\ud55c\uae00 \uc785\ub825\uae30 \ud65c\uc131\ud654", None))

        self.infoMenu.setTitle(QCoreApplication.translate("MainWin", "\uc815\ubcf4", None))
        self.acOpenLicense.setText(QCoreApplication.translate("MainWin", "\uc624\ud508 \uc18c\uc2a4 \ub77c\uc774\uc120\uc2a4", None))
        self.acLicense.setText(QCoreApplication.translate("MainWin", "\ub77c\uc774\uc120\uc2a4", None))
        self.acInfo.setText(QCoreApplication.translate("MainWin", "\uc815\ubcf4", None))
        # retranslateUi
