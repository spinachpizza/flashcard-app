import customtkinter as ctk
from data import colours, resource_path, paths
from screen import screen
from PIL import Image


class displayscreen(screen):

    def __init__(self, root, app):
        self.imghold = ctk.CTkImage(light_image=Image.open(resource_path(paths[11])), size=(1,1))
        super().__init__(root, app)
        self.op = 0
        self.index = 0
        self.cards = []

        self.setupkeys()



    def setup(self):
        self.frame = ctk.CTkFrame(self.main, width=700, height=400, border_width=5, border_color=colours[2])
        self.frame.place(x=25,y=25)
        

        self.qdisplay = ctk.CTkButton(self.frame, text="", text_color=colours[0], fg_color=colours[1], hover_color=colours[1],
                              font=("Helvetica", 19), width=690, height=390, command=self.swaptext, corner_radius=3)
        self.adisplay = ctk.CTkButton(self.frame, text="", text_color=colours[0], fg_color=colours[1], hover_color=colours[1],
                              font=("Helvetica", 19), width=690, height=390, command=self.swaptext, corner_radius=3, image=self.imghold)
        self.qdisplay.place(x=5,y=5)

        
        self.returnbutton = ctk.CTkButton(self.main, text_color=colours[0], fg_color=colours[2], hover_color=colours[3],
                                     text="Return", font=("Helvetica", 14), width=100, height=40, command=self.app.open_main)
        self.returnbutton.place(x=25,y=440)


        self.cardnum = ctk.CTkLabel(self.main, text_color=colours[0], text="", font=("Helvetica", 16), width=40, height=40)
        self.cardnum.place(relx=0.5,y=460, anchor="center")


        self.prevbutton = ctk.CTkButton(self.main, text_color=colours[0], fg_color=colours[2], hover_color=colours[3],
                                       text="<", font=("Helvetica", 14), width=40, height=40, command=self.prevcard)
        self.prevbutton.place(x=305,y=440)

        
        self.nextbutton = ctk.CTkButton(self.main, text_color=colours[0], fg_color=colours[2], hover_color=colours[3],
                                       text=">", font=("Helvetica", 14), width=40, height=40, command=self.nextcard)
        self.nextbutton.place(x=405,y=440)



    def show(self,topic):
        super().show()
        self.setupkeys()
        self.dokeypresses = True
        if(len(self.cards) > 0):
            self.displaycard()


    def hide(self):
        super().hide()
        self.qdisplay.configure(text="")
        self.img = None
        self.adisplay.configure(text="", image=None)
        self.cardnum.configure(text="0/0")
        self.dokeypresses = False


    def displaycard(self):

        if(len(self.cards) > 0):

            qtext = self.cards[self.index].getquestion()
            self.qdisplay.configure(text=qtext)
            
            if(self.cards[self.index].getdisplayimg()):
                imgnum = self.cards[self.index].getimgnum()
                path = f"data/img/img{imgnum}.png"
                pil_image = Image.open(resource_path(path))
                w, h = pil_image.size
                self.img = ctk.CTkImage(light_image=Image.open(resource_path(path)), size=(w,h))
                self.adisplay.configure(text="", image=self.img)
            else:
                atext = self.cards[self.index].getanswer()
                self.adisplay.configure(text=atext, image=self.imghold)


            
            if(self.op == 0):
                self.qdisplay.place(x=5,y=5)
                self.adisplay.place_forget()
            else:
                self.qdisplay.place_forget()
                self.adisplay.place(x=5,y=5)


            text = (self.index+1, "/" , len(self.cards))
            self.cardnum.configure(text=text)


    def swaptext(self):
        if(len(self.cards) > 0):
            self.op += 1
            if(self.op > 1):
                self.op = 0
            self.displaycard()


    def prevcard(self):
        self.op = 0
        if(len(self.cards) > 0):
            if(self.index > 0):
                self.index -= 1
            self.displaycard()


    def nextcard(self):
        self.op = 0
        if(len(self.cards) > 0):
            if(self.index < len(self.cards) - 1):
                self.index += 1
            self.displaycard()



    def setupkeys(self):
        self.dokeypresses = False

        # Bind spacebar to flip the card
        def spacebar_press(event):
            if(self.dokeypresses):
                self.swaptext()
        self.root.bind("<space>", spacebar_press)

        # Bind left arrow to prev card
        def larrow_press(event):
            if(self.dokeypresses):
                self.prevcard()
        self.root.bind("<Left>", larrow_press)

        # Bind right arrow to next card
        def rarrow_press(event):
            if(self.dokeypresses):
                self.nextcard()
        self.root.bind("<Right>", rarrow_press)
        
