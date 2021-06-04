from PySide6.QtCore import Signal, Qt, QItemSelectionModel, QDate
from PySide6.QtWidgets import (
    QMainWindow, QApplication, QWidget, QGroupBox,
    QLabel, QTreeView, QMessageBox, QFileDialog
)

import os
import io
import json
import argparse
import datetime
import threading
import traceback
import ftplib

from UI import (
    Ui_Txt, Ui_Info, Ui_Pg, Ui_Login, Ui_MainWin,
    Ui_TabCate, Ui_TabData, Ui_TabStatS, Ui_TabStatM,
    Ui_GbAddDelCate, Ui_GbAddDelChk
)
from model_numpy import Data, Stat_Data
from constants import DATADIR, DEFAULT_STD_DAY


CONFIG_DIR = DATADIR + 'hys.moneymanage'
CONFIG_FILE = DATADIR + 'hys.moneymanage/config'


DEFAULT_ENCODING = 'utf-8'


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


class GbCateBase(QGroupBox):
    def __init__(self, parent, model, functions):
        super().__init__(parent)

        self._model = model
        self._editing_row = -1

        self._set_saved = functions['set_saved']
        self._set_stat_type = functions['set_stat_type']
        self._refresh_data = functions['refresh_data']

        model.orderChanged.connect(self._change_ord)
        # self.lvOrd.doubleClicked.connect(self._remove)

    @staticmethod
    def _set_save_and_stat_type(func):
        # pylint: disable=redefined-outer-name, protected-access
        def base(self, *args):
            func(self, *args)
            self._set_saved(False)
            self._set_stat_type()
        return base

    @staticmethod
    def _set_save_stat_type_and_refresh_data(func):
        # pylint: disable=redefined-outer-name, protected-access
        def base(self, *args):
            func(self, *args)
            self._set_saved(False)
            self._set_stat_type()
            self._refresh_data()
        return base

    def __set_save_and_stat_type(func):  # pylint: disable=no-self-argument
        # pylint: disable=redefined-outer-name, protected-access
        def base(self, *args):
            func(self, *args)
            self._set_saved(False)
            self._set_stat_type()
        return base

    @__set_save_and_stat_type
    def _change_ord(self):
        pass

    # @__set_save_and_stat_type
    # def _remove(self, index):
        # self._model.del_index(index.row())
        # raise NotImplementedError

    def _end_edit(self):
        assert self._editing_row > -1
        self._editing_row = -1
        self.btnAdd.show()
        self.btnApply.hide()
        self.btnCancel.hide()
        self.lnAdd.setText('')


class GbAddDelCate(GbCateBase, Ui_GbAddDelCate):
    def __init__(self, parent, model, functions):
        super().__init__(parent, model, functions)
        self.setupUi(self)

        self.btnAdd.clicked.connect(self.__add)
        self.lvOrd.selectionChanged = self.__start_edit
        self.btnApply.clicked.connect(self.__apply)
        self.btnCancel.clicked.connect(self._end_edit)

    @GbCateBase._set_save_and_stat_type
    def __add(self):
        self._model.add_data(self.lnAdd.text())

    def __start_edit(self, selected, _):
        indexes = selected.indexes()
        if indexes:
            self.btnAdd.hide()
            self.btnApply.show()
            self.btnCancel.show()

            row_no = indexes[0].row()
            self._editing_row = row_no
            self.lnAdd.setText(self._model.get_at_index(row_no))

    @GbCateBase._set_save_stat_type_and_refresh_data
    def __apply(self):
        assert self._editing_row > -1
        text = self.lnAdd.text()
        if text.startswith('* '):
            QMessageBox.warning(self, '경고', '올바르지 않은 이름')
            return
        self._model.set_index(self._editing_row, text)
        self._end_edit()


