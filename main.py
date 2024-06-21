import tkinter as tk
from tkinter import PhotoImage
from buttons import create_buttons

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Button Example")
        self.root.geometry("1280x720")
        self.root.resizable(False, False)

        # 배경 이미지 로드
        background_image_path = "background.png"
        self.background_image = PhotoImage(file=background_image_path)
        
        # Canvas 생성 후 배경 이미지 표시
        self.canvas = tk.Canvas(self.root, width=1280, height=720)
        self.canvas.pack(fill="both", expand=True)
        
        #버튼들 생성
        create_buttons(self.canvas)     
        
        self.canvas.create_image(0, 0, image=self.background_image, anchor="nw")


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
