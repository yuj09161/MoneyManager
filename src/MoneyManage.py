# -*- coding: utf-8 -*-

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from UI import *

import numpy as np
import os,sys,json,time,datetime,traceback


STD_DAY=730120


class NotInitalizedError(Exception):
    pass


class ComboData(QStandardItemModel):
    def __init__(self,parent=None):
        super().__init__(0,0,parent)
        self.__data=[]
    
    def get_data(self):
        return self.__data
    
    def set_data(self,datas):
        self.clear()
        for data in datas:
            self.appendRow(QStandardItem(data))
        self.__data=datas
    
    def add_data(self,data):
        self.appendRow(QStandardItem(data))
        self.__data.append(data)
    
    def get_at(self,k):
        return self.__data[k]
    
    def set_at(self,k,data):
        self.setItem(k,QStandardItem(data))
        self.__data[k]=data
    
    def del_at(self,k):
        self.removeRow(k)
        del self.__data[k]


class Data(QStandardItemModel):
    __header_text = ('일시', '구분', '원천', '상세/이동처', '금액', '설명')
    __type_text   = ('수입','지출','이동','초기')
    __data_form   = [
        ('date', 'uint16'), ('type', 'int8'  ), ('src' , 'uint8'),
        ('det' , 'uint8' ), ('val' , 'uint32'), ('desc', '<U64' )
    ]
    __data_name   = ('date', 'type', 'src', 'det', 'val', 'desc')
    
    __qitem_vec   = np.vectorize(lambda x: QStandardItem(str(x)))
    
    __parse_date  = lambda x: datetime.date.fromordinal(x+STD_DAY).isoformat()
    __parse_vdate = np.vectorize(__parse_date)
    
    __empty_arr   = np.array((0,0,0,0,0,''), __data_form)
    
    column_count=len(__header_text)
    
    def __init__(self,parent):
        super().__init__(0,0,parent)
        self.setHorizontalHeaderLabels(self.__header_text)
        
        self.__parse_vdet  = np.vectorize(self.__parse_det)
        
        self.__version    = 1
        
        self.type     = ComboData()
        self.sources  = ComboData()
        self.in_type  = ComboData()
        self.out_type = ComboData()
        
        self.list_detail = (self.in_type, self.out_type, self.sources)
        
        self.__data = np.empty((10000,), self.__data_form)
        
        self.type.set_data(self.__type_text[:-1])
        
        self.row_count=0
    
    def __unpacker(self,data):
        self.clear()
        
        self.__version = data['version']
        
        self.sources.set_data(data['sources'])
        self.in_type.set_data(data['in_type'])
        self.out_type.set_data(data['out_type'])
        
        self.__row_count=len(data['data'])
        if self.__row_count>10000:
            raise ValueError('Too much data: Please contact to developer')
        else:
            raw_data=list(map(tuple,data['data']))
            self.__data = np.asarray(raw_data,self.__data_form)
        
        #parse data & set data
        self.__tmp_src_txt = data['sources']
        self.__tmp_in_txt  = data['in_type']
        self.__tmp_out_txt = data['out_type']
        
        #date
        dates=self.__data['date']
        dates=self.__parse_vdate(dates)
        self.appendColumn(self.__qitem_vec(dates).tolist())
        
        #type&det
        types=self.__data['type'] #.astype('<U4')
        dets=self.__data['det']
        types,dets=self.__parse_vdet(types,dets)
        for k,txt in enumerate(self.__type_text):
            types[types==str(k)]=txt
        self.appendColumn(self.__qitem_vec(types).tolist())
        
        #src
        srcs=self.__data['src'].astype('<U8')
        for k,txt in enumerate(self.__tmp_src_txt):
            srcs[srcs==str(k)]=txt
        self.appendColumn(self.__qitem_vec(srcs).tolist())
        
        #det&val&desc (append)
        self.appendColumn(self.__qitem_vec(dets).tolist())
        self.appendColumn(self.__qitem_vec(self.__data['val'].astype('<U10')).tolist())
        self.appendColumn(self.__qitem_vec(self.__data['desc']).tolist())
        #end parser
        
        self.setHorizontalHeaderLabels(self.__header_text)
            
        if self.__row_count<10000:
            self.__data=np.append(
                np.asarray(raw_data                 , self.__data_form),
                np.empty  ((10000-self.__row_count,), self.__data_form)
            )
    
    def __packer(self):
        data={}
        
        data['version'] = self.__version
        
        data['sources']  = self.sources.get_data()
        data['in_type']  = self.in_type.get_data()
        data['out_type'] = self.out_type.get_data()
        
        data['data'] = self.__data[:self.row_count].tolist()
        
        return data
    
    def load_data(self,file_path):
        with open(file_path,'r',encoding='utf-8') as file:
            data=json.load(file)
        
        self.__unpacker(data)
    
    def save_data(self,file_path):
        data=self.__packer()
        
        with open(file_path,'w',encoding='utf-8') as file:
            json.dump(data,file,ensure_ascii=False,indent=4)
    
    def import_data(self,file_type,file_path,type_path,*,encoding='utf-8'):
        data={}
        with open(file_path,'r',encoding=encoding) as file:
            raw_data=file.readlines()
        
        data['version']  = self.__version
        
        with open(type_path,'r',encoding=encoding) as file:
            types=json.load(file)
        
        sources  = data['sources']  = types['sources']
        in_type  = data['in_type']  = types['in_type']
        out_type = data['out_type'] = types['out_type']
        
        if file_type==0: #tsv
            data['data']=self.__tsv_parser(raw_data,sources,in_type,out_type)
        elif file_type==1: #txt
            pass
        else:
            raise ValueError(f'Wrong file_type no: {file_type}')
        
        self.__unpacker(data)
    
    def export_data(self,file_type,file_path,type_path='',*,encoding='utf-8'):
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
            types['sources']  = data['sources']
            types['in_type']  = data['in_type']
            types['out_type'] = data['out_type']
            with open(type_path,'w',encoding=encoding) as file:
                json.dump(types,file)
    
    #parser
    def __parse_det(self,type_,data):
        parsed_type=self.__type_text[type_]
        
        if type_==0:
            parsed_data=self.__tmp_in_txt[data]
        elif type_==1:
            parsed_data=self.__tmp_out_txt[data]
        elif type_==2:
            parsed_data=self.__tmp_src_txt[data]
        elif type_==3:
            parsed_data='-'
        else:
            raise ValueError
        
        return parsed_type,parsed_data
    
    def __tsv_parser(self,raw_data,sources,in_type,out_type):
        def parse13(row1,row3):
            res1=self.__type_text.index(row1)
            
            if res1==0:
                res3=in_type.index(row3)
            elif res1==1:
                res3=out_type.index(row3)
            elif res1==2:
                res3=sources.index(row3)
            elif res1==4:
                res3=0
            else:
                raise ValueError
            
            return res1,res3
        
        parse0 = lambda x: datetime.date.fromisoformat(x).toordinal()-STD_DAY
        parse2 = lambda x: sources.index(x) if x else 0
        
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
    def add_data(self,date,type_,src,det,val,desc):
        try:
            type_=self.__type_text.index(type_)
            src_txt=self.sources.get_data()
            
            if type_==0:
                det=self.in_type.get_data().index(det)
            elif type_==1:
                det=self.out_type.get_data().index(det)
            elif type_==2:
                det=src_txt.index(det)
            else:
                raise ValueError
            
            parsed_data=(
                datetime.date.fromisoformat(date).toordinal()-STD_DAY,
                type_,
                src_txt.index(src),
                det,
                val,
                desc
            )
        except:
            raise ValueError('Tried to add data with wrong arguments')
        else:
            self.appendRow(self.__qitem_vec((date,type_,src,det,val,desc)).tolist())
            self.__data[self.row_count]=parsed_data
            
            self.row_count+=1
    
    def del_data(self,row_no):
        self.removeRow(row_no)
        self.__data=np.append(np.delete(self.__data,row_no),self.__empty_arr)
        self.row_count-=1
    
    def get_data(self):
        sources  = self.sources .get_data()
        in_type  = self.in_type .get_data()
        out_type = self.out_type.get_data()
        
        return self.__data,sources,in_type,out_type


