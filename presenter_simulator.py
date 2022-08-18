'''
STARlet Simulatior의 프레젠터 역할을 수행하는 모듈이다.
모델에게서는 AiosData 객체를 얻어와 이로부터 필요한 정보를 얻는다.
각 뷰 객체에게는
'''
import threading
import time
from view_simulator import ViewSimulator, window_frame
from model_simulator import ModelSimulator, AiosData

class PresenterSimulator:
    '''
    STARlet Simuator의 presenter. Simulator의 전체적인 동작을 여기서 총괄한다.
    '''
    aiosdata = AiosData()

    def __init__(self):
        self.view_simulator = ViewSimulator()
        self.model_simulator = ModelSimulator()
        simulator_thread = threading.Thread(target=self._periodic_func)
        simulator_thread.start()
        window_frame.mainloop()
    def _update_label_frame(self, value:AiosData):
        '''
        AiosData를 인수로 받은 다음 자신의 AiosData와 비교한다.
        다른 부분이 있으면 관련 labelframe의 메시지를 업데이트 한다.
        마지막으로 자신의 AiosData를 갱신한다.
        '''
        if value.cfx_status != self.cfx_status:
            self.view_simulator.cfx_status.contents = value.cfx_status
        if value.elevator_enable != self.elevator_enable:
            self.view_simulator.elevator_enable.contents = value.elevator_enable
        if value.plate_exist != self.plate_exist:
            self.view_simulator.plate_exist.contents = value.plate_exist
        if value.method_status != self.method_status:
            self.view_simulator.method_status.contents = value.method_status
        self.aiosdata = value
    def _periodic_func(self):
        '''
        presenter에서 자체 동작하는 쓰레드 함수
        1초마다 동작해서 model 객체로부터 AiosData를 읽고 label frame을 갱신한다.
        '''
        while True:
            # model_simulator.value
            self._update_label_frame(self.model_simulator.value)
            time.sleep(1)

if __name__ == '__main__':
    simulator = PresenterSimulator()
