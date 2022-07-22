'''
STARlet Simulator의 모델을 나타내는 모듈이다.
3개의 클래스, AiosData, _FileChecker, ModelSimulator로 구성된다.
AiosData를 Presenter와 주고 받는다.
이는 ModelSimulator의 value를 통해 이루어진다.
'''
import os
import csv
from dataclasses import dataclass

@dataclass
class AiosData:
    '''
    simulator에서 공통적으로 사용될 데이터 클래스임
    Presenter가 해당 클래스를 가져와 자신의 객체 내에 보관
    '''
    cfx_status:list
    method_status:list
    elevator_enable:str = ""
    plate_exist:str = ""
    method_run:str = ""
    elevator_request:str = ""
    plrn1_name:str = ""
    plrn2_name:str = ""
    message:str = ""

class _FileChecker:
    '''
    비공개 은닉 클래스, 내부에서만 동작하며 객체 단위로 갖는 정보를 바탕으로
    파일의 존재여부를 확인하거나 내용을 읽고 쓴다.
    '''
    def __init__(self, path, name):
        self.path = path
        self.name = name
    @property
    def is_exist(self)->str:
        '''
        self.path 경로의 self.name 이름의 파일 존재 여부를 확인한다.
        '''
        filenames = os.listdir(self.path)
        if self.name in filenames:
            return_value = "Existing"
        else:
            return_value = "Non existing"
        return return_value
    @property
    def contents(self)->list:
        '''
        변수:list = 객체.contents 로 읽는다.
        self.path 경로의 self.name 이름의 파일을 읽고 그 내용을 반환한다.
        name의 확장자에 맞춰, csv 파일 또는 text 파일을 읽어낸다.
        '''
        if (return_value:=self.is_exist)== "Non existing":
            return return_value
        if ".csv" in self.name:
            with open(self.path+self.name,'r', encoding='utf-8') as f_csv:
                lines = [line for line in csv.reader(f_csv, delimiter=" ") if line]
        else:
            with open(self.path+self.name,'r', encoding='utf-8') as f_txt:
                lines = f_txt.readlines()
        return lines
    @contents.setter
    def contents(self, value=list)->None:
        '''
        객체.contents = 변수:list로 사용
        self.path 경로에 self.name 이름의 파일을 쓴다.
        name의 파일 명을 확인한 다음, csv 파일 또는 trc 파일을 만든다.
        '''
        if ".csv" in self.name:
            with open(self.path+self.name,'w', encoding='utf-8') as f_csv:
                for list_value in value:
                    csv.writer(f_csv, lineterminator='\n', delimiter=' ').writerow(list_value)
        else:
            with open(self.path+self.name,'w', encoding='utf-8') as f_trc:
                for string in (string for list in value for string in list):
                    f_trc.write(string)

class ModelSimulator:
    '''
    Simulator for Starlet.
    기능은 매우 단순하다:
    1) 특정 경로의 폴더를 탐색하여 파일의 존재 여부를 확인하는 기능
    - Elevator_enable.csv 및 Plate_Exist.csv가 여기에 해당
    2) 특정 경로의 파일을 열어 그 내용을 읽는 기능
    - CFX_Status.csv 및 yy-mm-dd.txt가 여기에 해당
    3) 특정 경로에 지정된 이름의 파일을 쓰는 기능
    - Method_status.csv 및 *.trc가 여기에 해당
    '''
    contents_method_status=[
    ["Method","run,",""],
    ["Elevator","requeset,",""],
    ["Plrn1,",""],
    ["Plrn2,",""]
    ]
    info_cfx_status = ("C:/Seegene_Method_Setting/RM_module/",
                      "CFX_status.csv")
    info_elevator_enable = ("C:/Seegene_Method_Setting/RM_module/elevator_status/",
                           "Method_status.csv")
    info_plate_exist = ("C:/Seegene_Method_Setting/RM_module/elevator_status/",
                       "Elevator_enable.csv")
    info_method_status = ("C:/Seegene_Method_Setting/RM_module/",
                         "Plate_exist.csv")
    info_trc = ("C:/Program Files (x86)/HAMILTON/LogFile/",
               "test.trc")
    def __init__(self):
        self.aios_data = AiosData(
            [['CFX#1', "00:00:00"],['CFX#2', "00:00:00"]],#cfx_status
            self.contents_method_status, #method_status
        )
    @property #read CFX_Status.csv file, check Plate_exist and Elevator_enable
    def value(self)->AiosData:
        '''
        호출 시 cfx_status.csv 파일 내용 및 elevator_enable, plate_exist
        파일의 존재여부를 반환한다.
        '''
        self.aios_data.cfx_status = _FileChecker(*self.info_cfx_status).contents
        self.aios_data.elevator_enable = _FileChecker(*self.info_elevator_enable).is_exist
        self.aios_data.plate_exist = _FileChecker(*self.info_plate_exist).is_exist
        return self.aios_data
    @value.setter #write method_status.csv file
    def value(self, obj:AiosData)->None:
        '''
        객체.value = 변수:AiosData로 사용한다.
        호출 시 method_status.csv 파일을 쓴다.
        '''
        self.contents_method_status[0][2] = obj.method_run
        self.contents_method_status[1][2] = obj.elevator_request
        self.contents_method_status[2][1] = obj.plrn1_name
        self.contents_method_status[3][1] = obj.plrn2_name
        _FileChecker(*self.info_method_status).contents = self.contents_method_status
        _FileChecker(*self.info_trc).contents = obj.message
