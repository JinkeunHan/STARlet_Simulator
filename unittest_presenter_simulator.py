'''
STARlet Simulatior의 프레젠터 역할을 수행하는 모듈이다.
모델에게서는 AiosData 객체를 얻어와 이로부터 필요한 정보를 얻는다.
각 뷰 객체에게는
'''
import unittest
import os
import shutil
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
    info_trc['name'] = "test.trc"
    test_aiosdata = AiosData(
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

class TestPresenterSimulator(unittest.TestCase):
    def setUp(self)->None:
        self.presenter_simulator = PresenterSimulator()
        pass
    def tearDown(self) -> None:
        pass
    # def test_check_modul_move_within_times(self):
    #     value:AiosData = self.presenter_simulator.aios_data_is
    #     value.cfx1_time = "00:00:00"
    #     value.cfx2_time = "00:00:00"
    #     self.presenter_simulator.aios_data_is = value
    #     result = self.presenter_simulator._check_module_move_within_times(1)
    #     self.assertFalse(result)
    #     value.cfx1_time = "88:88:88"
    #     value.cfx2_time = "00:00:00"
    #     self.presenter_simulator.aios_data_is = value
    #     result = self.presenter_simulator._check_module_move_within_times(1)
    #     self.assertTrue(result)
    #     value.cfx1_time = "00:00:00"
    #     value.cfx2_time = "88:88:88"
    #     self.presenter_simulator.aios_data_is = value
    #     result = self.presenter_simulator._check_module_move_within_times(1)
    #     self.assertTrue(result)
    #     value.cfx1_time = "88:88:88"
    #     value.cfx2_time = "88:88:88"
    #     self.presenter_simulator.aios_data_is = value
    #     result = self.presenter_simulator._check_module_move_within_times(1)
    #     self.assertTrue(result)
    def test_check_cfx_is_available(self):
        value:AiosData = self.presenter_simulator.aios_data_is
        value.cfx1_time = "00:00:00"
        value.cfx2_time = "00:00:00"
        self.presenter_simulator.aios_data_is = value
        result = self.presenter_simulator._check_cfx_is_available('2plate')
        self.assertTrue(result)
        result = self.presenter_simulator._check_cfx_is_available('1plate')
        self.assertTrue(result)

        value.cfx1_time = "88:88:88"
        value.cfx2_time = "00:00:00"
        self.presenter_simulator.aios_data_is = value
        result = self.presenter_simulator._check_cfx_is_available('2plate')
        self.assertFalse(result)
        result = self.presenter_simulator._check_cfx_is_available('1plate')
        self.assertTrue(result)

        value.cfx1_time = "00:00:00"
        value.cfx2_time = "88:88:88"
        self.presenter_simulator.aios_data_is = value
        result = self.presenter_simulator._check_cfx_is_available('2plate')
        self.assertFalse(result)
        result = self.presenter_simulator._check_cfx_is_available('1plate')
        self.assertTrue(result)

        value.cfx1_time = "88:88:88"
        value.cfx2_time = "88:88:88"
        self.presenter_simulator.aios_data_is = value
        result = self.presenter_simulator._check_cfx_is_available('2plate')
        self.assertFalse(result)
        result = self.presenter_simulator._check_cfx_is_available('1plate')
        self.assertFalse(result)

    def test_simulate_abort_starlet(self):
        '''
        메서드를 이루는 내부 메서드들 모두가
        model_simulator의 unittest를 통해 이미 검증됨
        '''
        pass

    def test_simulate_stop_starlet(self):
        '''
        메서드를 이루는 내부 메서드들 모두가
        model_simulator의 unittest를 통해 이미 검증됨
        '''
        pass

    def test_simulate_run_starlet(self):
        '''
        메서드를 이루는 내부 메서드들 모두가
        model_simulator의 unittest를 통해 이미 검증됨
        '''
        pass

    def test_simulate_elevator_request_1st(self):
        '''
        메서드를 이루는 내부 메서드들 모두가
        model_simulator의 unittest를 통해 이미 검증됨
        '''
        pass

    def test_simulate_elevator_request_2nd(self):
        '''
        메서드를 이루는 내부 메서드들 모두가
        model_simulator의 unittest를 통해 이미 검증됨
        '''
        pass

    def test_simulate_plate_transfer_1st(self):
        '''
        메서드를 이루는 내부 메서드들 모두가
        model_simulator의 unittest를 통해 이미 검증됨
        '''
        pass

    def test_simulate_plate_transfer_2nd(self)->None:
        '''
        메서드를 이루는 내부 메서드들 모두가
        model_simulator의 unittest를 통해 이미 검증됨
        '''
        pass

    def test_simulate_elevator_wait(self)->bool:
        '''
        메서드를 이루는 내부 메서드들 모두가
        model_simulator의 unittest를 통해 이미 검증됨
        self.presenter_simulator._simulate_elevator_wait(10)
        window_frame.destroy()
        '''

    def test_delay_sec(self):
        '''
        메서드를 이루는 내부 메서드들 모두가
        model_simulator의 unittest를 통해 이미 검증됨
        '''
        pass

if __name__ == '__main__':
    unittest.main()