'''
STARlet Simulator의 모델을 나타내는 모듈이다.
3개의 클래스, AiosData, FileChecker, ModelSimulator로 구성된다.
AiosData를 Presenter와 주고 받는다.
이는 ModelSimulator의 file_data를 통해 이루어진다.
'''
import time
from dataclasses import dataclass
from file_checker import FileChecker

info_cfx_status = {'path':"C:/Seegene_Method_Setting/RM_module/",
                   'name':"CFX_status.csv"}
info_elevator_enable = {'path':"C:/Seegene_Method_Setting/RM_module/elevator_status/",
                        'name':"elevator_enable.csv"}
info_plate_exist = {'path':"C:/Seegene_Method_Setting/RM_module/elevator_status/",
                    'name':"plate_exist.csv"}
info_method_status = {'path':"C:/Seegene_Method_Setting/RM_module/",
                      'name':"method_status.csv"}
info_trc = {'path':"C:/Program Files (x86)/HAMILTON/LogFiles/",
            'name':"test.trc"}
info_aios_log = {'path':"D:/Release/Logs/Debug/",
                'name':"test.txt"}
@dataclass
class AiosData:
    '''
    simulator에서 공통적으로 사용될 데이터 클래스임
    Presenter가 해당 클래스를 가져와 자신의 객체 내에 보관
    '''
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
        trc_time = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime(time.time()))
        trc_name = f"test_{trc_time}.trc"
        info_trc['name'] = trc_name
        self.aios_data_is = AiosData()
        self.elevator_enable_file = FileChecker(**info_elevator_enable)
        self.plate_exist_file = FileChecker(**info_plate_exist)
        self.method_status_file = FileChecker(**info_method_status)
        self.cfx_status_file = FileChecker(**info_cfx_status)
        self.aios_log_file = FileChecker(**info_aios_log)
        self.trc_file = FileChecker(**info_trc)

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

    def get_updated_log(self, target:FileChecker)->list[str]:
        '''
        target log에서 갱신된 부분만을 별도로 발췌한다.
        find_time_in_log 보다 반드시 먼저 호출해야 한다.
        '''
        return target.get_updated_contents()

    @property
    def file_data(self)->AiosData:
        '''
        호출 시 cfx_status.csv 내용 및 elevator_enable, plate_exist 존재여부를 확인.
        또한 CFX1과 CFX2의 남은 시간과 control status를 갱신한다.
        이후 갱신된 정보를 반환한다.
        '''
        value:AiosData = self.aios_data_is
        self.cfx_status_file.copy_file()
        cfx_status:list[str] = self.cfx_status_file.read_file()
        self.cfx_status_file.del_file()
        value.elevator_enable = self.elevator_enable_file.is_exist
        value.plate_exist = self.plate_exist_file.is_exist
        if isinstance(cfx_status, list):
            value.cfx1_time = cfx_status[0].split(',')[1].rstrip('\n')
            value.cfx2_time = cfx_status[1].split(',')[1].rstrip('\n')
            value.control_status = cfx_status[2].split(',')[1].rstrip('\n')
        else: #return value is "None existing"
            value.cfx1_time = cfx_status
            value.cfx2_time = cfx_status
            value.control_status = cfx_status
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
        temp_method_status:list = []
        temp_method_status += [(f'Method run,{obj.method_run}'.split(','))]
        temp_method_status += [(f'Elevator request,{obj.elevator_request}'.split(','))]
        temp_method_status += [(f'Plrn1, {obj.plrn1_name}'.split(','))]
        temp_method_status += [(f'Plrn1, {obj.plrn2_name}'.split(','))]
        temp_method_status += ['']
        self.method_status_file.write_file(temp_method_status)
        if obj.message:
            self.trc_file.write_file(obj.message)
            obj.message = ""
