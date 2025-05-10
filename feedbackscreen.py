import customtkinter as ctk
from PIL import Image, ImageTk, ImageDraw
from data import colours, paths

class feedback():

    def __init__(self, root, app):
        self.main = ctk.CTkFrame(root, width=750, height=500, fg_color=colours[1])
        imgsize = 64
        self.imgS = ctk.CTkImage(light_image=Image.open(paths[3]), size=(imgsize,imgsize))
        self.imgN = ctk.CTkImage(light_image=Image.open(paths[4]), size=(imgsize,imgsize))
        self.imgH = ctk.CTkImage(light_image=Image.open(paths[5]), size=(imgsize,imgsize))
        self.root = root
        self.app = app
        self.setup()


    def setup(self):

        self.sback = ctk.CTkButton(self.main, width=64, height=64, corner_radius=32, text="", fg_color=colours[2])
        self.sback.place(x=100,y=100)
        
        self.sadbutton = ctk.CTkLabel(self.main, width=64, height=64, text="", corner_radius=32,
                                       image=self.imgS)
        self.sadbutton.place(x=100,y=100)

        

        
        


    def show(self):
        self.main.place(x=0,y=0)


    def hide(self):
        self.main.place_forget()
