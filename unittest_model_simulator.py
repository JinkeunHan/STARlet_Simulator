from model_simulator import *
from model_simulator import FileChecker
import os
import unittest
import time

contents_cfx_status = [
    ['CFX#1','00:00:00'],
    ['CFX#2','12:34:56'],
    ['Control Status','0']
    ]

contents_test1 = [
    "this is a test\n",
    "this is a test2\n",
    "this is a test3,"
    ]

contents_test2 = [
    "this is a newly added sentence"
    ]

def info_reset_for_test():
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

class TestModelSimulator(unittest.TestCase):
    def setUp(self) -> None: #기본 테스트 함수, 각 테스트 수행 시마다 자동으로 호출
        '''
        유닛 테스트 수행 전 필요한 밑작업 수행
        - 테스트용 더미 객체 생성
        - 테스트용 임시 폴더 생성
        - 사용하는 파일명 및 경로 수정
        '''
        self.model_simulator = ModelSimulator()
        info_reset_for_test()

    def tearDown(self) -> None: #기본 테스트 함수, 각 테스트 수행 시마다 자동으로 호출
        '''
        유닛 테스트 수행 후 뒷처리 작업 수행
        '''
        pass

    def test_aios_data_is(self):
        dummy:AiosData = AiosData(
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
        self.model_simulator.aios_data_is = dummy
        temp_value = self.model_simulator.aios_data_is
        self.assertEqual(dummy,
                         temp_value,
                         msg="값 확인용, 같은 내용을 쓰고 읽어야 함")

    def test_file_data_setter(self):
        obj = self.model_simulator.aios_data_is
        temp_method_status:list[str] = []
        temp_method_status.append(f'Method run,{obj.method_run}\n')
        temp_method_status.append(f'Elevator request,{obj.elevator_request}\n')
        temp_method_status.append(f'Plrn1, {obj.plrn1_name}\n')
        temp_method_status.append(f'Plrn1, {obj.plrn2_name}\n')
        temp_method_status.append('\n')
        self.model_simulator.file_data = self.model_simulator.aios_data_is
        method_status_csv = self.model_simulator.method_status_file
        method_status_csv.contents_is = method_status_csv.read_file()
        self.assertEqual(temp_method_status,
                         method_status_csv.contents_is,
                         msg="파일 확인용, 같은 내용을 쓰고 읽어야 함")

    def test_file_data_getter(self):
        cfx_file = self.model_simulator.cfx_status_file
        cfx_file.write_file(contents_cfx_status)
        aios_value:AiosData = self.model_simulator.file_data
        self.assertEqual(contents_cfx_status[0][1],
                         aios_value.cfx1_time
                         )
        self.assertEqual(contents_cfx_status[1][1],
                         aios_value.cfx2_time
                         )
        self.assertEqual(contents_cfx_status[2][1],
                         aios_value.control_status
                         )

        plate_info = self.model_simulator.plate_exist_file
        elevator_info = self.model_simulator.elevator_enable_file

        if plate_info.is_exist == 'Existing':
            os.remove(info_plate_exist['path']+info_plate_exist['name'])
        if elevator_info.is_exist == 'Existing':
            os.remove(info_elevator_enable['path']+info_elevator_enable['name'])

        aios_value:AiosData = self.model_simulator.file_data
        self.assertEqual("Non existing",
                         aios_value.elevator_enable,
                         msg="파일 확인용, 파일 자체가 없으므로 없다고 해야 함")
        self.assertEqual("Non existing",
                         aios_value.plate_exist,
                         msg="파일 확인용, 파일 자체가 없으므로 없다고 해야 함")

        plate_info.write_file(["test"])
        aios_value:AiosData = self.model_simulator.file_data
        self.assertEqual("Non existing",
                         aios_value.elevator_enable,
                         msg="파일 확인용, 파일 자체가 없으므로 없다고 해야 함")
        self.assertEqual("Existing",
                         aios_value.plate_exist,
                         msg="파일 확인용, 생성 이후이므로 있다고 해야 함")

        elevator_info.write_file(["test"])
        aios_value:AiosData = self.model_simulator.file_data
        self.assertEqual("Existing",
                         aios_value.elevator_enable,
                         msg="파일 확인용, 생성 이후이므로 있다고 해야 함")

    def test_find_recent_file_and_get_time(self):
        aios_log_file = self.model_simulator.aios_log_file
        aios_log_file.write_file(contents_test1)
        now = time.localtime(time.time())
        now_time = time.strftime("%Y-%m-%d %H:%M:%S", now)
        written_time = aios_log_file.get_modified_time('strftime')
        self.assertEqual(written_time, now_time)
        self.assertEqual(info_aios_log['name'], aios_log_file.name_is)
        path, name = aios_log_file.path_and_name_is
        os.remove(path+name)

if __name__ == "__main__":
    unittest.main()