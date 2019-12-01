import tkinter as tk
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk

class test_window(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.frame1 = tk.Frame(root)
        self.initUI()    
        self.frame1.pack()
        self.pack()

    def initUI(self):
        self.canvas = tk.Canvas(self.frame1, width=640, height=480, bg='green')
        self.canvas.pack()
        image = Image.open("background.png")
        tkimg = ImageTk.PhotoImage(image)
        self.canvas.create_image(200,200, image=tkimg, tags='img')

if __name__ == "__main__":
    root = tk.Tk()
    root.title("test-window")
    Grid.rowconfigure(root, 0, weight=1)
    Grid.columnconfigure(root, 0, weight=1)
    root.geometry("640x480")
    app = test_window(root)
    app.mainloop()
 