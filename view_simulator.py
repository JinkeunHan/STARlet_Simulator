'''
STARlet Simulator의 뷰 역할을 수행하는 모듈이다.
라벨 프레임 클래스와 버튼 클래스를 갖는다.
라벨 프레임 클래스는 내부에 메세지 위젯을 통해 내용을 표시하고 갱신한다.
'''
import tkinter as tk
import tkinter.font as tkFont
from tkinter import filedialog
from tkinter import messagebox

SIM_VERISON = "v1.0"
window_frame = tk.Tk()

window_frame.title("STARlet, AIOS log logger")
window_frame.geometry("740x575")
window_frame.config(bg = '#4472C4')
window_frame.resizable(height=False, width=False)

font_labelframe = tkFont.Font(family="Arial", size=14, weight='bold', underline=True)
font_contents = tkFont.Font(family="Arial", size=12)
font_title = tkFont.Font(family="Arial", size=18, weight='bold', underline=False)

info_button_1plate = {'order':0, 'state':"normal", 'text':"1plate"}
info_button_2plate = {'order':1, 'state':"normal", 'text':"2plate"}
info_button_abort1 = {'order':2, 'state':"disabled", 'text':"Abort1"}
info_button_abort2 = {'order':3, 'state':"disabled", 'text':"Abort2"}
info_button_abort3 = {'order':4, 'state':"disabled", 'text':"Abort3"}
info_button_run = {'order':5, 'state':"disabled", 'text':"Run"}
info_button_error1 = {'order':0, 'state':"disabled", 'text':"Error1"}
info_button_error2 = {'order':1, 'state':"disabled", 'text':"Error2"}
info_button_error3 = {'order':2, 'state':"disabled", 'text':"Error3"}
info_button_error4 = {'order':3, 'state':"disabled", 'text':"Error4"}
info_button_error5 = {'order':4, 'state':"disabled", 'text':"Error5"}
info_button_error6 = {'order':5, 'state':"disabled", 'text':"Error6"}
info_button_reset1 = {'order':6, 'state':"disabled", 'text':"Reset1"}
info_button_reset2 = {'order':7, 'state':"disabled", 'text':"Reset2"}
info_title = {
	'text':"",
    'place':{'x':211, 'y':25, 'width':333, 'height':45},
    'message_place':{'x':0, 'y':0, 'width':333},
    'message_config':{'text':"AIOS Simulatior v1.0", 'font':font_title},
	}
info_cfx_status = {
	'text':"CFX_Status.csv",
    'place':{'x':57, 'y':99, 'width':192, 'height':106},
    'message_place':{'x':13, 'y':5, 'width':162}, # place하는 메시지의 위젯 그 자체의 폭이다.
    'message_config':{'text':"", 'anchor':'w','justify':'left','font':font_contents},
	}
info_method_status = {
	'text':"Method_Status.csv",
    'place':{'x':267, 'y':99, 'width':193, 'height':106},
    'message_place':{'x':0, 'y':0, 'width':193},
    'message_config':{'text':"", 'anchor':'w','justify':'left','font':font_contents},
	}
info_elevator_enable = {
	'text':"Elevator_enable.csv",
    'place':{'x':479, 'y':99, 'width':233, 'height':50},
    'message_place':{'x':0, 'y':0, 'width':233},
    'message_config':{'text':"Non existing",'font':font_contents},
	}
info_plate_exist = {
	'text':"Plate_exist.csv",
    'place':{'x':479, 'y':155, 'width':233, 'height':50},
    'message_place':{'x':0, 'y':0, 'width':233},
    'message_config':{'text':"Non existing",'font':font_contents},
	}
info_control_log = {
	'text':"Control_Log",
    'place':{'x':307, 'y':223, 'width':405, 'height':316},
    'message_place':{'x':0, 'y':0, 'width':405},
    'message_config':{'text':"", 'anchor':'w','justify':'left','font':font_contents},
	}
info_auto_run = {
	'text':"Auto_Run",
    'place':{'x':57, 'y':223, 'width':235, 'height':135},
	}
info_error_simulation = {
	'text':"Error Simulation",
    'place':{'x':57, 'y':369, 'width':235, 'height':170},
	}
info_plrn_file = {
    'initialdir':"d:",
    'title':"plrn 파일을 선택해 주세요.",
    'filetypes':(("*.plrn, *plrn"), ("*.txt, *txt"))
}

