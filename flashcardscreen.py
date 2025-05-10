import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk
from data import colours, topics, paths, save_data
import random
from displayscreen import displayscreen


class flashcards(displayscreen):

    
    def __init__(self, root, app):
        self.imgC = ctk.CTkImage(light_image=Image.open(paths[8]), size=(20,20))
        super().__init__(root,app)
        self.feedbackval = 1
        self.feedbackopen = False
        




    def show(self, topic):
        self.cards = topic.getcards()
        self.dofeedback = topic.getdofeedback()
        for card in self.cards:
            card.resetprovidefeedback()
        #If feedback on apply a weighted shuffle to prioritise lower known cards
        if(self.dofeedback == True):
            self.cards = self.weightedshuffle()
        else:
            random.shuffle(self.cards)
        super().show(topic)
        self.frame.place(x=25, y=25)


        self.qdisplay.configure(fg_color=topic.getbg(), hover_color=topic.getbg())
        self.adisplay.configure(fg_color=topic.getbg(), hover_color=topic.getbg())







            


    def hide(self):
        super().hide()
        self.feedbackframe.place_forget()

        self.index = 0
        self.op = 0

        for card in self.cards:
            card.resetprovidefeedback()


    def prevcard(self):
        if(self.feedbackopen):
            self.closefeedback()
        self.op = 0
        if(len(self.cards) > 0):
            if(self.index > 0):
                self.index -= 1
            self.displaycard()



    def nextcard(self):
        if(self.feedbackopen == True):
            self.closefeedback()
        elif(self.cards[self.index].providedfeedback == False and self.dofeedback):
            self.openfeedback()
        else:
            self.op = 0
            if(len(self.cards) > 0):
                if(self.index < len(self.cards) - 1):
                    self.index += 1
                else:
                    self.app.open_main()
                self.displaycard()



    def openfeedback(self):
        self.feedbackopen = True
        self.frame.place_forget()
        self.feedbackframe.place(x=25,y=25)


    def closefeedback(self):
        self.feedbackopen = False
        self.feedbackframe.place_forget()
        self.frame.place(x=25,y=25)

        self.canvas.itemconfig(self.circle, fill=colours[1])
        self.canvas.itemconfig(self.circle1, fill=colours[1])
        self.canvas.itemconfig(self.circle2, fill=colours[1])


        self.cards[self.index].providefeedback(self.feedbackval)

        self.feedbackval=1

        save_data()

        self.nextcard()



    def weightedshuffle(self):
        

        weighted = []

        for card in self.cards:
            weighted.append([card, card.getkval()])
    
        result = []
    
        while weighted:
            total = sum(w for _, w in weighted)
            r = random.uniform(0, total)
            
            # Find which card "wins" this position
            current = 0
            for i, (card, w) in enumerate(weighted):
                current += w
                if r <= current:
                    result.append(card)
                    del weighted[i]
                    break
        
        return result



    def setup(self):
        super().setup()
        self.feedbacksetup()







    def feedbacksetup(self):

        self.feedbackval = 1

        self.feedbackframe = ctk.CTkFrame(self.main, width=700, height=400, border_width=5, border_color=colours[2],
                                          fg_color=colours[1])



        ctk.CTkLabel(self.feedbackframe, text="How did you find \n that question?", font=("Helvetica", 20),
                     text_color=colours[0], width=150, height=80).place(x=275,y=30)


        #self.continuebutton = ctk.CTkButton(self.feedbackframe, width=100, height=40, text_color=colours[0], fg_color=colours[2],
                                           #hover_color=colours[3], text="Continue", font=("Helvetica", 14), command=self.closefeedback)
        #self.continuebutton.place(x=300, y=270)

    
        self.canvas = tk.Canvas(self.feedbackframe, width=300, height=100, highlightthickness=0, bg=colours[1])
        self.canvas.place(x=300, y=170)
        
        self.circle = self.canvas.create_oval(2, 0, 79, 79, fill=colours[1], outline="")
        self.circle1 = self.canvas.create_oval(102, 0, 179, 79, fill=colours[1], outline="")
        self.circle2 = self.canvas.create_oval(200, 0, 279, 79, fill=colours[1], outline="")

        imgS = Image.open(paths[3]).resize((96, 96))
        imgS = ImageTk.PhotoImage(imgS)

        imgN = Image.open(paths[4]).resize((96, 96))
        imgN = ImageTk.PhotoImage(imgN)

        imgH = Image.open(paths[5]).resize((96, 96))
        imgH = ImageTk.PhotoImage(imgH)

        # Place the image on the canvas
        sadface = self.canvas.create_image(40, 40, image=imgS)  # Center of canvas
        self.canvas.image1 = imgS

        neutralface = self.canvas.create_image(140, 40, image=imgN)  # Center of canvas
        self.canvas.image2 = imgN

        happyface = self.canvas.create_image(238, 40, image=imgH)  # Center of canvas
        self.canvas.image3 = imgH


        ctk.CTkLabel(self.feedbackframe, text="Bad", font=("Helvetica", 15),
            text_color=colours[0], width=80, height=20).place(x=230,y=210)

        ctk.CTkLabel(self.feedbackframe, text="Okay", font=("Helvetica", 15),
            text_color=colours[0], width=80, height=20).place(x=310,y=210)
        
        ctk.CTkLabel(self.feedbackframe, text="Good", font=("Helvetica", 15),
            text_color=colours[0], width=80, height=20).place(x=390,y=210)


        def onsadclick(event):
            self.feedbackval = 0
            self.canvas.itemconfig(self.circle, fill=colours[2])
            self.canvas.itemconfig(self.circle1, fill=colours[1])
            self.canvas.itemconfig(self.circle2, fill=colours[1])

        def onneutralclick(event):
            self.feedbackval = 1
            self.canvas.itemconfig(self.circle, fill=colours[1])
            self.canvas.itemconfig(self.circle1, fill=colours[2])
            self.canvas.itemconfig(self.circle2, fill=colours[1])

        def onhappyclick(event):
            self.feedbackval = 2
            self.canvas.itemconfig(self.circle, fill=colours[1])
            self.canvas.itemconfig(self.circle1, fill=colours[1])
            self.canvas.itemconfig(self.circle2, fill=colours[2])

        self.canvas.tag_bind(sadface, "<Button-1>", onsadclick)
        self.canvas.tag_bind(neutralface, "<Button-1>", onneutralclick)
        self.canvas.tag_bind(happyface, "<Button-1>", onhappyclick)

            
