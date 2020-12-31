# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'stat_m.ui'
##
## Created by: Qt User Interface Compiler version 6.0.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class Ui_TabStatM(object):
    def setupUi(self, TabStatM):
        if not TabStatM.objectName():
            TabStatM.setObjectName(u"TabStatM")
        TabStatM.resize(776, 510)
        self.glCent = QGridLayout(TabStatM)
        self.glCent.setObjectName(u"glCent")
        self.gbOutcome = QGroupBox(TabStatM)
        self.gbOutcome.setObjectName(u"gbOutcome")
        self.glOutcome = QGridLayout(self.gbOutcome)
        self.glOutcome.setObjectName(u"glOutcome")
        self.lbTitleOutcome23 = QLabel(self.gbOutcome)
        self.lbTitleOutcome23.setObjectName(u"lbTitleOutcome23")
        self.lbTitleOutcome23.setAlignment(Qt.AlignCenter)

        self.glOutcome.addWidget(self.lbTitleOutcome23, 3, 2, 1, 1)

        self.lbTitleOutcome24 = QLabel(self.gbOutcome)
        self.lbTitleOutcome24.setObjectName(u"lbTitleOutcome24")
        self.lbTitleOutcome24.setAlignment(Qt.AlignCenter)

        self.glOutcome.addWidget(self.lbTitleOutcome24, 3, 3, 1, 1)

        self.lbTitleOutcome21 = QLabel(self.gbOutcome)
        self.lbTitleOutcome21.setObjectName(u"lbTitleOutcome21")
        self.lbTitleOutcome21.setAlignment(Qt.AlignCenter)

        self.glOutcome.addWidget(self.lbTitleOutcome21, 3, 0, 1, 1)

        self.lbTitleOutcome22 = QLabel(self.gbOutcome)
        self.lbTitleOutcome22.setObjectName(u"lbTitleOutcome22")
        self.lbTitleOutcome22.setAlignment(Qt.AlignCenter)

        self.glOutcome.addWidget(self.lbTitleOutcome22, 3, 1, 1, 1)

        self.lbTitleOutcome12 = QLabel(self.gbOutcome)
        self.lbTitleOutcome12.setObjectName(u"lbTitleOutcome12")
        self.lbTitleOutcome12.setAlignment(Qt.AlignCenter)

        self.glOutcome.addWidget(self.lbTitleOutcome12, 1, 2, 1, 2)

        self.lbTitleOutcome11 = QLabel(self.gbOutcome)
        self.lbTitleOutcome11.setObjectName(u"lbTitleOutcome11")
        self.lbTitleOutcome11.setAlignment(Qt.AlignCenter)

        self.glOutcome.addWidget(self.lbTitleOutcome11, 1, 0, 1, 2)

        self.lbTitleOutcome = QLabel(self.gbOutcome)
        self.lbTitleOutcome.setObjectName(u"lbTitleOutcome")
        self.lbTitleOutcome.setAlignment(Qt.AlignCenter)

        self.glOutcome.addWidget(self.lbTitleOutcome, 0, 0, 1, 2)

        self.lbSumOutcome = QLabel(self.gbOutcome)
        self.lbSumOutcome.setObjectName(u"lbSumOutcome")
        self.lbSumOutcome.setAlignment(Qt.AlignCenter)

        self.glOutcome.addWidget(self.lbSumOutcome, 0, 2, 1, 2)


        self.glCent.addWidget(self.gbOutcome, 2, 0, 1, 1)

        self.gbIncome = QGroupBox(TabStatM)
        self.gbIncome.setObjectName(u"gbIncome")
        self.glIncome = QGridLayout(self.gbIncome)
        self.glIncome.setObjectName(u"glIncome")
        self.lbTitleIncome23 = QLabel(self.gbIncome)
        self.lbTitleIncome23.setObjectName(u"lbTitleIncome23")
        self.lbTitleIncome23.setAlignment(Qt.AlignCenter)

        self.glIncome.addWidget(self.lbTitleIncome23, 2, 2, 1, 1)

        self.lbTitleIncome21 = QLabel(self.gbIncome)
        self.lbTitleIncome21.setObjectName(u"lbTitleIncome21")
        self.lbTitleIncome21.setAlignment(Qt.AlignCenter)

        self.glIncome.addWidget(self.lbTitleIncome21, 2, 0, 1, 1)

        self.lbTitleIncome22 = QLabel(self.gbIncome)
        self.lbTitleIncome22.setObjectName(u"lbTitleIncome22")
        self.lbTitleIncome22.setAlignment(Qt.AlignCenter)

        self.glIncome.addWidget(self.lbTitleIncome22, 2, 1, 1, 1)

        self.lbTitleIncome11 = QLabel(self.gbIncome)
        self.lbTitleIncome11.setObjectName(u"lbTitleIncome11")
        self.lbTitleIncome11.setAlignment(Qt.AlignCenter)

        self.glIncome.addWidget(self.lbTitleIncome11, 1, 0, 1, 2)

        self.lbTitleIncome24 = QLabel(self.gbIncome)
        self.lbTitleIncome24.setObjectName(u"lbTitleIncome24")
        self.lbTitleIncome24.setAlignment(Qt.AlignCenter)

        self.glIncome.addWidget(self.lbTitleIncome24, 2, 3, 1, 1)

        self.lbTitleIncome12 = QLabel(self.gbIncome)
        self.lbTitleIncome12.setObjectName(u"lbTitleIncome12")
        self.lbTitleIncome12.setAlignment(Qt.AlignCenter)

        self.glIncome.addWidget(self.lbTitleIncome12, 1, 2, 1, 2)

        self.lbTitleIncome = QLabel(self.gbIncome)
        self.lbTitleIncome.setObjectName(u"lbTitleIncome")
        self.lbTitleIncome.setAlignment(Qt.AlignCenter)

        self.glIncome.addWidget(self.lbTitleIncome, 0, 0, 1, 2)

        self.lbSumIncome = QLabel(self.gbIncome)
        self.lbSumIncome.setObjectName(u"lbSumIncome")
        self.lbSumIncome.setAlignment(Qt.AlignCenter)

        self.glIncome.addWidget(self.lbSumIncome, 0, 2, 1, 2)


        self.glCent.addWidget(self.gbIncome, 1, 0, 1, 1)

        self.gbCurrent = QGroupBox(TabStatM)
        self.gbCurrent.setObjectName(u"gbCurrent")
        self.glCurrent = QGridLayout(self.gbCurrent)
        self.glCurrent.setObjectName(u"glCurrent")
        self.lbTitleCurrent1 = QLabel(self.gbCurrent)
        self.lbTitleCurrent1.setObjectName(u"lbTitleCurrent1")
        self.lbTitleCurrent1.setAlignment(Qt.AlignCenter)

        self.glCurrent.addWidget(self.lbTitleCurrent1, 1, 0, 1, 1)

        self.lbTitleCurrent2 = QLabel(self.gbCurrent)
        self.lbTitleCurrent2.setObjectName(u"lbTitleCurrent2")
        self.lbTitleCurrent2.setAlignment(Qt.AlignCenter)

        self.glCurrent.addWidget(self.lbTitleCurrent2, 1, 1, 1, 1)

        self.lbTitleCurrent = QLabel(self.gbCurrent)
        self.lbTitleCurrent.setObjectName(u"lbTitleCurrent")
        self.lbTitleCurrent.setAlignment(Qt.AlignCenter)

        self.glCurrent.addWidget(self.lbTitleCurrent, 0, 0, 1, 2)


        self.glCent.addWidget(self.gbCurrent, 1, 1, 1, 1)

        self.gbStat = QGroupBox(TabStatM)
        self.gbStat.setObjectName(u"gbStat")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gbStat.sizePolicy().hasHeightForWidth())
        self.gbStat.setSizePolicy(sizePolicy)
        self.glStat = QGridLayout(self.gbStat)
        self.glStat.setObjectName(u"glStat")
        self.lbTitleNet = QLabel(self.gbStat)
        self.lbTitleNet.setObjectName(u"lbTitleNet")
        sizePolicy.setHeightForWidth(self.lbTitleNet.sizePolicy().hasHeightForWidth())
        self.lbTitleNet.setSizePolicy(sizePolicy)
        self.lbTitleNet.setAlignment(Qt.AlignCenter)

        self.glStat.addWidget(self.lbTitleNet, 0, 0, 1, 1)

        self.lbTitleOut1 = QLabel(self.gbStat)
        self.lbTitleOut1.setObjectName(u"lbTitleOut1")
        sizePolicy.setHeightForWidth(self.lbTitleOut1.sizePolicy().hasHeightForWidth())
        self.lbTitleOut1.setSizePolicy(sizePolicy)
        self.lbTitleOut1.setAlignment(Qt.AlignCenter)

        self.glStat.addWidget(self.lbTitleOut1, 0, 1, 1, 1)

        self.lbTitleOut2 = QLabel(self.gbStat)
        self.lbTitleOut2.setObjectName(u"lbTitleOut2")
        sizePolicy.setHeightForWidth(self.lbTitleOut2.sizePolicy().hasHeightForWidth())
        self.lbTitleOut2.setSizePolicy(sizePolicy)
        self.lbTitleOut2.setAlignment(Qt.AlignCenter)

        self.glStat.addWidget(self.lbTitleOut2, 0, 2, 1, 1)

        self.lbNet = QLabel(self.gbStat)
        self.lbNet.setObjectName(u"lbNet")
        sizePolicy.setHeightForWidth(self.lbNet.sizePolicy().hasHeightForWidth())
        self.lbNet.setSizePolicy(sizePolicy)
        self.lbNet.setAlignment(Qt.AlignCenter)

        self.glStat.addWidget(self.lbNet, 1, 0, 1, 1)

        self.lbOut1 = QLabel(self.gbStat)
        self.lbOut1.setObjectName(u"lbOut1")
        sizePolicy.setHeightForWidth(self.lbOut1.sizePolicy().hasHeightForWidth())
        self.lbOut1.setSizePolicy(sizePolicy)
        self.lbOut1.setAlignment(Qt.AlignCenter)

        self.glStat.addWidget(self.lbOut1, 1, 1, 1, 1)

        self.lbOut2 = QLabel(self.gbStat)
        self.lbOut2.setObjectName(u"lbOut2")
        sizePolicy.setHeightForWidth(self.lbOut2.sizePolicy().hasHeightForWidth())
        self.lbOut2.setSizePolicy(sizePolicy)
        self.lbOut2.setAlignment(Qt.AlignCenter)

        self.glStat.addWidget(self.lbOut2, 1, 2, 1, 1)


        self.glCent.addWidget(self.gbStat, 3, 0, 1, 2)

        self.gbMove = QGroupBox(TabStatM)
        self.gbMove.setObjectName(u"gbMove")
        self.glMove = QGridLayout(self.gbMove)
        self.glMove.setObjectName(u"glMove")
        self.lbTitleMove21 = QLabel(self.gbMove)
        self.lbTitleMove21.setObjectName(u"lbTitleMove21")
        self.lbTitleMove21.setAlignment(Qt.AlignCenter)

        self.glMove.addWidget(self.lbTitleMove21, 2, 0, 1, 1)

        self.lbTitleMove23 = QLabel(self.gbMove)
        self.lbTitleMove23.setObjectName(u"lbTitleMove23")
        self.lbTitleMove23.setAlignment(Qt.AlignCenter)

        self.glMove.addWidget(self.lbTitleMove23, 2, 2, 1, 1)

        self.lbTitleMove24 = QLabel(self.gbMove)
        self.lbTitleMove24.setObjectName(u"lbTitleMove24")
        self.lbTitleMove24.setAlignment(Qt.AlignCenter)

        self.glMove.addWidget(self.lbTitleMove24, 2, 3, 1, 1)

        self.lbTitleMove22 = QLabel(self.gbMove)
        self.lbTitleMove22.setObjectName(u"lbTitleMove22")
        self.lbTitleMove22.setAlignment(Qt.AlignCenter)

        self.glMove.addWidget(self.lbTitleMove22, 2, 1, 1, 1)

        self.lbTitleMove11 = QLabel(self.gbMove)
        self.lbTitleMove11.setObjectName(u"lbTitleMove11")
        self.lbTitleMove11.setAlignment(Qt.AlignCenter)

        self.glMove.addWidget(self.lbTitleMove11, 1, 0, 1, 2)

        self.lbTitleMove12 = QLabel(self.gbMove)
        self.lbTitleMove12.setObjectName(u"lbTitleMove12")
        self.lbTitleMove12.setAlignment(Qt.AlignCenter)

        self.glMove.addWidget(self.lbTitleMove12, 1, 2, 1, 2)

        self.lbTitleMove = QLabel(self.gbMove)
        self.lbTitleMove.setObjectName(u"lbTitleMove")
        self.lbTitleMove.setAlignment(Qt.AlignCenter)

        self.glMove.addWidget(self.lbTitleMove, 0, 0, 1, 2)

        self.lbSumMove = QLabel(self.gbMove)
        self.lbSumMove.setObjectName(u"lbSumMove")
        self.lbSumMove.setAlignment(Qt.AlignCenter)

        self.glMove.addWidget(self.lbSumMove, 0, 2, 1, 2)


        self.glCent.addWidget(self.gbMove, 2, 1, 1, 1)

        self.gbMonth = QGroupBox(TabStatM)
        self.gbMonth.setObjectName(u"gbMonth")
        sizePolicy.setHeightForWidth(self.gbMonth.sizePolicy().hasHeightForWidth())
        self.gbMonth.setSizePolicy(sizePolicy)
        self.horizontalLayout = QHBoxLayout(self.gbMonth)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.lbTitleMonth = QLabel(self.gbMonth)
        self.lbTitleMonth.setObjectName(u"lbTitleMonth")
        self.lbTitleMonth.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.lbTitleMonth)

        self.cbMonth = QComboBox(self.gbMonth)
        self.cbMonth.setObjectName(u"cbMonth")

        self.horizontalLayout.addWidget(self.cbMonth)

        self.btnChange = QPushButton(self.gbMonth)
        self.btnChange.setObjectName(u"btnChange")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.btnChange.sizePolicy().hasHeightForWidth())
        self.btnChange.setSizePolicy(sizePolicy1)

        self.horizontalLayout.addWidget(self.btnChange)


        self.glCent.addWidget(self.gbMonth, 0, 0, 1, 2)


        self.retranslateUi(TabStatM)

        QMetaObject.connectSlotsByName(TabStatM)
    # setupUi

    def retranslateUi(self, TabStatM):
        TabStatM.setWindowTitle(QCoreApplication.translate("TabStatM", u"TabStatM", None))
        self.gbOutcome.setTitle(QCoreApplication.translate("TabStatM", u"\uc9c0\ucd9c", None))
        self.lbTitleOutcome12.setText(QCoreApplication.translate("TabStatM", u"\uc6d0\ucc9c\ubcc4", None))
        self.lbTitleOutcome11.setText(QCoreApplication.translate("TabStatM", u"\uc694\ubaa9\ubcc4", None))
        self.lbTitleOutcome.setText(QCoreApplication.translate("TabStatM", u"\ucd1d\uc561", None))
        self.gbIncome.setTitle(QCoreApplication.translate("TabStatM", u"\uc218\uc785", None))
        self.lbTitleIncome11.setText(QCoreApplication.translate("TabStatM", u"\uc694\ubaa9\ubcc4", None))
        self.lbTitleIncome12.setText(QCoreApplication.translate("TabStatM", u"\uc6d0\ucc9c\ubcc4", None))
        self.lbTitleIncome.setText(QCoreApplication.translate("TabStatM", u"\ucd1d\uc561", None))
        self.gbCurrent.setTitle(QCoreApplication.translate("TabStatM", u"\ud604 \uc7ac\uc0b0", None))
        self.gbStat.setTitle(QCoreApplication.translate("TabStatM", u"\ud1b5\uacc4", None))
        self.lbTitleNet.setText(QCoreApplication.translate("TabStatM", u"\uc21c\uc218\uc775", None))
        self.lbTitleOut1.setText(QCoreApplication.translate("TabStatM", u"\ud544\uc218\uc9c0\ucd9c", None))
        self.lbTitleOut2.setText(QCoreApplication.translate("TabStatM", u"\ucd08\uacfc\uc9c0\ucd9c", None))
        self.gbMove.setTitle(QCoreApplication.translate("TabStatM", u"\uc774\ub3d9\uc561", None))
        self.lbTitleMove11.setText(QCoreApplication.translate("TabStatM", u"\uc774\ub3d9_\u51fa", None))
        self.lbTitleMove12.setText(QCoreApplication.translate("TabStatM", u"\uc774\ub3d9_\u5165", None))
        self.lbTitleMove.setText(QCoreApplication.translate("TabStatM", u"\ucd1d\uc561", None))
        self.gbMonth.setTitle(QCoreApplication.translate("TabStatM", u"\ud1b5\uacc4 \uc124\uc815", None))
        self.lbTitleMonth.setText(QCoreApplication.translate("TabStatM", u"\uc5f0-\uc6d4", None))
        self.btnChange.setText(QCoreApplication.translate("TabStatM", u"\ubcc0\uacbd", None))
    # retranslateUi

