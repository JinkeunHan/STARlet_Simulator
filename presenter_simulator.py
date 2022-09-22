'''
STARlet Simulatior의 프레젠터 역할을 수행하는 모듈이다.
'''
import threading
import time
from tkinter import Tk, messagebox
from view_simulator import ViewSimulator, window_frame
from model_simulator import AiosData, ModelSimulator

info_message:dict = {
    'info_0':{'m_type':'info', 'message':'STARlet이 Abort 되었습니다.', 'time_out':3000},
    'info_1':{'m_type':'info', 'message':'엘리베이터 모듈에 플레이트를 놓고 OK를 눌러주세요.', 'time_out':3000},
    'info_2':{'m_type':'info', 'message':'Abort1 시나리오를 시작합니다.', 'time_out':3000},
    'info_3':{'m_type':'info', 'message':'Abort1 시나리오 완료.', 'time_out':3000},
    'info_4':{'m_type':'info', 'message':'Abort1 시나리오 실패', 'time_out':3000},
    'info_5':{'m_type':'info', 'message':'Abort2 시나리오를 시작합니다.', 'time_out':3000},
    'info_6':{'m_type':'info', 'message':'Abort2 시나리오 완료', 'time_out':3000},
    'info_7':{'m_type':'info', 'message':'Abort2 시나리오 실패', 'time_out':3000},
    'info_8':{'m_type':'info', 'message':'Abort3 시나리오를 시작합니다.', 'time_out':3000},
    'info_9':{'m_type':'info', 'message':'Abort3 시나리오 완료', 'time_out':3000},
    'info_10':{'m_type':'info', 'message':'Abort3 시나리오 실패', 'time_out':3000},
}

warning_message:dict = {
    'warn_0':{'m_type':'warning', 'message':"CFX 장비가 동작 중입니다.", 'time_out':3000},
}

error_message:dict = {
    'err_0':{'m_type':'error', 'message':'모듈이 정해진 시간(30초) 안에 도착하지 않았습니다.', 'time_out':3000},
}

