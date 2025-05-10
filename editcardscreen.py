import customtkinter as ctk
from data import colours, save_data, userimgs
from entryscreen import entryscreen
import shutil
import os

class editcard(entryscreen):

    def __init__(self, root, app):
        super().__init__(root, app)
        self.card = None


    def setup(self):
        super().setup()

        self.cancelbutton = ctk.CTkButton(self.main, text="Cancel", font=("Helvetica", 15), width=120,height=40,
                                          text_color=colours[0], fg_color=colours[2], hover_color=colours[3])
        self.cancelbutton.place(x=115,y=440)

        self.savebutton = ctk.CTkButton(self.main, text="Save Changes", font=("Helvetica",15), width=120, height=40,
                                        text_color=colours[0], fg_color=colours[2], hover_color=colours[3])
        self.savebutton.place(x=515,y=440)


    def show(self, topic, index):
        super().show(topic)
        
        self.card = topic.getcards()[index]

        self.cancelbutton.configure(command=lambda: self.app.open_edit(topic, False))
        self.savebutton.configure(command=lambda: self.savecard(topic, index))

        qtext = self.card.getquestion()
        atext = self.card.getanswer()

        self.qEntry.insert("0.0",qtext)
        self.aEntry.insert("0.0",atext)



    def savecard(self, topic, index):
        
        texts = super().savecard(topic)

        qtext = texts[0]
        atext = texts[1]

        self.card.changetext(qtext,atext)


        if self.file_path and self.imgselected == True:
            self.saveimage(topic)


        save_data()
        self.app.open_edit(topic, False)



    def saveimage(self, topic):
        


        print(self.card.getimgnum())
        if self.card.getimgnum():
            filenum = self.card.getimgnum()
        else:
            filenum = userimgs[0]
            userimgs[0] += 1
            
        filename = f"img{filenum}.png"
        dest_path = os.path.join("data/img", filename)
        shutil.copy(self.file_path, dest_path)
        
        self.resizeimg(dest_path)

        self.card.changeimage(filenum)

        save_data()

        



