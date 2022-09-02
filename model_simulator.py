'''
STARlet Simulator의 모델을 나타내는 모듈이다.
3개의 클래스, AiosData, FileChecker, ModelSimulator로 구성된다.
AiosData를 Presenter와 주고 받는다.
이는 ModelSimulator의 file_data를 통해 이루어진다.
'''
import os
import csv
from dataclasses import dataclass

info_cfx_status = {'path':"C:/Seegene_Method_Setting/RM_module/",
                   'name':"CFX_status.csv"}
info_elevator_enable = {'path':"C:/Seegene_Method_Setting/RM_module/elevator_status/",
                        'name':"elevator_enable.csv"}
info_plate_exist = {'path':"C:/Seegene_Method_Setting/RM_module/elevator_status/",
                    'name':"plate_exist.csv"}
info_method_status = {'path':"C:/Seegene_Method_Setting/RM_module/",
                      'name':"Method_status.csv"}
info_trc = {'path':"C:/Program Files (x86)/HAMILTON/LogFile/",
            'name':"test.trc"}
contents_method_status=[
        ["Method","run,",""],
        ["Elevator","requeset,",""],
        ["Plrn1,",""],
        ["Plrn2,",""]
    ]
contents_cfx_status = [
        ['CFX#1', "00:00:00"],
        ['CFX#2', "00:00:00"],
        ['Control','Status','0']
    ]
@dataclass
class AiosData:
    '''
    simulator에서 공통적으로 사용될 데이터 클래스임
    Presenter가 해당 클래스를 가져와 자신의 객체 내에 보관
    '''
    cfx_status:list
    method_status:list
    cfx1_time:str=""
    cfx2_time:str=""
    control_status:str=""
    method_run:str = ""
    elevator_request:str = ""
    plrn1_name:str = ""
    plrn2_name:str = ""
    elevator_enable:str = ""
    plate_exist:str = ""
    message:str = ""

class FileChecker:
    '''
    추후 재사용을 위해 따로 분리한 클래스.
    파일의 존재여부를 확인하거나 내용을 읽고 쓴다.
    '''
    def __init__(self, path, name):
        self.__path = path
        self.__name = name

    @property
    def path_and_name_is(self)->tuple:
        '''
        미리 지정된 경로 및 파일명을 반환한다.
        경로, 파일명 의 순서이니 주의할 것.
        '''
        return (self.__path, self.__name)

    @property
    def is_exist(self)->str:
        '''
        self.path 경로의 self.name 이름의 파일 존재 여부를 확인한다.
        '''
        path, name = self.path_and_name_is
        filenames = os.listdir(path)
        return "Existing" if name in filenames else "Non existing"
    @property
    def contents(self)->list or str:
        '''
        self.path 경로의 self.name 이름의 파일을 name의 확장자에 맞춰
        csv 파일 또는 text 파일을 읽고 그 내용을 리스트로 반환한다.
        만약 읽고자 하는 파일이 경로에 없다면 Non exsiting 문자열을 반환한다.
        '''
        if (return_value:=self.is_exist)== "Non existing":
            return return_value
        path, name = self.path_and_name_is
        if ".csv" in name:
            with open(path+name,'r', encoding='utf-8') as f_csv:
                lines = [line for line in csv.reader(f_csv, delimiter=" ") if line]
        else:
            with open(path+name,'r', encoding='utf-8') as f_txt:
                lines = f_txt.readlines()
        return lines
    @contents.setter
    def contents(self, value=list)->None:
        '''
        객체.contents = 변수:list로 사용
        self.path 경로에 self.name 이름의 파일을 쓴다.
        name의 파일 명을 확인한 다음, csv 파일 또는 trc 파일을 만든다.
        '''
        path, name = self.path_and_name_is
        if ".csv" in name:
            with open(path+name,'w', encoding='utf-8') as f_csv:
                for list_value in value:
                    csv.writer(f_csv, lineterminator='\n', delimiter=' ').writerow(list_value)
        else:
            with open(path+name,'w', encoding='utf-8') as f_trc:
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
    def __init__(self):
        self.__aios_data = AiosData(
            cfx_status= contents_cfx_status,
            method_status = contents_method_status,
        )

    @property
    def aios_data_is(self)->AiosData:
        '''
        file_data에 의해 갱신된 AiosData를 반환한다.
        별도의 파일 읽기를 다시 하지 않고 정보를 얻기 위해 따로 보관한다.
        '''
        return self.__aios_data
    @aios_data_is.setter
    def aios_data_is(self, value:AiosData)->None:
        '''
        file_data에 의해서만 호출되어야 하는 메서드.
        별도의 파일 읽기를 다시 하지 않고 정보를 얻기 위해 따로 보관하기 위해 존재.
        '''
        self.__aios_data = value

    @property
    def file_data(self)->AiosData:
        '''
        호출 시 cfx_status.csv 내용 및 elevator_enable, plate_exist 존재여부를 확인.
        또한 CFX1과 CFX2의 남은 시간과 control status를 갱신한다.
        이후 갱신된 정보를 반환한다.
        '''
        value = self.aios_data_is
        value.cfx_status = FileChecker(**info_cfx_status).contents
        value.elevator_enable = FileChecker(**info_elevator_enable).is_exist
        value.plate_exist = FileChecker(**info_plate_exist).is_exist
        if isinstance(value.cfx_status, list):
            value.cfx1_time = value.cfx_status[0][1]
            value.cfx2_time = value.cfx_status[1][1]
            value.control_status = value.cfx_status[2][2]
        else: #return of "None existing"
            value.cfx1_time = value.cfx_status
            value.cfx2_time = value.cfx_status
            value.control_status = value.cfx_status
        self.aios_data_is = value
        return value

    @file_data.setter #write method_status.csv file
    def file_data(self, obj:AiosData)->None:
        '''
        객체.file_data = 변수:AiosData로 사용한다.
        호출 시 두 개의 파일의 내용을 바꾼다.
        - method_status.csv
        - .trc
        '''
        obj.method_status[0][2] = obj.method_run
        obj.method_status[1][2] = obj.elevator_request
        obj.method_status[2][1] = obj.plrn1_name
        obj.method_status[3][1] = obj.plrn2_name
        FileChecker(**info_method_status).contents = obj.method_status
        if obj.message:
            FileChecker(**info_trc).contents = obj.message
