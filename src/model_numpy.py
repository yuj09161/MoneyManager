from PySide6.QtCore import Signal, QTimer, Qt
from PySide6.QtGui import QStandardItemModel, QStandardItem

import datetime

import numpy as np


STD_DAY = 730120
MAX_DATA_CNT = 10000


def arr_to_qitem(arr):
    return [QStandardItem(str(x)) for x in arr]


class NotInitalizedError(Exception):
    pass


class MaxDataCountError(Exception):
    pass


class ComboData(QStandardItemModel):
    orderChanged = Signal()

    def __init__(self, parent=None):
        super().__init__(0, 0, parent)

        self._data = []

        # self.dataChanged.connect(self.change_order)
        self.dataChanged.connect(
            lambda: QTimer.singleShot(10, self.change_order)
        )

    # this func is based from stackoverflow question 1263451
    def _bypass_ordchange(func):  # pylint: disable=no-self-argument
        def inner(self, *args, **kwargs):
            # pylint: disable=protected-access
            self.__changing = True
            res = func(self, *args, **kwargs)
            self.__changing = False
            return res
        return inner

    def __item(self, obj):
        item = QStandardItem(obj)
        item.setFlags(item.flags() & ~Qt.ItemIsDropEnabled)
        return item

    # converters
    def get_no_txt(self):
        return dict(sorted(self._data))

    def get_no_index(self):
        return {n: i for i, (n, t) in sorted(
            enumerate(self._data), key=lambda x: x[1][0])}

    def get_txt_no(self):
        return {t: n for n, t in self._data}

    def get_txt_index(self):
        return {t: i for i, (n, t) in enumerate(self._data)}

    def get_index_no(self):
        return {i: n for i, (n, t) in enumerate(self._data)}

    def get_index_txt(self):
        return {i: t for i, (n, t) in enumerate(self._data)}

    # get one element
    def get_no(self):
        return [n for n, t in sorted(self._data)]

    def get_index(self):
        return tuple(range(len(self._data)))

    def get_txt(self):
        return [t for n, t in self._data]

    def get_txt_s(self):
        return [t for n, t in sorted(self._data)]

    def get_at_index(self, index):
        return self._data[index][1]

    # get raw data (for save/export)
    def get_raw(self):
        return self._data

    # setter func
    @_bypass_ordchange
    def add_data(self, txt):
        if self._data:
            index = max(x for x, _ in self._data) + 1
        else:
            index = 0

        self._data.append((index, txt))
        self.appendRow(self.__item(txt))

    @_bypass_ordchange
    def set_data(self, txts):
        self._data = list(map(tuple, txts))
        self.clear()
        for _, txt in txts:
            self.appendRow(self.__item(txt))

    @_bypass_ordchange
    def set_index(self, index, value):
        self._data[index] = (self._data[index][0], value)
        self.setItem(index, QStandardItem(value))

    @_bypass_ordchange
    def del_no(self, no):
        self.del_index(self.get_no_index()[no])

    @_bypass_ordchange
    def del_index(self, index):
        del self._data[index]
        self.removeRow(index)

    def change_order(self):
        if not self.__changing:
            items = []
            for k in range(self.rowCount()):
                items.append(self.item(k).text())
            self._data.sort(key=lambda x: items.index(x[1]))
            self.orderChanged.emit()


class ComboDataChk(ComboData):
    # pylint: disable=arguments-differ
    __prefix = '* '

    def get_chk_no(self):
        return [
            txt.startswith(self.__prefix) for _, txt in sorted(self._data)
        ]

    def get_chk_index(self):
        return [
            txt.startswith(self.__prefix) for _, txt in self._data
        ]

    def get_no_chk(self):
        return {
            n: t.startswith(self.__prefix) for n, t in sorted(self._data)
        }

    def get_index_chk(self):
        return {
            i: t.startswith(self.__prefix)
            for i, (n, t) in enumerate(self._data)
        }

    def get_at_index(self, index):
        text = self._data[index][1]
        if text.startswith('* '):
            return True, text.replace('* ', '')
        else:
            return False, text

    def add_data(self, checked, data):
        __prefix = self.__prefix if checked else ''
        super().add_data(__prefix + data)

    def set_index(self, index, checked, value):
        super().set_index(index, ('* ' if checked else '') + value)


