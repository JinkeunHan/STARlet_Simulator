'''
STARlet Simulatior의 프레젠터 역할을 수행하는 모듈이다.
모델에게서는 AiosData 객체를 얻어와 이로부터 필요한 정보를 얻는다.
각 뷰 객체에게는
'''
import unittest
import os
import shutil
from datetime import datetime, timedelta
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
        self.test_model = PresenterSimulator()
        pass
    def tearDown(self) -> None:
        pass

    def test__check_modul_move_within_times(self):
        '''
        단순히 시간 내에 모듈이 움직이기 시작했음을 확인하는 메서드이므로,
        이를 테스트 하기 위해 cfx1 또는 cfx2의 시간에 88:88:88을 써넣어 테스트하였다.
        '''
        value:AiosData = self.test_model.aios_data_is

        value.cfx1_time = "00:00:00"
        value.cfx2_time = "00:00:00"
        self.test_model.aios_data_is = value
        result = self.test_model._PresenterSimulator__check_module_move_within_times(0)
        self.assertFalse(result)

        value.cfx1_time = "88:88:88"
        value.cfx2_time = "00:00:00"
        self.test_model.aios_data_is = value
        result = self.test_model._PresenterSimulator__check_module_move_within_times(1)
        self.assertTrue(result)

        value.cfx1_time = "00:00:00"
        value.cfx2_time = "88:88:88"
        self.test_model.aios_data_is = value
        result = self.test_model._PresenterSimulator__check_module_move_within_times(1)
        self.assertTrue(result)

        value.cfx1_time = "88:88:88"
        value.cfx2_time = "88:88:88"
        self.test_model.aios_data_is = value
        result = self.test_model._PresenterSimulator__check_module_move_within_times(1)
        self.assertTrue(result)

    def test__check_cfx_is_available(self):
        '''
        CFX 시간을 읽고서 각 플레이트 시나리오를 수행 할 수 있는지 여부를 확인하는 메서드이다.
        그에 따라 시간을 각기 조절하여 가능 여부를 판단한다.
        '''
        value:AiosData = self.test_model.aios_data_is
        value.cfx1_time = "00:00:00"
        value.cfx2_time = "00:00:00"
        self.test_model.aios_data_is = value
        result = self.test_model._PresenterSimulator__check_cfx_is_available('2plate')
        self.assertTrue(result)
        result = self.test_model._PresenterSimulator__check_cfx_is_available('1plate')
        self.assertTrue(result)

        value.cfx1_time = "88:88:88"
        value.cfx2_time = "00:00:00"
        self.test_model.aios_data_is = value
        result = self.test_model._PresenterSimulator__check_cfx_is_available('2plate')
        self.assertFalse(result)
        result = self.test_model._PresenterSimulator__check_cfx_is_available('1plate')
        self.assertTrue(result)

        value.cfx1_time = "00:00:00"
        value.cfx2_time = "88:88:88"
        self.test_model.aios_data_is = value
        result = self.test_model._PresenterSimulator__check_cfx_is_available('2plate')
        self.assertFalse(result)
        result = self.test_model._PresenterSimulator__check_cfx_is_available('1plate')
        self.assertTrue(result)

        value.cfx1_time = "88:88:88"
        value.cfx2_time = "88:88:88"
        self.test_model.aios_data_is = value
        result = self.test_model._PresenterSimulator__check_cfx_is_available('2plate')
        self.assertFalse(result)
        result = self.test_model._PresenterSimulator__check_cfx_is_available('1plate')
        self.assertFalse(result)

    def test__waiting_for_cfx_remain_time_change(self):
        '''
        CFX1의 남은 시간을 바꿔가며 테스트 하였다. 
        시간이 0이 될 때까지도 CFX1의 시간이 정해진 시간으로 바뀌지 않으면 False,
        0이 되기 전에 바뀌면 True가 반환되어야 함에 따라 이를 테스트 하였다
        '''
        value:AiosData = self.test_model.aios_data_is

        value.cfx1_time = "00:00:00"
        self.test_model.aios_data_is = value
        result = self.test_model._PresenterSimulator__waiting_for_cfx_remain_time_change(0)
        self.assertFalse(result)

        value.cfx1_time = "88:88:88"
        self.test_model.aios_data_is = value
        result = self.test_model._PresenterSimulator__waiting_for_cfx_remain_time_change(0)
        self.assertFalse(result)

        value.cfx1_time = "99:99:99"
        self.test_model.aios_data_is = value
        result = self.test_model._PresenterSimulator__waiting_for_cfx_remain_time_change(0)
        self.assertFalse(result)

        value.cfx1_time = "12:34:56"
        self.test_model.aios_data_is = value
        result = self.test_model._PresenterSimulator__waiting_for_cfx_remain_time_change(10)
        self.assertTrue(result)

    def test__wating_for_elevator_enable_file_creation(self):
        '''
        elevator_enable.csv 파일의 시간을 조절해가며 테스트 하였다. 
        시간이 0이 될 때까지도 파일이 생기지 않으면 False, 
        0이 되기 전에 생기면 True가 반환되어야 함에 따라 이를 테스트 하였다
        '''
        value:AiosData = self.test_model.aios_data_is

        value.elevator_enable = "Non existing"
        self.test_model.aios_data_is = value
        result = self.test_model._PresenterSimulator__waiting_for_elevator_enable_file_creation(0)
        self.assertFalse(result)

        value.elevator_enable = "Existing"
        self.test_model.aios_data_is = value
        result = self.test_model._PresenterSimulator__waiting_for_elevator_enable_file_creation(10)
        self.assertTrue(result)

    def test__waiting_for_plate_exist_file_creation(self):
        '''
        plate_exist.csv 파일의 시간을 조절해가며 테스트 하였다. 
        시간이 0이 될 때까지도 파일이 생기지 않으면 False, 
        0이 되기 전에 생기면 True가 반환되어야 함에 따라 이를 테스트 하였다
        '''
        value:AiosData = self.test_model.aios_data_is

        value.plate_exist = "Non existing"
        self.test_model.aios_data_is = value
        result = self.test_model._PresenterSimulator__waiting_for_plate_exist_file_creation(0)
        self.assertFalse(result)

        value.plate_exist = "Existing"
        self.test_model.aios_data_is = value
        result = self.test_model._PresenterSimulator__waiting_for_plate_exist_file_creation(10)
        self.assertTrue(result)

    def test__simulate_run_starlet(self):
        '''
        plrn_info를 직접 조절하여 적절한 내용을 넣은 다음,
        생성된 파일을 다시 읽어 들여 그 내용을 확인하는 방식으로 테스트
        '''
        test_dict = {'scenario': '', 'plrn_name': ''}
        test_dict["scenario"] = '1plate'
        test_dict["plrn_name"] = 'test_plrn.plrn'
        self.test_model.plrn_info_is = test_dict
        self.test_model._PresenterSimulator__simulate_run_starlet()
        mlist = self.test_model.method_status_file.read_file()        
        plrn1_info = mlist[2].split(',')[1].rstrip('\n')
        plrn2_info = mlist[3].split(',')[1].rstrip('\n')
        self.assertEqual(plrn1_info, test_dict["plrn_name"])
        self.assertEqual(plrn2_info, "")

        test_dict["scenario"] = '2plate'
        test_dict["plrn_name"] = 'test_plrn_second.plrn'
        self.test_model.plrn_info_is = test_dict
        self.test_model._PresenterSimulator__simulate_run_starlet()
        mlist = self.test_model.method_status_file.read_file()        
        plrn1_info = mlist[2].split(',')[1].rstrip('\n')
        plrn2_info = mlist[3].split(',')[1].rstrip('\n')
        self.assertEqual(plrn1_info, test_dict["plrn_name"])
        self.assertEqual(plrn2_info, test_dict["plrn_name"])

    def test__delay_sec(self):
        '''
        딜레이 기능 자체가 충실히 구현되었는지를 검증
        '''
        test_time = 3
        test_count = 3
        test_list = []
        for result in self.test_model._PresenterSimulator__delay_sec(test_time):
            test_count -=1
            test_list.append(result)
            if not test_count:
                break
        self.assertEqual(test_list,[True, True, True])

        test_time = 0
        test_count = 3
        test_list = []
        for result in self.test_model._PresenterSimulator__delay_sec(test_time):
            test_count -=1
            test_list.append(result)
            if not test_count:
                break
        self.assertEqual(test_list,[True, False])

if __name__ == '__main__':
    unittest.main()