'''
STARlet Simulatior의 프레젠터 역할을 수행하는 모듈이다.
'''
import threading, time
from tkinter import messagebox
from view_simulator import ViewSimulator, window_frame
from model_simulator import ModelSimulator
class PresenterSimulator(ModelSimulator, ViewSimulator):
    '''
    STARlet Simuator의 presenter. Simulator의 전체적인 동작을 여기서 총괄한다.
    '''
    def __init__(self):
        ModelSimulator.__init__(self)
        ViewSimulator.__init__(self)
        self._time_is = 0
        self.button_abort1.command_list = self._command_abort1_button
        self.button_abort2.command_list = self._command_abort2_button
        self.button_abort3.command_list = self._command_abort3_button
        self.button_run.command_list = self._command_run_button
        simulator_thread = threading.Thread(target=self._periodic_func)
        simulator_thread.start()
        window_frame.mainloop()

    @property
    def _time_is(self)->int:
        '''
        내부 동작 타이머의 남은 시간 확인 메서드
        '''
        return self.__sec_time
    @_time_is.setter
    def _time_is(self, value:int)->None:
        '''
        내부 동작 타이머의 동작 시간 설정 메서드
        '''
        self.__sec_time = value

    def _periodic_func(self):
        '''
        presenter에서 자체 동작하는 쓰레드 함수
        1초마다 file_data 메서드를 호출, AiosData를 읽고 하기 화면을 갱신한다.
        - CFX_status.csv, Plate_exist.csv, Elevator_enable.csv
        '''
        while True:
            if (temp_time:=self._time_is)>0:
                self._time_is = temp_time-1
                print(f"Remain time is {self._time_is}")
            value = self.file_data
            self.cfx_status.contents = value.cfx_status
            self.elevator_enable.contents = value.elevator_enable
            self.plate_exist.contents = value.plate_exist
            self.method_status.contents = value.method_status
            time.sleep(1)

    def _check_cfx_is_available(self, scenario:str)->bool:
        '''
        CFX#1과 #2의 남은 시간과 동작할 시나리오에 맞춰 CFX가 시나리오에
        맞춰 동작 가능한지 판단하고 이를 판환한다.
        '''
        value = self.aios_data_is
        if value.cfx1_time == '00:00:00':
            result = True if value.cfx2_time == '00:00:00' else (scenario == '1plate')
        elif value.cfx2_time == '00:00:00':
            result = (scenario == '1plate')
        else:
            result = False #모든 CFX 동작 중이므로 False
        return result

    def _simulate_abort_starlet(self):
        method_status = self.aios_data_is
        method_status.method_run = '2'
        self.file_data = method_status

    def _simulate_stop_starlet(self):
        method_status = self.aios_data_is
        method_status.method_run = '0'
        method_status.elevator_request = '0'
        method_status.plrn1_name = ""
        method_status.plrn2_name = ""
        self.file_data = method_status

    def _simulate_run_starlet(self):
        method_status = self.aios_data_is
        method_status.method_run = '1'
        method_status.elevator_request = '0'
        plrn_info = self.plrn_info_is
        method_status.plrn1_name = plrn_info['plrn_name']
        if plrn_info['scenario'] == '2plate':
            method_status.plrn2_name = plrn_info['plrn_name']
        else:
            method_status.plrn2_name = ''
        self.file_data = method_status

    def _simulate_elevator_request_1st(self):
        method_status = self.aios_data_is
        method_status.elevator_request = '1 plrn1'
        self.file_data = method_status

    def _simulate_elevator_request_2nd(self):
        method_status = self.aios_data_is
        method_status.elevator_request = '1 plrn2'
        self.file_data = method_status

    def _simulate_plate_transfer_1st(self):
        method_status = self.aios_data_is
        method_status.elevator_request = '2 plrn1'
        self.file_data = method_status

    def _simulate_plate_transfer_2nd(self):
        method_status = self.aios_data_is
        method_status.elevator_request = '2 plrn2'
        self.file_data = method_status

    def _simulate_elevator_wait(self)->bool:
        self._time_is = 30
        return_value = True
        while self._time_is: #wait for elevator enable during 30 seconds
            if self.aios_data_is.elevator_enable == 'Existing':
                self._time_is = 0 #if elevator is ready, break while
        if self.aios_data_is.elevator_enable == 'Existing':
            messagebox.showinfo("알림","엘리베이터 모듈에 플레이트를 놓고 OK를 눌러주세요.")
        else:
            messagebox.showerror("에러"," 모듈이 정해진 시간(30초) 안에 도착하지 않았습니다.")
            return_value = False
        return return_value

    def _delay_sec(self, seconds):
        self._time_is = seconds
        while self._time_is:
            pass

    def _command_run_button(self)->None:
        '''
        Run 버튼 객체에 추가될 메서드. Auto Run 시나리오를 수행
        버튼의 상태가 'normal'이면 STARlet 정지 구현
        버튼의 상태가 'active'이면 Auto Run 시나리오 구현
        plrn 정보를 바탕으로 1plate 또는 2plate 시나리오를 수행한다.
        '''
        if self.button_run.contents == 'normal':
            self._simulate_stop_starlet()
        elif self.button_run.contents == 'active':
            plrn_info = self.plrn_info_is
            if self._check_cfx_is_available(plrn_info['scenario']):
                self._simulate_run_starlet()
                #self._delay_sec(5)
                window_frame.after(3000) # instead of delay, using after
                self._simulate_elevator_request_1st()
                if not self._simulate_elevator_wait():
                    return
                self._simulate_plate_transfer_1st()
                if plrn_info['scenario'] == '2plate':
                    window_frame.after(15*60*000) # instead of delay, using after
                    #self._delay_sec(15*60)
                    self._simulate_elevator_request_2nd()
                    if not self._simulate_elevator_wait():
                        return
                    self._simulate_plate_transfer_2nd()
            else:
                messagebox.showinfo("경고","CFX 장비가 동작 중입니다.")
                self.button_run.contents = 'normal'

    def _command_abort3_button(self)->None:
        '''
        Abort3 버튼 객체에 추가될 메서드. Abort3 시나리오를 수행
        버튼의 상태가 'normal'이면 STARlet 정지 구현
        버튼의 상태가 'active'이면 Abort3 시나리오 구현
        '''
        if self.button_abort3.contents == 'normal':
            self._simulate_stop_starlet()
        elif self.button_abort3.contents == 'active':
            if self._check_cfx_is_available('1plate'):
                self._simulate_run_starlet()
                self._delay_sec(5)
                self._simulate_elevator_request_1st()
                self._time_is = 30
                while self._time_is:
                    cfx_info = self.aios_data_is
                    if "88:88:88" in (cfx_info.cfx1_time, cfx_info.cfx2_time):
                        self._simulate_plate_transfer_1st()
                        return
                messagebox.showinfo("경고","Abort3 시나리오를 실패했습니다.")
            else:
                messagebox.showinfo("경고","CFX 장비가 모두 동작 중입니다.")

    def _command_abort2_button(self)->None:
        '''
        Abort2 버튼 객체에 추가될 메서드. Abort2 시나리오를 수행
        버튼의 상태가 'normal'이면 STARlet 정지 구현
        버튼의 상태가 'active'이면 Abort2 시나리오 구현
        '''
        if self.button_abort2.contents == 'normal':
            self._simulate_stop_starlet()
        elif self.button_abort2.contents == 'active':
            if self._check_cfx_is_available('1plate'):
                self._simulate_run_starlet()
                #messagebox.showinfo("알림","Abort2 시나리오를 시작합니다.")
                window_frame.after(5000)
                self._simulate_elevator_request_1st()
                window_frame.after(30*1000)
                cfx_info = self.aios_data_is
                if "88:88:88" in (cfx_info.cfx1_time, cfx_info.cfx2_time):
                    self._simulate_abort_starlet()
            else:
                messagebox.showinfo("경고","CFX 장비가 모두 동작 중입니다.")

    def _command_abort1_button(self)->None:
        '''
        Abort1 버튼 객체에 추가될 메서드. Abort1 시나리오를 수행
        버튼의 상태가 'normal'이면 STARlet 정지 구현
        버튼의 상태가 'active'이면 Abort1 시나리오 구현
        '''
        if self.button_abort1.contents == 'normal':
            self._simulate_stop_starlet()
        elif self.button_abort1.contents == 'active':
            self._simulate_abort_starlet()
            #messagebox.showinfo("알림","Abort1 시나리오를 시작합니다.")

if __name__ == '__main__':
    simulator = PresenterSimulator()
