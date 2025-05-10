import customtkinter as ctk
from data import colours, topics, save_data, resource_path
from displayscreen import displayscreen
import os

class edit(displayscreen):

    def __init__(self, root, app):
        super().__init__(root,app)
        


    def setup(self):
        super().setup()

        self.delbutton = ctk.CTkButton(self.main, width=100, height=40, text="Delete", font=("Helvetica", 15),
                                              text_color=colours[0], fg_color=colours[2], hover_color=colours[3])
        self.delbutton.place(x=625,y=440)


        self.editbutton = ctk.CTkButton(self.main, width=100, height=40, text="Edit Text", font=("Helvetica", 15),
                                            text_color=colours[0], fg_color=colours[2], hover_color=colours[3])
        self.editbutton.place(x=155,y=440)

    def setup2(self):
        self.frame = ctk.CTkFrame(self.main, width=630, height=360, border_width=5, border_color=colours[2])
        self.frame.place(x=60,y=20)

        self.text = ctk.CTkButton(self.frame, text_color=colours[0], fg_color=colours[1], hover_color=colours[1],
                                       text="", font=("Helvetica", 18), width=620, height=350, command=self.swaptext)
        self.text.place(x=5,y=5)


        self.bar = ctk.CTkFrame(self.main, width=750, height=100, fg_color=colours[4])
        self.bar.place(x=0,y=400)


        self.backbutton = ctk.CTkButton(self.bar, width=85, height=40, text="Return", font=("Helvetica", 15),
                                        text_color=colours[0], fg_color=colours[1], hover_color=colours[2])
        self.backbutton.place(x=20,y=20)


        self.delbutton = ctk.CTkButton(self.bar, width=100, height=40, text="Delete", font=("Helvetica", 15),
                                              text_color=colours[0], fg_color=colours[1], hover_color=colours[2])
        self.delbutton.place(x=630,y=20)


        self.editbutton = ctk.CTkButton(self.bar, width=100, height=40, text="Edit Text", font=("Helvetica", 15),
                                            text_color=colours[0], fg_color=colours[1], hover_color=colours[2])
        self.editbutton.place(x=155,y=20)

        self.cardnum = ctk.CTkLabel(self.bar, text_color=colours[0], text="", font=("Helvetica", 16), width=40, height=40,
                                    fg_color=colours[4])
        self.cardnum.place(relx=0.5,y=40, anchor="center")


        self.prevbutton = ctk.CTkButton(self.bar, text_color=colours[0], fg_color=colours[1], hover_color=colours[2],
                                       text="<", font=("Helvetica", 14), width=40, height=40, command=self.prevcard)
        self.prevbutton.place(x=305,y=20)

        
        self.nextbutton = ctk.CTkButton(self.bar, text_color=colours[0], fg_color=colours[1], hover_color=colours[2],
                                       text=">", font=("Helvetica", 14), width=40, height=40, command=self.nextcard)
        self.nextbutton.place(x=405,y=20)






    def show(self, topic, reset):
        self.cards = topic.getcards()
        if(reset):
            self.index = 0
        super().show(topic)


        self.returnbutton.configure(command=lambda: self.app.open_options(topic))
        self.delbutton.configure(command=lambda: self.removecard(topic))
        self.editbutton.configure(command=lambda: self.app.open_editcard(topic, self.index))



    def hide(self):
        super().hide()
        self.img = None
        self.adisplay.configure(image=None)
        



    def removecard(self, topic):
        print("attempting to delete")
        self.deleteimage(topic)
        if(topic.removecard(self.index) == 1):
            print("Removed")
            if(self.index >= len(topic.getcards())):
                self.index -= 1
                if(self.index < 0):
                    self.app.open_options(topic)
            self.displaycard()
        else:
            print("failed to delete")
        save_data()


    def deleteimage(self, topic):
        imgnum = topic.getcards()[self.index].getimgnum()
        if imgnum:
            self.img = None
            self.adisplay.configure(image=None)
            path = f"images/user/img{imgnum}.png"
            #os.remove(resource_path(path))
            try:
                os.remove(resource_path(path))
                print(f"File img{imgnum} deleted")
            except:
                pass

