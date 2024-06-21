import tkinter as tk
from tkinter import PhotoImage
from button_events import ButtonEventGroup  # 수정된 import 문

def create_buttons(canvas):
    button_events = ButtonEventGroup()  # button_event_group() 대신 ButtonEventGroup() 사용

    pick_image_path = "./btn_images/pick.png"
    put_image_path = "./btn_images/put.png"
    stop_image_path = "./btn_images/stop.png"

    pick_image = PhotoImage(file=pick_image_path)
    put_image = PhotoImage(file=put_image_path)
    stop_image = PhotoImage(file=stop_image_path)

    pick_button = tk.Button(canvas, image=pick_image, bd=0, command=lambda: pick_clicked(button_events))
    pick_button.image = pick_image  # 이미지 객체를 버튼의 속성으로 설정
    pick_button.place(x=835, y=346)

    put_button = tk.Button(canvas, image=put_image, bd=0, command=lambda: put_clicked(button_events))
    put_button.image = put_image  # 이미지 객체를 버튼의 속성으로 설정
    put_button.place(x=835, y=458)

    stop_button = tk.Button(canvas, image=stop_image, bd=0, command=lambda: stop_clicked(button_events))
    stop_button.image = stop_image  # 이미지 객체를 버튼의 속성으로 설정
    stop_button.place(x=835, y=570)

    # Hover 이벤트 처리
    pick_button.bind("<Enter>", lambda event, btn=pick_button: on_enter(event, btn, pick_image))
    pick_button.bind("<Leave>", lambda event, btn=pick_button: on_leave(event, btn, pick_image))
    put_button.bind("<Enter>", lambda event, btn=put_button: on_enter(event, btn, put_image))
    put_button.bind("<Leave>", lambda event, btn=put_button: on_leave(event, btn, put_image))
    stop_button.bind("<Enter>", lambda event, btn=stop_button: on_enter(event, btn, stop_image))
    stop_button.bind("<Leave>", lambda event, btn=stop_button: on_leave(event, btn, stop_image))

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