class Data(QStandardItemModel):
    __header_text = ('일시', '구분', '원천', '상세/이동처', '금액', '설명')
    __type_text = ('수입', '지출', '이동', '초기')
    __data_form = [
        ('date', 'uint16'), ('type', 'uint8'), ('src', 'uint8'),
        ('det', 'uint8'), ('val', 'uint32'), ('desc', '<U64')
    ]
    __data_name = ('date', 'type', 'src', 'det', 'val', 'desc')

    __empty_arr = np.array((0, 0, 0, 0, 0, ''), __data_form)

    column_count = len(__header_text)

    def __init__(self, parent):
        super().__init__(0, 0, parent)
        self.setHorizontalHeaderLabels(self.__header_text)

        self.__version = 2

        self.__tmp_src_txt = {}
        self.__tmp_in_txt = {}
        self.__tmp_out_txt = {}

        self.type = ComboData()
        self.sources = ComboDataChk()
        self.in_type = ComboData()
        self.out_type = ComboDataChk()

        self.list_detail = (self.in_type, self.out_type, self.sources)

        self.__data = np.empty((MAX_DATA_CNT,), self.__data_form)

        self.type.set_data(
            list((k, x) for k, x in enumerate(self.__type_text[:-1]))
        )

        self.row_count = 0

    def load_data(self, data):
        self.__version = data['version']

        self.sources.set_data(data['sources'])
        self.in_type.set_data(data['in_type'])
        self.out_type.set_data(data['out_type'])

        self.row_count = len(data['data'])
        if self.row_count > MAX_DATA_CNT:
            raise MaxDataCountError
        else:
            raw_data = list(map(tuple, data['data']))
            self.__data = np.asarray(raw_data, self.__data_form)

        self.refresh(self.__data)

        if self.row_count < MAX_DATA_CNT:
            self.__data = np.append(
                np.asarray(raw_data, self.__data_form),
                np.empty((MAX_DATA_CNT - self.row_count,), self.__data_form)
            )

    def refresh(self, data=None):
        # clear view
        self.clear()

        # get data (to display)
        if data is None:
            data = self.__data[:self.row_count]

        # parse data & set data
        src_txt = self.sources.get_txt_s()
        in_txt = self.in_type.get_txt_s()
        out_txt = self.out_type.get_txt_s()

        # date
        dates = [
            datetime.date.fromordinal(x).isoformat()
            for x in data['date'] + STD_DAY
        ]
        self.appendColumn(arr_to_qitem(dates))

        # type, source, detail
        shape = data.shape
        types = np.zeros(shape, '<U12')
        dets = np.zeros(shape, '<U12')
        srcs = np.zeros(shape, '<U12')

        # parse type
        for type_num in range(4):
            types[data['type'] == type_num] = self.__type_text[type_num]

        # parse detail
        for num, txt in enumerate(in_txt):
            dets[
                (data['type'] == 0) & (data['det'] == num)
            ] = txt
        for num, txt in enumerate(out_txt):
            dets[
                (data['type'] == 1) & (data['det'] == num)
            ] = txt
        for num, txt in enumerate(src_txt):
            srcs[data['src'] == num] = txt
            dets[
                (data['type'] == 2) & (data['det'] == num)
            ] = txt
        dets[data['type'] == 3] = '-'

        self.appendColumn(arr_to_qitem(types))
        self.appendColumn(arr_to_qitem(srcs))
        self.appendColumn(arr_to_qitem(dets))
        # end type, source, detail

        # value, description
        self.appendColumn(arr_to_qitem(
            data['val'].astype('<U10').tolist()
        ))
        self.appendColumn(arr_to_qitem(data['desc']))
        # end parser

        self.setHorizontalHeaderLabels(self.__header_text)

    def save_data(self):
        data = {}

        data['version'] = self.__version

        data['sources'] = self.sources.get_raw()
        data['in_type'] = self.in_type.get_raw()
        data['out_type'] = self.out_type.get_raw()

        data['data'] = self.__data[:self.row_count].tolist()

        return data

    def import_data(self, file_type, raw_data, types):
        data = {}
        data['version'] = self.__version
        raw_sources = data['sources'] = types['sources']
        raw_in_type = data['in_type'] = types['in_type']
        raw_out_type = data['out_type'] = types['out_type']

        self.sources.set_data(raw_sources)
        self.in_type.set_data(raw_in_type)
        self.out_type.set_data(raw_out_type)

        sources = self.sources.get_txt_no()
        in_type = self.in_type.get_txt_no()
        out_type = self.out_type.get_txt_no()

        if file_type == 0:  # tsv
            data['data'] = self.__tsv_parser(
                raw_data, sources, in_type, out_type
            )
        elif file_type == 1:  # txt
            pass
        else:
            raise ValueError(f'Wrong file_type no: {file_type}')

        raise NotImplementedError(f'unpacker not implemented\nres:\n{data}')
        # self.__unpacker(data)

    def export_data(self, file_type):
        # pylint: disable=unreachable
        raise NotImplementedError('packer not implemented')
        data = self.__packer()

        if file_type == 0:  # tsv
            pass
        elif file_type == 1:  # txt
            pass
        else:
            raise ValueError(f'Wrong file_type no: {file_type}')

        types = {
            'sources': self.sources.get_raw(),
            'in_type': self.in_type.get_raw(),
            'out_type': self.out_type.get_raw(),
        }

        return data, types

    # parser
    def __tsv_parser(self, raw_data, sources, in_type, out_type):
        '''
        argument information

        sources, in_type, out_type: txt -> no
        rows: date, type, source, detail, value, description
        '''

        raw_data = list(map(lambda x: x.replace(
            '\n', '').split('\t'), raw_data))
        raw_data = np.array(raw_data)

        # parse row 0, 2, 4
        row0 = [(datetime.date.fromisoformat(x).toordinal() - STD_DAY)
                for x in raw_data[:-1, 0]]
        row2 = [sources[x] for x in raw_data[:-1, 2]]
        row4 = [int(x) for x in raw_data[:-1, 5]]

        # parse row 1, 3
        row1 = np.zeros(raw_data[:-1, 1].shape, 'uint8')
        row3 = np.zeros(raw_data[:-1, 3].shape, 'uint8')

        for no, txt in enumerate(self.__type_text):
            row1[raw_data[:-1, 1] == txt] = no

        for txt, no in sources:
            row3[
                (raw_data[:-1, 1] == self.__type_text[0])
                & (raw_data[:-1, 3] == txt)
            ] = no
        for txt, no in in_type:
            row3[
                (raw_data[:-1, 1] == self.__type_text[1])
                & (raw_data[:-1, 3] == txt)
            ] = no
        for txt, no in out_type:
            row3[
                (raw_data[:-1, 1] == self.__type_text[2])
                & (raw_data[:-1, 3] == txt)
            ] = no

        data = np.column_stack(
            (row0, row1, row2, row3, row4, raw_data[:-1, 4])
        )

        return data

    # getter/setter func
    def add_data(self, *args):
        assert len(args) == 6
        date, type_, src, det, val, desc = args

        if self.row_count >= MAX_DATA_CNT:
            raise MaxDataCountError
        else:
            try:
                date = datetime.date.fromisoformat(date).toordinal() - STD_DAY
                src_txt = self.sources.get_txt_no()
                type_ = self.__type_text.index(type_)

                if type_ == 0:
                    det = self.in_type.get_txt_no()[det]
                elif type_ == 1:
                    det = self.out_type.get_txt_no()[det]
                elif type_ == 2:
                    det = src_txt[det]
                else:
                    raise ValueError

                parsed_data = (
                    date,
                    type_,
                    src_txt[src],
                    det,
                    int(val),
                    desc
                )
            except Exception:
                raise ValueError('Tried to add data with wrong arguments')
            else:
                real_date = self.__data[:self.row_count]['date']
                if date >= real_date[-1]:  # append(=insert at end)
                    index = self.row_count
                    self.appendRow(arr_to_qitem(args))
                    self.__data[index] = parsed_data
                else:
                    index = np.searchsorted(real_date, date, 'right')
                    tmp_list = np.array(parsed_data, self.__data_form)
                    self.insertRow(index, arr_to_qitem(args))
                    if not index:
                        self.__data = np.append(
                            tmp_list, self.__data[:MAX_DATA_CNT - 1]
                        )
                    else:
                        tmp_list = np.append(self.__data[:index], tmp_list)
                        self.__data = np.append(
                            tmp_list, self.__data[index:MAX_DATA_CNT - 1]
                        )
                self.row_count += 1
                return index, parsed_data

    def del_data(self, row_no):
        data = self.__data[row_no]
        self.removeRow(row_no)
        self.__data = np.append(
            np.delete(self.__data, row_no), self.__empty_arr
        )
        self.row_count -= 1
        return data

    def get_data(self):
        return self.__data

    def get_at(self, row_no):
        return self.__data[row_no]

    def set_at(self, row_no, *args):
        assert len(args) == 6
        date, type_, src, det, val, desc = args

        try:
            date = datetime.date.fromisoformat(date).toordinal() - STD_DAY
            src_txt = self.sources.get_txt_no()
            type_ = self.__type_text.index(type_)

            if type_ == 0:
                det = self.in_type.get_txt_no()[det]
            elif type_ == 1:
                det = self.out_type.get_txt_no()[det]
            elif type_ == 2:
                det = src_txt[det]
            else:
                raise ValueError

            parsed_data = (
                date,
                type_,
                src_txt[src],
                det,
                int(val),
                desc
            )
        except Exception:
            raise ValueError('Tried to set data with wrong arguments')
        else:
            self.__data[row_no] = parsed_data
            for k, item in enumerate(arr_to_qitem(args)):
                self.setItem(row_no, k, item)
            return parsed_data

    @property
    def data_name(self):
        return self.__data_name


