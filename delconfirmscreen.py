import customtkinter as ctk
from data import colours, topics, save_data, resource_path
from screen import screen
import os

class delconfirm(screen):

    def __init__(self, root, app):
        super().__init__(root, app)


    def setup(self):
        self.frame = ctk.CTkFrame(self.main, width=300, height=200, fg_color=colours[4])
        self.frame.place(x=225,y=140)
        
        ctk.CTkLabel(self.frame, text="Are you sure you want to \n delete this topic?", font=("Helvetica", 24)
                     ).place(relx=0.5, rely=0.25, anchor="center")

        self.confirmbutton = ctk.CTkButton(self.frame, text="Confirm", font=("Helvetica", 15), width=80, height=40,
                                              text_color=colours[0], fg_color=colours[2], hover_color=colours[3])
        self.confirmbutton.place(relx=0.7, rely=0.65, anchor="center")

        self.cancelbutton = ctk.CTkButton(self.frame, text="Cancel", font=("Helvetica", 15), width=80, height=40,
                                             text_color=colours[0], fg_color=colours[2], hover_color=colours[3])
        self.cancelbutton.place(relx=0.3, rely=0.65, anchor="center")


    def show(self, topic):
        super().show()
        self.confirmbutton.configure(command=lambda: self.deletetopic(topic))
        self.cancelbutton.configure(command=lambda: self.app.open_options(topic))



    def deletetopic(self, topic):
        cards = topic.getcards()
        for card in cards:
            self.deleteimage(card)
        topics.remove(topic)
        save_data()
        self.app.open_main()


    def deleteimage(self, card):
        imgnum = card.getimgnum()
        if imgnum:
            print(imgnum)
            path = f"images/user/img{imgnum}.png"
            try:
                os.remove(resource_path(path))
            except:
                print("Could not remove")
                pass