class GbAddDelChk(GbCateBase, Ui_GbAddDelChk):
    def __init__(self, parent, model, functions, chk_txt):
        super().__init__(parent, model, functions)
        self.setupUi(self, chk_txt)

        model.orderChanged.connect(self._change_ord)
        self.btnAdd.clicked.connect(self.__add)
        self.lvOrd.selectionChanged = self.__start_edit
        self.btnApply.clicked.connect(self.__apply)
        self.btnCancel.clicked.connect(self._end_edit)

    @GbCateBase._set_save_and_stat_type
    def __add(self):
        self._model.add_data(bool(self.chk.checkState()), self.lnAdd.text())

    def __start_edit(self, selected, _):
        indexes = selected.indexes()
        if indexes:
            self.btnAdd.hide()
            self.btnApply.show()
            self.btnCancel.show()

            row_no = indexes[0].row()
            self._editing_row = row_no
            checked, text = self._model.get_at_index(row_no)
            self.chk.setChecked(checked)
            self.lnAdd.setText(text)

    def _end_edit(self):
        super()._end_edit()
        self.chk.setChecked(False)

    @GbCateBase._set_save_stat_type_and_refresh_data
    def __apply(self):
        assert self._editing_row > -1
        text = self.lnAdd.text()
        if text.startswith('* '):
            QMessageBox.warning(self, '경고', '올바르지 않은 이름')
            return
        self._model.set_index(
            self._editing_row,
            self.chk.isChecked(),
            text
        )
        self._end_edit()


class TabCate(QWidget, Ui_TabCate):
    def __init__(self, parent, models, functions):
        super().__init__(parent)

        self.__data = models['data']
        self.__stat = models['stat']

        self.gbSrc = GbAddDelChk(
            self, self.__data.sources, functions, "현금성"
        )
        self.gbIn = GbAddDelCate(
            self, self.__data.in_type, functions
        )
        self.gbOut = GbAddDelChk(
            self, self.__data.out_type, functions, "필수?"
        )

        self.setupUi(self)

        self.__set_saved = functions['set_saved']
        self.__set_stat_type = functions['set_stat_type']

        # set model
        self.gbSrc.lvOrd.setModel(self.__data.sources)
        self.gbIn.lvOrd.setModel(self.__data.in_type)
        self.gbOut.lvOrd.setModel(self.__data.out_type)


