'''
STARlet Simulatior의 프레젠터 역할을 수행하는 모듈이다.
View와 Model의 메서드를 조합하여 상위 메서드를 구현, 목표로 하는 기능을 구현한다.
'''
import threading
import time
from tkinter import Tk, messagebox
from xmlrpc.client import boolean
from view_simulator import ViewSimulator, window_frame
from model_simulator import AiosData, ModelSimulator, trc_file_contents

info_message:dict = {
    'info_0':{'m_type':'info', 'message':'STARlet이 Abort 되었습니다.', 'time_sec':3},
    'info_1':{'m_type':'info', 'message':'엘리베이터 모듈에 플레이트를 놓고 OK를 눌러주세요.', 'time_sec':30},
    'info_2':{'m_type':'info', 'message':'Abort1 시나리오를 시작합니다.', 'time_sec':3},
    'info_3':{'m_type':'info', 'message':'Abort1 시나리오 완료.', 'time_sec':3},
    'info_4':{'m_type':'info', 'message':'Abort1 시나리오 실패', 'time_sec':3},
    'info_5':{'m_type':'info', 'message':'Abort2 시나리오를 시작합니다.', 'time_sec':3},
    'info_6':{'m_type':'info', 'message':'Abort2 시나리오 완료', 'time_sec':3},
    'info_7':{'m_type':'info', 'message':'Abort2 시나리오 실패', 'time_sec':3},
    'info_8':{'m_type':'info', 'message':'Abort3 시나리오를 시작합니다.', 'time_sec':3},
    'info_9':{'m_type':'info', 'message':'Abort3 시나리오 완료', 'time_sec':3},
    'info_10':{'m_type':'info', 'message':'Abort3 시나리오 실패', 'time_sec':3},
}
warning_message:dict = {
    'warn_0':{'m_type':'warning', 'message':"CFX 장비가 동작 중입니다.", 'time_sec':3},
}
error_message:dict = {
    'err_0':{'m_type':'error', 'message':'모듈이 정해진 시간(30초) 안에 도착하지 않았습니다.', 'time_sec':3},
    'err_1':{'m_type':'error', 'message':'엘리베이터 모듈의 움직임이 감지되지 않았습니다.', 'time_sec':3},
}
class PresenterSimulator(ModelSimulator, ViewSimulator):
    '''
    STARlet Simuator의 presenter. Simulator의 전체적인 동작을 여기서 총괄한다.
    '''
    def __init__(self):
        ModelSimulator.__init__(self)
        ViewSimulator.__init__(self)
        self._time_is = 0
        self.button_1plate.command_list = self._command_plate_button
        self.button_2plate.command_list = self._command_plate_button
        self.button_abort1.command_list = self._command_abort1_button
        self.button_abort2.command_list = self._command_abort2_button
        self.button_abort3.command_list = self._command_abort3_button
        self.button_run.command_list = self._command_run_button
        self.button_error1.command_list = self._command_error1_button
        self.button_error2.command_list = self._command_error2_button
        self.button_error3.command_list = self._command_error3_button
        self.button_error4.command_list = self._command_error4_button
        self.button_error5.command_list = self._command_error5_button
        self.button_error6.command_list = self._command_error6_button
        self.button_reset1.command_list = self._command_reset1_button
        self.button_reset2.command_list = self._command_reset2_button

    def _start(self):
        simulator_thread = threading.Thread(target=self._periodic_func)
        simulator_thread.start()
        window_frame.mainloop()

    def _periodic_func(self):
        '''
        presenter에서 자체 동작하는 쓰레드 함수
        1초마다 file_data 메서드를 호출, AiosData를 읽고 하기 화면을 갱신한다.
        - CFX_status.csv, Plate_exist.csv, Elevator_enable.csv
        '''
        while True:
            if (temp_time:=self._time_is)>0:
                now = time.ctime(time.time())
                print(now + f", Remain time is {self._time_is}")
                self._time_is = temp_time-1
            value:AiosData = self.file_data
            self.elevator_enable.message_is = value.elevator_enable
            self.plate_exist.message_is = value.plate_exist
            self.cfx_status.message_is = self.__convert_cfx_info_for_display(value)
            self.method_status.message_is = self.__convert_method_info_for_display(value)
            time.sleep(1)
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

    def _command_plate_button(self)->None:
        '''
        1plate 및 2plate 버튼에 command_list 메서드를 통해 추가될 메서드
        두 버튼의 상태가 모두 보통 상태면 STARlet의 정지 상태를 모사한다.
        '''
        if self.button_2plate.state_is == self.button_1plate.state_is =='normal':
            self.__simulate_stop_starlet()

    def _command_abort1_button(self)->None:
        '''
        Abort1 버튼 객체에 추가될 메서드. Abort1 시나리오를 수행
        버튼의 상태가 'normal'이면 STARlet 정지 구현
        버튼의 상태가 'active'이면 Abort1 시나리오 구현
        Abort1 시나리오: STARlet 동작 중 STARlet Abort 발생
        '''
        if self.button_abort1.state_is == 'normal':
            self.__simulate_stop_starlet()
        elif self.button_abort1.state_is == 'active':
            self.button_abort1.state_is = 'inactive'
            self.__simulate_run_starlet()
            self.__show_messagebox(**info_message['info_2'])
            for _ in self.__delay_sec(5):
                pass#의도적 지연. 사용자의 상태 변화 인식을 위함
            self.__simulate_abort_starlet()
            self.__show_messagebox(**info_message['info_3'])
            self.button_abort1.state_is = 'active'

    def _command_abort2_button(self)->None:
        '''
        Abort2 버튼 객체에 추가될 메서드. Abort2 시나리오를 수행
        버튼의 상태가 'normal'이면 STARlet 정지 구현
        버튼의 상태가 'active'이면 Abort2 시나리오 구현
        Abort2 시나리오: STARlet에게서 플레이트 수령 실패
        '''
        if self.button_abort2.state_is == 'normal':
            self.__simulate_stop_starlet()
        elif self.button_abort2.state_is == 'active':
            if self.__check_cfx_is_available('1plate'):
                self.button_abort2.state_is = 'inactive'
                self.__show_messagebox(**info_message['info_5'])
                self.__simulate_run_starlet()
                for _ in self.__delay_sec(5):
                    pass#의도적 지연. 사용자의 상태 변화 인식을 위함
                self.__simulate_elevator_request_1st()
                if self.__waiting_for_elevator_enable_file_creation():
                    self.__simulate_plate_transfer_1st()
                    self.__show_messagebox(**info_message['info_6'])
                else:
                    self.__show_messagebox(**info_message['info_7'])
                    self.__show_messagebox(**error_message['err_0'])
                self.button_abort2.state_is = 'active'
            else:
                self.__show_messagebox(**warning_message['warn_0'])

    def _command_abort3_button(self)->None:
        '''
        Abort3 버튼 객체에 추가될 메서드. Abort3 시나리오를 수행
        버튼의 상태가 'normal'이면 STARlet 정지 구현
        버튼의 상태가 'active'이면 Abort3 시나리오 구현
        Abort3 시나리오: STARlet 모듈 호출 시 정해진 시간 이내에 도달 실패
        '''
        if self.button_abort3.state_is == 'normal':
            self.__simulate_stop_starlet()
        elif self.button_abort3.state_is == 'active':
            if self.__check_cfx_is_available('1plate'):
                self.button_abort3.state_is = 'inactive'
                self.__simulate_run_starlet()
                self.__show_messagebox(**info_message['info_8'])
                for _ in self.__delay_sec(5):
                    pass#의도적 지연. 사용자의 상태 변화 인식을 위함
                self.__simulate_elevator_request_1st()
                if self.__check_module_move_within_times(30):
                    self.__simulate_abort_starlet()
                    self.__show_messagebox(**info_message['info_9'])
                else:
                    self.__show_messagebox(**info_message['info_10'])
                    self.__show_messagebox(**error_message['err_1'])
                self.button_abort3.state_is = 'active'
            else:
                self.__show_messagebox(**warning_message['warn_0'])

    def _command_run_button(self)->None:
        '''
        Run 버튼 객체에 추가될 메서드. Auto Run 시나리오를 수행
        버튼의 상태가 'normal'이면 STARlet 정지 구현
        버튼의 상태가 'active'이면 Auto Run 시나리오 구현
        plrn 정보를 바탕으로 1plate 또는 2plate 시나리오를 수행한다.
        '''
        if self.button_run.state_is == 'normal':
            self.__simulate_stop_starlet()
        elif self.button_run.state_is == 'active':
            plrn_info = self.plrn_info_is
            if self.__check_cfx_is_available(plrn_info['scenario']):
                self.button_run.state_is = 'inactive'
                if not self._run_1st_plate() or plrn_info['scenario'] == '1plate':
                    pass # 1st plate transfer failure or 1plate scenario complete
                elif plrn_info['scenario'] == '2plate':
                    self._run_2nd_plate()
                self.button_run.state_is = 'active'
            else:
                self.__show_messagebox(**warning_message['warn_0'])

    def _run_1st_plate(self)->bool:
        '''
        1plate 또는 2plate 시나리오에서 첫 번째 플레이트를 전달할 때 사용하는 메서드
        1) elevator 모듈을 요청한다.
        2) 시간 내에 엘리베이터 모듈이 도착하면 플레이트를 놓으라고 한다.
        3) 사용자가 놓으면 plate를 전달했음을 알린다.
        '''
        sentence = ("Start auto run scenario with 1st plate\n")
        self.control_log.message_is = sentence
        self.__simulate_run_starlet()
        for _ in self.__delay_sec(5):
            pass#의도적 지연. 사용자의 상태 변화 인식을 위함
        self.__simulate_elevator_request_1st()
        if not self.__waiting_for_elevator_enable_file_creation(): #비동기 동작 메서드
            sentence = ("Transfer failure. Elevator module didn't arrive\n")
            self.control_log.message_is = sentence
            self.__show_messagebox(**error_message['err_0'])
            self.button_run.state_is = 'active'
            return False
        sentence = ("Elevator module arrived. Try to transfer 1st plate\n")
        self.control_log.message_is = sentence
        self.__show_messagebox(**info_message['info_1'])
        self.__simulate_plate_transfer_1st()
        return True

    def _run_2nd_plate(self)->bool:
        '''
        2plate 시나리오에서 두 번째 플레이트를 전달할 때 사용하는 메서드
        1) 첫 번째 플레이트가 CFX1에 도달, CFX1이 동작할 때까지 대기한다.
        2) elevator 모듈을 요청한다.
        3) 시간 내에 엘리베이터 모듈이 도착하면 플레이트를 놓으라고 한다.
        4) 사용자가 놓으면 plate를 전달했음을 알린다.
        '''
        sentence = ("Start auto run scenario with 2nd plate\n")
        self.control_log.message_is = sentence
        self.__simulate_run_starlet()
        if self.__waiting_for_cfx_remain_time_change():
            self.__simulate_elevator_request_2nd()
            if not self.__waiting_for_elevator_enable_file_creation(): #비동기 동작 메서드
                sentence = ("Transfer failure. Elevator module didn't arrive\n")
                self.control_log.message_is = sentence
                self.__show_messagebox(**error_message['err_0'])
                self.button_run.state_is = 'active'
                return False
            sentence = ("Elevator module arrived. Try to transfer 2nd plate\n")
            self.control_log.message_is = sentence
            self.__show_messagebox(**info_message['info_1'])
            self.__simulate_plate_transfer_2nd()
            return True
        sentence = ('''Failure to auto run scenario with 2nd plate\n.
                     Failed to check cfx1's operation in 15 min\n''')
        self.control_log.message_is = sentence
        return False

    def _command_error1_button(self)->None:
        '''
        Error1 버튼이 눌렸을 시 대응
        1) 정해진 문장을 trc 파일에 쓴다.
        2) Starlet의 abort 상태를 모방한다.
        '''
        self.__simulate_run_starlet()
        for _ in self.__delay_sec(1):
            pass#의도적 지연. 사용자의 상태 변화 인식을 위함
        value:AiosData
        value.message = trc_file_contents['Error1']
        self.file_data = value
        sentence = f"Error1 button is clicked. Write {trc_file_contents['Error1']}"
        self.control_log.message_is = sentence
        self.__simulate_abort_starlet()

    def _command_error2_button(self)->None:
        '''
        Error2 버튼이 눌렸을 시 대응
        1) 정해진 문장을 trc 파일에 쓴다.
        2) Starlet의 abort 상태를 모방한다.
        '''
        self.__simulate_run_starlet()
        for _ in self.__delay_sec(1):
            pass#의도적 지연. 사용자의 상태 변화 인식을 위함
        value:AiosData
        value.message = trc_file_contents['Error2']
        self.file_data = value
        sentence = (f"Error2 button is clicked. Write {trc_file_contents['Error2']}")
        self.control_log.message_is = sentence
        self.__simulate_abort_starlet()

    def _command_error3_button(self)->None:
        '''
        Error3 버튼이 눌렸을 시 대응
        1) 정해진 문장을 trc 파일에 쓴다.
        2) Starlet의 abort 상태를 모방한다.
        '''
        self.__simulate_run_starlet()
        while self.__delay_sec(1):
            pass#의도적 지연. 사용자의 상태 변화 인식을 위함
        value:AiosData
        value.message = trc_file_contents['Error3']
        self.file_data = value
        sentence = (f"Error3 button is clicked. Write {trc_file_contents['Error3']}")
        self.control_log.message_is = sentence
        self.__simulate_abort_starlet()

    def _command_error4_button(self)->None:
        '''
        Error4 버튼이 눌렸을 시 대응
        1) 정해진 문장을 trc 파일에 쓴다.
        2) Starlet의 abort 상태를 모방한다.
        '''
        self.__simulate_run_starlet()
        while self.__delay_sec(1):
            pass#의도적 지연. 사용자의 상태 변화 인식을 위함
        value:AiosData
        value.message = trc_file_contents['Error4']
        self.file_data = value
        self.trc_file.write_file([trc_file_contents['Error4']])
        sentence = (f"Error4 button is clicked. Write {trc_file_contents['Error4']}")
        self.control_log.message_is = sentence
        self.__simulate_abort_starlet()

    def _command_error5_button(self)->None:
        '''
        Error5 버튼이 눌렸을 시 대응
        1) 정해진 문장을 trc 파일에 쓴다.
        2) Starlet의 abort 상태를 모방한다.
        '''
        self.__simulate_run_starlet()
        while self.__delay_sec(1):
            pass#의도적 지연. 사용자의 상태 변화 인식을 위함
        value:AiosData
        value.message = trc_file_contents['Error5']
        self.file_data = value
        sentence = (f"Error5 button is clicked. Write {trc_file_contents['Error5']}")
        self.control_log.message_is = sentence
        self.__simulate_abort_starlet()

    def _command_error6_button(self)->None:
        '''
        Error6 버튼이 눌렸을 시 대응
        1) 정해진 문장을 trc 파일에 쓴다.
        2) Starlet의 abort 상태를 모방한다.
        '''
        self.__simulate_run_starlet()
        while self.__delay_sec(1):
            pass#의도적 지연. 사용자의 상태 변화 인식을 위함
        value:AiosData
        value.message = trc_file_contents['Error6']
        self.file_data = value
        sentence = (f"Error6 button is clicked. Write {trc_file_contents['Error6']}")
        self.control_log.message_is = sentence
        self.__simulate_abort_starlet()

    def _command_reset1_button(self)->None:
        '''
        Reset1 버튼이 눌렸을 시 대응
        1) 정해진 문장을 trc 파일에 쓴다.
        2) Starlet의 abort 상태를 모방한다.
        '''
        value:AiosData
        value.message = trc_file_contents['Reset1']
        self.file_data = value
        sentence = (f"Reset1 button is clicked. Write {trc_file_contents['Reset1']}")
        self.control_log.message_is = sentence
        self.__simulate_run_starlet()

    def _command_reset2_button(self)->None:
        '''
        Reset1 버튼이 눌렸을 시 대응
        1) 정해진 문장을 trc 파일에 쓴다.
        2) Starlet의 abort 상태를 모방한다.
        '''
        value:AiosData
        value.message = trc_file_contents['Reset2']
        self.file_data = value
        sentence = (f"Reset1 button is clicked. Write {trc_file_contents['Reset2']}")
        self.control_log.message_is = sentence
        self.__simulate_run_starlet()

    def __show_messagebox(self, m_type:str, message:str, time_sec:int = 3)->None:
        '''
        Abort1, Abort2, Abort3 및 Run 버튼을 눌러 각 시나리오를 테스트할 시
        관련 정보를 사용자에게 제공하기 위한 메시지 박스
        정해진 시간이 지나면 자동으로 사라진다.
        '''
        root = Tk()
        root.withdraw()
        if time_sec:
            time_out = time_sec * 1000
        root.after(time_out, root.destroy)
        if m_type == 'info':
            messagebox.showinfo('Info', message, master=root)
        elif m_type == 'warning':
            messagebox.showwarning('Warning', message, master=root)
        elif m_type == 'error':
            messagebox.showerror('Error', message, master=root)
        sentence = (f"{m_type} : {message} printed\n")
        self.control_log.message_is = sentence

    def __check_module_move_within_times(self, time_sec:int = 30)->bool:
        '''
        설정한 시간동안 handler를 관찰, 이 시간 내 plate hanlder가 움직이면 True
        시간이 초과될 동안 오지 않으면 False 반환
        CFX_status.csv 내 시간 값이 88:88:88이면 움직이는 것으로 간주.
        '''
        sentence = ("Waiting for elevator module's movement.\n")
        self.control_log.message_is = sentence
        for _ in self.__delay_sec(time_sec):
            cfx_info = self.aios_data_is
            if "88:88:88" in (cfx_info.cfx1_time, cfx_info.cfx2_time):
                sentence = ("elevator is moving now\n")
                self.control_log.message_is = sentence
                return True
        sentence = ("elevator module didn't arrive in 30 seconds\n")
        self.control_log.message_is = sentence
        return False

    def __check_cfx_is_available(self, scenario:str)->bool:
        '''
        CFX#1과 #2의 남은 시간과 동작할 시나리오에 맞춰 CFX가 시나리오에
        맞춰 동작 가능한지 판단하고 이를 반환한다.
        '''
        value = self.aios_data_is
        sentence = ("Check CFX remain time\n")
        self.control_log.message_is = sentence
        if value.cfx1_time == '00:00:00':
            result = True if value.cfx2_time == '00:00:00' else (scenario == '1plate')
        elif value.cfx2_time == '00:00:00':
            result = (scenario == '1plate')
        else:
            result = False #모든 CFX 동작 중이므로 False
        if result:
            sentence = (f"For {scenario} scenario, CFX is available\n")
            self.control_log.message_is = sentence
        else:
            sentence = ("CFX is not available\n")
            self.control_log.message_is = sentence
        return result

    def __convert_method_info_for_display(self, value:AiosData)->list:
        '''
        AiosData를 method_status 라벨 프레임에 표시할 때 사용하는 메서드
        AiosData를 읽고 적절한 리스트로 변환한다.
        '''
        temp_method_status = [
            ['Method run,', ''],
            ['Elevator requeset,', ''],
            ['Plrn1,', ''],
            ['Plrn2,', ''],
            ]
        temp_method_status[0][1] = value.method_run
        temp_method_status[1][1] = value.elevator_request
        temp_method_status[2][1] = value.plrn1_name
        temp_method_status[3][1] = value.plrn2_name
        return temp_method_status

    def __convert_cfx_info_for_display(self, value:AiosData)->list:
        '''
        AiosData를 cfx_status 라벨 프레임에 표시할 때 사용하는 메서드
        AiosData를 읽고 적절한 리스트로 변환한다.
        '''
        temp_cfx_status = [
            ['CFX#1', ''],
            ['CFX#2', ''],
            ['Control Status', '']
            ]
        temp_cfx_status[0][1] = value.cfx1_time
        temp_cfx_status[1][1] = value.cfx2_time
        temp_cfx_status[2][1] = value.control_status
        return temp_cfx_status

    def __simulate_abort_starlet(self):
        '''
        AiosData를 읽어온 다음 method_run 값을 조절,
        AIOS에게 STARlet이 Abort 되었음을 알린다.
        '''
        value = self.aios_data_is
        value.method_run = '2'
        self.file_data = value
        self.__show_messagebox(**info_message['info_0'])
        sentence = (f"Change method_staus.csv.{self.__convert_method_info_for_display(value)}\n")
        self.control_log.message_is = sentence

    def __simulate_stop_starlet(self):
        '''
        AIOS에게 STARlet이 정지하였음을 알린다.
        또한 plrn 정보를 없앤다.
        '''
        sentence = ("Stop starlet\n")
        self.control_log.message_is = sentence
        self.plrn_info_is = {'scenario':'','plrn_name':''}
        value = self.aios_data_is
        value.method_run = '0'
        value.elevator_request = '0'
        value.plrn1_name = ""
        value.plrn2_name = ""
        self.file_data = value
        sentence = (f"Change method_staus.csv.{self.__convert_method_info_for_display(value)}\n")
        self.control_log.message_is = sentence

    def __simulate_run_starlet(self):
        '''
        AiosData를 읽어온 다음 여기에 plrn 정보를 추가한다.
        그리고 AIOS에게 STARlet이 동작 중임을 알린다.
        '''
        method_status:AiosData = self.aios_data_is
        method_status.method_run = '1'
        method_status.elevator_request = '0'
        plrn_info = self.plrn_info_is
        method_status.plrn1_name = plrn_info['plrn_name']
        if plrn_info['scenario'] == '2plate':
            method_status.plrn2_name = plrn_info['plrn_name']
        else:
            method_status.plrn2_name = ''
        self.file_data = method_status
        sentence = "Change method_staus.csv."\
                +f"{self.__convert_method_info_for_display(method_status)}\n"
        self.control_log.message_is = sentence

    def __simulate_elevator_request_1st(self):
        '''
        첫 번쨰 플레이트를 전달하기 위해 AIOS에게
        엘리베이터 모듈을 요청한다.
        '''
        method_status:AiosData = self.aios_data_is
        method_status.elevator_request = '1,plrn1'
        self.file_data = method_status
        sentence = ("Call elevator module for 1st plate\n")
        self.control_log.message_is = sentence
        sentence = "Change method_staus.csv."\
                +f"{self.__convert_method_info_for_display(method_status)}\n"
        self.control_log.message_is = sentence

    def __simulate_elevator_request_2nd(self):
        '''
        두 번쨰 플레이트를 전달하기 위해 AIOS에게
        엘리베이터 모듈을 요청한다.
        '''
        method_status = self.aios_data_is
        method_status.elevator_request = '1,plrn2'
        self.file_data = method_status
        sentence = ("Call elevator module for 2nd plate\n")
        self.control_log.message_is = sentence
        sentence = "Change method_staus.csv."\
                +f"{self.__convert_method_info_for_display(method_status)}\n"
        self.control_log.message_is = sentence

    def __simulate_plate_transfer_1st(self)->None:
        '''
        AIOS에게 첫 번째 플레이트를 전달했음을 알린다.
        '''
        method_status = self.aios_data_is
        method_status.elevator_request = '2,plrn1'
        self.file_data = method_status
        sentence = ("Transfer 1st plate\n")
        self.control_log.message_is = sentence
        sentence = "Change method_staus.csv."\
                +f"{self.__convert_method_info_for_display(method_status)}\n"
        self.control_log.message_is = sentence
        self.__waiting_for_plate_exist_file_creation(300)
        for _ in self.__delay_sec(5):
            pass#의도적 지연. 사용자의 상태 변화 인식을 위함

    def __simulate_plate_transfer_2nd(self)->None:
        '''
        AIOS에게 두 번째 플레이트를 전달했음을 알린다.
        '''
        method_status = self.aios_data_is
        method_status.elevator_request = '2,plrn2'
        self.file_data = method_status
        sentence = ("Transfer 2nd plate\n")
        self.control_log.message_is = sentence
        sentence = "Change method_staus.csv."\
                +f"{self.__convert_method_info_for_display(method_status)}\n"
        self.control_log.message_is = sentence
        self.__waiting_for_plate_exist_file_creation(300)
        for _ in self.__delay_sec(5):
            pass#의도적 지연. 사용자의 상태 변화 인식을 위함

    def __waiting_for_plate_exist_file_creation(self, wtime)->bool:
        '''
        plate_exist.csv 파일이 생성될 때까지 대기한다.
        이 파일은 AIOS에 의해 생성된다. 일정 시간 대기하는 동안
        파일이 생성되면 True 아니면 False를 반환한다.
        '''
        sentence = ("waiting for 'place_exist.csv' ") + f"{wtime}seconds\n"
        self.control_log.message_is = sentence
        for _ in self.__delay_sec(wtime):
            if self.aios_data_is.plate_exist == "Existing":
                break
        return bool(self._time_is)

    def __waiting_for_elevator_enable_file_creation(self, wtime:int = 60)->bool:
        '''
        AIOS로부터 엘리베이터 모듈이 올 때까지 60초 대기한다.
        그 사이에 엘리베이터 모듈이 올라오면 True
        올라오지 않으면 False를 반환한다.
        '''
        sentence = (f"waiting for elevator module for {wtime} seconds\n")
        self.control_log.message_is = sentence
        for _ in self.__delay_sec(wtime):
            if self.aios_data_is.elevator_enable == 'Existing':
                break
        if bool(self._time_is):
            sentence = ("Elevator module arrived\n")
        else:
            sentence = ("elevator module didn't arrive\n")
        self.control_log.message_is = sentence
        return bool(self._time_is)

    def __waiting_for_cfx_remain_time_change(self, wtime:int = 9000)->bool:
        '''
        2plate 시나리오에서 두 번째 플레이트 전달 시 사용하는 메서드.
        CFX_status.csv 파일의 동작 시간은 CFX가 동작 상태가 되면
        그 시간이 00:00:00 또는 88:88:88에서 다른 것으로 변한다.
        그 외 disconnected를 감지하기 위해 99:99:99도 인식한다.
        이 시간대가 아닌 다른 시간이 되면 CFX1이 동작 상태가 되었다고 판단한다.
        '''
        sentence = (f"Wait until cfx1 runs for {wtime} seconds\n")
        self.control_log.message_is = sentence
        for _ in self.__delay_sec(wtime): #wait for elevator enable during 15 minuntes
            value:AiosData = self.aios_data_is
            if value.cfx1_time not in ("00:00:00", "88:88:88","99:99:99"):
                sentence = (f"Cfx runs. Its time is {value.cfx1_time} seconds\n")
                self.control_log.message_is = sentence
                break
        if not bool(self._time_is):
            sentence = ("CFX1 didn't run\n")
            self.control_log.message_is = sentence
        return bool(self._time_is)

    # def __delay_sec(self, seconds):
    #     self._time_is = seconds
    #     sentence = (f"Delay {seconds} seconds\n")
    #     self.control_log.message_is = sentence
    #     while self._time_is:
    #         window_frame.update()

    def __delay_sec(self, seconds)->bool:
        '''
        딜레이 기능의 완료 여부를 판단하기 위해 Generator로 구현, 
        Delay가 끝나면 False, Delay 중이면 True를 반환하도록 설계하였다.
        다른 함수에서 for _ in self.__delay_sec로 쓰이며, 처음 한 번은 
        무조건 for문 내부를 돌 수 있도록 처음엔 무조건 True를 반환하도록 설계하였다.
        '''
        self._time_is = seconds
        sentence = (f"Delay {seconds} seconds\n")
        self.control_log.message_is = sentence
        yield True
        while self._time_is:
            window_frame.update()
            yield True
        yield False

if __name__ == '__main__':
    simulator = PresenterSimulator()
    simulator._start()
