# -*- coding: utf-8 -*-

from PySide6.QtCore    import *
from PySide6.QtGui     import *
from PySide6.QtWidgets import *

from UI import *

import numpy as np
import os,sys,json,datetime,threading
import traceback
import io,ftplib


STD_DAY      = 730120
MAX_DATA_CNT = 10000

CONFIG_DIR  = os.environ['localappdata']+'/hys.moneymanage'
CONFIG_FILE = os.environ['localappdata']+'/hys.moneymanage/config'


class NotInitalizedError(Exception):
    pass

class MaxDataCountError(Exception):
    pass


class ComboData(QStandardItemModel):
    order_changed=Signal()
    
    def __init__(self,parent=None):
        super().__init__(0,0,parent)
        
        self._data=[]
        
        #self.dataChanged.connect(self.change_order)
        self.dataChanged.connect(lambda: QTimer.singleShot(10,self.change_order))
    
    #this func is based from stackoverflow question 1263451
    def _bypass_ordchange(func):
        def inner(self,*args,**kwargs):
            self.__changing=True
            res=func(self,*args,**kwargs)
            self.__changing=False
            return res
        return inner
    
    def __item(self,obj):
        item=QStandardItem(obj)
        item.setFlags(item.flags()^Qt.ItemIsDropEnabled)
        return item
    
    #converters
    def get_no_txt(self):
        return {n:t for n,t in sorted(self._data)}
    
    def get_no_index(self):
        return {n:i for i,(n,t) in sorted(enumerate(self._data),key=lambda x: x[1][0])}
    
    def get_txt_no(self):
        return {t:n for n,t in self._data}
    
    def get_txt_index(self):
        return {t:i for i,(n,t) in enumerate(self._data)}
    
    def get_index_no(self):
        return {i:n for i,(n,t) in enumerate(self._data)}
    
    def get_index_txt(self):
        return {i:t for i,(n,t) in enumerate(self._data)}
    
    #get one element
    def get_no(self):
        return tuple(n for n,t in sorted(self._data))
    
    def get_index(self):
        return tuple(range(len(self._data)))
    
    def get_txt(self):
        return tuple(t for n,t in self._data)
    
    def get_txt_s(self):
        return tuple(t for n,t in sorted(self._data))
    
    #get raw data (for save/export)
    def get_raw(self):
        return self._data
    
    #setter func
    @_bypass_ordchange
    def add_data(self,txt):
        self._data.append((max(x for x,_ in self._data)+1,txt))
        self.appendRow(self.__item(txt))
    
    @_bypass_ordchange
    def set_data(self,txts):
        self._data=list(map(tuple,txts))
        self.clear()
        for _,txt in txts:
            self.appendRow(self.__item(txt))
    
    @_bypass_ordchange
    def del_no(self,no):
        self.del_index(self.get_no_index()[no])
    
    @_bypass_ordchange
    def del_index(self,index):
        del self._data[index]
        self.removeRow(index)
    
    def change_order(self):
        if not self.__changing:
            items = []
            for k in range(self.rowCount()):
                items.append(self.item(k).text())
            self._data.sort(key=lambda x: items.index(x[1]))
            self.order_changed.emit()


class ComboDataChk(ComboData):
    prefix='* '
    
    def get_chk_no(self):
        return list(txt.startswith(self.prefix) for _,txt in sorted(self._data))
    
    def get_chk_index(self):
        return list(txt.startswith(self.prefix) for _,txt in self._data)
    
    def get_no_chk(self):
        no_txt = self.get_no_txt()
        return {n:t.startswith(self.prefix) for n,t in sorted(self._data)}
    
    def get_index_chk(self):
        return {i:t.startswith(self.prefix) for i,(n,t) in enumerate(self._data)}
    
    def add_data(self,chk,data):
        prefix = self.prefix if chk else ''
        super().add_data(prefix+data)


