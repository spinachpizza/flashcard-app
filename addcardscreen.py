import customtkinter as ctk
from data import colours, topics, save_data, userimgs, resource_path
from card import card
from topic import topic
from entryscreen import entryscreen
import shutil
import os




class addcard(entryscreen):

    def __init__(self, root, app):
        super().__init__(root, app)



    def setup(self):
        super().setup()

        self.cancelbutton = ctk.CTkButton(self.main, text="Cancel", font=("Helvetica", 15), width=120,height=40, text_color=colours[0],
                                     fg_color=colours[2], hover_color=colours[3])
        self.cancelbutton.place(x=115,y=440)

        self.savebutton = ctk.CTkButton(self.main, text="Enter", font=("Helvetica",15), width=120, height=40, text_color=colours[0],
                                        fg_color=colours[2], hover_color=colours[3])
        self.savebutton.place(x=515,y=440)


    def show(self, topic):
        super().show(topic)
        self.cancelbutton.configure(command=lambda: self.app.open_options(topic))
        self.savebutton.configure(command=lambda: self.savecard(topic))



    def savecard(self, topic):
        texts = super().savecard(topic)

        qtext = texts[0]
        atext = texts[1]


        topic.addcard(card(qtext,atext))
        self.qEntry.delete(1.0, ctk.END)
        self.aEntry.delete(1.0, ctk.END)
        
        if self.file_path and self.imgselected == True:
            cards = topic.getcards()
            cards[len(cards)-1].changetext(qtext,"")
            self.saveimage(topic)

        save_data()
        self.app.open_options(topic)



    def saveimage(self, topic):
        
        cards = topic.getcards()
        index = len(cards) - 1

        
        if cards[index].getimgnum():
            filenum = cards[index].getimgnum()
        else:
            filenum = userimgs[0]
            userimgs[0] += 1
            
        filename = f"img{filenum}.png"
        dest_path = os.path.join(resource_path("data/img"), filename)
        shutil.copy(self.file_path, dest_path)
        
        self.resizeimg(dest_path)

        cards = topic.getcards()
        index = len(cards) - 1
        print(filenum)
        cards[index].changeimage(filenum)

        save_data()







    
