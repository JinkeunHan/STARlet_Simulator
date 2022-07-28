'''
뷰 클래스에 대한 검증이다 보니, 직접적으로 unittest 모듈을 쓰지 않고,
대신 기능을 별도로 구현하여 검증한다.
'''
from view_simulator import *

view_title = LabelFrame(window_frame, info_title)
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

list_array_method_status = [
                            ["Method","run,",""],
                            ["Elevator","requeset,",""],
                            ["Plrn1,",""],
                            ["Plrn2,",""],
                           ]

list_array_cfx_status = [
                         ["CFX#1","00:00:00"],
                         ["CFX#2","00:00:00"],
                         ["Control Status,","0"],
                        ]

view_cfx_status.contents = list_array_cfx_status
view_method_status.contents = list_array_method_status
view_elevator_enable.contents = "Existing"
view_plate_exist.contents ="Non existing"
view_control_log.contents = "Test messageblah, blah, blah~~~~~~~~~~~~~~~~~~~ㄹㅇㄹㅇㄹㅇㄹㅇㄹㅇㄹㅇㄹㅇㄹㅇ~`"
view_title.contents = "AIOS Version 0.0"

window_frame.mainloop()

print("HelloWorld")
