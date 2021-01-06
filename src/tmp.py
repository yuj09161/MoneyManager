class ComboData(QStandardItemModel):
    def __init__(self,parent=None):
        super().__init__(0,0,parent)
        
        self._data=[]
        
        self.dataChanged.connect(self.change_order)
    
    def get_no_txt(self):
        return {n:t for n,t in self._data}
    
    def get_no_index(self):
        return {n:i in i,(n,t) in enumerate(self._data)}
    
    def get_txt_no(self):
        return {t:n for n,t in self._data}
    
    def get_txt_index(self):
        return {t:i in i,(n,t) in enumerate(self._data)}
    
    def get_index_no(self):
        return {i:n in i,(n,t) in enumerate(self._data)}
    
    def get_index_txt(self):
        return {i:t in i,(n,t) in enumerate(self._data)}
    
    def get_raw(self):
        return self._data
    
    def add_data(self,data):
        self._data.append((max(x for x,_ in self._data),data))
        self.insertRow(QStandardItem(data))
    
    def set_data(self,datas):
        self._data=datas
        self.clear()
        for data in datas:
            self.insertRow(QStandardItem(data))
    
    def del_no(self,no):
        self.del_index(self.get_no_index()[no])
    
    def del_index(self,index):
        del self._data[index]
        self.removeRow(index)
    
    def change_order(self):
        if not self.__changing:
            items = []
            for k in range(self.rowCount()):
                items.append(self.item(k).text())
            self._data.sort(key=lambda x: items.index(x[0]))


class ComboDataChk(ComboData):
    def __init__(self,*args):
        super().__init__(*args)
    
    def get_chk(self):
        res=[]
        for item in self._types:
            res.append(item.startswith('* '))
        return res
    
    def add_data(self,chk,data):
        prefix = '* ' if chk else ''
        super().add_data(prefix+data)