class Data(QStandardItemModel):
    __header_text = ('일시', '구분', '원천', '상세/이동처', '금액', '설명')
    __type_text   = ('수입','지출','이동','초기')
    __data_form   = [
        ('date', 'uint16'), ('type', 'int8'  ), ('src' , 'uint8'),
        ('det' , 'uint8' ), ('val' , 'uint32'), ('desc', '<U64' )
    ]
    __data_name   = ('date', 'type', 'src', 'det', 'val', 'desc')
    
    __qitem_vec   = np.vectorize(lambda x: QStandardItem(str(x)))
    __parse_vdate = np.vectorize(lambda x: datetime.date.fromordinal(x+STD_DAY).isoformat())
    
    __empty_arr   = np.array((0,0,0,0,0,''), __data_form)
    
    column_count=len(__header_text)
    
    def __init__(self,parent):
        super().__init__(0,0,parent)
        self.setHorizontalHeaderLabels(self.__header_text)
        
        self.__parse_vdet  = np.vectorize(self.__parse_det)
        
        self.__version = 2
        
        self.type     = ComboData()
        self.sources  = ComboDataChk()
        self.in_type  = ComboData()
        self.out_type = ComboDataChk()
        
        self.list_detail = (self.in_type, self.out_type, self.sources)
        
        self.__data = np.empty((MAX_DATA_CNT,), self.__data_form)
        
        self.type.set_data(list((k,x) for k,x in enumerate(self.__type_text[:-1])))
        
        self.row_count=0
    
    def load_data(self,data):
        self.clear()
        
        self.__version = data['version']
        
        self.sources .set_data(data['sources'])
        self.in_type .set_data(data['in_type'])
        self.out_type.set_data(data['out_type'])
        
        self.row_count=len(data['data'])
        if self.row_count>MAX_DATA_CNT:
            raise MaxDataCountError
        else:
            raw_data=list(map(tuple,data['data']))
            self.__data = np.asarray(raw_data,self.__data_form)
        
        #parse data & set data
        self.__tmp_src_txt = self.sources .get_no_txt()
        self.__tmp_in_txt  = self.in_type .get_no_txt()
        self.__tmp_out_txt = self.out_type.get_no_txt()
        
        #date
        dates=self.__data['date']
        dates=self.__parse_vdate(dates)
        self.appendColumn(self.__qitem_vec(dates).tolist())
        
        #type&det
        types,dets=self.__parse_vdet(self.__data['type'],self.__data['det'])
        '''
        for k,txt in enumerate(self.__type_text):
            types[types==str(k)]=txt
        '''
        self.appendColumn(self.__qitem_vec(types).tolist())
        
        #src
        srcs=self.__data['src'].astype('<U12')
        for no,txt in self.__tmp_src_txt.items():
            srcs[srcs==str(no)]=txt
        self.appendColumn(self.__qitem_vec(srcs).tolist())
        
        #det&val&desc (append)
        self.appendColumn(self.__qitem_vec(dets).tolist())
        self.appendColumn(self.__qitem_vec(self.__data['val'].astype('<U10')).tolist())
        self.appendColumn(self.__qitem_vec(self.__data['desc']).tolist())
        #end parser
        
        self.setHorizontalHeaderLabels(self.__header_text)
        
        if self.row_count<MAX_DATA_CNT:
            self.__data=np.append(
                np.asarray(raw_data                      , self.__data_form),
                np.empty  ((MAX_DATA_CNT-self.row_count,), self.__data_form)
            )
    
    def save_data(self):
        data={}
        
        data['version'] = self.__version
        
        data['sources']  = self.sources .get_raw()
        data['in_type']  = self.in_type .get_raw()
        data['out_type'] = self.out_type.get_raw()
        
        data['data'] = self.__data[:self.row_count].tolist()
        
        return data
    
    def import_data(self,file_type,file_path,type_path,*,encoding='utf-8'):
        data={}
        with open(file_path,'r',encoding=encoding) as file:
            raw_data=file.readlines()
        
        data['version'] = self.__version
        
        with open(type_path,'r',encoding=encoding) as file:
            types=json.load(file)
        
        raw_sources  = data['sources']  = types['sources']
        raw_in_type  = data['in_type']  = types['in_type']
        raw_out_type = data['out_type'] = types['out_type']
        
        self.sources .set_data(raw_sources)
        self.in_type .set_data(raw_in_type)
        self.out_type.set_data(raw_out_type)
        
        sources  = self.sources .get_txt_no()
        in_type  = self.in_type .get_txt_no()
        out_type = self.out_type.get_txt_no()
        
        if file_type==0: #tsv
            data['data']=self.__tsv_parser(raw_data,sources,in_type,out_type)
        elif file_type==1: #txt
            pass
        else:
            raise ValueError(f'Wrong file_type no: {file_type}')
        
        raise NotImplementedError(f'unpacker not implemented\nres:\n{data}')
        #self.__unpacker(data)
    
    def export_data(self,file_type,file_path,type_path='',*,encoding='utf-8'):
        raise NotImplementedError('packer not implemented')
        data=self.__packer()
        
        if file_type==0: #tsv
            pass
        elif file_type==1: #txt
            pass
        else:
            raise ValueError(f'Wrong file_type no: {file_type}')
        
        with open(file_path,'w',encoding=encoding) as file:
            file.write(data)
        
        if type_path:
            types={}
            types['sources' ] = self.sources .get_raw()
            types['in_type' ] = self.in_type .get_raw()
            types['out_type'] = self.out_type.get_raw()
            with open(type_path,'w',encoding=encoding) as file:
                json.dump(types,file)
    
    #parser
    def __parse_det(self,type_,det):
        parsed_type=self.__type_text[type_]
        
        if type_==0:
            parsed_det=self.__tmp_in_txt[det]
        elif type_==1:
            parsed_det=self.__tmp_out_txt[det]
        elif type_==2:
            parsed_det=self.__tmp_src_txt[det]
        elif type_==3:
            parsed_det='-'
        else:
            raise ValueError
        
        return parsed_type,parsed_det
    
    def __tsv_parser(self,raw_data,sources,in_type,out_type):
        def parse13(row1,row3):
            res1=self.__type_text.index(row1)
            
            if res1==0:
                res3=in_type[row3]
            elif res1==1:
                res3=out_type[row3]
            elif res1==2:
                res3=sources[row3]
            elif res1==4:
                res3=0
            else:
                raise ValueError
            
            return res1,res3
        
        parse0 = lambda x: datetime.date.fromisoformat(x).toordinal()-STD_DAY
        parse2 = lambda x: sources[x] if x else 0
        
        def parse4(x):
            if x:
                return int(x)
        
        vp0   = np.vectorize(parse0)
        vp2   = np.vectorize(parse2)
        vp13  = np.vectorize(parse13)
        vp4   = np.vectorize(parse4)
        
        raw_data=list(map(lambda x: x.replace('\n','').split('\t'),raw_data))
        raw_data=np.array(raw_data)
        
        row0=vp0(raw_data[:-1,0])
        row2=vp2(raw_data[:-1,2])
        row1,row3=vp13(raw_data[:-1,1],raw_data[:-1,3])
        row4=vp4(raw_data[:-1,5])
        #row4=np.array(raw_data[:-1,5],dtype=np.uint32)
        
        data=np.column_stack((row0,row1,row2,row3,row4,raw_data[:-1,4]))
        
        return data
    
    #getter/setter func
    def add_data(self,*args):
        assert len(args)==6
        date,type_,src,det,val,desc=args
        
        if self.row_count>=MAX_DATA_CNT:
            raise MaxDataCountError
        else:
            try:
                date=datetime.date.fromisoformat(date).toordinal()-STD_DAY
                src_txt=self.sources.get_txt_no()
                type_=self.__type_text.index(type_)
                
                if type_==0:
                    det=self.in_type.get_txt_no()[det]
                elif type_==1:
                    det=self.out_type.get_txt_no()[det]
                elif type_==2:
                    det=src_txt[det]
                else:
                    raise ValueError
                
                parsed_data=(
                    date        ,
                    type_       ,
                    src_txt[src],
                    det         ,
                    int(val)    ,
                    desc              
                )
            except:
                raise ValueError('Tried to add data with wrong arguments')
            else:
                real_date=self.__data[:self.row_count]['date']
                if date>=real_date[-1]: #append(=insert at end)
                    self.appendRow(self.__qitem_vec(args).tolist())
                    self.__data[self.row_count]=parsed_data
                else:
                    index    = np.searchsorted(real_date,date,'right')
                    tmp_list = np.array(parsed_data,self.__data_form)
                    self.insertRow(index,self.__qitem_vec(args).tolist())
                    if not index:
                        self.__data = np.append(tmp_list,self.__data[:MAX_DATA_CNT-1])
                    else:
                        tmp_list    = np.append(self.__data[:index],tmp_list)
                        self.__data = np.append(tmp_list,self.__data[index:MAX_DATA_CNT-1])
                self.row_count+=1
                return parsed_data
    
    def del_data(self,row_no):
        data = self.__data[row_no]
        self.removeRow(row_no)
        self.__data = np.append(np.delete(self.__data,row_no),self.__empty_arr)
        self.row_count-=1
        return data
    
    def get_data(self):
        return self.__data
    
    def get_at(self,row_no):
        return self.__data[row_no]
    
    def set_at(self,row_no,*args):
        assert len(args)==6
        date,type_,src,det,val,desc=args
        
        try:
            date=datetime.date.fromisoformat(date).toordinal()-STD_DAY
            src_txt=self.sources.get_txt_no()
            type_=self.__type_text.index(type_)
            
            if type_==0:
                det=self.in_type.get_txt_no()[det]
            elif type_==1:
                det=self.out_type.get_txt_no()[det]
            elif type_==2:
                det=src_txt[det]
            else:
                raise ValueError
            
            parsed_data=(
                date        ,
                type_       ,
                src_txt[src],
                det         ,
                int(val)    ,
                desc              
            )
        except:
            raise ValueError('Tried to set data with wrong arguments')
        else:
            self.__data[row_no]=parsed_data
            for k,item in enumerate(self.__qitem_vec(args).tolist()):
                self.setItem(row_no,k,item)
            return parsed_data
    
    @property
    def data_name(self):
        return self.__data_name