class Stat_Data(QStandardItemModel):
    __header_text = (
        '연월'   , '총 재산', '현금성',
        '순 수익', '수입'   , '지출'  , '이동액'
    )
    __data_name = (
        'year',  'month',  'current',
        'income_src',  'outcome_src',
        'income_typ',  'outcome_typ',
        'move_in'   ,     'move_out',
    )
    __type_col  = ('income_src', 'outcome_src')
    column_count=len(__header_text)
    
    __qitem_vec = np.vectorize(lambda x: QStandardItem(str(x)))
    
    def __init__(self,parent=None):
        super().__init__(0,0,parent=None)
        self.setHorizontalHeaderLabels(self.__header_text)
        
        self.months=ComboData()
        
        self.__initalized=False
    
    @property
    def initalized(self):
        return self.__initalized
    
    def set_type(self,sources,in_type,out_type):
        self.__sources  = sources
        self.__in_type  = in_type
        self.__out_type = out_type
        self.__len = (len(sources), len(in_type), len(out_type))
        #print('\n'.join(map(str,(sources, in_type, out_type))))
        
        self.__data_form = [
            ('year' , 'uint16'),    ('month' , 'uint8'),    ('current', 'int32' , (self.__len[0],)),
            ('income_src', 'int32', (self.__len[0],)), ('outcome_src', 'int32', (self.__len[0],)),
            ('income_typ', 'int32', (self.__len[1],)), ('outcome_typ', 'int32', (self.__len[2],)),
            ('move_in'   , 'int32', (self.__len[0],)), ('move_out'   , 'int32', (self.__len[0],))
        ]
        self.__empty_arr = np.zeros((1,), self.__data_form)
        
        self.__initalized=True
    
    def get_data(self):
        return self.__data
    
    def set_data(self,data):
        if self.__initalized:
            first_date = datetime.date.fromordinal(data['date'].min()+STD_DAY)
            last_date  = datetime.date.fromordinal(data['date'].max()+STD_DAY)
            first_y,first_m = first_date.year,first_date.month
            last_y ,last_m  = last_date.year ,last_date.month
            
            months=[]
            for m in range(first_m,13):
                months.append((first_y,m))
            for y in range(first_y+1,last_y):
                for m in range(1,13):
                    months.append((y,m))
            for m in range(1,last_m+1):
                months.append((last_y,m))
            l=len(months)
            
            self.__data = np.zeros((l,), self.__data_form)
            #print(self.__data.shape,self.__data[10])
            
            #last_month = self.__empty_arr.copy()
            #print(self.__data_form)
            for k,(y,m) in enumerate(months):
                self.__data[k]['year']  = y
                self.__data[k]['month'] = m
                
                if m==12:
                    next_m=(y+1,1)
                else:
                    next_m=(y,m+1)
                
                first_date_m = datetime.date(y,  m  ,1).toordinal()-STD_DAY
                last_date_m  = datetime.date(*next_m,1).toordinal()-STD_DAY
                month_data=data[(data['date']>=first_date_m)&(data['date']<last_date_m)]
                #print(k,y,m,first_date_m,last_date_m,month_data)
                
                if month_data.size:
                    for t in range(2):
                        for s in range(self.__len[0]):
                            type_sum=month_data[(month_data['type']==t)&(month_data['src']==s)]['val'].sum()
                            #print(t,s,type_sum)
                            self.__data[k][self.__type_col[t]][s]=type_sum
                    
                    for d in range(self.__len[1]):
                        type_sum=month_data[(month_data['type']==0)&(month_data['det']==d)]['val'].sum()
                        #print(0,d,type_sum)
                        self.__data[k]['income_typ'][d]=type_sum
                    #print(self.__data[k]['income_typ'],self.__data[k][5])
                    
                    for d in range(self.__len[2]):
                        type_sum=month_data[(month_data['type']==1)&(month_data['det']==d)]['val'].sum()
                        #print(1,d,type_sum)
                        self.__data[k]['outcome_typ'][d]=type_sum
                    
                    for s1 in range(self.__len[0]):
                        type_sum=month_data[(month_data['type']==2)&(month_data['src']==s1)]['val'].sum()
                        #print(2,s1,type_sum)
                        self.__data[k]['move_in'][s1]=type_sum
                    
                    for s2 in range(self.__len[0]):
                        type_sum=month_data[(month_data['type']==2)&(month_data['det']==s2)]['val'].sum()
                        #print(2,s2,type_sum)
                        self.__data[k]['move_out'][s2]=type_sum
                    
                    #초기금
                    first_val=month_data[(month_data['type']==3)]['val'].sum()
                    #print(3,0,first_val)
                        
                    if k==0:
                        last_month=self.__empty_arr[0]
                    else:
                        last_month=self.__data[k-1]
                    d_c=self.__data[k]
                    
                    for s in range(self.__len[0]):
                        sum_=(
                            d_c['income_src'][s]     +\
                            d_c['move_in'][s]        -\
                            d_c['outcome_src'][s]    -\
                            d_c['move_out'][s]       +\
                            last_month['current'][s] +\
                            first_val
                        )
                        d_c['current'][s]=sum_
                    
                    c0 = d_c[0].sum() #year
                    c1 = d_c[1].sum() #month
                    c2 = d_c[2].sum() #current
                    c3 = d_c[3].sum() #income_src
                    c4 = d_c[4].sum() #outcome_src
                    c5 = d_c[5].sum() #income_typ
                    c6 = d_c[6].sum() #outcome_typ
                    c7 = d_c[7].sum() #move_in
                    c8 = d_c[8].sum() #move_out
                    
                    #print(d_c)
                    #print(c0,c1,c7,c8)
                    
                    if c3!=c5 or c4!=c6 or c7!=c8:
                        raise ValueError
                    else:
                        tmp_data=self.__qitem_vec((f'{y}-{m}',c2,'',c3-c4,c3,c4,c7)).tolist()
                        #print(tmp_data)
                        self.appendRow(tmp_data)
            
            #print(self.__data)
        else:
            raise NotInitalizedError
    

