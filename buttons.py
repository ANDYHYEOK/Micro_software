import tkinter as tk
from tkinter import PhotoImage
from button_events import button_event_group
        
def create_buttons(canvas):           
    """_summary_
    
    버튼들을 따로 관리하여 가독성을 높히고 각 기능별 수행하여야하는 것들을 명시할 수 있게 합니다.
    
    Args:
        canvas (_type_): tkinter의 캔버스 객체를 전달하여 버튼이 생성될 수 있게 합니다.
    """
    button_events = button_event_group()
    
    pick_image_path = "./btn_images/pick.png"
    put_image_path = "./btn_images/put.png"
    stop_image_path = "./btn_images/stop.png"

    pick_image = PhotoImage(file=pick_image_path)
    put_image = PhotoImage(file=put_image_path)
    stop_image = PhotoImage(file=stop_image_path)

        # 버튼 생성 및 배치
    pick_button = tk.Button(canvas, image=pick_image, bd=0,
                                 command=pick_clicked(button_events=button_events), bg="white")
    pick_button.place(x=835, y=346)

    put_button = tk.Button(canvas, image=put_image(button_events=button_events), bd=0,
                                command=put_clicked, bg="white")
    put_button.place(x=835, y=458)
    stop_button = tk.Button(canvas, image=stop_image(button_events=button_events), bd=0,
                                 command=stop_clicked, bg="white")
    stop_button.place(x=835, y=570)
    # Hover 이벤트 처리
    pick_button.bind("<Enter>", lambda event, btn=pick_button: on_enter(event, btn, pick_image))
    pick_button.bind("<Leave>", lambda event, btn=pick_button: on_leave(event, btn, pick_image))
    put_button.bind("<Enter>", lambda event, btn=put_button: on_enter(event, btn, put_image))
    put_button.bind("<Leave>", lambda event, btn=put_button: on_leave(event, btn, put_image))
    stop_button.bind("<Enter>", lambda event, btn=stop_button: on_enter(event, btn, stop_image))
    stop_button.bind("<Leave>", lambda event, btn=stop_button: on_leave(event, btn, stop_image))



    
    # 실제 제어랑 연관된 부분
def pick_clicked(button_events):
    print("Pick button clicked")
    button_events.grab()
    
def put_clicked(button_events):
    print("Put button clicked")
    button_events.release()
def stop_clicked(button_events):
    print("Stop button clicked")
    button_events.emergency_stop()
    
def on_enter(event, button, image):
    button.config(bg="gray")  # Hover 시 배경색 변경
    button.config(image=image)  # 이미지 객체 설정

def on_leave(event, button, image):
    button.config(bg="white")  # Hover 떠날 때 배경색 원래대로
    button.config(image=image)  # 이미지 객체 설정