class Stat_Data(QStandardItemModel):
    __header_text = (
        '연월', '총 재산', '현금성',
        '순 수익', '수입', '지출', '이동액'
    )
    __data_name = (
        'year',  'month',  'current',
        'income_src',  'outcome_src',
        'income_typ',  'outcome_typ',
        'move_in'   ,     'move_out',
    )
    __type_col  = ('income_src', 'outcome_src')
    __type_col2 = ('income_typ', 'outcome_typ')
    column_count=len(__header_text)
        
    __qitem_vec = np.vectorize(lambda x: QStandardItem(str(x)))
    
    
    def __init__(self,parent=None):
        super().__init__(0,0,parent=None)
        self.setHorizontalHeaderLabels(self.__header_text)
        
        self.months=ComboData()
        
        self.__initalized=False
    
    def set_type(self,sources,in_type,out_type,is_cash,is_ness):
        self.__sources  = sources
        self.__in_type  = in_type
        self.__out_type = out_type
        
        sources_cnt = max(sources)+1
        in_cnt      = max(in_type)+1
        out_cnt     = max(out_type)+1
        
        self.__cash_src = np.array(self.__sources )[is_cash].tolist()
        self.__ness_dst = np.array(self.__out_type)[is_ness].tolist()
        
        self.__data_form = [
            ('year', 'uint16'),  ('month', 'uint8'), ('current'    , 'int32', (sources_cnt,)),
            ('income_src', 'int32', (sources_cnt,)), ('outcome_src', 'int32', (sources_cnt,)),
            ('income_typ', 'int32', (in_cnt,)),      ('outcome_typ', 'int32', (out_cnt,)    ),
            ('move_in'   , 'int32', (sources_cnt,)), ('move_out'   , 'int32', (sources_cnt,))
        ]
        self.__empty_arr = np.zeros((1,), self.__data_form)
        
        self.__initalized=True
    
    def set_data(self,data):
        if self.__initalized:
            self.__first_date = datetime.date.fromordinal(data['date'].min()+STD_DAY)
            self.__last_date  = datetime.date.fromordinal(data['date'].max()+STD_DAY)
            first_y, first_m = self.__first_date.year, self.__first_date.month
            last_y , last_m  = self.__last_date.year , self.__last_date.month
            
            self.clear()
            self.setHorizontalHeaderLabels(self.__header_text)
            
            self.months.clear()
            
            self.__month_list=[]
            for m in range(first_m,13):
                self.__month_list.append((first_y,m))
            for y in range(first_y+1,last_y):
                for m in range(1,13):
                    self.__month_list.append((y,m))
            for m in range(1,last_m+1):
                self.__month_list.append((last_y,m))
            
            self.__data = np.zeros((len(self.__month_list),), self.__data_form)
            
            self.__real_month = []
            last_current = self.__empty_arr[0]['current']
            for k,(y,m) in enumerate(self.__month_list):
                self.__data[k]['year']  = y
                self.__data[k]['month'] = m
                
                if m==12:
                    next_m=(y+1,1)
                else:
                    next_m=(y,m+1)
                
                first_date_m = datetime.date(y,  m  ,1).toordinal()-STD_DAY
                last_date_m  = datetime.date(*next_m,1).toordinal()-STD_DAY
                month_data=data[(data['date']>=first_date_m)&(data['date']<last_date_m)]
                
                if month_data.size:
                    d_c  = self.__data[k]
                    cash = 0
                    ness = 0
                    
                    for t in range(2):
                        for s in self.__sources:
                            type_sum=month_data[(month_data['type']==t)&(month_data['src']==s)]['val'].sum()
                            d_c[self.__type_col[t]][s]=type_sum
                    
                    for d in self.__in_type:
                        type_sum=month_data[(month_data['type']==0)&(month_data['det']==d)]['val'].sum()
                        d_c['income_typ'][d]=type_sum
                    
                    for d in self.__out_type:
                        type_sum=month_data[(month_data['type']==1)&(month_data['det']==d)]['val'].sum()
                        d_c['outcome_typ'][d]=type_sum
                        
                        if d in self.__ness_dst:
                            ness+=d_c['outcome_typ'][d]
                    
                    for s in self.__sources:
                        type_sum_o=month_data[(month_data['type']==2)&(month_data['src']==s)]['val'].sum()
                        d_c['move_out'][s]=type_sum_o
                        
                        type_sum_i=month_data[(month_data['type']==2)&(month_data['det']==s)]['val'].sum()
                        d_c['move_in'][s]=type_sum_i
                        
                        type_sum_f=month_data[(month_data['type']==3)&(month_data['src']==s)]['val'].sum()
                        sum_=(
                            d_c['income_src'][s]  +\
                            d_c['move_in'][s]     -\
                            d_c['outcome_src'][s] -\
                            d_c['move_out'][s]    +\
                            last_current[s]       +\
                            type_sum_f
                        )
                        d_c['current'][s]=sum_
                        if s in self.__cash_src:
                            cash+=sum_
                        
                        c2 = d_c['current'].sum()
                        c3 = d_c['income_src'].sum()
                        c4 = d_c['outcome_src'].sum()
                        c5 = d_c['income_typ'].sum()
                        c6 = d_c['outcome_typ'].sum()
                        c7 = d_c['move_in'].sum()
                        c8 = d_c['move_out'].sum()
                        
                    if c3!=c5 or c4!=c6 or c7!=c8:
                        raise ValueError
                    else:
                        self.appendRow(self.__qitem_vec((f'{y}-{m}',c2,cash,c3-c4,c3,c4,c7)).tolist())
                        last_current=d_c['current']
                        self.__real_month.append(f'{y}-{m}')
                else:
                    self.__data[k]['current']=last_current.copy()
            
            self.months.set_data(list((k,x) for k,x in enumerate(['-']+self.__real_month)))
        else:
            raise NotInitalizedError
    
    def get_raw(self):
        return self.__data
    
    def get_month(self,month):
        if month:
            index = self.__month_list.index(month)
            d_c   = self.__data[index].copy()
            
            cash = 0
            for s in self.__sources:
                if s in self.__cash_src:
                    cash+=d_c['current'][s]
            
            ness = 0
            for d in self.__out_type:
                if d in self.__ness_dst:
                    ness+=d_c['outcome_typ'][d]
            
            c2 = d_c[2].sum() #current
            c3 = d_c[3].sum() #income_src
            c4 = d_c[4].sum() #outcome_src
            c5 = d_c[5].sum() #income_typ
            c6 = d_c[6].sum() #outcome_typ
            c7 = d_c[7].sum() #move_in
            c8 = d_c[8].sum() #move_out
            
            if c3!=c5 or c4!=c6 or c7!=c8:
                raise ValueError
            else:
                return (d_c,map(str,(c3,c4,c2,cash,c7,c3-c4,ness,c4-ness)))
        
    def add_data(self,data):
        d=datetime.date.fromordinal(data[0]+STD_DAY)
        m_c=(d.year,d.month)
        
        if m_c in self.__month_list:
            month_txt=f'{m_c[0]}-{m_c[1]}'
            if not month_txt in self.__real_month:
                last_index=len(self.__real_month)-2
                
                self.__real_month.append(month_txt)
                self.__real_month.sort()
                insert=True
                
                index_m = self.__real_month.index(month_txt)
                if index_m>last_index:
                    self.months.appendRow(QStandardItem(month_txt))
                else:
                    self.months.insertRow(index_m+1,QStandardItem(month_txt))
            else:
                insert=False
            
            index  = self.__month_list.index(m_c)
            index2 = self.__real_month.index(f'{m_c[0]}-{m_c[1]}')
            d_c    = self.__data[index]
            
            type_ = data[1]
            src   = data[2]
            val   = data[4]
            
            if type_==2: #move
                dst=data[3]
                d_c['move_in'] [dst]+=val
                d_c['current'] [dst]+=val
                d_c['move_out'][src]+=val
                d_c['current'] [src]-=val
            else: #income or outcome
                det=data[3]
                d_c[self.__type_col [type_]][src]+=val
                d_c[self.__type_col2[type_]][det]+=val
                if type_==0:
                    d_c['current'][src]+=val
                elif type_==1:
                    d_c['current'][src]-=val
            
            #recalculate summary
            cash=0
            for s in self.__cash_src:
                cash+=d_c['current'][s]
            
            ness = 0
            for d in self.__ness_dst:
                ness+=d_c['outcome_typ'][d]
            
            c2 = d_c['current'].sum()
            c3 = d_c['income_src'].sum()
            c4 = d_c['outcome_src'].sum()
            c5 = d_c['income_typ'].sum()
            c6 = d_c['outcome_typ'].sum()
            c7 = d_c['move_in'].sum()
            c8 = d_c['move_out'].sum()
            
            if c3!=c5 or c4!=c6 or c7!=c8:
                raise ValueError
            else:
                items=self.__qitem_vec((f'{m_c[0]}-{m_c[1]}',c2,cash,c3-c4,c3,c4,c7)).tolist()
                if insert:
                    self.insertRow(index2,items)
                else:
                    for k,item in enumerate(items):
                        self.setItem(index2,k,item)
        else:
            '''
            if d<self.__first_date:
                tmp_m=[]
                for m in range(m_c[1],13):
                    tmp_m.append((m_c[0],m))
                if m_c[0]<self.__month_list[0][0]:
                    for y in range(m_c[0]+1,self.__month_list[0][0]+1):
                        for m in range(1,13):
                            tmp_m.append((y,m))
                
                self.__real_month = [f'{m_c[0]}-{m_c[1]}']+self.__real_month
                self.__month_list = tmp_m+self.__month_list
                
                print(self.__month_list,self.__real_month)
            el
            '''
            if d>self.__last_date:
                tmp_m=[]
                if m_c[0]>self.__month_list[-1][0]:
                    for y in range(self.__month_list[0][0],m_c[0]):
                        for m in range(1,13):
                            tmp_m.append((y,m))
                for m in range(1,m_c[1]+1):
                    tmp_m.append((m_c[0],m))
                
                self.__real_month.append(f'{m_c[0]}-{m_c[1]}')
                self.__month_list = self.__month_list+tmp_m
            else:
                raise ValueError('Cannnot parse data')
            
            l=len(tmp_m)
            last_month = self.__data[-1]
            tmp_data   = np.zeros((l,), self.__data_form)
            for k,(y,m) in enumerate(tmp_m):
                tmp_data[k]['year']  = y
                tmp_data[k]['month'] = m
                tmp_data[k]['current']=last_month['current'].copy()
                last_month=tmp_data[k]
                
            if d>self.__last_date:
                self.__data = np.append(self.__data,tmp_data)
                self.__last_date=d
            elif d<self.__first_date:
                self.__data = np.append(tmp_data,self.__data)
                self.__first_date=d
        
    def del_data(self,data):
        d=datetime.date.fromordinal(data[0]+STD_DAY)
        m_c=(d.year,d.month)
        
        if m_c in self.__month_list:
            index  = self.__month_list.index(m_c)
            index2 = self.__real_month.index(f'{m_c[0]}-{m_c[1]}')
            d_c    = self.__data[index]
            
            type_ = data[1]
            src   = data[2]
            val   = data[4]
            
            if type_==2: #move
                dst=data[3]
                d_c['move_in'] [dst]-=val
                d_c['current'] [dst]-=val
                d_c['move_out'][src]-=val
                d_c['current'] [src]+=val
            else: #income or outcome
                det=data[3]
                d_c[self.__type_col [type_]][src]-=val
                d_c[self.__type_col2[type_]][det]-=val
                if type_==0:
                    d_c['current'][src]-=val
                elif type_==1:
                    d_c['current'][src]+=val
            
            #recalculate summary
            cash=0
            for s in self.__cash_src:
                cash+=d_c['current'][s]
            
            ness = 0
            for d in self.__ness_dst:
                ness+=d_c['outcome_typ'][d]
            
            c2 = d_c['current'].sum()
            c3 = d_c['income_src'].sum()
            c4 = d_c['outcome_src'].sum()
            c5 = d_c['income_typ'].sum()
            c6 = d_c['outcome_typ'].sum()
            c7 = d_c['move_in'].sum()
            c8 = d_c['move_out'].sum()
            
            if c3!=c5 or c4!=c6 or c7!=c8:
                raise ValueError
            else:
                items=self.__qitem_vec((f'{m_c[0]}-{m_c[1]}',c2,cash,c3-c4,c3,c4,c7)).tolist()
                for k,item in enumerate(items):
                    self.setItem(index2,k,item)
    
    @property
    def initalized(self):
        return self.__initalized
    
    @property
    def data_name(self):
        return self.__data_name