trc_file_contents = {
    'Reset1':"SYSTEM : User Output Dialog - complete;\n",
    'Reset2':"progress; Error manually recovered by user.\n",
    'Error1':"SYSTEM : User Output Dialog - start;\n",
    'Error2':"progress; Error handling waiting for manual recovery\n",
    'Error3':"SYSTEM : Abort method - start;\n",
    'Error4':"SYSTEM : Method has been aborted by the system - complete;\n",
    'Error5':"SYSTEM : Method has been aborted by the method - complete;\n",
    'Error6':"SYSTEM : Method has been aborted by the user - complete;\n",
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
                print(f"Remain time is {self._time_is}")
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
        Abort1 버튼 객체에 추가될 메서드. Abort1 시나리오를 수행
        버튼의 상태가 'normal'이면 STARlet 정지 구현
        버튼의 상태가 'active'이면 Abort1 시나리오 구현
        '''
        if self.button_2plate.state_is == self.button_1plate.state_is =='normal':
            self.__simulate_stop_starlet()


    def _command_abort1_button(self)->None:
        '''
        Abort1 버튼 객체에 추가될 메서드. Abort1 시나리오를 수행
        버튼의 상태가 'normal'이면 STARlet 정지 구현
        버튼의 상태가 'active'이면 Abort1 시나리오 구현
        '''
        if self.button_abort1.state_is == 'normal':
            self.__simulate_stop_starlet()
        elif self.button_abort1.state_is == 'active':
            self.button_abort1.state_is = 'inactive'
            self.__simulate_run_starlet()
            self.__show_messagebox(**info_message['info_2'])
            self._delay_sec(3) #의도적 지연. 사용자의 상태 변화 인식을 위함
            self.__simulate_abort_starlet()
            self.__show_messagebox(**info_message['info_3'])
            self.button_abort1.state_is = 'active'

    def _command_abort2_button(self)->None:
        '''
        Abort2 버튼 객체에 추가될 메서드. Abort2 시나리오를 수행
        버튼의 상태가 'normal'이면 STARlet 정지 구현
        버튼의 상태가 'active'이면 Abort2 시나리오 구현
        '''
        if self.button_abort3.state_is == 'normal':
            self.__simulate_stop_starlet()
        elif self.button_abort3.state_is == 'active':
            if self.__check_cfx_is_available('1plate'):
                self.button_abort3.state_is = 'inactive'
                self.__show_messagebox(**info_message['info_8'])
                self.__simulate_run_starlet()
                self._delay_sec(5) #의도적 지연. 사용자의 상태 변화 인식을 위함
                self.__simulate_elevator_request_1st()
                if self.__waiting_for_elevator_enable_file_creation():
                    self.__simulate_plate_transfer_1st()
                    self.__show_messagebox(**info_message['info_9'])
                else:
                    self.__show_messagebox(**info_message['info_10'])
                    self.__show_messagebox(**error_message['err_0'])
                self.button_abort3.state_is = 'active'
            else:
                self.__show_messagebox(**warning_message['warn_0'])

    def _command_abort3_button(self)->None:
        '''
        Abort3 버튼 객체에 추가될 메서드. Abort3 시나리오를 수행
        버튼의 상태가 'normal'이면 STARlet 정지 구현
        버튼의 상태가 'active'이면 Abort3 시나리오 구현
        '''
        if self.button_abort2.state_is == 'normal':
            self.__simulate_stop_starlet()
        elif self.button_abort2.state_is == 'active':
            if self.__check_cfx_is_available('1plate'):
                self.button_abort2.state_is = 'inactive'
                self.__simulate_run_starlet()
                self.__show_messagebox(**info_message['info_5'])
                self._delay_sec(5) #의도적 지연. 사용자의 상태 변화 인식을 위함
                self.__simulate_elevator_request_1st()
                if self.__check_module_move_within_times(30):
                    self.__simulate_abort_starlet()
                    self.__show_messagebox(**info_message['info_6'])
                else:
                    self.__show_messagebox(**info_message['info_7'])
                self.button_abort2.state_is = 'active'
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
                if not self.__run_1plate_scenario(): #fail
                    return
                if plrn_info['scenario'] == '1plate':
                    self.button_run.state_is = 'active'
                elif plrn_info['scenario'] == '2plate':
                    if not self.__run_2plate_scenario(): #fail
                        return
                    self.button_run.state_is = 'active'
            else:
                self.__show_messagebox(**warning_message['warn_0'])

    def _command_error1_button(self)->None:
        '''
        Error1 버튼이 눌렸을 시 대응
        1) 정해진 문장을 trc 파일에 쓴다.
        2) Starlet의 abort 상태를 모방한다.
        '''
        self.__simulate_run_starlet()
        self._delay_sec(1)
        self.trc_file.write_file([trc_file_contents['Error1']])
        print(f"Error1 button is clicked. Write {trc_file_contents['Error1']}")
        self.__simulate_abort_starlet()

    def _command_error2_button(self)->None:
        '''
        Error2 버튼이 눌렸을 시 대응
        1) 정해진 문장을 trc 파일에 쓴다.
        2) Starlet의 abort 상태를 모방한다.
        '''
        self.__simulate_run_starlet()
        self._delay_sec(1)
        self.trc_file.write_file([trc_file_contents['Error2']])
        print(f"Error2 button is clicked. Write {trc_file_contents['Error2']}")
        self.__simulate_abort_starlet()

    def _command_error3_button(self)->None:
        '''
        Error3 버튼이 눌렸을 시 대응
        1) 정해진 문장을 trc 파일에 쓴다.
        2) Starlet의 abort 상태를 모방한다.
        '''
        self.__simulate_run_starlet()
        self._delay_sec(1)
        self.trc_file.write_file([trc_file_contents['Error3']])
        print(f"Error3 button is clicked. Write {trc_file_contents['Error3']}")
        self.__simulate_abort_starlet()

    def _command_error4_button(self)->None:
        '''
        Error4 버튼이 눌렸을 시 대응
        1) 정해진 문장을 trc 파일에 쓴다.
        2) Starlet의 abort 상태를 모방한다.
        '''
        self.__simulate_run_starlet()
        self._delay_sec(1)
        self.trc_file.write_file([trc_file_contents['Error4']])
        print(f"Error4 button is clicked. Write {trc_file_contents['Error4']}")
        self.__simulate_abort_starlet()

    def _command_error5_button(self)->None:
        '''
        Error5 버튼이 눌렸을 시 대응
        1) 정해진 문장을 trc 파일에 쓴다.
        2) Starlet의 abort 상태를 모방한다.
        '''
        self.__simulate_run_starlet()
        self._delay_sec(1)
        self.trc_file.write_file([trc_file_contents['Error5']])
        print(f"Error5 button is clicked. Write {trc_file_contents['Error5']}")
        self.__simulate_abort_starlet()

    def _command_error6_button(self)->None:
        '''
        Error6 버튼이 눌렸을 시 대응
        1) 정해진 문장을 trc 파일에 쓴다.
        2) Starlet의 abort 상태를 모방한다.
        '''
        self.__simulate_run_starlet()
        self._delay_sec(1)
        self.trc_file.write_file([trc_file_contents['Error6']])
        print(f"Error6 button is clicked. Write {trc_file_contents['Error6']}")
        self.__simulate_abort_starlet()

    def _command_reset1_button(self)->None:
        '''
        Reset1 버튼이 눌렸을 시 대응
        1) 정해진 문장을 trc 파일에 쓴다.
        2) Starlet의 abort 상태를 모방한다.
        '''
        self.trc_file.write_file([trc_file_contents['Reset1']])
        print(f"Reset1 button is clicked. Write {trc_file_contents['Reset1']}")
        self.__simulate_run_starlet()

    def _command_reset2_button(self)->None:
        '''
        Reset1 버튼이 눌렸을 시 대응
        1) 정해진 문장을 trc 파일에 쓴다.
        2) Starlet의 abort 상태를 모방한다.
        '''
        self.trc_file.write_file([trc_file_contents['Reset2']])
        print(f"Reset1 button is clicked. Write {trc_file_contents['Reset2']}")
        self.__simulate_run_starlet()

    def __show_messagebox(self, m_type:str, message:str, time_out:int, time_sec = None):
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
        print(f"{m_type} : {message} printed\n")

    def __check_module_move_within_times(self, time_sec:int = 30)->bool:
        '''
        설정한 시간동안 handler를 관찰, 이 시간 내 plate hanlder가 움직이면 True
        시간이 초과될 동안 오지 않으면 False 반환
        '''
        self._time_is = time_sec
        print("엘리베이터 모듈이 움직이기 시작할 때까지 기다립니다.\n")
        while self._time_is:
            cfx_info = self.aios_data_is
            window_frame.update()
            if "88:88:88" in (cfx_info.cfx1_time, cfx_info.cfx2_time):
                print("elevator is moving now\n")
                return True
        print("elevator didn't arrive in 30 seconds\n")
        return False

    def __convert_method_info_for_display(self, value:AiosData)->list:
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
        temp_cfx_status = [
            ['CFX#1', ''],
            ['CFX#2', ''],
            ['Control Status', '']
            ]
        temp_cfx_status[0][1] = value.cfx1_time
        temp_cfx_status[1][1] = value.cfx2_time
        temp_cfx_status[2][1] = value.control_status
        return temp_cfx_status

    def __check_cfx_is_available(self, scenario:str)->bool:
        '''
        CFX#1과 #2의 남은 시간과 동작할 시나리오에 맞춰 CFX가 시나리오에
        맞춰 동작 가능한지 판단하고 이를 판환한다.
        '''
        value = self.aios_data_is
        print("CFX remain time check")
        if value.cfx1_time == '00:00:00':
            result = True if value.cfx2_time == '00:00:00' else (scenario == '1plate')
        elif value.cfx2_time == '00:00:00':
            result = (scenario == '1plate')
        else:
            result = False #모든 CFX 동작 중이므로 False
        if result:
            print(f"for {scenario} scenario, CFX is available\n")
        else:
            print("cfx is not available\n")
        return result

    def __simulate_abort_starlet(self):
        '''
        AiosData를 읽어온 다음 method_run 값을 조절,
        AIOS에게 STARlet이 Abort 되었음을 알린다.
        '''
        value = self.aios_data_is
        value.method_run = '2'
        self.file_data = value
        self.__show_messagebox(**info_message['info_0'])
        print(f"change method_staus.csv.{self.__convert_method_info_for_display(value)}\n")

    def __simulate_stop_starlet(self):
        '''
        AIOS에게 STARlet이 정지하였음을 알린다.
        또한 plrn 정보를 없앤다.
        '''
        print("starlet stop\n")
        self.plrn_info_is = {'scenario':'','plrn_name':''}
        value = self.aios_data_is
        value.method_run = '0'
        value.elevator_request = '0'
        value.plrn1_name = ""
        value.plrn2_name = ""
        self.file_data = value
        print(f"change method_staus.csv.{self.__convert_method_info_for_display(value)}\n")

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
        print(f"change method_staus.csv.{self.__convert_method_info_for_display(method_status)}\n")

    def __waiting_for_plate_exist_file_creation(self):
        print("waiting for 'place_exist.csv'\n")
        while self.aios_data_is.plate_exist == "Non existing":
            window_frame.update()

    def __waiting_for_elevator_enable_file_creation(self, wtime:int = 30)->bool:
        '''
        AIOS로부터 엘리베이터 모듈이 올 때까지 30초 대기한다.
        그 사이에 엘리베이터 모듈이 올라오면 True
        올라오지 않으면 False를 반환한다.
        '''
        self._time_is = wtime
        print(f"waiting for elevator module for {self._time_is} seconds\n")
        while self._time_is and self.aios_data_is.elevator_enable == 'Non existing':
            window_frame.update()
        if bool(self._time_is):
            print("elevator module arrived\n")
        else:
            print("elevator module didn't arrive\n")
        return bool(self._time_is)

    def __waiting_for_cfx_remain_time_change(self, wtime:int = 9000)->bool:
        '''
        CFX가 동작 상태가 되기까지 기다린다.
        '''
        self._time_is = wtime
        print(f"wait until cfx1 runs for {self._time_is} seconds\n")
        while self._time_is: #wait for elevator enable during 15 minuntes
            window_frame.update()
            value:AiosData = self.aios_data_is
            if value.cfx1_time not in ("00:00:00", "88:88:88"):
                print(f"cfx runs. Its time is {value.cfx1_time} seconds\n")
                break
        if not bool(self._time_is):
            print("CFX1 didn't run\n")
        return bool(self._time_is)

    def __simulate_elevator_request_1st(self):
        '''
        첫 번쨰 플레이트를 전달하기 위해 AIOS에게
        엘리베이터 모듈을 요청한다.
        '''
        method_status:AiosData = self.aios_data_is
        method_status.elevator_request = '1,plrn1'
        self.file_data = method_status
        print("1번 플레이트 전달을 위한 엘리베이터 호출")
        print(f"change method_staus.csv.{self.__convert_method_info_for_display(method_status)}\n")

    def __simulate_elevator_request_2nd(self):
        '''
        두 번쨰 플레이트를 전달하기 위해 AIOS에게
        엘리베이터 모듈을 요청한다.
        '''
        method_status = self.aios_data_is
        method_status.elevator_request = '1,plrn2'
        self.file_data = method_status
        print("2번 플레이트 전달을 위한 엘리베이터 호출")
        print(f"change method_staus.csv.{self.__convert_method_info_for_display(method_status)}\n")

    def __simulate_plate_transfer_1st(self)->None:
        '''
        AIOS에게 첫 번째 플레이트를 전달했음을 알린다.
        '''
        method_status = self.aios_data_is
        method_status.elevator_request = '2,plrn1'
        self.file_data = method_status
        print("1번 플레이트 전달\n")
        print(f"change method_staus.csv.{self.__convert_method_info_for_display(method_status)}\n")

        self.__waiting_for_plate_exist_file_creation()
        self._delay_sec(5) #의도적 지연. 사용자의 상태 변화 인식을 위함

    def __simulate_plate_transfer_2nd(self)->None:
        '''
        AIOS에게 두 번째 플레이트를 전달했음을 알린다.
        '''
        method_status = self.aios_data_is
        method_status.elevator_request = '2,plrn2'
        self.file_data = method_status
        print("2번 플레이트 전달\n")
        print(f"change method_staus.csv.{self.__convert_method_info_for_display(method_status)}\n")

        self.__waiting_for_plate_exist_file_creation()
        self._delay_sec(5) #의도적 지연. 사용자의 상태 변화 인식을 위함

    def _delay_sec(self, seconds):
        self._time_is = seconds
        print(f"delay {seconds} seconds\n")
        while self._time_is:
            window_frame.update()

    def __run_1plate_scenario(self)->bool:
        '''
        1) elevator 모듈을 요청한다.
        2) 시간 내에 엘리베이터 모듈이 도착하면 플레이트를 놓으라고 한다.
        3) 사용자가 놓으면 plate를 전달했음을 알린다.
        '''
        print("1번 플레이트 전달 시작\n")
        self.__simulate_run_starlet()
        self._delay_sec(5) #의도적 지연. 사용자의 상태 변화 인식을 위함
        self.__simulate_elevator_request_1st()
        if not self.__waiting_for_elevator_enable_file_creation(): #비동기 동작 메서드
            print("1번 전달 실패. 엘리베이터 모듈 도착 안 함\n")
            self.__show_messagebox(**error_message['err_0'])
            self.button_run.state_is = 'active'
            return False
        print("엘리베이터 모듈 도착 확인. 1번 플레이트 전달 시도\n")
        self.__show_messagebox(**info_message['info_1'], time_sec=300)
        self.__simulate_plate_transfer_1st()
        return True

    def __run_2plate_scenario(self)->bool:
        '''
        1) elevator 모듈을 요청한다.
        2) 시간 내에 엘리베이터 모듈이 도착하면 플레이트를 놓으라고 한다.
        3) 사용자가 놓으면 plate를 전달했음을 알린다.
        '''
        print("2번 플레이트 전달 시작\n")
        self.__simulate_run_starlet()
        if self.__waiting_for_cfx_remain_time_change():
            self.__simulate_elevator_request_2nd()
            if not self.__waiting_for_elevator_enable_file_creation(): #비동기 동작 메서드
                print("2번 전달 실패. 엘리베이터 모듈 도착 안 함\n")
                self.__show_messagebox(**error_message['err_0'])
                self.button_run.state_is = 'active'
                return False
            print("엘리베이터 모듈 도착 확인. 2번 플레이트 전달 시도\n")
            self.__show_messagebox(**info_message['info_1'], time_sec=300)
            self.__simulate_plate_transfer_2nd()
            return True
        print("2번 플레이트 전달 실패. CFX 시간이 변경되지 않음\n")
        return False

if __name__ == '__main__':
    simulator = PresenterSimulator()
