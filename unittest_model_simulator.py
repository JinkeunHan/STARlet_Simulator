from dataclasses import dataclass
from model_simulator import ModelSimulator, AiosData, _FileChecker
import os
import unittest

class TestModelSimulator(unittest.TestCase):
    def setUp(self) -> None: #기본 테스트 함수, 각 테스트 수행 시마다 자동으로 호출
        self.model_simulator = ModelSimulator()
        test_dir = "d:/test_simulator/"
        if "test_simulator" in os.listdir("d:/"):
            import shutil
            shutil.rmtree("/test_simulator")
        os.mkdir(test_dir)
        self.model_simulator.info_cfx_status = (test_dir,"test.csv")
        self.model_simulator.info_elevator_enable = (test_dir,"test.csv")
        self.model_simulator.info_plate_exist = (test_dir,"test.csv")
        self.model_simulator.info_method_status = (test_dir,"test.csv")
        self.model_simulator.info_trc = (test_dir,"test.trc")
        self.test = AiosData(
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
    def tearDown(self) -> None:
        pass
    def test_value_method_of_model(self):
        self.assertEqual("Non existing",
                         self.model_simulator.value.elevator_enable,
                         msg="파일 확인용, 파일 자체가 없으므로 없다고 해야 함")
        self.assertEqual("Non existing",
                         self.model_simulator.value.plate_exist,
                         msg="파일 확인용, 파일 자체가 없으므로 없다고 해야 함")
        self.model_simulator.value = self.test # method_status.csv, elevator_enable.csv, 
                                               #plate_exist.csv 파일 생성
        self.assertEqual([['Method', 'run,', '0'],
                          ['Elevator', 'requeset,', '0'],
                          ['Plrn1,', 'test_plrn1.plrn'],
                          ['Plrn2,', 'test_plrn2.plrn']],
                        self.model_simulator.contents_method_status,
                        "파일 생성 중 contents_method_status를 수정, 내용이 위와 같아야 함")
        self.assertEqual("Existing",
                         self.model_simulator.value.elevator_enable,
                         msg="파일 확인용, 생성 이후이므로 있다고 해야 함")
        self.assertEqual("Existing",
                         self.model_simulator.value.plate_exist,
                         msg="파일 확인용, 생성 이후이므로 있다고 해야 함")
        self.assertEqual(self.model_simulator.value.cfx_status,
                        self.model_simulator.contents_method_status,
                        "method_status.csv파일을 읽어 이를 그대로 cfx_status에 저장 후 비교, 같아야 함")
        self.assertEqual([self.test.message],
                         _FileChecker(*self.model_simulator.info_trc).contents,
                         "생성된 trc 파일을 txt로 읽어 비교한다. 같아야 한다.")

if __name__ == "__main__":
    unittest.main()