class Stat_Data(QStandardItemModel):
    # pylint: disable=attribute-defined-outside-init
    __header_text = (
        '연월', '총 재산', '현금성',
        '순 수익', '수입', '지출', '이동액'
    )
    __data_name = (
        'year', 'month', 'current',
        'income_src', 'outcome_src',
        'income_typ', 'outcome_typ',
        'move_in', 'move_out',
    )
    __type_col = ('income_src', 'outcome_src')
    __type_col2 = ('income_typ', 'outcome_typ')
    column_count = len(__header_text)

    def __init__(self, parent=None):
        super().__init__(0, 0, parent)
        self.setHorizontalHeaderLabels(self.__header_text)

        self.months = ComboData()

        self.__initalized = False

    def set_type(self, sources, in_type, out_type, is_cash, is_ness):
        self.__sources = sources
        self.__in_type = in_type
        self.__out_type = out_type

        sources_cnt = (max(sources) + 1) if sources else 0
        in_cnt = (max(in_type) + 1) if in_type else 0
        out_cnt = (max(out_type) + 1) if out_type else 0

        self.__cash_src = [is_cash.get(n, False) for n in range(sources_cnt)]
        self.__ness_dst = [is_ness.get(n, False) for n in range(out_cnt)]

        self.__data_form = [
            ('year', 'uint16'),
            ('month', 'uint8'),
            ('current', 'int32', (sources_cnt,)),
            ('income_src', 'int32', (sources_cnt,)),
            ('outcome_src', 'int32', (sources_cnt,)),
            ('income_typ', 'int32', (in_cnt,)),
            ('outcome_typ', 'int32', (out_cnt,)),
            ('move_in', 'int32', (sources_cnt,)),
            ('move_out', 'int32', (sources_cnt,))
        ]
        self.__empty_arr = np.zeros((1,), self.__data_form)

        self.__initalized = True

    def __caluclate_summary(self, d_c):
        cash = d_c['current'][self.__cash_src].sum()

        c2 = d_c['current'].sum()
        c3 = d_c['income_src'].sum()
        c4 = d_c['outcome_src'].sum()
        c5 = d_c['income_typ'].sum()
        c6 = d_c['outcome_typ'].sum()
        c7 = d_c['move_in'].sum()
        c8 = d_c['move_out'].sum()

        if c3 != c5 or c4 != c6 or c7 != c8:
            raise ValueError
        else:
            # sum of (current, cash, income, outcome, net, move)
            return c2, cash, c3, c4, c3-c4, c7  # noqa: E226

    def set_data(self, data):
        if not self.__initalized:
            raise NotInitalizedError

        self.__first_date = datetime.date.fromordinal(
            data['date'].min() + STD_DAY
        )
        self.__last_date = datetime.date.fromordinal(
            data['date'].max() + STD_DAY
        )
        first_y, first_m = self.__first_date.year, self.__first_date.month
        last_y, last_m = self.__last_date.year, self.__last_date.month

        self.clear()
        self.setHorizontalHeaderLabels(self.__header_text)

        self.months.clear()

        self.__month_list = []
        for m in range(first_m, 13):
            self.__month_list.append((first_y, m))
        for y in range(first_y + 1, last_y):
            for m in range(1, 13):
                self.__month_list.append((y, m))
        for m in range(1, last_m + 1):
            self.__month_list.append((last_y, m))

        self.__data = np.zeros((len(self.__month_list),), self.__data_form)

        self.__real_month = []
        last_current = self.__empty_arr[0]['current']
        for k, (y, m) in enumerate(self.__month_list):
            self.__data[k]['year'] = y
            self.__data[k]['month'] = m

            if m == 12:
                next_m = (y + 1, 1)
            else:
                next_m = (y, m + 1)

            first_date_m = datetime.date(y, m, 1).toordinal() - STD_DAY
            last_date_m = datetime.date(*next_m, 1).toordinal() - STD_DAY
            month_data = data[(
                (data['date'] >= first_date_m) & (data['date'] < last_date_m)
            )]

            if not month_data.size:
                self.__data[k]['current'] = last_current.copy()
                continue

            d_c = self.__data[k]

            # loop: in_type
            for d in self.__in_type:
                d_c['income_typ'][d] = month_data[(
                    (month_data['type'] == 0) & (month_data['det'] == d)
                )]['val'].sum()

            # loop: out_type
            for d in self.__out_type:
                d_c['outcome_typ'][d] = month_data[(
                    (month_data['type'] == 1) & (month_data['det'] == d)
                )]['val'].sum()

            # loop: sources
            for s in self.__sources:
                # income
                sum_in_src = month_data[(
                    (month_data['type'] == 0) & (month_data['src'] == s)
                )]['val'].sum()
                d_c['income_src'][s] = sum_in_src

                # outcome
                sum_out_src = month_data[(
                    (month_data['type'] == 1) & (month_data['src'] == s)
                )]['val'].sum()
                d_c['outcome_src'][s] = sum_out_src

                # move: out
                sum_mv_out = month_data[(
                    (month_data['type'] == 2) & (month_data['src'] == s)
                )]['val'].sum()
                d_c['move_out'][s] = sum_mv_out

                # move: in
                sum_mv_in = month_data[(
                    (month_data['type'] == 2) & (month_data['det'] == s)
                )]['val'].sum()
                d_c['move_in'][s] = sum_mv_in

                # first
                sum_f = month_data[(
                    (month_data['type'] == 3) & (month_data['src'] == s)
                )]['val'].sum()

                d_c['current'][s] = (
                    sum_in_src.astype(np.int64)
                    + sum_mv_in
                    - sum_out_src
                    - sum_mv_out
                    + last_current[s]
                    + sum_f
                )
            # end sources loop

            # calculate summary
            current, cash, income, outcome, net, move\
                = self.__caluclate_summary(d_c)

            if not any((income, outcome, move)):
                self.appendRow(arr_to_qitem(
                    ('최초', current, cash, '-', '-', '-', '-')
                ))
            else:
                self.appendRow(arr_to_qitem((
                    f'{y}-{m}', current, cash,
                    net, income, outcome, move
                )))
            last_current = d_c['current']
            self.__real_month.append(f'{y}-{m}')

        self.months.set_data(
            list((k, x) for k, x in enumerate(['-'] + self.__real_month))
        )

    def get_raw(self):
        return self.__data

    def get_month(self, month):
        if month:
            d_c = self.__data[self.__month_list.index(month)].copy()

            current, cash, income, outcome, net, move\
                = self.__caluclate_summary(d_c)
            ness = d_c['outcome_typ'][self.__ness_dst].sum()

            return (d_c, map(str, (
                income, outcome, current, cash, move,
                net, ness, outcome - ness
            )))

    def add_data(self, data):
        d = datetime.date.fromordinal(data[0] + STD_DAY)
        m_c = (d.year, d.month)

        if m_c in self.__month_list:
            month_txt = f'{m_c[0]}-{m_c[1]}'
            if month_txt not in self.__real_month:
                last_index = len(self.__real_month) - 2

                self.__real_month.append(month_txt)
                self.__real_month.sort()
                insert = True

                index_m = self.__real_month.index(month_txt)
                if index_m > last_index:
                    self.months.appendRow(
                        QStandardItem(month_txt)
                    )
                else:
                    self.months.insertRow(
                        index_m + 1, QStandardItem(month_txt)
                    )
            else:
                insert = False

            index = self.__month_list.index(m_c)
            index2 = self.__real_month.index(f'{m_c[0]}-{m_c[1]}')
            d_c = self.__data[index]

            type_ = data[1]
            src = data[2]
            val = data[4]

            if type_ == 2:  # move
                dst = data[3]
                d_c['move_in'][dst] += val
                d_c['current'][dst] += val
                d_c['move_out'][src] += val
                d_c['current'][src] -= val
            else:  # income or outcome
                det = data[3]
                d_c[self.__type_col[type_]][src] += val
                d_c[self.__type_col2[type_]][det] += val
                if type_ == 0:
                    d_c['current'][src] += val
                elif type_ == 1:
                    d_c['current'][src] -= val

            # recalculate summary
            current, cash, income, outcome, net, move\
                = self.__caluclate_summary(d_c)

            items = arr_to_qitem((
                f'{m_c[0]}-{m_c[1]}', current, cash,
                net, income, outcome, move
            ))
            if insert:
                self.insertRow(index2, items)
            else:
                for k, item in enumerate(items):
                    self.setItem(index2, k, item)
        else:
            '''
            if d<self.__first_date:
                tmp_m = []
                for m in range(m_c[1],13):
                    tmp_m.append((m_c[0], m))
                if m_c[0]<self.__month_list[0][0]:
                    for y in range(m_c[0] + 1,self.__month_list[0][0] + 1):
                        for m in range(1, 13):
                            tmp_m.append((y, m))

                self.__month_list = tmp_m + self.__month_list

                print(self.__month_list)
            el
            '''
            if d > self.__last_date:
                tmp_m = []
                if m_c[0] > self.__month_list[-1][0]:
                    for y in range(self.__month_list[0][0], m_c[0]):
                        for m in range(1, 13):
                            tmp_m.append((y, m))
                for m in range(1, m_c[1] + 1):
                    tmp_m.append((m_c[0], m))

                self.__month_list = self.__month_list + tmp_m
            else:
                # raise ValueError
                raise NotImplementedError(
                    'This case(d<self.__first_date) is not implemented'
                )

            l = len(tmp_m)  # noqa: E741
            last_month = self.__data[-1]
            tmp_data = np.zeros((l,), self.__data_form)
            for k, (y, m) in enumerate(tmp_m):
                tmp_data[k]['year'] = y
                tmp_data[k]['month'] = m
                tmp_data[k]['current'] = last_month['current'].copy()
                last_month = tmp_data[k]

            if d > self.__last_date:
                self.__data = np.append(self.__data, tmp_data)
                self.__last_date = d
            elif d < self.__first_date:
                self.__data = np.append(tmp_data, self.__data)
                self.__first_date = d

            self.add_data(data)

    def del_data(self, data):
        d = datetime.date.fromordinal(data[0] + STD_DAY)
        m_c = (d.year, d.month)

        if m_c in self.__month_list:
            index = self.__month_list.index(m_c)
            index2 = self.__real_month.index(f'{m_c[0]}-{m_c[1]}')
            d_c = self.__data[index]

            type_ = data[1]
            src = data[2]
            val = data[4]

            if type_ == 2:  # move
                dst = data[3]
                d_c['move_in'][dst] -= val
                d_c['current'][dst] -= val
                d_c['move_out'][src] -= val
                d_c['current'][src] += val
            else:  # income or outcome
                det = data[3]
                d_c[self.__type_col[type_]][src] -= val
                d_c[self.__type_col2[type_]][det] -= val
                if type_ == 0:
                    d_c['current'][src] -= val
                elif type_ == 1:
                    d_c['current'][src] += val

            # recalculate summary
            current, cash, income, outcome, net, move\
                = self.__caluclate_summary(d_c)

            items = arr_to_qitem((
                f'{m_c[0]}-{m_c[1]}', current, cash,
                net, income, outcome, move
            ))
            for k, item in enumerate(items):
                self.setItem(index2, k, item)

    @property
    def initalized(self):
        return self.__initalized

    @property
    def data_name(self):
        return self.__data_name