class TabData(QWidget, Ui_TabData):
    def __init__(self, parent, models, functions):
        super().__init__(parent)
        self.setupUi(self)

        self.__data = models['data']
        self.__stat = models['stat']

        self.__refresh_stat = functions['refresh_stat']
        self.__set_saved = functions['set_saved']

        self.__editing_row = -1

        # set model
        self.treeData.setModel(self.__data)
        self.cbType.setModel(self.__data.type)
        self.cbSrc.setModel(self.__data.sources)
        self.cbDetail.setModel(self.__data.in_type)

        # connect signals
        self.treeData.selectionModel()\
            .selectionChanged.connect(self.__start_edit)
        self.treeData.doubleClicked.connect(self.__del_data)

        self.cbType.currentIndexChanged.connect(self.__set_type)

        self.lnDate.escapePressed.connect(self.__clear_date)
        self.lnCost.returnPressed.connect(self.__add_or_edit)
        self.lnDetail.returnPressed.connect(self.__add_or_edit)
        self.btnAddData.clicked.connect(self.__add_data)
        self.btnEdit.clicked.connect(self.__edit_data)
        self.btnCancel.clicked.connect(self.__end_edit)
        self.btnUp.clicked.connect(lambda: self.__move(-1))
        self.btnDown.clicked.connect(lambda: self.__move(1))

    def resize(self):
        for k in range(0, self.__data.column_count):
            self.treeData.resizeColumnToContents(k)

    def refresh_data(self):
        self.__data.refresh()
        self.resize()

    def to_bottom(self):
        self.treeData.scrollToBottom()

    def __clear_date(self):
        self.lnDate.clear()
        self.lnDate.setCursorPosition(2)

    def __add_or_edit(self):
        if self.__editing_row > 0:
            self.__edit_data()
        else:
            self.__add_data()

    def __reset_focus(self):
        self.lnDate.setFocus()
        self.lnDate.setCursorPosition(2)

    def __add_data(self):
        try:
            date = self.lnDate.text()
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

            type_ = self.cbType.currentText()
            src = self.cbSrc.currentText()
            detail = self.cbDetail.currentText()
            cost = self.lnCost.text()
            desc = self.lnDetail.text()

            index, parsed = self.__data.add_data(
                date, type_, src, detail, cost, desc
            )
            self.__stat.add_data(parsed)
            self.__refresh_stat()

            self.treeData.scrollTo(
                self.__data.index(index, 0), QTreeView.PositionAtCenter
            )
        except Exception:  # pylint: disable=broad-except
            msgbox = QMessageBox(
                QMessageBox.Warning, '경고', f"{'잘못된 입력':70}",
                QMessageBox.Cancel, self
            )
            msgbox.setDetailedText(traceback.format_exc())
            msgbox.exec()
        else:
            self.resize()
            self.__set_saved(False)

            self.lnDate.setText('')
            self.cbType.setCurrentIndex(0)
            self.cbSrc.setCurrentIndex(0)
            self.cbDetail.setCurrentIndex(0)
            self.lnCost.setText('')
            self.lnDetail.setText('')
            self.__reset_focus()

    def __del_data(self, data_no):
        row = data_no.row()
        if self.__data.get_at(row)[1] != 3:
            data = self.__data.del_data(row)
            self.__stat.del_data(data)
            self.__refresh_stat()
            self.resize()
            self.__set_saved(False)
        self.__end_edit()

    def __check_date(self):
        assert self.__editing_row > 0
        head, tail = self.__data.check_date(self.__editing_row)
        self.btnUp.setEnabled(head)
        self.btnDown.setEnabled(tail)

    def __start_edit(self, sel, _):
        selection = sel.indexes()
        if selection:
            self.__edit_at(selection[0].row())

    def __edit_at(self, row_no):
        self.__editing_row = row_no
        type_ = self.__data.get_at(row_no)['type']

        if type_ == 3:
            return

        date = self.__data.item(row_no, 0).text()
        src = self.__data.item(row_no, 2).text()
        det = self.__data.item(row_no, 3).text()
        cost = self.__data.item(row_no, 4).text()
        desc = self.__data.item(row_no, 5).text()

        self.lnDate.setText(date)
        self.cbType.setCurrentIndex(type_)
        self.cbSrc.setCurrentText(src)
        self.cbDetail.setCurrentText(det)
        self.lnCost.setText(cost)
        self.lnDetail.setText(desc)

        self.__check_date()

        self.btnEdit.show()
        self.btnCancel.show()
        self.btnUp.show()
        self.btnDown.show()
        self.btnAddData.hide()

    def __end_edit(self):
        assert self.__editing_row >= 0

        self.lnDate.setText('')
        self.cbType.setCurrentIndex(0)
        self.cbSrc.setCurrentIndex(0)
        self.cbDetail.setCurrentIndex(0)
        self.lnCost.setText('')
        self.lnDetail.setText('')

        self.btnEdit.hide()
        self.btnCancel.hide()
        self.btnUp.hide()
        self.btnDown.hide()
        self.btnAddData.show()

        self.treeData.clearSelection()
        self.__reset_focus()
        self.__editing_row = -1

    def __edit_data(self):
        assert self.__editing_row >= 0

        # get priv information
        row_no = self.__editing_row
        data = self.__data.get_at(row_no)
        priv_date = self.__data.item(row_no, 0).text()

        # delete stat
        self.__stat.del_data(data)
        # change data & add stat
        try:
            date = self.lnDate.text()
            type_ = self.cbType.currentText()
            src = self.cbSrc.currentText()
            detail = self.cbDetail.currentText()
            cost = self.lnCost.text()
            desc = self.lnDetail.text()

            if date == priv_date:
                parsed = self.__data.set_at(
                    row_no, date, type_, src, detail, cost, desc
                )
                selection = self.__data.index(row_no, 0)
            else:
                self.__data.del_data(row_no)
                index, parsed = self.__data.add_data(
                    date, type_, src, detail, cost, desc
                )
                selection = self.__data.index(index, 0)
            self.__stat.add_data(parsed)
            self.__refresh_stat()

            self.treeData.scrollTo(
                selection, QTreeView.PositionAtCenter
            )
        except Exception:  # pylint: disable=broad-except
            msgbox = QMessageBox(
                QMessageBox.Warning, '경고',
                f"{'잘못된 입력':70}",
                QMessageBox.Cancel,
                self
            )
            msgbox.setDetailedText(traceback.format_exc())
            msgbox.exec()
        else:
            self.resize()
            self.__set_saved(False)
            self.__end_edit()

    def __move(self, diff):
        # move data & view
        assert self.__editing_row >= 0
        dest = self.__editing_row + diff
        self.__data.move(self.__editing_row, dest)
        self.__set_saved(False)

        # change selection
        self.__edit_at(dest)
        self.treeData.selectionModel().select(
            self.__data.index(dest, 0),
            QItemSelectionModel.Rows | QItemSelectionModel.ClearAndSelect
        )

        self.__check_date()

    def __set_type(self, index):
        if index == 2:
            self.lbDetail.setText('이동처')
        else:
            self.lbDetail.setText('상세')

        self.cbDetail.setModel(self.__data.list_detail[index])


