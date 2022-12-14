'''
STARlet Simulator의 모델을 나타내는 모듈이다.
3개의 클래스, AiosData, _FileChecker, ModelSimulator로 구성된다.
AiosData를 Presenter와 주고 받는다.
이는 ModelSimulator의 value를 통해 이루어진다.
'''
import os
import csv
from dataclasses import dataclass
import doctest

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
        if (return_value:=self.is_exist)== "Non existing": return return_value
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
    >>> model_simulator = ModelSimulator() 
    >>> test_dir = "d:/test_simulator/"
    >>> if "test_simulator" in os.listdir("d:/"):
    ...     import shutil
    ...     shutil.rmtree("/test_simulator")
    >>> os.mkdir(test_dir)
    >>> model_simulator.loc_cfx_status = (test_dir,"test.csv")
    >>> model_simulator.loc_elevator_enable = (test_dir,"test.csv")
    >>> model_simulator.loc_plate_exist = (test_dir,"test.csv")
    >>> model_simulator.loc_method_status = (test_dir,"test.csv")
    >>> model_simulator.loc_trc = (test_dir,"test.trc")
    >>> test = AiosData(cfx_status = [], method_status = [])
    >>> test.method_run ='0'
    >>> test.elevator_request = '0'
    >>> test.plrn1_name = 'test_plrn1.plrn'
    >>> test.plrn2_name = 'test_plrn2.plrn'
    >>> test.message = 'test_message'
    >>> model_simulator.value.elevator_enable
    'Non existing'
    >>> model_simulator.value.plate_exist
    'Non existing'
    >>> model_simulator.value = test
    >>> model_simulator.value.elevator_enable
    'Existing'
    >>> model_simulator.value.plate_exist
    'Existing'
    >>> model_simulator.value.cfx_status
    [['Method', 'run,', '0'], ['Elevator', 'requeset,', '0'], ['Plrn1,', 'test_plrn1.plrn'], ['Plrn2,', 'test_plrn2.plrn']]
    '''
    contents_method_status=[
    ["Method","run,",""],
    ["Elevator","requeset,",""],
    ["Plrn1,",""],
    ["Plrn2,",""]
    ]
    loc_cfx_status = ("d:/","test.csv")
    loc_elevator_enable = ("d:/","test.csv")
    loc_plate_exist = ("d:/","test.csv")
    loc_method_status = ("d:/","test.csv")
    loc_trc = ("d:/","test.trc")

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
        self.aios_data.cfx_status = _FileChecker(*self.loc_cfx_status).contents
        self.aios_data.elevator_enable = _FileChecker(*self.loc_elevator_enable).is_exist
        self.aios_data.plate_exist = _FileChecker(*self.loc_plate_exist).is_exist
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
        _FileChecker(*self.loc_method_status).contents = self.contents_method_status
        _FileChecker(*self.loc_trc).contents = obj.message

doctest.testmod()