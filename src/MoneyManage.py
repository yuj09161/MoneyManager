from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import (
    QMainWindow, QMessageBox, QFileDialog, QLabel, QApplication
)

import os
import json
import io
import datetime
import threading
import traceback

import ftplib

from UI import Ui_Txt, Ui_Info, Ui_Pg, Ui_Login, Ui_MainWin
from model_numpy import Data, Stat_Data


CURRENT_DIR = os.path.dirname(__file__)
CONFIG_DIR = os.environ['localappdata'] + '/hys.moneymanage'
CONFIG_FILE = os.environ['localappdata'] + '/hys.moneymanage/config'


class Txt(QMainWindow, Ui_Txt):
    def __init__(self, parent, title, info_text):
        super().__init__(parent)
        self.setupUi(self, title, info_text)

        self.btnExit.clicked.connect(self.hide)

    def set_text(self, text):
        self.pteMain.setPlainText(text)


class Info(QMainWindow, Ui_Info):
    def __init__(self, parent, title, info_text):
        super().__init__(parent)
        self.setupUi(self, title, info_text)

        self.btnExit.clicked.connect(self.hide)
        self.btnQt.clicked.connect(lambda: QMessageBox.aboutQt(self))


class Pg(QMainWindow, Ui_Pg):
    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi(self)

    def set_detail(self, txt):
        self.lbStatus.setText(txt)


class Login(QMainWindow, Ui_Login):
    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi(self)

        self.username = ''
        self.password = ''
        self.__file = ''
        self.upload = False

        self.btnFile.clicked.connect(self.__set_file)

    def __set_file(self):
        file, _ = QFileDialog.getOpenFileName(
            self, '업로드', filter='데이터 파일(*.json)')
        if file:
            self.__file = file
            self.btnConnect.setEnabled(True)

    def show_get(self):
        self.show()
        self.upload = False
        self.btnFile.hide()
        self.btnConnect.setEnabled(True)
        self.btnConnect.setText('다운로드')

    def show_put(self):
        self.show()
        self.upload = True
        self.btnFile.show()
        self.btnConnect.setEnabled(False)
        self.btnConnect.setText('업로드')

    def do_get(self, signal):
        path_txt = self.lnPath.text()
        self.username = self.lnUser.text()
        self.password = self.lnPass.text()

        try:
            if path_txt:
                tmp, path = path_txt.split('ftp://')[-1].split('/', 1)
                if ':' in tmp:
                    tmp = tmp.split(':')
                    addr, port = tmp
                else:
                    addr = tmp
                    port = 0
                print(addr, port, path)

                with io.BytesIO() as tmp:
                    if self.chkEnc.checkState():
                        with ftplib.FTP_TLS() as srv:
                            srv.connect(addr, port)
                            srv.auth()
                            srv.prot_p()
                            srv.login(self.username, self.password)
                            srv.retrbinary(f'RETR /{path}', tmp.write)
                    else:
                        with ftplib.FTP() as srv:
                            srv.connect(addr, port)
                            srv.login(self.username, self.password)
                            srv.retrbinary(f'RETR /{path}', tmp.write)
                    tmp.seek(0)
                    raw_data = tmp.read()

                data = raw_data.decode('utf-8')
                signal.emit(0, data, '')
            else:
                signal.emit(1, {}, '')
        except Exception:  # pylint: disable=broad-except
            signal.emit(2, {}, traceback.format_exc())

    def do_put(self, data, signal):
        path_txt = self.lnPath.text()
        self.username = self.lnUser.text()
        self.password = self.lnPass.text()
        try:
            if path_txt:
                tmp, path = path_txt.split('ftp://')[-1].split('/', 1)
                if ':' in tmp:
                    tmp = tmp.split(':')
                    addr, port = tmp
                else:
                    addr = tmp
                    port = 0
                print(addr, port, path)

                with io.BytesIO() as tmp:
                    if not data:
                        with open(self.__file, 'r', encoding='utf-8') as file:
                            tmp.write(file.read().encode('utf-8'))
                    else:
                        tmp.write(data.encode('utf-8'))
                    tmp.seek(0)
                    if self.chkEnc.checkState():
                        with ftplib.FTP_TLS() as srv:
                            srv.connect(addr, port)
                            srv.auth()
                            srv.prot_p()
                            srv.login(self.username, self.password)
                            srv.storbinary(f'STOR /{path}', tmp)
                    else:
                        with ftplib.FTP() as srv:
                            srv.connect(addr, port)
                            srv.login(self.username, self.password)
                            srv.storbinary(f'STOR /{path}', tmp)

                signal.emit(0, {}, '')
            else:
                signal.emit(1, {}, '')
        except Exception:  # pylint: disable=broad-except
            signal.emit(2, {}, traceback.format_exc())