class TabStatS(QWidget, Ui_TabStatS):
    def __init__(self, parent, models):
        super().__init__(parent)
        self.setupUi(self)

        self.__stat = models['stat']

        # set model
        self.treeStatS.setModel(self.__stat)


class TabStatM(QWidget, Ui_TabStatM):
    MONTHLY = 0
    WEEKLY = 1
    DAILY = 2

    def __init__(self, parent, models):
        super().__init__(parent)
        self.setupUi(self)

        self.__data = models['data']
        self.__stat = models['stat']

        self.__mode = self.MONTHLY

        # set model
        self.cbMonth.setModel(self.__stat.months)

        # connect signals
        self.rbMonthly.clicked.connect(self.__set_interval)
        self.rbWeekly.clicked.connect(self.__set_interval)
        self.rbDaily.clicked.connect(self.__set_interval)
        self.cbMonth.currentTextChanged.connect(self.__set_month)
        self.calInterval.selectionChanged.connect((
            lambda: self.__set_week() if self.__mode == self.WEEKLY
            else self.__set_day()
        ))

    def refresh_stat(self):
        self.__set_month(self.cbMonth.currentText())

    def show_currrent(self):
        currents, total, cache = self.__stat.get_current_at_now()
        changer = self.__data.sources.get_index_no()
        for wids in self.__data_labels:
            for wid in wids:
                wid.setText('-')
        for wid in self.__sum_labels:
            wid.setText('-')
        for k, current_wid in enumerate(self.lbDataCurrent):
            current_wid.setText(str(currents[changer[k]]))
        self.lbSumCurrent.setText(str(total))
        self.lbSumCash.setText(str(cache))

    def __first_day_of_week(self, date):
        assert isinstance(date, QDate)
        weekday = date.dayOfWeek()
        return date.addDays(0 if weekday == 7 else -weekday)

    def __set_interval(self):
        if self.rbMonthly.isChecked():
            self.calInterval.hide()
            self.cbMonth.show()
            self.cbMonth.setCurrentIndex(0)
            self.__set_month('-')
            self.__mode = self.MONTHLY
        else:
            self.calInterval.show()
            self.cbMonth.hide()
            date = QDate.currentDate()
            if self.rbWeekly.isChecked():
                self.__mode = self.WEEKLY
                self.calInterval.setSelectedDate(
                    self.__first_day_of_week(date)
                )
                self.__set_week(date)
            else:  # daily
                self.__mode = self.DAILY
                self.calInterval.setSelectedDate(date)
                self.__set_day(date)

    def __set_stat(self, data):
        data, sums = data

        src_ni = self.__data.sources.get_index_no()
        in_ni = self.__data.in_type.get_index_no()
        out_ni = self.__data.out_type.get_index_no()

        for wids, type_, changer in zip(
            self.__data_labels, self.__stat.data_name[2:],
            (src_ni, src_ni, src_ni, in_ni, out_ni, src_ni, src_ni)
        ):
            for b, wid in enumerate(wids):
                wid.setText(str(data[type_][changer[b]]))

        for wid, sum_ in zip(self.__sum_labels, sums):
            wid.setText(sum_)

    def __set_month(self, text):
        if text and text != '-':  # if month -> set data
            m_c = tuple(map(int, text.split('-')))
            raw_data = self.__stat.get_month(m_c)
            if raw_data:
                self.__set_stat(raw_data)
        else:  # if not month -> clear
            self.show_currrent()

    def __set_week(self, date=None):
        if not date:
            date = self.calInterval.selectedDate()
        start_date = self.__first_day_of_week(date).toPython()
        end_date = start_date + datetime.timedelta(6)
        self.calInterval.setSelectedDate(start_date)
        self.__set_stat(
            self.__stat.get_intv(self.__data.raw, start_date, end_date)
        )

    def __set_day(self, date=None):
        if not date:
            date = self.calInterval.selectedDate()
        start_date = end_date = date.toPython()
        self.__set_stat(
            self.__stat.get_intv(self.__data.raw, start_date, end_date)
        )

    def set_stat_type(self):
        # pylint: disable=attribute-defined-outside-init
        try:
            self.cbMonth.currentTextChanged.disconnect()
        except Exception:  # pylint: disable=broad-except
            pass

        for grid in (
            self.glCurrent, self.glIncome, self.glOutcome, self.glMove
        ):
            for k in reversed(range(grid.count())):
                wid = grid.itemAt(k).widget()
                if not wid.objectName():
                    wid.deleteLater()

        data = self.__data.raw

        self.__stat.set_type(
            self.__data.sources.get_no(),  # source (numbers)
            self.__data.in_type.get_no(),  # income (numbers)
            self.__data.out_type.get_no(),  # outcome (numbers)
            self.__data.sources.get_no_chk(),  # is cash? (no. -> chk)
            self.__data.out_type.get_no_chk(),  # is ness outcome? (no. -> chk)
            self.__data.std_day,  # standard day
        )
        self.__stat.set_data(data)

        # generate stat labels
        self.lbDataIncomeS = []
        self.lbDataOutcomeS = []
        self.lbDataCurrent = []
        self.lbDataMoveIn = []
        self.lbDataMoveOut = []

        self.lbTitleIncomeT = []
        self.lbDataIncomeT = []

        self.lbTitleOutcomeT = []
        self.lbDataOutcomeT = []

        self.__data_labels = (
            self.lbDataCurrent,
            self.lbDataIncomeS,
            self.lbDataOutcomeS,
            self.lbDataIncomeT,
            self.lbDataOutcomeT,
            self.lbDataMoveIn,
            self.lbDataMoveOut
        )
        self.__sum_labels = (
            self.lbSumIncome,
            self.lbSumOutcome,
            self.lbInStat,
            self.lbOutStat,
            self.lbSumCurrent,
            self.lbSumCash,
            self.lbSumMove,
            self.lbNet,
            self.lbOut1,
            self.lbOut2
        )

        for k, txt in enumerate(self.__data.sources.get_txt()):
            lbTitleIncome = QLabel(txt, self.gbIncome)
            lbTitleOutcome = QLabel(txt, self.gbOutcome)
            lbTitleCurrent = QLabel(txt, self.gbCurrent)
            lbTitleMoveIn = QLabel(txt, self.gbMove)
            lbTitleMoveOut = QLabel(txt, self.gbMove)

            lbTitleIncome.setAlignment(Qt.AlignCenter)
            lbTitleOutcome.setAlignment(Qt.AlignCenter)
            lbTitleCurrent.setAlignment(Qt.AlignCenter)
            lbTitleMoveIn.setAlignment(Qt.AlignCenter)
            lbTitleMoveOut.setAlignment(Qt.AlignCenter)

            self.glIncome.addWidget(lbTitleIncome, k + 2, 2, 1, 1)
            self.glOutcome.addWidget(lbTitleOutcome, k + 2, 2, 1, 1)
            self.glCurrent.addWidget(lbTitleCurrent, k + 2, 0, 1, 1)
            self.glMove.addWidget(lbTitleMoveIn, k + 2, 0, 1, 1)
            self.glMove.addWidget(lbTitleMoveOut, k + 2, 2, 1, 1)

            lbDataIncome = QLabel(self.gbIncome)
            lbDataOutcome = QLabel(self.gbOutcome)
            lbDataCurrent = QLabel(self.gbCurrent)
            lbDataMoveOut = QLabel(self.gbMove)
            lbDataMoveIn = QLabel(self.gbMove)

            lbDataIncome.setAlignment(Qt.AlignCenter)
            lbDataOutcome.setAlignment(Qt.AlignCenter)
            lbDataCurrent.setAlignment(Qt.AlignCenter)
            lbDataMoveOut.setAlignment(Qt.AlignCenter)
            lbDataMoveIn.setAlignment(Qt.AlignCenter)

            self.lbDataIncomeS.append(lbDataIncome)
            self.lbDataOutcomeS.append(lbDataOutcome)
            self.lbDataCurrent.append(lbDataCurrent)
            self.lbDataMoveOut.append(lbDataMoveOut)
            self.lbDataMoveIn.append(lbDataMoveIn)

            self.glIncome.addWidget(lbDataIncome, k + 2, 3, 1, 1)
            self.glOutcome.addWidget(lbDataOutcome, k + 2, 3, 1, 1)
            self.glCurrent.addWidget(lbDataCurrent, k + 2, 1, 1, 1)
            self.glMove.addWidget(lbDataMoveOut, k + 2, 1, 1, 1)
            self.glMove.addWidget(lbDataMoveIn, k + 2, 3, 1, 1)

        for k, txt in enumerate(self.__data.in_type.get_txt()):
            lbTitleIncome = QLabel(txt, self.gbIncome)
            lbTitleIncome.setAlignment(Qt.AlignCenter)
            self.lbTitleIncomeT.append(lbTitleIncome)
            self.glIncome.addWidget(lbTitleIncome, k + 2, 0, 1, 1)

            lbDataIncome = QLabel(self.gbIncome)
            lbDataIncome.setAlignment(Qt.AlignCenter)
            self.lbDataIncomeT.append(lbDataIncome)
            self.glIncome.addWidget(lbDataIncome, k + 2, 1, 1, 1)

        for k, txt in enumerate(self.__data.out_type.get_txt()):
            lbTitleOutcome = QLabel(txt, self.gbOutcome)
            lbTitleOutcome.setAlignment(Qt.AlignCenter)
            self.lbTitleOutcomeT.append(lbTitleOutcome)
            self.glOutcome.addWidget(lbTitleOutcome, k + 2, 0, 1, 1)

            lbDataOutcome = QLabel(self.gbOutcome)
            lbDataOutcome.setAlignment(Qt.AlignCenter)
            self.lbDataOutcomeT.append(lbDataOutcome)
            self.glOutcome.addWidget(lbDataOutcome, k + 2, 1, 1, 1)

        for wid in self.__sum_labels:
            wid.setText('')

        self.cbMonth.currentTextChanged.connect(self.__set_month)
        self.rbMonthly.setChecked(True)


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

        # define models
        self.__data = Data(None)
        self.__stat = Stat_Data(None)
        models = {
            'data': self.__data,
            'stat': self.__stat
        }

        # define tabs
        self.tabStatM = TabStatM(self, models)
        self.tabStatS = TabStatS(self, models)

        functions = {
            'refresh_stat': self.tabStatM.refresh_stat,
            'set_stat_type': self.tabStatM.set_stat_type,
            'set_saved': self.set_saved
        }

        self.tabData = TabData(self, models, functions)

        functions |= {
            'refresh_data': self.tabData.refresh_data
        }

        self.tabCate = TabCate(self, models, functions)

        # add tabs
        self.tabWidget.addTab(
            self.tabCate, u"\ubd84\ub958 \uad00\ub9ac"
        )
        self.tabWidget.addTab(
            self.tabData, u"\uae30\ub85d \ucd94\uac00/\uc218\uc815"
        )
        self.tabWidget.addTab(
            self.tabStatS, u"\uac04\ub7b5\ud1b5\uacc4"
        )
        self.tabWidget.addTab(
            self.tabStatM, u"\uc0c1\uc138\ud1b5\uacc4"
        )

        # set models' parent
        self.__data.setParent(self.tabData.treeData)
        self.__stat.setParent(self.tabStatS.treeStatS)

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
                self, 'License', 'License file (License) does not exist'
            )
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
            if self.__load(file_name):
                self.tabStatM.show_currrent()
        elif os.path.isfile(last_file):
            if self.__load(last_file):
                self.tabStatM.show_currrent()

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

    def set_saved(self, value):
        self.__saved = value

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
                response = msgbox.exec()
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
            response = msgbox.exec()
            if response == QMessageBox.Retry:
                self.__do_transfer()

    def __show_err(self, err_type, txt):
        self.__err_win.set_text(f'{err_type}\n{txt}')
        self.__err_win.show()

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
                if data['version'] == 2:
                    data['std_day'] = DEFAULT_STD_DAY
                    data['version'] = 3

                self.__data.load_data(data)

                self.tabStatM.set_stat_type()
            except Exception:  # pylint: disable=broad-except
                msgbox = QMessageBox(
                    QMessageBox.Warning, '재시도',
                    f"{'불러오는 중 오류 발생: 재시도?':70}",
                    QMessageBox.Retry | QMessageBox.Abort,
                    self
                )
                msgbox.setDetailedText(traceback.format_exc())
                response = msgbox.exec()
                if response == QMessageBox.Abort:
                    return False
            else:
                self.__last_file = file_path
                self.__saved = True
                self.tabData.resize()
                self.tabData.to_bottom()
                self.statusbar.showMessage('불러오기 성공', timeout=2000)
                return True

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
                response = msgbox.exec()
                if response == QMessageBox.Abort:
                    break
            else:
                self.__last_file = file_path
                self.__saved = True
                self.statusbar.showMessage('저장 성공', timeout=2000)
                break

    def __import_as(self, *, encoding=DEFAULT_ENCODING):
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
                        with open(file_path, 'r', encoding=encoding) as file:
                            raw_data = file.readlines()
                        with open(type_path, 'r', encoding=encoding) as file:
                            types = json.load(file)

                        self.__data.import_data(type_, raw_data, types)
                    except Exception:  # pylint: disable=broad-except
                        msgbox = QMessageBox(
                            QMessageBox.Warning, '재시도',
                            f"{'가져오는 중 오류 발생: 재시도?':70}",
                            QMessageBox.Retry | QMessageBox.Abort,
                            self
                        )
                        msgbox.setDetailedText(traceback.format_exc())
                        response = msgbox.exec()
                        if response == QMessageBox.Abort:
                            break
                    else:
                        break

    def __export_as(self, *, encoding=DEFAULT_ENCODING):
        file_path, raw_type = QFileDialog.getSaveFileName(
            self, '내보내기', filter=self.__export_type
        )

        if file_path:
            type_path, _ = QFileDialog.getOpenFileName(
                self, '범례 파일 선택', filter='범례 파일(*.json)')
            type_no = self.__export_text.index(raw_type)

            while True:
                try:
                    data, types = self.__data.export_data(type_no)

                    with open(file_path, 'w', encoding=encoding) as file:
                        file.write(data)
                    if type_path:
                        with open(type_path, 'w',
                                  encoding=encoding) as file:
                            json.dump(types, file)
                except Exception:  # pylint: disable=broad-except
                    msgbox = QMessageBox(
                        QMessageBox.Warning, '재시도',
                        f"{'내보내는 중 오류 발생: 재시도?':70}",
                        QMessageBox.Retry | QMessageBox.Abort,
                        self
                    )
                    msgbox.setDetailedText(traceback.format_exc())
                    response = msgbox.exec()
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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'file_name', help='Path of file', nargs='?', default=''
    )
    args = parser.parse_args()

    app = QApplication()
    main_win = MainWin(args.file_name)
    main_win.show()
    app.exec()


if __name__ == '__main__':
    main()
