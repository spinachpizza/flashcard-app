import customtkinter as ctk
from data import colours

class screen():

    def __init__(self, root, app):
        self.main = ctk.CTkFrame(root, width=750, height=500, fg_color=colours[1])
        self.root = root
        self.app = app
        self.setup()


    def show(self):
        self.main.place(x=0,y=0)


    def hide(self):
        self.main.place_forget()
