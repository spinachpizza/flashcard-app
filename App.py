import customtkinter as ctk
from mainscreen import main
from optionscreen import options
from addcardscreen import addcard
from flashcardscreen import flashcards
from delconfirmscreen import delconfirm
from editscreen import edit
from editcardscreen import editcard
from feedbackscreen import feedback
import data


from data import paths

class App():

    def __init__(self):
        self.setup()
        


    def setup(self):

        self.root = ctk.CTk()
        self.root.title("FlashCards")
        self.root.geometry("750x500")
        self.root.resizable(False, False)
        self.root.iconbitmap(paths[2])


        self.main = main(self.root,self)
        self.options = options(self.root,self)
        self.addcard = addcard(self.root,self)
        self.flashcards = flashcards(self.root, self)
        self.delconfirm = delconfirm(self.root, self)
        self.edit = edit(self.root, self)
        self.editcard = editcard(self.root, self)
        self.main.show()

        

        self.root.mainloop()


    def hideall(self):
        self.main.hide()
        self.options.hide()
        self.addcard.hide()
        self.flashcards.hide()
        self.delconfirm.hide()
        self.edit.hide()
        self.editcard.hide()


    def open_main(self):
        self.hideall()
        self.main.show()


    def open_options(self, topic):
        self.hideall()
        self.options.show(topic)


    def open_addcard(self, topic):
        self.hideall()
        self.addcard.show(topic)


    def open_flashcard(self, topic):
        self.hideall()
        self.flashcards.show(topic)


    def open_delconfirm(self, topic):
        self.hideall()
        self.delconfirm.show(topic)


    def open_edit(self, topic, boolean):
        if(len(topic.getcards()) > 0):
            self.hideall()
            self.edit.show(topic, boolean)


    def open_editcard(self, topic, index):
        self.hideall()
        self.editcard.show(topic, index)



app = App()
