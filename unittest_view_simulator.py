'''
뷰 클래스에 대한 검증이다 보니, 직접적으로 unittest 모듈을 쓰지 않고,
대신 기능을 별도로 구현하여 검증한다.
'''
from view_simulator import *

#뷰 객체를 생성, 이미지 구현. 구현된 이미지가 요구사항의 것과 같아야 한다.
view_simulator = ViewSimulator() 

# 각 라벨 프레임의 setter를 대상으로 값 입력, 표시되는 내용 확인
# 하기 내용이 그대로 표시되어야 한다.
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

view_simulator.cfx_status.contents = list_array_cfx_status
view_simulator.method_status.contents = list_array_method_status
view_simulator.elevator_enable.contents = "Existing"
view_simulator.plate_exist.contents ="Non existing"
view_simulator.control_log.contents = "Test messageblah, blah, blah~~~~~~~~~~~~~~~~~~~ㄹㅇㄹㅇㄹㅇㄹㅇㄹㅇㄹㅇㄹㅇㄹㅇ~`"
view_simulator.title.contents = "AIOS Version 0.0"

window_frame.mainloop()

print("HelloWorld")
