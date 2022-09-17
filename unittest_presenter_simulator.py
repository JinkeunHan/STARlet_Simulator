'''
STARlet Simulatior의 프레젠터 역할을 수행하는 모듈이다.
모델에게서는 AiosData 객체를 얻어와 이로부터 필요한 정보를 얻는다.
각 뷰 객체에게는
'''
import unittest
from view_simulator import *
from model_simulator import *
from presenter_simulator import *

def info_reset_for_presenter_test():
    '''
    유닛 테스트 수행 전 필요한 밑작업 수행
    - 테스트용 더미 객체 생성
    - 테스트용 임시 폴더 생성
    - 사용하는 파일명 및 경로 수정
    - 테스트용 더미 AiosData 데이터 생성
    '''
    test_dir = "d:/test_simulator/"
    if "test_simulator" in os.listdir("d:/"):
        import shutil
        shutil.rmtree("/test_simulator")
    os.mkdir(test_dir)
    info_cfx_status['path'] = test_dir
    info_cfx_status['name'] ="CFX_status.csv"
    info_elevator_enable['path'] = test_dir
    info_elevator_enable['name'] = "elevator_enable.csv"
    info_plate_exist['path'] = test_dir
    info_plate_exist['name'] = "plate_exist.csv"
    info_method_status['path'] = test_dir
    info_method_status['name'] = "Method_status.csv"
    info_trc['path'] = test_dir
    info_trc['name'] = "test.trc"
    test_aiosdata = AiosData(
        cfx_status = contents_cfx_status,
        method_status = contents_method_status,
        cfx1_time = "00:00:00",
        cfx2_time = "01:23:45",
        control_status = '3',
        method_run = "0",
        elevator_request = "0",
        plrn1_name = "test_plrn1.plrn",
        plrn2_name = "test_plrn2.plrn",
        elevator_enable = "",
        plate_exist = "",
        message = "test message",
    )    
    FileChecker(**info_plate_exist).write_file(test_aiosdata.plate_exist)
    FileChecker(**info_elevator_enable).write_file(test_aiosdata.elevator_enable)
    FileChecker(**info_cfx_status).write_file(test_aiosdata.cfx_status)

if __name__ == '__main__':
    info_reset_for_presenter_test()
    #asyncio.run(PresenterSimulator()._command_abort2_button)
    simulator = PresenterSimulator()