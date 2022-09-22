'''
Class for log, which is made by Jinkeun Han
'''

from typing import Any

class LogCompareException(Exception):
    '''
    Used to raise exception when compare different log
    in this case, compare log's name
    '''
    def __str__(self):
        return "can't comapre, not same log"

class LogClass:
    '''
    Class for log. To get contents of log in <list> type, use contents is
    or to get in <str> type, use "str(instance)"
    '''
    __contents:list = []
    __name:str = ""

    def __init__(self, name:str):
        self.name_is = name

    @property
    def contents_is(self)->list:
        '''
        get contents as list[str]
        '''
        return self.__contents

    @contents_is.setter
    def contents_is(self, value:list):
        '''
        set log's contents. It is type<list>'
        '''
        self.__contents = value

    @property
    def name_is(self):
        '''
        get log's name. It is type<str>'
        '''
        return self.__name

    @name_is.setter
    def name_is(self, name:str):
        '''
        set log's name. It is type<str>'
        '''
        self.__name = name

    def update(self, value:Any)->None:
        '''
        update log by adding value.
        '''
        if isinstance(value, list):
            self.contents_is += value
        elif isinstance(value, str):
            self.contents_is += value.split('\n')
        elif isinstance(value, LogClass):
            self.contents_is += value.contents_is
        else:
            self.contents_is.append(str(value))

    def find(self, target:str):
        '''
        find target sentence in log's contents in reverse order.
        If find target, return its index in list (from 0 to len of log)
        else return -1
        '''
        length = len(self)-1
        for num in range(length, -1, -1):
            sentence:Any = self.contents_is[num]
            if str(sentence).find(target) >-1:
                return num
        return -1

    def __eq__(self, other):
        return self.name_is == other.name_is

    def __ne__(self, other):
        return self.name_is != other.name_is

    def __gt__(self, other):
        if self != other:
            raise LogCompareException()
        return len(self.contents_is)>len(other.contents_is)

    def __ge__(self, other):
        if self != other:
            raise LogCompareException()
        return len(self.contents_is)>=len(other.contents_is)

    def __lt__(self, other):
        if self != other:
            raise LogCompareException()
        return len(self.contents_is)<len(other.contents_is)

    def __le__(self, other):
        if self != other:
            raise LogCompareException()
        return len(self.contents_is)<=len(other.contents_is)

    def __len__(self):
        return len(self.contents_is)

    def __del__(self):
        self.contents_is = []

    def __add__(self, other):
        if self != other:
            raise LogCompareException()
        temp_log = LogClass(self.name_is)
        temp_log.contents_is = self.contents_is + other.contents_is
        return temp_log

    def __sub__(self, other):
        if self != other:
            other.contents_is = []
        temp_log = LogClass(self.name_is)
        diff_length= len(self.contents_is) - len(other.contents_is)
        if diff_length>0:#new one
            temp_log.contents_is = self.contents_is[-diff_length::]
        else:
            temp_log.contents_is = []
        return temp_log

    def __repr__(self):
        return f"'{self.name_is}' is instance of class 'LogClass'\
            \nIts contents are {'-'*20}\n{str(self)}"

    def __str__(self):
        contents = (' ').join(self.contents_is)
        return f"{contents}"


if __name__ == '__main__':
    test_list = ['1,2,3']
    test_list2 = ['4,5,6','7']
    test_list3 = ['1st sentence','2nd sentence','3rd sentence','4th sentence',
                  '5th sentence']

    log1 = LogClass("test log1")
    log1.contents_is = test_list3

    print(log1.find('sentence'))
