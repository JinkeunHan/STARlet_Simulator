'''
FileChecker 클래스.
관리하고자 하는 파일을 해당 클래스의 객체로 생성하면 제어가 가능하다.
'''
import os
import csv
import shutil
import time
from typing import Any
from logger_jk import LogClass


class FileChecker(LogClass):
    '''
    추후 재사용을 위해 따로 분리한 클래스.
    파일의 존재여부를 확인하거나 내용을 읽고 쓴다.
    '''
    def __init__(self, path:str, name:str):
        self.mtime_is:float = 0
        LogClass.__init__(self, name)
        self.path_and_name_is = path, self.name_is

    @property
    def mtime_is(self)->float:#getter
        '''
        get modified time in timestamp format.
        '''
        return self.__mtime
    @mtime_is.setter
    def mtime_is(self, value:float):#setter
        self.__mtime = value

    @property
    def path_and_name_is(self)->tuple:
        '''
        미리 지정된 경로 및 파일명을 반환한다.
        경로, 파일명 의 순서이니 주의할 것.
        '''
        return (self.__path, self.name_is)

    @path_and_name_is.setter
    def path_and_name_is(self, path_and_name:tuple):
        self.__path = path_and_name[0]
        self.name_is = path_and_name[1]

    @property
    def is_exist(self)->str:
        '''
        self.path 경로의 self.name 이름의 파일 존재 여부를 확인한다.
        '''
        path, name = self.path_and_name_is
        return "Existing" if os.path.exists(path+name) else "Non existing"

    def copy_file(self)->None:
        '''
        파일을 정해진 경로 (D:/AIOS_STARLET_Logger/)로 복사한다.
        '''
        safe_dir = "D:/AIOS_STARLET_Logger/"
        # if 'AIOS_STARLET_Logger' not in os.listdir('D:/'):
        if not os.path.exists(safe_dir):
            os.mkdir(safe_dir)
        path, name = self.path_and_name_is
        shutil.copy(path+name, safe_dir)

    def del_file(self)->None:
        '''
        파일을 정해진 경로 (D:/AIOS_STARLET_Logger/)에서 삭제한다.
        '''
        _, name = self.path_and_name_is
        safe_dir = "D:/AIOS_STARLET_Logger/"
        # if 'AIOS_STARLET_Logger' in os.listdir('D:/'):
        if os.path.exists(safe_dir+name):
            os.remove(safe_dir+name)

    def read_file(self)->list :
        '''
        지정된 경로 ("D:/AIOS_STARLET_Logger/") 내 지정된 이름의 파일을 찾고, 파일 확장자에 맞춰 그 내용을 읽는다.
        이후 그 내용을 리스트로 반환한다.
        만약 읽고자 하는 파일이 경로에 없다면 []을 반환한다.
        '''
        lines = []
        path, name = self.path_and_name_is

        if self.is_exist == "Existing":
            if ".csv" in name:
                with open(path+name,'r', encoding='utf-8', errors='ignore') as f_csv:
                    lines = f_csv.readlines()
            elif ".trc" in name:
                with open(path+name,'r', encoding='utf-8', errors='ignore') as f_txt:
                    lines = f_txt.readlines()
            else:
                with open(path+name,'r', encoding='utf-8') as f_txt:
                    lines = f_txt.readlines()

        return lines

    def read_file_safely(self)->list :
        '''
        지정된 경로 ("D:/AIOS_STARLET_Logger/") 내 지정된 이름의 파일을 찾고, 파일 확장자에 맞춰 그 내용을 읽는다.
        이후 그 내용을 리스트로 반환한다.
        만약 읽고자 하는 파일이 경로에 없다면 []을 반환한다.
        '''
        self.copy_file()
        path = "D:/AIOS_STARLET_Logger/"
        lines = []
        b_path, name = self.path_and_name_is
        self.path_and_name_is = path, name

        if self.is_exist == "Existing":
            if ".csv" in name:
                with open(path+name,'r', encoding='utf-8') as f_csv:
                    lines = f_csv.readlines()
            elif ".trc" in name:
                with open(path+name,'r', encoding='utf-8', errors='ignore') as f_txt:
                    lines = f_txt.readlines()
            else:
                with open(path+name,'r', encoding='utf-8') as f_txt:
                    lines = f_txt.readlines()

        self.path_and_name_is = b_path, name
        self.del_file()
        return lines

    def write_file(self, value=list)->None:
        '''
        객체.contents = 변수:list로 사용. str을 전달해도 작성함.
        self.path 경로에 self.name 이름의 파일을 쓴다.
        name의 파일 명을 확인한 다음, csv 파일 또는 trc 파일을 만든다.
        '''
        path, name = self.path_and_name_is
        if ".csv" in name: #csv file writing
            with open(path+name,'w', encoding='utf-8') as f_csv:
                for list_value in value:
                    csv.writer(f_csv, lineterminator='\n', delimiter=',').writerow(list_value)
        else: #trc or txt file writing
            if self.is_exist == "Existing":
                with open(path+name,'a', encoding='utf-8') as f_trc:
                    for string in (string for list in value for string in list):
                        f_trc.write(string)
            else:
                with open(path+name,'w', encoding='utf-8') as f_trc:
                    for string in (string for list in value for string in list):
                        f_trc.write(string)

    def get_updated_contents(self)->list:
        '''
        본 log 객체의 내용을 읽어 온다.
        이후 기존 내용과 비교하여 이번에 읽은 내용과 다른 부분을 반환한다.
        '''
        new_log = LogClass(self.name_is)
        new_log.contents_is = self.read_file()
        return (new_log - self).contents_is

    def update_contents(self, value:Any):
        '''
        value의 내용을 업데이트 한다.
        update(self, value:Any) 메서드와 동일하다.
        '''
        self.update(value)

    def get_file_lists(self)->list:
        '''
        자신과 같은 확장자를 갖는 파일들의 리스트를 반환한다.
        가장 최근에 수정된 파일들부터 앞에 존재한다.
        만약 찾지 못하면 null을 반환한다.
        '''
        path, target_file = self.path_and_name_is

        file_type = target_file.split('.')[-1]
        file_list:list = os.listdir(path)
        same_typed_files = [
                            [file_name, os.path.getmtime(path+file_name)]
                            for file_name in file_list
                            if file_name.find(file_type)>-1
                            ]
        if not same_typed_files:
            return_value = []
        else:
            sorted_list = sorted(same_typed_files, key=lambda x: x[1], reverse=True)
            return_value = [file_name for file_name, _ in sorted_list]
        return return_value

    def get_modified_time(self, time_type:str = 'mtime')->Any:
        '''
        file의 수정 시간을 얻는다.
        time stamp로 반환한다.
        만약 'str'을 인수로 전달하면 strftime "Y-M-D H:m:s"로 반환한다.
        '''
        path, name = self.path_and_name_is
        mtime:Any = os.path.getmtime(path + name)
        if time_type == 'strftime':
            mtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(mtime))
        return mtime

    def check_file_updated_or_not(self)->bool:
        '''
        파일 업데이트 여부를 확인한다.
        업데이트 되었으면 True를 아니면 False를 반환한다.
        또한 파일 자체의 업데이트 시간(time stamp)을 갱신한다.
        '''
        written_time = self.get_modified_time()
        return_value = written_time != self.mtime_is
        self.mtime_is = written_time
        return return_value
