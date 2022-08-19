'''
STARlet Simulatior의 프레젠터 역할을 수행하는 모듈이다.
모델에게서는 AiosData 객체를 얻어와 이로부터 필요한 정보를 얻는다.
각 뷰 객체에게는
'''
import threading
import time
from view_simulator import ViewSimulator, window_frame
from model_simulator import ModelSimulator, AiosData
from tkinter import messagebox
class PresenterSimulator:
    '''
    STARlet Simuator의 presenter. Simulator의 전체적인 동작을 여기서 총괄한다.
    '''
    def __init__(self):
        self.view_simulator = ViewSimulator()
        self.model_simulator = ModelSimulator()
        self.aios_data = self.model_simulator.value
        self.view_simulator.button_abort1.command_list = self.__command_abort1_button
        self.view_simulator.button_abort2.command_list = self.__command_abort2_button
        self.view_simulator.button_abort3.command_list = self.__command_abort3_button
        self.view_simulator.button_run.command_list = self.__command_run_button
        simulator_thread = threading.Thread(target=self.__periodic_func)
        simulator_thread.start()
        window_frame.mainloop()

    def __periodic_func(self):
        '''
        presenter에서 자체 동작하는 쓰레드 함수
        1초마다 동작해서 model 객체로부터 AiosData를 읽고 필요한 정보를 갱신한다.
        정보가 달라지면 label frame을 갱신한다.
        '''
        while True:
            if self.sec_timer>0:
                self.sec_timer -=1

            value = self.model_simulator.value
            if value.cfx_status != self.aios_data.cfx_status:
                self.view_simulator.cfx_status.contents = value.cfx_status
            if value.elevator_enable != self.aios_data.elevator_enable:
                self.view_simulator.elevator_enable.contents = value.elevator_enable
            if value.plate_exist != self.aios_data.plate_exist:
                self.view_simulator.plate_exist.contents = value.plate_exist
            if value.method_status != self.aios_data.method_status:
                self.view_simulator.method_status.contents = value.method_status
            self.aios_data = value
            time.sleep(1)

    def __check_cfx_is_available(self, scenario:str)->bool:
        if self.aios_data.cfx1_time == '00:00:00':
            if self.aios_data.cfx2_time == '00:00:00':
                return True #scenario와 무관하게 무조건 true
            elif scenario == '1plate':
                return True #1plate scenario 이므로 true
        elif self.aios_data.cfx2_time == '00:00:00':
            if scenario == '1plate':
                return True #1plate scenario 이므로 true
            else:
                return False #2plate scenario 이므로 False
        else:
            return False #모든 CFX 동작 중이므로 False

    def __command_run_button(self):
        pass

    def __command_abort3_button(self):
        '''
        Abort3 버튼 객체에 추가될 메서드. Abort3 시나리오를 수행
        버튼의 상태가 'normal'이면 STARlet 정지 구현
        버튼의 상태가 'active'이면 Abort3 시나리오 구현
        '''
        if self.view_simulator.button_abort3.contents == 'normal':
            self.__simulate_stop_starlet()
            return
        elif self.view_simulator.button_abort3.contents == 'active':
            if self.__check_cfx_is_available('1plate'):
                self.__simulate_run_starlet()
                self.sec_timer = 5
                while self.sec_timer:
                    pass
                self.__simulate_elevator_request_1st()
                self.sec_timer = 30
                while self.sec_timer:
                    if "88:88:88" in (self.aios_data.cfx1_time, self.aios_data.cfx2_time):
                        self.__simulate_plate_transfer_1st()
                        return
                messagebox.showinfo("경고","Abort3 시나리오를 실패했습니다.")
            else:
                messagebox.showinfo("경고","CFX 장비가 모두 동작 중입니다.")

    def __command_abort2_button(self)->None:
        '''
        Abort2 버튼 객체에 추가될 메서드. Abort2 시나리오를 수행
        버튼의 상태가 'normal'이면 STARlet 정지 구현
        버튼의 상태가 'active'이면 Abort2 시나리오 구현
        '''
        if self.view_simulator.button_abort2.contents == 'normal':
            self.__simulate_stop_starlet()
            return
        elif self.view_simulator.button_abort2.contents == 'active':
            if self.__check_cfx_is_available('1plate'):
                self.__simulate_run_starlet()
                #messagebox.showinfo("알림","Abort2 시나리오를 시작합니다.")
                self.sec_timer = 5
                while self.sec_timer:
                    pass
                self.__simulate_elevator_request_1st()
                self.sec_timer = 30
                while self.sec_timer:
                    if '88:88:88' in (self.aios_data.cfx1_time, self.aios_data.cfx2_time):
                        break
                self.__simulate_abort_starlet()
            else:
                messagebox.showinfo("경고","CFX 장비가 모두 동작 중입니다.")

    def __command_abort1_button(self):
        '''
        Abort1 버튼 객체에 추가될 메서드. Abort1 시나리오를 수행
        버튼의 상태가 'normal'이면 STARlet 정지 구현
        버튼의 상태가 'active'이면 Abort1 시나리오 구현
        '''
        if self.view_simulator.button_abort1.contents == 'normal':
            self.__simulate_stop_starlet()
        elif self.view_simulator.button_abort1.contents == 'active':
            self.__simulate_abort_starlet()
            #messagebox.showinfo("알림","Abort1 시나리오를 시작합니다.")

    def __simulate_abort_starlet(self):
        self.aios_data.method_run = '2'
        self.model_simulator.value = self.aios_data

    def __simulate_stop_starlet(self):
        self.aios_data.method_run = '0'
        self.aios_data.elevator_request = '0'
        self.aios_data.plrn1_name = ""
        self.aios_data.plrn2_name = ""
        self.model_simulator.value = self.aios_data

    def __simulate_run_starlet(self):
        self.aios_data.method_run = '1'
        self.aios_data.elevator_request = '0'
        plrn_info = self.view_simulator.get_plrn()
        if plrn_info['scenario'] == '1plate':
            self.aios_data.plrn1_name = plrn_info['plrn1_name']
            self.aios_data.plrn2_name = ''
        self.model_simulator.value = self.aios_data

    def __simulate_elevator_request_1st(self):
        self.aios_data.elevator_request = '1 plrn1'
        self.model_simulator.value = self.aios_data

    def __simulate_elevator_request_2nd(self):
        self.aios_data.elevator_request = '1 plrn2'
        self.model_simulator.value = self.aios_data

    def __simulate_plate_transfer_1st(self):
        self.aios_data.elevator_request = '2 plrn1'
        self.model_simulator.value = self.aios_data

    def __simulate_plate_transfer_2nd(self):
        self.aios_data.elevator_request = '2 plrn2'
        self.model_simulator.value = self.aios_data

if __name__ == '__main__':
    simulator = PresenterSimulator()
