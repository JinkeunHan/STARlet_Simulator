import os
import csv
from dataclasses import dataclass
from turtle import Terminator

@dataclass
class AiosData:
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
    def is_exist(self):
        filenames = os.listdir(self.path)
        if self.name in filenames:
            return "Existing"
        else:
            return "Non existing"
    @property
    def contents(self):
        if ".csv" in self.name:
            with open(self.path+self.name,'r') as f:
                lines = [line for line in csv.reader(f, delimiter=" ") if line]
        else:
            with open(self.path+self.name,'r') as f:
                lines = f.readlines()
        return lines
    @contents.setter
    def contents(self, value=list):
        if ".csv" in self.name:
            with open(self.path+self.name,'w') as f:
                for list in value: 
                    csv.writer(f, lineterminator='\n', delimiter=' ').writerow(list)
        else:
            with open(self.path+self.name,'w') as f:
                for string in (string for list in value for string in list): 
                    f.write(string)            
        return

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
    4) 파일 탐색기를 열어 사용자로 하여금 선택하게 해주고, 선택된 파일의 이름을 기록하는 기능
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
    def value(self):
        self.aios_data.cfx_status = _FileChecker(*self.loc_cfx_status).contents
        self.aios_data.elevator_enable = _FileChecker(*self.loc_elevator_enable).is_exist
        self.aios_data.plate_exist = _FileChecker(*self.loc_plate_exist).is_exist
        return self.aios_data
    
    @value.setter #write method_status.csv file
    def value(self, obj:AiosData):
        self.contents_method_status[0][2] = obj.method_run
        self.contents_method_status[1][2] = obj.elevator_request
        self.contents_method_status[2][1] = obj.plrn1_name
        self.contents_method_status[3][1] = obj.plrn2_name
        _FileChecker(*self.loc_method_status).contents = self.contents_method_status
        _FileChecker(*self.loc_trc).contents = obj.message
        return

model_simulator = ModelSimulator()
test = AiosData(
    cfx_status = [],
    method_status = [],
    elevator_enable = "",
    plate_exist = "",
    method_run = "0",
    elevator_request = "0",
    plrn1_name = "test_plrn1.plrn",
    plrn2_name = "test_plrn2.plrn",
    message = "test message"
    )
model_simulator.value = test
for line in model_simulator.value.cfx_status:
    print(line)
print(model_simulator.value.elevator_enable)
print(model_simulator.value.plate_exist)