class Button:
    '''
    시뮬레이터 버튼 제어용 클래스
    생성 시 1 Plate, 2 Plate 버튼은 normal 상태로 생성
    그 외 버튼은 disabled 상태로 생성
    '''
    def __init__(self, target:tk.LabelFrame, info:dict):
        self.__command_list = [self._button_pressed,]
        self.__state = info['state']
        self.__obj = tk.Button(
            target, text = info['text'],
            command=lambda:[item() for item in self.__command_list], bd=3,
            font=font_contents, activebackground='#355EA8',
            activeforeground='#FFFFFF', disabledforeground='#7F7F7F',
            state= info['state']
        )
        self.contents = self.__state
        self.__obj.place(x=96*(info['order']%2)+6*(info['order']%2)+17,
                       y=35*(info['order']//2)+3, width=96, height=32)
    def _button_pressed(self):
        '''
        사용자가 버튼 누를 때마다 동작, 상태 변경용
        '''
        if self.__state == "normal":
            self.contents = "active"
        elif self.__state == 'active':
            self.contents = 'normal'
    @property
    def command_list(self)->list:
        '''
        button 객체에 클릭 이벤트 발생 시 수행할 메서드 리스트를 반환한다.
        '''
        return self.__command_list
    @command_list.setter
    def command_list(self, func)->None:
        '''
        button 객체에 클릭 이벤트 발생 시 수행할 메서드 리스트를 설정한다.
        인수가 없는 메서드만을 입력해야 한다.
        추가의 형태로 더해지므로 넣는 걸 잘 해야 한다.
        '''
        self.__command_list.append(func)
        self.__obj.config(command=lambda:[item() for item in self.__command_list])
    @property
    def contents(self)->str:
        '''
        버튼의 상태를 알기 위한 메소드
        '''
        return self.__state
    @contents.setter
    def contents(self, state:str)->None:
        '''
        버튼의 이미지 및 상태를 바꾸는 용도이다. normal, disabled 및 active에
        맞춰 설정해야 한다.
        '''
        self.__state = state
        if state == "normal":
            self.__obj.configure(bg='#4472C4', fg='#FFFFFF',state='normal',
                               relief='raised')
        elif state == "disabled":
            self.__obj.configure(bg='#D9D9D9', fg='#7F7F7F',state='disabled')
        elif state == 'active':
            self.__obj.configure(bg='#355EA8', fg='#FFFFFF',state='active',
                               relief='sunken')
class LabelFrame:
    '''
    "Auto Run", "Error Simulation", "Control_Log", "Elevator_enable.csv",
    "Plate_exist.csv", "Method_Status.csv", "CFX_Status.csv"
    상기 7개를 보여주기 위한 라벨 프레임 클래스
    '''
    def __init__(self, master:tk.Tk, info:dict):
        self.label_frame = tk.LabelFrame(master, text=info['text'],
                                         bg='#FFFFFF',
                                         font=font_labelframe,
                                         labelanchor='n', bd=0)
        self.label_frame.place(**info['place'])
        if 'message_place' in info:
            self.message = tk.Message(self.label_frame,
                                      width=info['place'].get('width')
                                            -info['message_place'].get('x'),
                                      **info['message_config'], bg='#FFFFFF')
            self.message.place(**info['message_place'])
    @property
    def contents(self):
        '''
        Getter는 자신의 message 객체를 반환한다.
        '''
        return self.message
    @contents.setter
    def contents(self, printing_info:list or str)->None:
        '''
        라벨 프레임 내에 텍스트를 집어넣기 위한 메서드다.
        CFX_Status.csv, Method_status.csv, Elevator_enable.csv,
        Plate_exist.csv 및 Control_Log에 내용을 써넣기 위해 존재한다.
        '''
        if isinstance(printing_info, list):
            message_list=[" ".join(sentence) for sentence in printing_info]
            message = '\n'.join(message_list)
        elif isinstance(printing_info, str):
            message = printing_info
        self.message.configure(text=message)

class ViewSimulator():
    '''
    STARlet Simuator의 뷰 객체들의 응집체
    객체 생성 시 관련 뷰 객체들을 생성한다.
    또한 버튼 객체들 간의 이미지 조율을 담당한다.
    '''
    def __init__(self):
        self._init_label_frame()
        self._init_buttons()
        self.__plrn_info = {'scenario': '', 'plrn_name': ''}

    def _init_label_frame(self):
        '''
        초기 실행 시 __init__에 의해 자동으로 호출
        라벨 프레임 객체를 자동으로 생성한다.
        반드시 _init_buttons보다 먼저 호출해야 한다.
        '''
        self.title = LabelFrame(window_frame, info_title)
        self.cfx_status = LabelFrame(window_frame, info_cfx_status)
        self.method_status = LabelFrame(window_frame, info_method_status)
        self.elevator_enable = LabelFrame(window_frame, info_elevator_enable)
        self.plate_exist = LabelFrame(window_frame, info_plate_exist)
        self.control_log = LabelFrame(window_frame, info_control_log)
        self.auto_run = LabelFrame(window_frame, info_auto_run).label_frame
        self.error_simulation = LabelFrame(window_frame, info_error_simulation).label_frame

    def _init_buttons(self):
        '''
        초기 실행 시 __init__에 의해 자동으로 호출
        버튼 객체를 생성하고, 본 클래스의 _update_button 메서드를 추가로 바인딩한다.
        '''
        self.button_1plate = Button(self.auto_run, info_button_1plate)
        self.button_2plate = Button(self.auto_run, info_button_2plate)
        self.button_abort1 = Button(self.auto_run, info_button_abort1)
        self.button_abort2 = Button(self.auto_run, info_button_abort2)
        self.button_abort3 = Button(self.auto_run, info_button_abort3)
        self.button_run = Button(self.auto_run, info_button_run)
        self.button_error1 = Button(self.error_simulation, info_button_error1)
        self.button_error2 = Button(self.error_simulation, info_button_error2)
        self.button_error3 = Button(self.error_simulation, info_button_error3)
        self.button_error4 = Button(self.error_simulation, info_button_error4)
        self.button_error5 = Button(self.error_simulation, info_button_error5)
        self.button_error6 = Button(self.error_simulation, info_button_error6)
        self.button_reset1 = Button(self.error_simulation, info_button_reset1)
        self.button_reset2 = Button(self.error_simulation, info_button_reset2)

        self.button_1plate.command_list = self._file_select
        self.button_1plate.command_list = self._update_button
        self.button_2plate.command_list = self._file_select
        self.button_2plate.command_list = self._update_button
        self.button_abort1.command_list = self._update_button
        self.button_abort2.command_list = self._update_button
        self.button_abort3.command_list = self._update_button
        self.button_run.command_list = self._update_button
        self.button_error1.command_list = self._update_button
        self.button_error2.command_list = self._update_button
        self.button_error3.command_list = self._update_button
        self.button_error4.command_list = self._update_button
        self.button_error5.command_list = self._update_button
        self.button_error6.command_list = self._update_button
        self.button_reset1.command_list = self._update_button
        self.button_reset2.command_list = self._update_button

    def _buttons_error_simulation(self, state:str):
        '''
        Error_Simulation label frame에 있는 버튼들은
        동작 형태가 같아 하나로 모아 관리
        '''
        self.button_error1.contents = state
        self.button_error2.contents = state
        self.button_error3.contents = state
        self.button_error4.contents = state
        self.button_error5.contents = state
        self.button_error6.contents = state
        self.button_reset1.contents = state
        self.button_reset2.contents = state

    def _buttons_auto_run(self, state:str, exception:Button=None):
        '''
        Error_Simulation label frame에 있는 버튼들은
        동작 형태가 같아 하나로 모아 관리
        인수로 exception을 받으며, exception이 있으면 해당 버튼의 상태는 안 바꿈.
        '''
        for item in (self.button_abort1, self.button_abort2,\
            self.button_abort3, self.button_run):
            if item is not exception:
                item.contents = state

    def _file_select(self):
        if 'active' in (self.button_1plate.contents, self.button_2plate.contents):
            file = filedialog.askopenfile(**info_plrn_file)
            if file is None:
                messagebox.showwarning("경고", "plrn파일을 선택하세요")
                self.button_1plate.contents = "normal"
                self.button_2plate.contents = "normal"
            else:
                if 'active' in self.button_1plate.contents:
                    self.plrn_info_is = dict(scenario='1plate', plrn_name=file.name)
                else:
                    self.plrn_info_is = dict(scenario='2plate', plrn_name=file.name)


    def _update_button(self):
        '''
        tkinter의 command와 binding 되어 event 기반으로 동작하는 method다.
        contents를 통해 얻어온 state를 바탕으로 이미지를 바꾸는 역할을 수행한다.
        또한 plrn_flag와 run_flag를 여기서 세우고 끈다.
        '''
        plrn_flag = False
        auto_run_flag = False
        if 'active' in self.button_1plate.contents:
            self.button_2plate.contents = 'normal'
            plrn_flag = True
        elif 'active' in self.button_2plate.contents:
            self.button_1plate.contents = 'normal'
            plrn_flag = True
        else:
            plrn_flag = False
            self._buttons_auto_run('normal') #눌린 상태로 존재하는 것 방지용.

        #check below buttons are pressed
        auto_run_flag = bool('active' in (self.button_abort1.contents,
                                          self.button_abort2.contents,
                                          self.button_abort3.contents,
                                          self.button_run.contents))

        if plrn_flag:
            if not auto_run_flag:
                self._buttons_auto_run('normal')
        else:
            self._buttons_auto_run('disabled')

        self._buttons_error_simulation('disabled')

        if 'active' in self.button_run.contents:
            self._buttons_auto_run('disabled', exception=self.button_run)
            self._buttons_error_simulation('normal')
        elif 'active' in self.button_abort1.contents:
            self._buttons_auto_run('disabled', exception=self.button_abort1)
        elif 'active' in self.button_abort2.contents:
            self._buttons_auto_run('disabled', exception=self.button_abort2)
        elif 'active' in self.button_abort3.contents:
            self._buttons_auto_run('disabled', exception=self.button_abort3)

    @property
    def plrn_info_is(self)->dict:
        '''
        plrn 파일 명 및 1plate 또는 2plate 시나리오를 알림
        '''
        return self.__plrn_info
    @plrn_info_is.setter
    def plrn_info_is(self,value:dict)->None:
        self.__plrn_info['scenario'] = value['scenario']
        self.__plrn_info['plrn_name'] = value['plrn_name']

if __name__ == '__main__':
    view_simulator = ViewSimulator()
    window_frame.mainloop()
    print("HelloWorld")
