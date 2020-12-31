from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

sizePolicy_PF = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
sizePolicy_PF.setHorizontalStretch(0)
sizePolicy_PF.setVerticalStretch(0)

sizePolicy_FF = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
sizePolicy_FF.setHorizontalStretch(0)
sizePolicy_FF.setVerticalStretch(0)


class TabStatM(object):
    def setupUi(self, TabStatM):
        if not TabStatM.objectName():
            TabStatM.setObjectName(u"TabStatM")
        TabStatM.setFixedSize(776,510)
        
        self.glCent = QGridLayout(TabStatM)
        self.glCent.setObjectName(u"glCent")


        self.gbMonth = QGroupBox(TabStatM)
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


        self.gbIncome = QGroupBox(TabStatM)
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


        self.gbOutcome = QGroupBox(TabStatM)
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


        self.gbCurrent = QGroupBox(TabStatM)
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


        self.gbMove = QGroupBox(TabStatM)
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


        self.gbStat = QGroupBox(TabStatM)
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

        self.retranslateUi(TabStatM)

        QMetaObject.connectSlotsByName(TabStatM)
    # setupUi

    def retranslateUi(self, TabStatM):
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


class Test(QWidget,TabStatM):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


if __name__=='__main__':
    app=QApplication()
    win=Test()
    win.show()
    app.exec_()