class Txt(QMainWindow,Ui_Txt):
    def __init__(self,parent,title,info_text):
        super().__init__(parent)
        self.setupUi(self,title,info_text)
        
        self.btnExit.clicked.connect(self.hide)
    
    def set_text(self,text):
        self.pteMain.setPlainText(text)


class Info(QMainWindow,Ui_Info):
    def __init__(self,parent,title,info_text):
        super().__init__(parent)
        self.setupUi(self,title,info_text)
        
        self.btnExit.clicked.connect(self.hide)
        self.btnQt.clicked.connect(lambda: QMessageBox.aboutQt(self))


class Pg(QMainWindow,Ui_Pg):
    def __init__(self,parent):
        super().__init__(parent)
        self.setupUi(self)
    
    def set_detail(self,txt):
        self.lbStatus.setText(txt)


class Login(QMainWindow,Ui_Login):
    def __init__(self,parent):
        super().__init__(parent)
        self.setupUi(self)
        
        self.username = ''
        self.password = ''
        
        self.btnFile.clicked.connect(self.__set_file)
    
    def __set_file(self):
        self.__file = None
        self.__file,_ = QFileDialog.getOpenFileName(self,'업로드',filter='데이터 파일(*.json)')
        if self.__file:
            self.btnConnect.setEnabled(True)
    
    def show_get(self):
        self.show()
        self.upload=False
        self.btnFile.hide()
        self.btnConnect.setEnabled(True)
        self.btnConnect.setText('다운로드')
    
    def show_put(self):
        self.show()
        self.upload=True
        self.btnFile.show()
        self.btnConnect.setEnabled(False)
        self.btnConnect.setText('업로드')
    
    def do_get(self,signal):
        path_txt      = self.lnPath.text()
        self.username = self.lnUser.text()
        self.password = self.lnPass.text()
        
        try:
            if path_txt:
                tmp,path=path_txt.split('ftp://')[-1].split('/',1)
                if ':' in tmp:
                    tmp=tmp.split(':')
                    addr,port=tmp
                else:
                    addr=tmp
                    port=0
                print(addr,port,path)
                
                with io.BytesIO() as tmp:
                    if self.chkEnc.checkState():
                        with ftplib.FTP_TLS() as srv:
                            srv.connect(addr,port)
                            srv.auth()
                            srv.prot_p()
                            srv.login(self.username, self.password)
                            srv.retrbinary(f'RETR /{path}',tmp.write)
                    else:
                        with ftplib.FTP() as srv:
                            srv.connect(addr,port)
                            srv.login(self.username, self.password)
                            srv.retrbinary(f'RETR /{path}',tmp.write)
                    tmp.seek(0)
                    raw_data=tmp.read()
                
                data=raw_data.decode('utf-8')
                signal.emit(0,data,'')
            else:
                signal.emit(1,{},'')
        except:
            signal.emit(2,{},traceback.format_exc())
    
    def do_put(self,data,signal):
        path_txt      = self.lnPath.text()
        self.username = self.lnUser.text()
        self.password = self.lnPass.text()
        try:
            if path_txt:
                tmp,path=path_txt.split('ftp://')[-1].split('/',1)
                if ':' in tmp:
                    tmp=tmp.split(':')
                    addr,port=tmp
                else:
                    addr=tmp
                    port=0
                print(addr,port,path)
            
                with io.BytesIO() as tmp:
                    with open(self.__file,'r',encoding='utf-8') as file:
                        tmp.write(file.read().encode('utf-8'))
                    tmp.seek(0)
                    if self.chkEnc.checkState():
                        with ftplib.FTP_TLS() as srv:
                            srv.connect(addr,port)
                            srv.auth()
                            srv.prot_p()
                            srv.login(self.username, self.password)
                            srv.storbinary(f'STOR /{path}',tmp)
                    else:
                        with ftplib.FTP() as srv:
                            srv.connect(addr,port)
                            srv.login(self.username, self.password)
                            srv.storbinary(f'STOR /{path}',tmp)
            
                signal.emit(0,{},'')
            else:
                signal.emit(1,{},'')
        except:
            signal.emit(2,{},traceback.format_exc())