class MainWin(QMainWindow, Ui_MainWin):
    __export_text = (
        'Excel 호환(*.tsv)',
        '텍스트 파일(*.txt)'
    )
    __file_text = (
        '데이터 파일(*.moneymanage)',
        'Json 파일(*.json)',
        '모든 파일(*.*)'
    )
    __header_text = (
        '헤더 파일(*.header)',
        'Json 파일(*.json)'
    )

    __export_type = (';;'.join(__export_text))
    __file_type = (';;'.join(__file_text))
    __header_type = (';;'.join(__header_text))

    trans_sig = Signal(int, dict, str)

    def __init__(self, file_name):
        super().__init__()
        self.setupUi(self)

        # define instance variable
        self.__saved = True
        self.__last_file = ''
        self.__title_labels = tuple()
        self.__data_labels = tuple()
        self.__sum_labels = tuple()

        # define models
        self.__data = Data(self.tabData.treeData)
        self.__stat = Stat_Data(self.tabStatS.treeStatS)

        # define sub-windows
        self.__login_win = Login(self)
        self.__login_win.btnConnect.clicked.connect(self.__do_transfer)

        self.__pg_win = Pg(self)

        try:
            with open('Notice', 'r', encoding='utf-8') as file:
                txt = file.read()
        except Exception:  # pylint: disable=broad-except
            self.__opensource_win = Info(
                self, 'Open Source License',
                'Open Source Notice file (Notice) does not exist'
            )
        else:
            self.__opensource_win = Info(self, 'Open Source License', txt)

        try:
            with open('License', 'r', encoding='utf-8') as file:
                txt = file.read()
        except Exception:  # pylint: disable=broad-except
            self.__license_win = Txt(
                self, 'License', 'License file (License) does not exist')
        else:
            self.__license_win = Txt(self, 'License', txt)

        self.__info_win = QMessageBox(self)
        self.__info_win.setWindowTitle('test')
        try:
            with open('Info', 'r', encoding='utf-8') as file:
                txt = file.read()
        except Exception:  # pylint: disable=broad-except
            self.acInfo.setEnabled(False)
        else:
            self.__info_win.setText(txt)
            self.acInfo.triggered.connect(self.__info_win.show)

        self.__err_win = Txt(self, 'Error', '')

        # load data
        if os.path.isfile(CONFIG_FILE):
            with open(CONFIG_FILE, 'r') as file:
                last_file, username, password = file.read().split('\n')

                self.__login_win.username = username
                self.__login_win.password = password

        if file_name:
            self.__load(file_name)
        else:
            if os.path.isfile(last_file):
                self.__load(last_file)

        # connect signals
        self.acLoad.triggered.connect(self.__load_as)
        self.acSave.triggered.connect(self.__save)
        self.acSaveAs.triggered.connect(self.__save_as)
        self.acGet.triggered.connect(self.__login_win.show_get)
        self.acPut.triggered.connect(self.__login_win.show_put)
        self.acImport.triggered.connect(self.__import_as)
        self.acExport.triggered.connect(self.__export_as)
        self.acExit.triggered.connect(self.close)

        self.acOpenLicense.triggered.connect(self.__opensource_win.show)
        self.acLicense.triggered.connect(self.__license_win.show)

        self.__data.sources.order_changed.connect(self.__change_ord)
        self.__data.in_type.order_changed.connect(self.__change_ord)
        self.__data.out_type.order_changed.connect(self.__change_ord)

        self.tabCate.gbSrc.lvOrd.setModel(self.__data.sources)
        self.tabCate.gbIn.lvOrd.setModel(self.__data.in_type)
        self.tabCate.gbOut.lvOrd.setModel(self.__data.out_type)

        self.tabCate.gbSrc.btnAdd.clicked.connect(self.__add_source)
        self.tabCate.gbIn.btnAdd.clicked.connect(self.__add_in)
        self.tabCate.gbOut.btnAdd.clicked.connect(self.__add_out)

        self.tabData.treeData.setModel(self.__data)
        self.tabData.treeData.selectionModel()\
            .selectionChanged.connect(self.__start_edit)

        self.tabData.cbType.setModel(self.__data.type)
        self.tabData.cbSrc.setModel(self.__data.sources)
        self.tabData.cbDetail.setModel(self.__data.in_type)

        self.tabData.cbType.currentIndexChanged.connect(self.__set_type)

        self.tabData.treeData.doubleClicked.connect(self.__del_data)
        self.tabData.btnAddData.clicked.connect(self.__add_data)
        self.tabData.btnCancel.clicked.connect(self.__end_edit)

        self.tabStatS.treeStatS.setModel(self.__stat)

        self.tabStatM.cbMonth.setModel(self.__stat.months)
        self.tabStatM.cbMonth.currentTextChanged.connect(self.__set_month)

        self.__resize()

    def __do_transfer(self):
        def next_trans(res, data, err_txt):
            self.trans_sig.disconnect()
            self.__pg_win.hide()

            if res == 0:
                if data:
                    self.__data.load_data(data)
            elif res == 1:
                QMessageBox.warning(self, '입력 오류', '파일 주소 입력 안됨')
            elif res == 2:
                msgbox = QMessageBox(
                    QMessageBox.Warning, '경고',
                    f"{'전송 도중 오류 발생':70}",
                    QMessageBox.Retry | QMessageBox.Cancel,
                    self
                )
                msgbox.setDetailedText(err_txt)
                response = msgbox.exec_()
                if response == QMessageBox.Retry:
                    self.__do_transfer()
        # next_trans

        self.__pg_win.show()
        try:
            if self.__login_win.upload:
                self.__pg_win.set_detail('데이터 업로드 중')
                data = self.__data.save_data()
                self.trans_sig.connect(next_trans)
                threading.Thread(
                    target=self.__login_win.do_put, args=(data, self.trans_sig)
                ).start()
            else:
                self.__pg_win.set_detail('데이터 다운로드 중')
                self.trans_sig.connect(next_trans)
                threading.Thread(
                    target=self.__login_win.do_get, args=(self.trans_sig,)
                ).start()
        except Exception:  # pylint: disable=broad-except
            msgbox = QMessageBox(
                QMessageBox.Warning, '경고',
                f"{'전송 전후 오류 발생':70}",
                QMessageBox.Retry | QMessageBox.Cancel,
                self
            )
            msgbox.setDetailedText(traceback.format_exc())
            response = msgbox.exec_()
            if response == QMessageBox.Retry:
                self.__do_transfer()

    def __show_err(self, err_type, txt):
        self.__err_win.set_text(f'{err_type}\n{txt}')
        self.__err_win.show()

    def __resize(self):
        for k in range(0, self.__data.column_count):
            self.tabData.treeData.resizeColumnToContents(k)

    def __add_data(self):
        try:
            date = self.tabData.lnDate.text()
            diff = (
                datetime.date.today() - datetime.date.fromisoformat(date)
            ).days
            if diff > 30:
                response = QMessageBox.warning(
                    self, '날짜 주의',
                    '현재보다 30일 이상 이전 날짜\n정확한 날짜?',
                    QMessageBox.Ok | QMessageBox.Cancel
                )
                if response == QMessageBox.Cancel:
                    return
            elif diff < 0:
                response = QMessageBox.warning(
                    self, '날짜 주의',
                    '미래의 날짜\n정확한 날짜?',
                    QMessageBox.Ok | QMessageBox.Cancel
                )
                if response == QMessageBox.Cancel:
                    return

            type_ = self.tabData.cbType.currentText()
            src = self.tabData.cbSrc.currentText()
            detail = self.tabData.cbDetail.currentText()
            cost = self.tabData.lnCost.text()
            desc = self.tabData.lnDetail.text()

            parsed = self.__data.add_data(date, type_, src, detail, cost, desc)
            self.__stat.add_data(parsed)
            self.__set_month(self.tabStatM.cbMonth.currentText())
        except Exception:  # pylint: disable=broad-except
            msgbox = QMessageBox(QMessageBox.Warning, '경고',
                                 f"{'잘못된 입력':70}", QMessageBox.Cancel, self)
            msgbox.setDetailedText(traceback.format_exc())
            msgbox.exec_()
        else:
            self.__resize()
            self.__saved = False

            self.tabData.lnDate.setText('')
            self.tabData.cbType.setCurrentIndex(0)
            self.tabData.cbSrc.setCurrentIndex(0)
            self.tabData.cbDetail.setCurrentIndex(0)
            self.tabData.lnCost.setText('')
            self.tabData.lnDetail.setText('')

    def __del_data(self, data_no):
        data = self.__data.del_data(data_no.row())
        self.__stat.del_data(data)
        self.__set_month(self.tabStatM.cbMonth.currentText())
        self.__resize()
        self.__saved = False

    def __start_edit(self, sel, _):
        data_no = sel.indexes()[0]
        row_no = data_no.row()

        data = self.__data.get_at(row_no)
        type_ = data[1]

        if type_ == 3:
            self.__end_edit()
        else:
            date = self.__data.item(row_no, 0).text()
            src = self.__data.item(row_no, 2).text()
            det = self.__data.item(row_no, 3).text()
            cost = self.__data.item(row_no, 4).text()
            desc = self.__data.item(row_no, 5).text()

            self.tabData.lnDate.setText(date)
            self.tabData.cbType.setCurrentIndex(type_)
            self.tabData.cbSrc.setCurrentText(src)
            self.tabData.cbDetail.setCurrentText(det)
            self.tabData.lnCost.setText(cost)
            self.tabData.lnDetail.setText(desc)

            self.tabData.btnAddData.setText('수정')
            self.tabData.btnCancel.show()
            self.tabData.btnAddData.clicked.disconnect()
            self.tabData.btnAddData.clicked.connect(
                lambda: self.__edit_data(data_no, date)
            )

    def __end_edit(self):
        self.tabData.lnDate.setText('')
        self.tabData.cbType.setCurrentIndex(0)
        self.tabData.cbSrc.setCurrentIndex(0)
        self.tabData.cbDetail.setCurrentIndex(0)
        self.tabData.lnCost.setText('')
        self.tabData.lnDetail.setText('')

        self.tabData.btnAddData.setText('추가')
        self.tabData.btnCancel.hide()
        self.tabData.btnAddData.clicked.disconnect()
        self.tabData.btnAddData.clicked.connect(self.__add_data)

    def __edit_data(self, data_no, priv_date):
        row_no = data_no.row()

        # delete stat
        data = self.__data.get_at(row_no)
        self.__stat.del_data(data)
        # change data & add stat
        try:
            date = self.tabData.lnDate.text()
            type_ = self.tabData.cbType.currentText()
            src = self.tabData.cbSrc.currentText()
            detail = self.tabData.cbDetail.currentText()
            cost = self.tabData.lnCost.text()
            desc = self.tabData.lnDetail.text()

            if date == priv_date:
                parsed = self.__data.set_at(
                    row_no, date, type_, src, detail, cost, desc
                )
            else:
                self.__del_data(data_no)
                parsed = self.__data.add_data(
                    date, type_, src, detail, cost, desc
                )
            self.__stat.add_data(parsed)
            self.__set_month(self.tabStatM.cbMonth.currentText())
        except Exception:  # pylint: disable=broad-except
            msgbox = QMessageBox(
                QMessageBox.Warning, '경고',
                f"{'잘못된 입력':70}",
                QMessageBox.Cancel,
                self
            )
            msgbox.setDetailedText(traceback.format_exc())
            msgbox.exec_()
        else:
            self.__resize()
            self.__saved = False
            self.__end_edit()

    def __set_month(self, text):
        if text and text != '-':  # if month -> set data
            m_c = tuple(map(int, text.split('-')))
            raw_data = self.__stat.get_month(m_c)
            if raw_data:
                data, sums = raw_data

                src_ni = self.__data.sources.get_index_no()
                in_ni = self.__data.in_type.get_index_no()
                out_ni = self.__data.out_type.get_index_no()

                data_changer = (
                    src_ni, src_ni, src_ni, in_ni, out_ni, src_ni, src_ni
                )
                for wids, type_, changer in zip(
                        self.__data_labels, self.__stat.data_name[2:],
                        data_changer
                        ):
                    for b, wid in enumerate(wids):
                        wid.setText(str(data[type_][changer[b]]))

                for wid, sum_ in zip(self.__sum_labels, sums):
                    wid.setText(sum_)
        else:  # if not month -> clear
            for wids in self.__data_labels:
                for wid in wids:
                    wid.setText('')
            for wid in self.__sum_labels:
                wid.setText('')

    def __set_stat_type(self):
        try:
            self.tabStatM.cbMonth.currentTextChanged.disconnect()
        except Exception:  # pylint: disable=broad-except
            pass

        grids = (self.tabStatM.glCurrent, self.tabStatM.glIncome,
                 self.tabStatM.glOutcome, self.tabStatM.glMove)
        for grid in grids:
            for k in reversed(range(grid.count())):
                wid = grid.itemAt(k).widget()
                if not wid.objectName():
                    wid.deleteLater()

        data = self.__data.get_data()

        src_no = self.__data.sources.get_no()
        in_no = self.__data.in_type.get_no()
        out_no = self.__data.out_type.get_no()

        src_txt = self.__data.sources.get_txt()
        in_txt = self.__data.in_type.get_txt()
        out_txt = self.__data.out_type.get_txt()

        is_cash = self.__data.sources.get_chk_no()
        is_ness = self.__data.out_type.get_chk_no()

        self.__stat.set_type(src_no, in_no, out_no, is_cash, is_ness)
        self.__stat.set_data(data)

        # generate stat labels
        self.tabStatM.lbTitleIncomeS = []
        self.tabStatM.lbTitleOutcomeS = []
        self.tabStatM.lbTitleCurrent = []
        self.tabStatM.lbTitleMoveIn = []
        self.tabStatM.lbTitleMoveOut = []

        self.tabStatM.lbDataIncomeS = []
        self.tabStatM.lbDataOutcomeS = []
        self.tabStatM.lbDataCurrent = []
        self.tabStatM.lbDataMoveIn = []
        self.tabStatM.lbDataMoveOut = []

        self.tabStatM.lbTitleIncomeT = []
        self.tabStatM.lbDataIncomeT = []

        self.tabStatM.lbTitleOutcomeT = []
        self.tabStatM.lbDataOutcomeT = []

        self.__title_labels = (
            self.tabStatM.lbTitleCurrent,
            self.tabStatM.lbTitleIncomeS,
            self.tabStatM.lbTitleOutcomeS,
            self.tabStatM.lbTitleIncomeT,
            self.tabStatM.lbTitleOutcomeT,
            self.tabStatM.lbTitleMoveIn,
            self.tabStatM.lbTitleMoveOut
        )
        self.__data_labels = (
            self.tabStatM.lbDataCurrent,
            self.tabStatM.lbDataIncomeS,
            self.tabStatM.lbDataOutcomeS,
            self.tabStatM.lbDataIncomeT,
            self.tabStatM.lbDataOutcomeT,
            self.tabStatM.lbDataMoveIn,
            self.tabStatM.lbDataMoveOut
        )
        self.__sum_labels = (
            self.tabStatM.lbSumIncome,
            self.tabStatM.lbSumOutcome,
            self.tabStatM.lbSumCurrent,
            self.tabStatM.lbSumCash,
            self.tabStatM.lbSumMove,
            self.tabStatM.lbNet,
            self.tabStatM.lbOut1,
            self.tabStatM.lbOut2
        )

        for k, txt in enumerate(src_txt):
            lbTitleIncome = QLabel(txt, self.tabStatM.gbIncome)
            lbTitleOutcome = QLabel(txt, self.tabStatM.gbOutcome)
            lbTitleCurrent = QLabel(txt, self.tabStatM.gbCurrent)
            lbTitleMoveIn = QLabel(txt, self.tabStatM.gbMove)
            lbTitleMoveOut = QLabel(txt, self.tabStatM.gbMove)

            lbTitleIncome.setAlignment(Qt.AlignCenter)
            lbTitleOutcome.setAlignment(Qt.AlignCenter)
            lbTitleCurrent.setAlignment(Qt.AlignCenter)
            lbTitleMoveIn.setAlignment(Qt.AlignCenter)
            lbTitleMoveOut.setAlignment(Qt.AlignCenter)

            self.tabStatM.lbTitleIncomeS.append(lbTitleIncome)
            self.tabStatM.lbTitleOutcomeS.append(lbTitleOutcome)
            self.tabStatM.lbTitleCurrent.append(lbTitleCurrent)
            self.tabStatM.lbTitleMoveIn.append(lbTitleMoveIn)
            self.tabStatM.lbTitleMoveOut.append(lbTitleMoveOut)

            self.tabStatM.glIncome.addWidget(lbTitleIncome, k + 2, 2, 1, 1)
            self.tabStatM.glOutcome.addWidget(lbTitleOutcome, k + 2, 2, 1, 1)
            self.tabStatM.glCurrent.addWidget(lbTitleCurrent, k + 2, 0, 1, 1)
            self.tabStatM.glMove.addWidget(lbTitleMoveIn, k + 2, 0, 1, 1)
            self.tabStatM.glMove.addWidget(lbTitleMoveOut, k + 2, 2, 1, 1)

            lbDataIncome = QLabel(self.tabStatM.gbIncome)
            lbDataOutcome = QLabel(self.tabStatM.gbOutcome)
            lbDataCurrent = QLabel(self.tabStatM.gbCurrent)
            lbDataMoveOut = QLabel(self.tabStatM.gbMove)
            lbDataMoveIn = QLabel(self.tabStatM.gbMove)

            lbDataIncome.setAlignment(Qt.AlignCenter)
            lbDataOutcome.setAlignment(Qt.AlignCenter)
            lbDataCurrent.setAlignment(Qt.AlignCenter)
            lbDataMoveOut.setAlignment(Qt.AlignCenter)
            lbDataMoveIn.setAlignment(Qt.AlignCenter)

            self.tabStatM.lbDataIncomeS.append(lbDataIncome)
            self.tabStatM.lbDataOutcomeS.append(lbDataOutcome)
            self.tabStatM.lbDataCurrent.append(lbDataCurrent)
            self.tabStatM.lbDataMoveOut.append(lbDataMoveOut)
            self.tabStatM.lbDataMoveIn.append(lbDataMoveIn)

            self.tabStatM.glIncome.addWidget(lbDataIncome, k + 2, 3, 1, 1)
            self.tabStatM.glOutcome.addWidget(lbDataOutcome, k + 2, 3, 1, 1)
            self.tabStatM.glCurrent.addWidget(lbDataCurrent, k + 2, 1, 1, 1)
            self.tabStatM.glMove.addWidget(lbDataMoveOut, k + 2, 1, 1, 1)
            self.tabStatM.glMove.addWidget(lbDataMoveIn, k + 2, 3, 1, 1)

        for k, txt in enumerate(in_txt):
            lbTitleIncome = QLabel(txt, self.tabStatM.gbIncome)
            lbTitleIncome.setAlignment(Qt.AlignCenter)
            self.tabStatM.lbTitleIncomeT.append(lbTitleIncome)
            self.tabStatM.glIncome.addWidget(lbTitleIncome, k + 2, 0, 1, 1)

            lbDataIncome = QLabel(self.tabStatM.gbIncome)
            lbDataIncome.setAlignment(Qt.AlignCenter)
            self.tabStatM.lbDataIncomeT.append(lbDataIncome)
            self.tabStatM.glIncome.addWidget(lbDataIncome, k + 2, 1, 1, 1)

        for k, txt in enumerate(out_txt):
            lbTitleOutcome = QLabel(txt, self.tabStatM.gbOutcome)
            lbTitleOutcome.setAlignment(Qt.AlignCenter)
            self.tabStatM.lbTitleOutcomeT.append(lbTitleOutcome)
            self.tabStatM.glOutcome.addWidget(lbTitleOutcome, k + 2, 0, 1, 1)

            lbDataOutcome = QLabel(self.tabStatM.gbOutcome)
            lbDataOutcome.setAlignment(Qt.AlignCenter)
            self.tabStatM.lbDataOutcomeT.append(lbDataOutcome)
            self.tabStatM.glOutcome.addWidget(lbDataOutcome, k + 2, 1, 1, 1)

        for wid in self.__sum_labels:
            wid.setText('')

        self.tabStatM.cbMonth.currentTextChanged.connect(self.__set_month)

    # this func is based from stackoverflow question 1263451
    def _set_save_and_stattype(func):  # pylint: disable=no-self-argument
        def inner(self, *args, **kwargs):
            # pylint: disable=protected-access, redefined-outer-name
            res = func(self, *args, **kwargs)
            self.__saved = False
            self.__set_stat_type()
            return res
        return inner

    @_set_save_and_stattype
    def __change_ord(self):
        pass

    @_set_save_and_stattype
    def __add_source(self):
        checked = bool(self.tabCate.gbSrc.chk.checkState())
        self.__data.sources.add_data(checked, self.tabCate.gbSrc.lnAdd.text())

    @_set_save_and_stattype
    def __del_source(self):
        self.__data.sources.del_at(self.tabCate.gbSrc.cbDel.currentIndex())

    @_set_save_and_stattype
    def __add_in(self):
        self.__data.in_type.add_data(self.tabCate.gbIn.lnAdd.text())

    @_set_save_and_stattype
    def __del_in(self):
        self.__data.in_type.del_at(self.tabCate.gbIn.cbDel.currentIndex())

    @_set_save_and_stattype
    def __add_out(self):
        checked = bool(self.tabCate.gbOut.chk.checkState())
        self.__data.out_type.add_data(checked, self.tabCate.gbOut.lnAdd.text())

    @_set_save_and_stattype
    def __del_out(self):
        self.__data.out_type.del_at(self.tabCate.gbOut.cbDel.currentIndex())

    def __set_type(self, index):
        if index == 2:
            self.tabData.lbDetail.setText('이동처')
        else:
            self.tabData.lbDetail.setText('상세')

        self.tabData.cbDetail.setModel(self.__data.list_detail[index])

    def __load_as(self):
        if not self.__saved:
            response = QMessageBox.warning(
                self, '불러오기', '저장하시겠습니까?',
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel
            )
            if response == QMessageBox.Save:
                self.__save()
            elif response == QMessageBox.Cancel:
                return

        path = QFileDialog.getOpenFileName(
            self, '불러오기', filter=self.__file_type)[0]
        if path:
            self.__load(path)

    def __load(self, file_path):
        while True:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)

                if data['version'] == 1:
                    for name in ('sources', 'in_type', 'out_type'):
                        data[name] =\
                            [(int(n), t) for n, t in data[name].items()]
                    data['version'] = 2

                self.__data.load_data(data)

                self.__set_stat_type()
            except Exception:  # pylint: disable=broad-except
                msgbox = QMessageBox(
                    QMessageBox.Warning, '재시도',
                    f"{'불러오는 중 오류 발생: 재시도?':70}",
                    QMessageBox.Retry | QMessageBox.Abort,
                    self
                )
                msgbox.setDetailedText(traceback.format_exc())
                response = msgbox.exec_()
                if response == QMessageBox.Abort:
                    break
            else:
                self.__last_file = file_path
                self.__saved = True
                self.__resize()
                self.statusbar.showMessage('불러오기 성공', timeout=2000)
                break

    def __save_as(self):
        path = QFileDialog.getSaveFileName(
            self, '저장', filter=self.__file_type)[0]
        if path:
            self.__save(path)

    def __save(self, file_path=''):
        if not file_path:
            if self.__last_file:
                file_path = self.__last_file
            else:
                self.__save_as()
                return

        while True:
            try:
                data = self.__data.save_data()
                with open(file_path, 'w', encoding='utf-8') as file:
                    json.dump(data, file, ensure_ascii=False, indent=4)
            except Exception:  # pylint: disable=broad-except
                msgbox = QMessageBox(
                    QMessageBox.Warning, '재시도',
                    f"{'저장하는 중 오류 발생: 재시도?':70}",
                    QMessageBox.Retry | QMessageBox.Abort,
                    self
                )
                msgbox.setDetailedText(traceback.format_exc())
                response = msgbox.exec_()
                if response == QMessageBox.Abort:
                    break
            else:
                self.__last_file = file_path
                self.__saved = True
                self.statusbar.showMessage('저장 성공', timeout=2000)
                break

    def __import_as(self):
        file_path, type_ = QFileDialog.getOpenFileName(
            self, '가져오기', filter=self.__export_type
        )

        if file_path:
            type_path, _ = QFileDialog.getOpenFileName(
                self, '범례 파일 선택', filter='범례 파일(*.json)'
            )
            type_ = self.__export_text.index(type_)

            if type_path:
                while True:
                    try:
                        self.__data.import_data(type_, file_path, type_path)
                    except Exception:  # pylint: disable=broad-except
                        msgbox = QMessageBox(
                            QMessageBox.Warning, '재시도',
                            f"{'가져오는 중 오류 발생: 재시도?':70}",
                            QMessageBox.Retry | QMessageBox.Abort,
                            self
                        )
                        msgbox.setDetailedText(traceback.format_exc())
                        response = msgbox.exec_()
                        if response == QMessageBox.Abort:
                            break
                    else:
                        break

    def __export_as(self):
        file_path, type_ = QFileDialog.getSaveFileName(
            self, '내보내기', filter=self.__export_type)

        if file_path:
            type_path, _ = QFileDialog.getOpenFileName(
                self, '범례 파일 선택', filter='범례 파일(*.json)')
            type_ = self.__export_text.index(type_)

            if type_path:
                while True:
                    try:
                        self.__data.export_data(type_, file_path, type_path)
                    except Exception:  # pylint: disable=broad-except
                        msgbox = QMessageBox(
                            QMessageBox.Warning, '재시도',
                            f"{'내보내는 중 오류 발생: 재시도?':70}",
                            QMessageBox.Retry | QMessageBox.Abort,
                            self
                        )
                        msgbox.setDetailedText(traceback.format_exc())
                        response = msgbox.exec_()
                        if response == QMessageBox.Abort:
                            break
                    else:
                        break

    def __save_config(self):
        if not os.path.isdir(CONFIG_DIR):
            os.mkdir(CONFIG_DIR)

        with open(CONFIG_FILE, 'w') as file:
            file.write('\n'.join((
                self.__last_file,
                self.__login_win.username,
                self.__login_win.password
            )))

    def closeEvent(self, event):
        if self.__saved:
            self.__save_config()
            event.accept()
        else:
            response = QMessageBox.warning(
                self, '종료', '저장하시겠습니까?',
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel
            )
            if response == QMessageBox.Cancel:
                event.ignore()
            else:
                if response == QMessageBox.Save:
                    self.__save()
                self.__save_config()
                event.accept()


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument(
        'file_name', help='Path of file', nargs='?', default=''
    )

    args = parser.parse_args()

    app = QApplication()

    main_win = MainWin(args.file_name)
    main_win.show()

    app.exec_()
