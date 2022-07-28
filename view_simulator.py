'''
STARlet Simulator의 뷰 역할을 수행하는 모듈이다.
라벨 프레임 클래스와 버튼 클래스를 갖는다.
라벨 프레임 클래스는 내부에 메세지 위젯을 통해 내용을 표시하고 갱신한다.
'''
import tkinter.font as tkFont
import tkinter as tk

#Start
SIM_VERISON = "v1.0"
window_frame = tk.Tk()

window_frame.title("STARlet Simualtor")
window_frame.geometry("740x575")
window_frame.config(bg = '#4472C4')
window_frame.resizable(height=False, width=False)

font_labelframe = tkFont.Font(family="Arial", size=14, weight='bold', underline=1)
font_contents = tkFont.Font(family="Arial", size=12)
font_title = tkFont.Font(family="Arial", size=18, weight='bold', underline=0)

# info_version = InfoLabel(39, 6, "STARlet Simulator"+SIM_VERISON)
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
class Button:
    '''
    시뮬레이터 버튼 제어용 클래스
    생성 시 1 Plate, 2 Plate 버튼은 normal 상태로 생성
    그 외 버튼은 disabled 상태로 생성
    '''
    def __init__(self, target:tk.LabelFrame, info:dict):
        self.state = info['state']
        self.obj = tk.Button(
            target, text = info['text'], command=self.button_pressed, bd=3,
            font=font_contents, activebackground='#355EA8',
            activeforeground='#FFFFFF', disabledforeground='#7F7F7F',
            state= info['state']
        )
        self.contents = self.state
        self.obj.place(x=96*(info['order']%2)+6*(info['order']%2)+17,
                       y=35*(info['order']//2)+3, width=96, height=32)
    def button_pressed(self):
        '''
        사용자가 버튼 누를 시 일단 여기로 오도록 설정 함
        추후 변경될 수 있음
        '''
        if self.state == "normal":
            self.contents = "active"
        elif self.state == 'active':
            self.contents = 'normal'
    @property
    def contents(self)->str:
        '''
        버튼의 상태를 알기 위한 메소드
        '''
        return self.state
    @contents.setter
    def contents(self, state:str)->None:
        '''
        버튼의 이미지 및 상태를 바꾸는 용도이다. normal, disabled 및 active에
        맞춰 설정해야 한다.
        '''
        self.state = state
        if state == "normal":
            self.obj.configure(bg='#4472C4', fg='#FFFFFF',state='normal',
                               relief='raised')
        elif state == "disabled":
            self.obj.configure(bg='#D9D9D9', fg='#7F7F7F',state='disabled')
        elif state == 'active':
            self.obj.configure(bg='#355EA8', fg='#FFFFFF',state='active',
                               relief='sunken')
class LabelFrame:
    '''
    "Auto Run", "Error Simulation", "Control_Log", "Elevator_enable.csv",
    "Plate_exist.csv", "Method_Status.csv", "CFX_Status.csv"
    상기 7개를 보여주기 위한 라벨 프레임 클래스
    '''
    def __init__(self, master:tk.Tk, info:dict):
        self.info = info
        self.label_frame = tk.LabelFrame(master, text=info['text'],
                                         bg='#FFFFFF',
                                         font=font_labelframe,
                                         labelanchor='n', bd=0)
        self.label_frame.place(**info['place'])
        if 'message_place' in info:
            self.message = tk.Message(self.label_frame,
                                      width=info['place'].get('width')
                                            -info['message_place'].get('x'),
                                      **info['message_config'], bg='#FFFFFF'
                                     )
            self.message.place(**info['message_place'])
    @property
    def contents(self):
        '''
        현재로서는 사용처가 없음
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
