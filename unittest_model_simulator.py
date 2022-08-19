from dataclasses import dataclass
from model_simulator import *
from model_simulator import FileChecker
import os
import unittest

class TestModelSimulator(unittest.TestCase):
    def setUp(self) -> None: #기본 테스트 함수, 각 테스트 수행 시마다 자동으로 호출
        '''
        유닛 테스트 수행 전 필요한 밑작업 수행
        - 테스트용 더미 객체 생성
        - 테스트용 임시 폴더 생성
        - 사용하는 파일명 및 경로 수정
        - 테스트용 더미 AiosData 데이터 생성
        '''
        self.model_simulator = ModelSimulator()
        test_dir = "d:/test_simulator/"
        if "test_simulator" in os.listdir("d:/"):
            import shutil
            shutil.rmtree("/test_simulator")
        os.mkdir(test_dir)
        info_cfx_status['path'] = test_dir
        info_cfx_status['name'] ="CFX_status.csv"
        info_elevator_enable['path'] = test_dir
        info_elevator_enable['name'] = "CFX_status.csv"
        info_plate_exist['path'] = test_dir
        info_plate_exist['name'] = "Method_status.csv"
        info_method_status['path'] = test_dir
        info_method_status['name'] = "Method_status.csv"
        info_trc['path'] = test_dir
        info_trc['name'] = "test.trc"
        self.test_aiosdata = AiosData(
            cfx_status = contents_cfx_status,
            method_status = contents_method_status,
            elevator_enable = "",
            plate_exist = "",
            method_run = "0",
            elevator_request = "0",
            plrn1_name = "test_plrn1.plrn",
            plrn2_name = "test_plrn2.plrn",
            message = "test message",
            cfx1_time = "00:00:00",
            cfx2_time = "01:23:45",
            control_status = '3'
        )
    def tearDown(self) -> None: #기본 테스트 함수, 각 테스트 수행 시마다 자동으로 호출
        '''
        유닛 테스트 수행 후 뒷처리 작업 수행
        '''
        pass
    def test_value_method_of_model(self):
        self.assertEqual("Non existing",
                         self.model_simulator.value.elevator_enable,
                         msg="파일 확인용, 파일 자체가 없으므로 없다고 해야 함")
        self.assertEqual("Non existing",
                         self.model_simulator.value.plate_exist,
                         msg="파일 확인용, 파일 자체가 없으므로 없다고 해야 함")
        FileChecker(**info_cfx_status).contents = self.test_aiosdata.cfx_status #CFX_status.csv 생성
        self.model_simulator.value = self.test_aiosdata #Method_status.csv, test.trc 생성
        self.assertEqual([['Method', 'run,', '0'],
                          ['Elevator', 'requeset,', '0'],
                          ['Plrn1,', 'test_plrn1.plrn'],
                          ['Plrn2,', 'test_plrn2.plrn']],
                        contents_method_status,
                        "파일 생성 시 contents_method_status를 수정, 내용이 위와 같아야 함")
        self.assertEqual("Existing",
                         self.model_simulator.value.elevator_enable,
                         msg="파일 확인용, 생성 이후이므로 있다고 해야 함")
        self.assertEqual("Existing",
                         self.model_simulator.value.plate_exist,
                         msg="파일 확인용, 생성 이후이므로 있다고 해야 함")
        self.assertEqual(self.model_simulator.value.cfx_status,
                        contents_cfx_status,
                        "method_status.csv파일을 읽어 이를 그대로 cfx_status에 저장 후 비교, 같아야 함")
        self.assertEqual([self.test_aiosdata.message],
                         FileChecker(**info_trc).contents,
                         "생성된 trc 파일을 txt로 읽어 비교한다. 같아야 한다.")

if __name__ == "__main__":
    unittest.main()