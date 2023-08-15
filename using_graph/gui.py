import tkinter as tk
from threading import Thread
import pygame
from PIL import Image, ImageTk

class GUIVideo:
    # cbfn should return a pygame surface
    def __init__(self, lbl, cbfn):
        self.cbfn = cbfn
        self.lbl = lbl
    def show(self):
        with open("thread out.txt","a+") as f:
            f.write("HERE\n")
        arr = pygame.surfarray.array3d(self.cbfn())
        im = Image.fromarray(arr)
        img = ImageTk.PhotoImage(image=im)
        self.lbl.configure(image=img)
        self.lbl.image=img
        self.lbl.pack()
        self.lbl.master.after(10, self.show)

class GUIWindow:
    def __init__(self, w, h, title="GUI WINDOW"):
        self.w = w
        self.h = h
        self.title = title
        self.running = False
        self.labels = []
        self.buttons = []
        self.videos = []
        self.init_tk()
    def init_tk(self):
        self.win  = tk.Tk()
        self.win.geometry(f"{self.w}x{self.h}")
        self.win.title(self.title)

    def text(self, txt):
        # TODO: if running, call update + if init
        if self.running:
            raise Exception("Cannot add to window once it is running")
        self.labels.append(tk.Label(self.win, text=txt).pack(pady=10))
        return len(self.labels) - 1

    def butt(self, txt, cbfn):
        if self.running:
            raise Exception("Cannot add to window once it is running")
        self.buttons.append(tk.Button(self.win, text=txt, command=cbfn).pack(pady=10))
        return len(self.buttons) - 1

    def add_video(self, cbfn):
        # cbfn should return a pygame surface
        self.videos.append(GUIVideo(tk.Label(self.win), cbfn))
        return len(self.videos) - 1

    def run(self):
        for video in self.videos:
            video.show()
        print("Here")
        self.running = True
        self.win.update()
        # self.win.mainloop()
        # t = Thread(target=self.win.mainloop)
        # t.daemon = True
        # t.start()
        