class MainWin(QMainWindow,Ui_MainWin):
    __type_text = (
        'Excel 호환(*.tsv)',
        '텍스트 파일(*.txt)'
    )
    __export_type = (';;'.join(__type_text))
    
    def __init__(self,file_name):
        super().__init__()
        self.setupUi(self)
        
        self.__saved=True
        self.__last_file=''
        
        self.__data=Data(self.tabData.treeData)
        self.__stat=Stat_Data(self.tabStatS.treeStatS)
        
        if file_name:
            self.__load(file_name)
        
        self.acLoad  .triggered.connect(self.__load_as)
        self.acSave  .triggered.connect(self.__save)
        self.acSaveAs.triggered.connect(self.__save_as)
        self.acImport.triggered.connect(self.__import_as)
        self.acExport.triggered.connect(self.__export_as)
        self.acExit  .triggered.connect(self.close)
        
        #self.acOpenLicense.triggered.connect(self.__show_open)
        #self.acLicense.triggered.connect(self.__show_license)
        #self.acInfo.triggered.connect(self.__show_info)
        
        
        self.tabCate.gbSrc.cbDel.setModel(self.__data.sources)
        self.tabCate.gbIn .cbDel.setModel(self.__data.in_type)
        self.tabCate.gbOut.cbDel.setModel(self.__data.out_type)
        
        self.tabCate.gbSrc.btnAdd.clicked.connect(self.__add_source)
        self.tabCate.gbSrc.btnDel.clicked.connect(self.__del_source)
        self.tabCate.gbIn .btnAdd.clicked.connect(self.__add_in)
        self.tabCate.gbIn .btnDel.clicked.connect(self.__del_in)
        self.tabCate.gbOut.btnAdd.clicked.connect(self.__add_out)
        self.tabCate.gbOut.btnDel.clicked.connect(self.__del_out)
        
        
        self.tabData.treeData.setModel(self.__data)
        
        self.tabData.cbType  .setModel(self.__data.type)
        self.tabData.cbSrc   .setModel(self.__data.sources)
        self.tabData.cbDetail.setModel(self.__data.in_type)
        
        self.tabData.cbType.currentIndexChanged.connect(self.__set_type)
        
        self.tabData.treeData.doubleClicked.connect(self.__del_data)
        self.tabData.btnAddData.clicked.connect(self.__add_data)
        
        
        self.tabStatS.treeStatS.setModel(self.__stat)
        
        
        self.tabStatM.cbMonth.setModel(self.__stat.months)
        
        
        self.__resize()
    
    def __resize(self):
        for k in range(0,self.__data.column_count):
            self.tabData.treeData.resizeColumnToContents(k)
        
        for k in range(0,self.__stat.column_count):
            self.tabStatS.treeStatS.resizeColumnToContents(k)
    
    def __add_data(self):
        try:
            date   = self.tabData.lnDate.text()
            type_  = self.tabData.cbType.currentText()
            src    = self.tabData.cbSrc.currentText()
            detail = self.tabData.cbDetail.currentText()
            cost   = self.tabData.lnCost.text()
            desc   = self.tabData.lnDetail.text()
            
            self.__data.add_data(date,type_,src,detail,cost,desc)
        except:
            QMessageBox.warning(None,'경고','잘못된 입력')
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
        self.__data.del_data(data_no.row())
        self.__resize()
        
    def __load_as(self):
        path=QFileDialog.getOpenFileName(self,'불러오기')[0]
        if path:
            self.__load(path)
    
    def __load(self,path):
        if not path:
            if self.__last_file:
                path=self.__last_file
            else:
                self.__load_as()
                return
        
        while True:
            try:
                self.__data.load_data(path)
                
                data,sources,in_type,out_type=self.__data.get_data()
                self.__stat.set_type(sources,in_type,out_type)
                self.__stat.set_data(data)
            except:
                print(traceback.format_exc())
                response=QMessageBox.question(self,'재시도','불러오는 중 오류 발생\n재시도?',QMessageBox.Retry|QMessageBox.Cancel)
                if response==QMessageBox.Cancel:
                    #break
                    sys.exit()
            else:
                self.__last_file=path
                self.__saved=True
                self.__resize()
                break
    
    def __save_as(self):
        path=QFileDialog.getSaveFileName(self,'저장')[0]
        if path:
            self.__save(path)
    
    def __save(self,path=''):
        if not path:
            if self.__last_file:
                path=self.__last_file
            else:
                self.__save_as()
                return
        
        while True:
            try:
                self.__data.save_data(path)
            except:
                print(traceback.format_exc())
                response=QMessageBox.question(self,'재시도','저장하는 중 오류 발생\n재시도?',QMessageBox.Retry|QMessageBox.Cancel)
                if response==QMessageBox.Cancel:
                    break
            else:
                self.__last_file=path
                self.__saved=True
                break
    
    def __import_as(self,path):
        file_path,type_=QFileDialog.getOpenFileName(self,'가져오기',filter=self.__export_type)
        type_path,_=QFileDialog.getOpenFileName(self,'범례 파일 선택',filter='범례 파일(*.json)')
        type_=self.__type_text.index(type_)
        
        if file_path and type_path:
            while True:
                try:
                    self.__data.import_data(type_,file_path,type_path)
                except:
                    print(traceback.format_exc())
                    response=QMessageBox.question(self,'재시도','가져오는 중 오류 발생\n재시도?',QMessageBox.Retry|QMessageBox.Cancel)
                    if response==QMessageBox.Cancel:
                        break
                else:
                    break
    
    def __export_as(self,path):
        file_path,type_=QFileDialog.getSaveFileName(self,'내보내기',filter=self.__export_type)
        type_path,_=QFileDialog.getOpenFileName(self,'범례 파일 선택',filter='범례 파일(*.json)')
        type_=self.__type_text.index(type_)
        
        if file_path and type_path:
            while True:
                try:
                    self.__data.export_data(type_,file_path,type_path)
                except:
                    print(traceback.format_exc())
                    response=QMessageBox.question(self,'재시도','내보내는 중 오류 발생\n재시도?',QMessageBox.Retry|QMessageBox.Cancel)
                    if response==QMessageBox.Cancel:
                        break
                else:
                    break
    
    def __add_source(self):
        self.__data.sources.add_data(self.tabCate.gbSrc.lnAdd.text())
    
    def __del_source(self):
        self.__data.sources.del_at(self.tabCate.gbSrc.cbDel.currentIndex())
    
    def __add_in(self):
        self.__data.in_type.add_data(self.tabCate.gbIn.lnAdd.text())
    
    def __del_in(self):
        self.__data.in_type.del_at(self.tabCate.gbIn.cbDel.currentIndex())
    
    def __add_out(self):
        self.__data.out_type.add_data(self.tabCate.gbOut.lnAdd.text())
    
    def __del_out(self):
        self.__data.out_type.del_at(self.tabCate.gbOut.cbDel.currentIndex())
    
    def __set_type(self,index):
        if index==2:
            self.tabData.lbDetail.setText('이동처')
        else:
            self.tabData.lbDetail.setText('상세')
        
        self.tabData.cbDetail.setModel(self.__data.list_detail[index])
    
    def closeEvent(self,event):
        if self.__saved:
            event.accept()
        else:
            response=QMessageBox.question(self,'종료','종료하시겠습니까?')
            if response==QMessageBox.Yes:
                event.accept()
            else:
                event.ignore()


if __name__=='__main__':
    import argparse
    
    parser=argparse.ArgumentParser()
    
    parser.add_argument('file_name',help='Path of file',nargs='?',default='')
    
    args=parser.parse_args()
    
    
    app=QApplication()
    
    main_win=MainWin(args.file_name)
    main_win.show()
    
    app.exec_()
