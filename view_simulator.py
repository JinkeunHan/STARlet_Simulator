from datetime import datetime
from dataclasses import dataclass
import tkinter.font as tkFont
import tkinter as tk

#Start
version = "v1.0"
window_frame = tk.Tk()

window_frame.title("STARlet Simualtor")
window_frame.geometry("740x575")
window_frame.config(bg = '#4472C4')
window_frame.resizable(height=False, width=False)

font_labelframe = tkFont.Font(family="Arial", size=14, weight='bold', underline=1)
font_button = tkFont.Font(family="Arial", size=12)
font_title = tkFont.Font(family="Arial", size=18, weight='bold', underline=0)

@dataclass
class InfoLabel:
    x:int
    y:int
    title:str
    
@dataclass
class InfoButton:
    order:int
    state:str
    title:str
    
@dataclass
class InfoLabelFrame:
    x:int
    y:int
    w:int
    h:int
    title:str

info_version = InfoLabel(
    39, 6,
    "STARlet Simulator"+version
    )

info_button_1plate = InfoButton(
    0, "normal", "1plate"
    )
info_button_2plate = InfoButton(
    1, "normal", "2plate"
    )
info_button_abort1 = InfoButton(
    2, "disabled", "Abort1"
    )
info_button_abort2 = InfoButton(
    3, "disabled", "Abort2"
    )
info_button_abort3 = InfoButton(
    4, "disabled", "Abort3"
    )
info_button_run = InfoButton(
    5, "disabled", "Run"
    )
info_button_error1 = InfoButton(
    0, "disabled", "Error1"
    )
info_button_error2 = InfoButton(
    1, "disabled", "Error2"
    )
info_button_error3 = InfoButton(
    2, "disabled", "Error3"
    )
info_button_error4 = InfoButton(
    3, "disabled", "Error4"
    )
info_button_error5 = InfoButton(
    4, "disabled", "Error5"
    )
info_button_error6 = InfoButton(
    5, "disabled", "Error6"
    )
info_button_reset1 = InfoButton(
    6, "disabled", "Reset1"
    )
info_button_reset2 = InfoButton(
    7, "disabled", "Reset2"
    )
info_title = InfoLabelFrame(
    211, 25, 333, 45, 
    "",
    )
info_cfx_status = InfoLabelFrame(
    57, 99, 192, 106,
    "CFX_Status.csv",
    )
info_method_status = InfoLabelFrame(
    267, 99, 193, 106,
    "Method_Status.csv",
    )
info_elevator_enable = InfoLabelFrame(
    479, 99, 233, 50,
    "Elevator_enable.csv", 
    )
info_plate_exist = InfoLabelFrame(
    479, 155, 233, 50,
    "Plate_exist.csv", 
    )
info_control_log = InfoLabelFrame(
    307, 223, 405, 316,
    "Control_Log", 
    )
info_auto_run = InfoLabelFrame(
    57, 223, 235, 135,
    "Auto_Run", 
    )
info_error_simulation = InfoLabelFrame(
    57, 369, 235, 170,
    "Error Simulation", 
    )

class Button:
    def __init__(self, target:tk.LabelFrame, info:InfoButton):
        self.state = info.state
        if info.state == "normal":
            self.obj = tk.Button(target, text = info.title, command=self.btn_pressed, bd=3, 
                                font=font_button, bg='#4472C4', fg='#FFFFFF',
                                activebackground='#4472C4', activeforeground='#FFFFFF',
                                disabledforeground='#7F7F7F', state= info.state)
        else:
            self.obj = tk.Button(target, text = info.title, command=self.btn_pressed, bd=3, 
                                font=font_button, bg='#D9D9D9', fg='#7F7F7F',
                                activebackground='#4472C4', activeforeground='#FFFFFF',
                                disabledforeground='#7F7F7F', state= info.state)
        if info.order%2:
            self.obj.place(x=96*(info.order%2)+ 23, y=35*(info.order//2)+3, 
                           width=96, height=32)
        else:
            self.obj.place(x=96*(info.order%2)+ 17, y=35*(info.order//2)+3, 
                           width=96, height=32)
    def btn_pressed(self):
        pass
    def setter(self, state:str):
        if state == "normal":
            self.obj.configure(bg='#4472C4', fg='#FFFFFF',state='normal')
        elif state == "disabled":
            self.obj.configure(bg='#D9D9D9', fg='#7F7F7F',state='disabled')
    def getter(self):
        return self

class Label:
    def __init__(self, master:tk.LabelFrame, info:InfoLabel):
        label = tk.Label(master, text= info.title, bg='#FFFFFF', font=font_title, 
                            anchor='center', bd=0)
        label.place(x=info.x, y=info.y)

class LabelFrame:
    def __init__(self, master:tk.Tk, info:InfoLabelFrame):
        self.label_frame = tk.LabelFrame(master, text=info.title, bg='#FFFFFF', 
                                    font=font_labelframe, labelanchor='n', bd=0 )
        self.label_frame.place(x=info.x, y=info.y)
        self.label_frame.configure(width = info.w, height= info.h)

view_title = LabelFrame(window_frame, info_title)
Label(view_title.label_frame, info_version)
view_cfx_status = LabelFrame(window_frame, info_cfx_status)
view_method_status = LabelFrame(window_frame, info_method_status)
view_elevator_enable = LabelFrame(window_frame, info_elevator_enable)
view_plate_exist = LabelFrame(window_frame, info_plate_exist)
view_control_log = LabelFrame(window_frame, info_control_log)
view_auto_run = LabelFrame(window_frame, info_auto_run)
view_error_simulation = LabelFrame(window_frame, info_error_simulation)
view_button_1plate = Button(view_auto_run.label_frame, info_button_1plate)
view_button_2plate = Button(view_auto_run.label_frame, info_button_2plate)
view_button_abort1 = Button(view_auto_run.label_frame, info_button_abort1)
view_button_abort2 = Button(view_auto_run.label_frame, info_button_abort2)
view_button_abort3 = Button(view_auto_run.label_frame, info_button_abort3)
view_button_run = Button(view_auto_run.label_frame, info_button_run)
view_button_error1 = Button(view_error_simulation.label_frame, info_button_error1)
view_button_error2 = Button(view_error_simulation.label_frame, info_button_error2)
view_button_error3 = Button(view_error_simulation.label_frame, info_button_error3)
view_button_error4 = Button(view_error_simulation.label_frame, info_button_error4)
view_button_error5 = Button(view_error_simulation.label_frame, info_button_error5)
view_button_error6 = Button(view_error_simulation.label_frame, info_button_error6)
view_button_reset1 = Button(view_error_simulation.label_frame, info_button_reset1)
view_button_reset2 = Button(view_error_simulation.label_frame, info_button_reset2)

window_frame.mainloop()

print("HelloWorld")