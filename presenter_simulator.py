'''
STARlet Simulatior의 프레젠터 역할을 수행하는 모듈이다.
'''
import threading
import time
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
    def _check_module_move_within_times(self, time_sec:int = 30)->bool:
        '''
        설정한 시간동안 handler를 관찰, 이 시간 내 plate hanlder가 움직이면 True
        시간이 초과될 동안 오지 않으면 False 반환
        '''
        self._time_is = time_sec
        while self._time_is:
            cfx_info = self.aios_data_is
            window_frame.update()
            if "88:88:88" in (cfx_info.cfx1_time, cfx_info.cfx2_time):
                return True
        return False

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
        '''
        AiosData를 읽어온 다음 method_run 값을 조절,
        AIOS에게 STARlet이 Abort 되었음을 알린다.
        '''
        value = self.aios_data_is
        value.method_run = '2'
        self.file_data = value
        messagebox.showinfo("알림","STARlet이 Abort 되었습니다.")

    def _simulate_stop_starlet(self):
        '''
        AIOS에게 STARlet이 정지하였음을 알린다.
        또한 plrn 정보를 없앤다.
        '''
        self.plrn_info_is = {}
        value = self.aios_data_is
        value.method_run = '0'
        value.elevator_request = '0'
        value.plrn1_name = ""
        value.plrn2_name = ""
        self.file_data = value

    def _simulate_run_starlet(self):
        '''
        AiosData를 읽어온 다음 여기에 plrn 정보를 추가한다.
        그리고 AIOS에게 STARlet이 동작 중임을 알린다.
        '''
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
        '''
        첫 번쨰 플레이트를 전달하기 위해 AIOS에게
        엘리베이터 모듈을 요청한다.
        '''
        method_status = self.aios_data_is
        method_status.elevator_request = '1 plrn1'
        self.file_data = method_status

    def _simulate_elevator_request_2nd(self):
        '''
        두 번쨰 플레이트를 전달하기 위해 AIOS에게
        엘리베이터 모듈을 요청한다.
        '''
        method_status = self.aios_data_is
        method_status.elevator_request = '1 plrn2'
        self.file_data = method_status

    def _simulate_plate_transfer_1st(self):
        '''
        AIOS에게 첫 번째 플레이트를 전달했음을 알린다.
        '''
        method_status = self.aios_data_is
        method_status.elevator_request = '2 plrn1'
        self.file_data = method_status

    def _simulate_plate_transfer_2nd(self):
        '''
        AIOS에게 두 번째 플레이트를 전달했음을 알린다.
        '''
        method_status = self.aios_data_is
        method_status.elevator_request = '2 plrn2'
        self.file_data = method_status

    def _simulate_elevator_wait(self)->bool:
        '''
        AIOS로부터 엘리베이터 모듈이 올 때까지 30초 대기한다.
        그 사이에 엘리베이터 모듈이 올라오면 True
        올라오지 않으면 False를 반환한다.
        '''
        self._time_is = 30
        while self._time_is: #wait for elevator enable during 30 seconds
            window_frame.update()
            if self.aios_data_is.elevator_enable == 'Existing':
                break
        return bool(self._time_is)

    def _delay_sec(self, seconds):
        self._time_is = seconds
        while self._time_is:
            window_frame.update()

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
                self._delay_sec(5)
                self._simulate_elevator_request_1st()
                if not self._simulate_elevator_wait():
                    messagebox.showerror("에러"," 모듈이 정해진 시간(30초) 안에 도착하지 않았습니다.")
                    return
                messagebox.showinfo("알림","엘리베이터 모듈에 플레이트를 놓고 OK를 눌러주세요.")
                self._simulate_plate_transfer_1st()
                if plrn_info['scenario'] == '1plate':
                    return
                self._simulate_elevator_request_2nd()
                if not self._simulate_elevator_wait():
                    messagebox.showerror("에러"," 모듈이 정해진 시간(30초) 안에 도착하지 않았습니다.")
                    return
                messagebox.showinfo("알림","엘리베이터 모듈에 플레이트를 놓고 OK를 눌러주세요.")
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
                self._delay_sec(5) #의도적 지연. 사용자로 하여금 상태 변화 인식을 위함
                self._simulate_elevator_request_1st()
                self._time_is = 30
                if self._simulate_elevator_wait():
                    self._simulate_abort_starlet()
                    messagebox.showinfo("알림","Abort3 시나리오 완료.")
                else:
                    messagebox.showinfo("주의","Abort3 시나리오 실패.")
            else:
                messagebox.showinfo("주의","CFX 장비가 모두 동작 중입니다.")

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
                messagebox.showinfo("알림","Abort2 시나리오를 시작합니다.")
                self._delay_sec(5) #의도적 지연. 사용자로 하여금 상태 변화 인식을 위함
                self._simulate_elevator_request_1st()
                if self._check_module_move_within_times(30):
                    self._simulate_abort_starlet()
                    messagebox.showinfo("알림","Abort2 시나리오 완료.")
                else:
                    messagebox.showinfo("주의","Abort2 시나리오 실패.")
            else:
                messagebox.showinfo("주의","CFX 장비가 모두 동작 중입니다.")
    def _command_abort1_button(self)->None:
        '''
        Abort1 버튼 객체에 추가될 메서드. Abort1 시나리오를 수행
        버튼의 상태가 'normal'이면 STARlet 정지 구현
        버튼의 상태가 'active'이면 Abort1 시나리오 구현
        '''
        if self.button_abort1.contents == 'normal':
            self._simulate_stop_starlet()
        elif self.button_abort1.contents == 'active':
            self._simulate_run_starlet()
            messagebox.showinfo("알림","Abort1 시나리오를 시작합니다.")
            self._delay_sec(3)
            self._simulate_abort_starlet()
            messagebox.showinfo("알림","Abort1 시나리오 완료.")

if __name__ == '__main__':
    simulator = PresenterSimulator()