class MainWin(QMainWindow,Ui_MainWin):
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
    __file_type   = (';;'.join(__file_text  ))
    __header_type = (';;'.join(__header_text))
    
    trans_sig = Signal(int,dict,str)
    
    def __init__(self,file_name):
        super().__init__()
        self.setupUi(self)
        
        
        #define instance variable
        self.__saved = True
        self.__last_file = ''
        self.__title_labels = tuple()
        self.__data_labels  = tuple()
        self.__sum_labels   = tuple()
        
        
        #define models
        self.__data = Data     (self.tabData.treeData)
        self.__stat = Stat_Data(self.tabStatS.treeStatS)
        
        
        #define sub-windows
        self.__login_win = Login(self)
        self.__login_win.btnConnect.clicked.connect(self.__do_transfer)
        
        self.__pg_win = Pg(self)
        
        try:
            with open('Notice','r',encoding='utf-8') as file:
                txt=file.read()
        except:
            self.__opensource_win = Info(self,'Open Source License','Open Source Notice file (Notice) does not exist')
        else:
            self.__opensource_win = Info(self,'Open Source License',txt)
        
        try:
            with open('License','r',encoding='utf-8') as file:
                txt=file.read()
        except:
            self.__license_win = Txt(self,'License','License file (License) does not exist')
        else:
            self.__license_win = Txt(self,'License',txt)
        
        self.__info_win = QMessageBox(self)
        self.__info_win.setWindowTitle('test')
        try:
            with open('Info','r',encoding='utf-8') as file:
                txt=file.read()
        except:
            self.acInfo.setEnabled(False)
        else:
            self.__info_win.setText(txt)
            self.acInfo.triggered.connect(self.__info_win.show)
        
        self.__err_win = Txt(self,'Error','')
        
        #load data
        if file_name:
            self.__load(file_name)
        else:
            if os.path.isfile(CONFIG_FILE):
                with open(CONFIG_FILE,'r') as file:
                    last_file,username,password=file.read().split('\n')
                    
                    self.__login_win.username = username
                    self.__login_win.password = password
                    
                    if os.path.isfile(last_file):
                        self.__load(last_file)
                    else:
                        print(last_file)
        
        #connect signals
        self.acLoad  .triggered.connect(self.__load_as)
        self.acSave  .triggered.connect(self.__save)
        self.acSaveAs.triggered.connect(self.__save_as)
        self.acGet   .triggered.connect(self.__login_win.show_get)
        self.acPut   .triggered.connect(self.__login_win.show_put)
        self.acImport.triggered.connect(self.__import_as)
        self.acExport.triggered.connect(self.__export_as)
        self.acExit  .triggered.connect(self.close)
        
        self.acOpenLicense.triggered.connect(self.__opensource_win.show)
        self.acLicense.triggered.connect(self.__license_win.show)
        
        self.__data.sources .order_changed.connect(self.__change_ord)
        self.__data.in_type .order_changed.connect(self.__change_ord)
        self.__data.out_type.order_changed.connect(self.__change_ord)
        
        self.tabCate.gbSrc.lvOrd.setModel(self.__data.sources)
        self.tabCate.gbIn .lvOrd.setModel(self.__data.in_type)
        self.tabCate.gbOut.lvOrd.setModel(self.__data.out_type)
        
        self.tabCate.gbSrc.btnAdd.clicked.connect(self.__add_source)
        self.tabCate.gbIn .btnAdd.clicked.connect(self.__add_in)
        self.tabCate.gbOut.btnAdd.clicked.connect(self.__add_out)
        
        self.tabData.treeData.setModel(self.__data)
        self.tabData.treeData.selectionModel().selectionChanged.connect(self.__start_edit)
        
        self.tabData.cbType  .setModel(self.__data.type)
        self.tabData.cbSrc   .setModel(self.__data.sources)
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
        def next_trans(res,data,err_txt):
            self.trans_sig.disconnect()
            self.__pg_win.hide()
            
            if res==0:
                if data:
                    self.__data.load_data(data)
            elif res==1:
                QMessageBox.warning(self,'입력 오류','파일 주소 입력 안됨')
            elif res==2:
                msgbox=QMessageBox(
                    QMessageBox.Warning,'경고',
                    f"{'전송 도중 오류 발생':70}",
                    QMessageBox.Retry|QMessageBox.Cancel,
                    self
                )
                msgbox.setDetailedText(err_txt)
                response=msgbox.exec_()
                if response==QMessageBox.Retry:
                    self.__do_transfer()
        #next_trans
        
        self.__pg_win.show()
        try:
            if self.__login_win.upload:
                self.__pg_win.set_detail('데이터 업로드 중')
                data=self.__data.save_data()
                self.trans_sig.connect(next_trans)
                threading.Thread(target=self.__login_win.do_put,args=(data,self.trans_sig)).start()
            else:
                self.__pg_win.set_detail('데이터 다운로드 중')
                self.trans_sig.connect(next_trans)
                threading.Thread(target=self.__login_win.do_get,args=(self.trans_sig,)).start()
        except:
            msgbox=QMessageBox(
                QMessageBox.Warning,'경고',
                f"{'전송 전후 오류 발생':70}",
                QMessageBox.Retry|QMessageBox.Cancel,
                self
            )
            msgbox.setDetailedText(traceback.format_exc())
            response=msgbox.exec_()
            if response==QMessageBox.Retry:
                self.__do_transfer()
    
    def __show_err(self,err_type,txt):
        self.__err_win.set_text(f'{err_type}\n{txt}')
        self.__err_win.show()
    
    def __resize(self):
        for k in range(0,self.__data.column_count):
            self.tabData.treeData.resizeColumnToContents(k)
    
    def __add_data(self):
        try:
            date   = self.tabData.lnDate.text()
            type_  = self.tabData.cbType.currentText()
            src    = self.tabData.cbSrc.currentText()
            detail = self.tabData.cbDetail.currentText()
            cost   = self.tabData.lnCost.text()
            desc   = self.tabData.lnDetail.text()
            
            parsed = self.__data.add_data(date,type_,src,detail,cost,desc)
            self.__stat.add_data(parsed)
            self.__set_month(self.tabStatM.cbMonth.currentText())
        except:
            msgbox=QMessageBox(QMessageBox.Warning,'경고',f"{'잘못된 입력':70}",QMessageBox.Cancel,self)
            msgbox.setDetailedText(traceback.format_exc())
            msgbox.exec_()
        else:
            self.__resize()
            self.__saved=False
            
            self.tabData.lnDate.setText('')
            self.tabData.cbType.setCurrentIndex(0)
            self.tabData.cbSrc.setCurrentIndex(0)
            self.tabData.cbDetail.setCurrentIndex(0)
            self.tabData.lnCost.setText('')
            self.tabData.lnDetail.setText('')
    
    def __del_data(self,data_no):
        data = self.__data.del_data(data_no.row())
        self.__stat.del_data(data)
        self.__set_month(self.tabStatM.cbMonth.currentText())
        self.__resize()
        self.__saved=False
    
    def __start_edit(self,sel,_):
        data_no = sel.indexes()[0]
        row_no  = data_no.row()
        
        data  = self.__data.get_at(row_no)
        type_ = data[1]
        
        if type_==3:
            self.__end_edit()
        else:
            date = self.__data.item(row_no,0).text()
            src  = self.__data.item(row_no,2).text()
            det  = self.__data.item(row_no,3).text()
            cost = self.__data.item(row_no,4).text()
            desc = self.__data.item(row_no,5).text()
            
            self.tabData.lnDate.setText(date)
            self.tabData.cbType.setCurrentIndex(type_)
            self.tabData.cbSrc.setCurrentText(src)
            self.tabData.cbDetail.setCurrentText(det)
            self.tabData.lnCost.setText(cost)
            self.tabData.lnDetail.setText(desc)
            
            self.tabData.btnAddData.setText('수정')
            self.tabData.btnCancel.show()
            self.tabData.btnAddData.clicked.disconnect()
            self.tabData.btnAddData.clicked.connect(lambda: self.__edit_data(data_no,date))
        
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
    
    def __edit_data(self,data_no,priv_date):
        row_no  = data_no.row()
        
        #delete stat
        data = self.__data.get_at(row_no)
        self.__stat.del_data(data)
        #change data & add stat
        try:
            date   = self.tabData.lnDate.text()
            type_  = self.tabData.cbType.currentText()
            src    = self.tabData.cbSrc.currentText()
            detail = self.tabData.cbDetail.currentText()
            cost   = self.tabData.lnCost.text()
            desc   = self.tabData.lnDetail.text()
            
            if date==priv_date:
                parsed = self.__data.set_at(row_no,date,type_,src,detail,cost,desc)
            else:
                self.__del_data(data_no)
                parsed = self.__data.add_data(date,type_,src,detail,cost,desc)
            self.__stat.add_data(parsed)
            self.__set_month(self.tabStatM.cbMonth.currentText())
        except:
            msgbox=QMessageBox(
                QMessageBox.Warning,'경고',
                f"{'잘못된 입력':70}",
                QMessageBox.Cancel,
                self
            )
            msgbox.setDetailedText(traceback.format_exc())
            msgbox.exec_()
        else:
            self.__resize()
            self.__saved=False
            self.__end_edit()
    
    def __set_month(self,text):
        if text and text!='-': #if month -> set data
            m_c=tuple(map(int,text.split('-')))
            raw_data=self.__stat.get_month(m_c)
            if raw_data:
                data,sums=raw_data
                
                src_ni = self.__data.sources.get_index_no()
                in_ni  = self.__data.in_type.get_index_no()
                out_ni = self.__data.out_type.get_index_no()
                
                data_changer = (src_ni,src_ni,src_ni,in_ni,out_ni,src_ni,src_ni)
                for wids,type_,changer in zip(self.__data_labels,self.__stat.data_name[2:],data_changer):
                    for b,wid in enumerate(wids):
                        wid.setText(str(data[type_][changer[b]]))
                
                for wid,sum_ in zip(self.__sum_labels,sums):
                    wid.setText(sum_)
        else: #if not month -> clear
            for wids in self.__data_labels:
                for wid in wids:
                    wid.setText('')
            for wid in self.__sum_labels:
                wid.setText('')
    
    def __set_stat_type(self):
        try:
            self.tabStatM.cbMonth.currentTextChanged.disconnect()
        except:
            pass
        
        grids=(self.tabStatM.glCurrent, self.tabStatM.glIncome, self.tabStatM.glOutcome, self.tabStatM.glMove)
        for grid in grids:
            for k in reversed(range(grid.count())):
                wid=grid.itemAt(k).widget()
                if not wid.objectName():
                    wid.deleteLater()
        
        data=self.__data.get_data()
        
        src_no = self.__data.sources .get_no()
        in_no  = self.__data.in_type .get_no()
        out_no = self.__data.out_type.get_no()
        
        src_txt = self.__data.sources .get_txt()
        in_txt  = self.__data.in_type .get_txt()
        out_txt = self.__data.out_type.get_txt()
        
        is_cash = self.__data.sources .get_chk_no()
        is_ness = self.__data.out_type.get_chk_no()
        
        self.__stat.set_type(src_no,in_no,out_no,is_cash,is_ness)
        self.__stat.set_data(data)
        
        #generate stat labels
        self.tabStatM.lbTitleIncomeS  = []
        self.tabStatM.lbTitleOutcomeS = []
        self.tabStatM.lbTitleCurrent  = []
        self.tabStatM.lbTitleMoveIn   = []
        self.tabStatM.lbTitleMoveOut  = []
        
        self.tabStatM.lbDataIncomeS   = []
        self.tabStatM.lbDataOutcomeS  = []
        self.tabStatM.lbDataCurrent   = []
        self.tabStatM.lbDataMoveIn    = []
        self.tabStatM.lbDataMoveOut   = []
        
        self.tabStatM.lbTitleIncomeT  = []
        self.tabStatM.lbDataIncomeT   = []
        
        self.tabStatM.lbTitleOutcomeT = []
        self.tabStatM.lbDataOutcomeT  = []
        
        self.__title_labels=(
            self.tabStatM.lbTitleCurrent ,
            self.tabStatM.lbTitleIncomeS ,
            self.tabStatM.lbTitleOutcomeS,
            self.tabStatM.lbTitleIncomeT ,
            self.tabStatM.lbTitleOutcomeT,
            self.tabStatM.lbTitleMoveIn  ,
            self.tabStatM.lbTitleMoveOut 
        )
        self.__data_labels=(
            self.tabStatM.lbDataCurrent ,
            self.tabStatM.lbDataIncomeS ,
            self.tabStatM.lbDataOutcomeS,
            self.tabStatM.lbDataIncomeT ,
            self.tabStatM.lbDataOutcomeT,
            self.tabStatM.lbDataMoveIn  ,
            self.tabStatM.lbDataMoveOut
        )
        self.__sum_labels=(
            self.tabStatM.lbSumIncome ,
            self.tabStatM.lbSumOutcome,
            self.tabStatM.lbSumCurrent,
            self.tabStatM.lbSumCash   ,
            self.tabStatM.lbSumMove   ,
            self.tabStatM.lbNet       ,
            self.tabStatM.lbOut1      ,
            self.tabStatM.lbOut2
        )
        
        
        for k,txt in enumerate(src_txt):
            lbTitleIncome  = QLabel(txt,self.tabStatM.gbIncome)
            lbTitleOutcome = QLabel(txt,self.tabStatM.gbOutcome)
            lbTitleCurrent = QLabel(txt,self.tabStatM.gbCurrent)
            lbTitleMoveIn  = QLabel(txt,self.tabStatM.gbMove)
            lbTitleMoveOut = QLabel(txt,self.tabStatM.gbMove)
            
            lbTitleIncome .setAlignment(Qt.AlignCenter)
            lbTitleOutcome.setAlignment(Qt.AlignCenter)
            lbTitleCurrent.setAlignment(Qt.AlignCenter)
            lbTitleMoveIn .setAlignment(Qt.AlignCenter)
            lbTitleMoveOut.setAlignment(Qt.AlignCenter)
            
            self.tabStatM.lbTitleIncomeS .append(lbTitleIncome)
            self.tabStatM.lbTitleOutcomeS.append(lbTitleOutcome)
            self.tabStatM.lbTitleCurrent .append(lbTitleCurrent)
            self.tabStatM.lbTitleMoveIn  .append(lbTitleMoveIn)
            self.tabStatM.lbTitleMoveOut .append(lbTitleMoveOut)
            
            self.tabStatM.glIncome .addWidget(lbTitleIncome ,k+2,2,1,1)
            self.tabStatM.glOutcome.addWidget(lbTitleOutcome,k+2,2,1,1)
            self.tabStatM.glCurrent.addWidget(lbTitleCurrent,k+2,0,1,1)
            self.tabStatM.glMove   .addWidget(lbTitleMoveIn ,k+2,0,1,1)
            self.tabStatM.glMove   .addWidget(lbTitleMoveOut,k+2,2,1,1)
            
            lbDataIncome  = QLabel(self.tabStatM.gbIncome)
            lbDataOutcome = QLabel(self.tabStatM.gbOutcome)
            lbDataCurrent = QLabel(self.tabStatM.gbCurrent)
            lbDataMoveOut = QLabel(self.tabStatM.gbMove)
            lbDataMoveIn  = QLabel(self.tabStatM.gbMove)
            
            lbDataIncome .setAlignment(Qt.AlignCenter)
            lbDataOutcome.setAlignment(Qt.AlignCenter)
            lbDataCurrent.setAlignment(Qt.AlignCenter)
            lbDataMoveOut.setAlignment(Qt.AlignCenter)
            lbDataMoveIn .setAlignment(Qt.AlignCenter)
            
            self.tabStatM.lbDataIncomeS .append(lbDataIncome)
            self.tabStatM.lbDataOutcomeS.append(lbDataOutcome)
            self.tabStatM.lbDataCurrent .append(lbDataCurrent)
            self.tabStatM.lbDataMoveOut .append(lbDataMoveOut)
            self.tabStatM.lbDataMoveIn  .append(lbDataMoveIn)
            
            self.tabStatM.glIncome .addWidget(lbDataIncome ,k+2,3,1,1)
            self.tabStatM.glOutcome.addWidget(lbDataOutcome,k+2,3,1,1)
            self.tabStatM.glCurrent.addWidget(lbDataCurrent,k+2,1,1,1)
            self.tabStatM.glMove   .addWidget(lbDataMoveOut,k+2,1,1,1)
            self.tabStatM.glMove   .addWidget(lbDataMoveIn ,k+2,3,1,1)
        
        for k,txt in enumerate(in_txt):
            lbTitleIncome = QLabel(txt,self.tabStatM.gbIncome)
            lbTitleIncome.setAlignment(Qt.AlignCenter)
            self.tabStatM.lbTitleIncomeT.append(lbTitleIncome)
            self.tabStatM.glIncome.addWidget(lbTitleIncome,k+2,0,1,1)
            
            lbDataIncome = QLabel(self.tabStatM.gbIncome)
            lbDataIncome.setAlignment(Qt.AlignCenter)
            self.tabStatM.lbDataIncomeT.append(lbDataIncome)
            self.tabStatM.glIncome.addWidget(lbDataIncome,k+2,1,1,1)
        
        for k,txt in enumerate(out_txt):
            lbTitleOutcome = QLabel(txt,self.tabStatM.gbOutcome)
            lbTitleOutcome.setAlignment(Qt.AlignCenter)
            self.tabStatM.lbTitleOutcomeT.append(lbTitleOutcome)
            self.tabStatM.glOutcome.addWidget(lbTitleOutcome,k+2,0,1,1)
            
            lbDataOutcome = QLabel(self.tabStatM.gbOutcome)
            lbDataOutcome.setAlignment(Qt.AlignCenter)
            self.tabStatM.lbDataOutcomeT.append(lbDataOutcome)
            self.tabStatM.glOutcome.addWidget(lbDataOutcome,k+2,1,1,1)
        
        for wid in self.__sum_labels:
            wid.setText('')
        
        self.tabStatM.cbMonth.currentTextChanged.connect(self.__set_month)
    
    def __add_source(self):
        checked = bool(self.tabCate.gbSrc.chk.checkState())
        self.__data.sources.add_data(checked,self.tabCate.gbSrc.lnAdd.text())
        
        self.__saved=False
        self.__set_stat_type()
    
    def __del_source(self):
        self.__data.sources.del_at(self.tabCate.gbSrc.cbDel.currentIndex())
        
        self.__saved=False
        self.__set_stat_type()
    
    def __add_in(self):
        self.__data.in_type.add_data(self.tabCate.gbIn.lnAdd.text())
        
        self.__saved=False
        self.__set_stat_type()
    
    def __del_in(self):
        self.__data.in_type.del_at(self.tabCate.gbIn.cbDel.currentIndex())
        
        self.__saved=False
        self.__set_stat_type()
    
    def __add_out(self):
        checked = bool(self.tabCate.gbOut.chk.checkState())
        self.__data.out_type.add_data(checked,self.tabCate.gbOut.lnAdd.text())
        
        self.__saved=False
        self.__set_stat_type()
    
    def __del_out(self):
        self.__data.out_type.del_at(self.tabCate.gbOut.cbDel.currentIndex())
        
        self.__saved=False
        self.__set_stat_type()
    
    def __set_type(self,index):
        if index==2:
            self.tabData.lbDetail.setText('이동처')
        else:
            self.tabData.lbDetail.setText('상세')
        
        self.tabData.cbDetail.setModel(self.__data.list_detail[index])
    
    def __change_ord(self):
        self.__saved=False
        self.__set_stat_type()
        
    def __load_as(self):
        if not self.__saved:
            response=QMessageBox.warning(
                self,'불러오기','저장하시겠습니까?',
                QMessageBox.Save|QMessageBox.Discard|QMessageBox.Cancel
            )
            if response==QMessageBox.Save:
                self.__save()
            elif response==QMessageBox.Cancel:
                return
        
        path=QFileDialog.getOpenFileName(self,'불러오기',filter=self.__file_type)[0]
        if path:
            self.__load(path)
    
    def __load(self,file_path):
        while True:
            try:
                with open(file_path,'r',encoding='utf-8') as file:
                    data=json.load(file)
                
                if data['version']==1:
                    for name in ('sources','in_type','out_type'):
                        data[name]=list((int(n),t) for n,t in data[name].items())
                    data['version']=2
                
                self.__data.load_data(data)
                
                self.__set_stat_type()
            except:
                msgbox=QMessageBox(
                    QMessageBox.Warning,'재시도',
                    f"{'불러오는 중 오류 발생: 재시도?':70}",
                    QMessageBox.Retry|QMessageBox.Abort,
                    self
                )
                msgbox.setDetailedText(traceback.format_exc())
                response=msgbox.exec_()
                if response==QMessageBox.Abort:
                    break
            else:
                self.__last_file=file_path
                self.__saved=True
                self.__resize()
                break
    
    def __save_as(self):
        path=QFileDialog.getSaveFileName(self,'저장',filter=self.__file_type)[0]
        if path:
            self.__save(path)
    
    def __save(self,file_path=''):
        if not file_path:
            if self.__last_file:
                file_path=self.__last_file
            else:
                self.__save_as()
                return
        
        while True:
            try:
                data=self.__data.save_data()
                with open(file_path,'w',encoding='utf-8') as file:
                    json.dump(data,file,ensure_ascii=False,indent=4)
            except:
                msgbox=QMessageBox(
                    QMessageBox.Warning,'재시도',
                    f"{'저장하는 중 오류 발생: 재시도?':70}",
                    QMessageBox.Retry|QMessageBox.Abort,
                    self
                )
                msgbox.setDetailedText(traceback.format_exc())
                response=msgbox.exec_()
                if response==QMessageBox.Abort:
                    break
            else:
                self.__last_file=file_path
                self.__saved=True
                break
    
    def __import_as(self,path):
        file_path,type_=QFileDialog.getOpenFileName(self,'가져오기',filter=self.__export_type)
        
        if file_path:
            type_path,_=QFileDialog.getOpenFileName(self,'범례 파일 선택',filter='범례 파일(*.json)')
            type_=self.__export_text.index(type_)
            
            if type_path:
                while True:
                    try:
                        self.__data.import_data(type_,file_path,type_path)
                    except:
                        msgbox=QMessageBox(
                            QMessageBox.Warning,'재시도',
                            f"{'가져오는 중 오류 발생: 재시도?':70}",
                            QMessageBox.Retry|QMessageBox.Abort,
                            self
                        )
                        msgbox.setDetailedText(traceback.format_exc())
                        response=msgbox.exec_()
                        if response==QMessageBox.Abort:
                            break
                    else:
                        break
    
    def __export_as(self,path):
        file_path,type_=QFileDialog.getSaveFileName(self,'내보내기',filter=self.__export_type)
        
        if file_path:
            type_path,_=QFileDialog.getOpenFileName(self,'범례 파일 선택',filter='범례 파일(*.json)')
            type_=self.__export_text.index(type_)
            
            if type_path:
                while True:
                    try:
                        self.__data.export_data(type_,file_path,type_path)
                    except:
                        msgbox=QMessageBox(
                            QMessageBox.Warning,'재시도',
                            f"{'내보내는 중 오류 발생: 재시도?':70}",
                            QMessageBox.Retry|QMessageBox.Abort,
                            self
                        )
                        msgbox.setDetailedText(traceback.format_exc())
                        response=msgbox.exec_()
                        if response==QMessageBox.Abort:
                            break
                    else:
                        break
    
    def __save_config(self):
        if not os.path.isdir(CONFIG_DIR):
            os.mkdir(CONFIG_DIR)
        
        with open(CONFIG_FILE,'w') as file:
            file.write('\n'.join((
                self.__last_file         ,
                self.__login_win.username,
                self.__login_win.password
            )))
    
    def closeEvent(self,event):
        if self.__saved:
            self.__save_config()
            event.accept()
        else:
            response=QMessageBox.warning(
                self,'종료','저장하시겠습니까?',
                QMessageBox.Save|QMessageBox.Discard|QMessageBox.Cancel
            )
            if response==QMessageBox.Cancel:
                event.ignore()
            else:
                if response==QMessageBox.Save:
                    self.__save()
                self.__save_config()
                event.accept()


if __name__=='__main__':
    import argparse
    
    parser=argparse.ArgumentParser()
    
    parser.add_argument('file_name',help='Path of file',nargs='?',default='')
    
    args=parser.parse_args()
    
    
    app=QApplication()
    
    main_win=MainWin(args.file_name)
    main_win.show()
    
    app.exec_()
