import customtkinter as ctk
from tkinter import colorchooser
from PIL import Image
from data import colours, topics, paths, save_data
from screen import screen

class options(screen):

    def __init__(self, root, app):
        self.imgW = ctk.CTkImage(light_image=Image.open(paths[6]), size=(20,20))
        self.imgB = ctk.CTkImage(light_image=Image.open(paths[7]), size=(20,20))
        self.imgC = ctk.CTkImage(light_image=Image.open(paths[8]), size=(20,20))
        super().__init__(root,app)
        self.colour = colours[1]

    

    def setup(self):

        self.frames = {}

        self.frames["sidebar"] = ctk.CTkFrame(self.main, fg_color=colours[4], width=225, height=500)
        self.frames["sidebar"].place(x=0,y=0)

        self.frames["edit"] = ctk.CTkFrame(self.main, width=525, height=500, fg_color=colours[1])

        self.frames["customisation"] = ctk.CTkFrame(self.main, width=525, height=500, fg_color=colours[1])

        self.frames["progression"] = ctk.CTkFrame(self.main, width=525, height=500, fg_color=colours[1])


        #Sidebar

        self.title = ctk.CTkLabel(self.frames["sidebar"], fg_color=colours[4], text_color=colours[0],text="Settings", font=("Helvetica", 32))
        self.title.place(relx=0.35, rely=0.1, anchor="center")


        self.editbutton = ctk.CTkButton(self.frames["sidebar"], text="Edit", font=("Helvetica", 15), anchor="w", image=self.imgW, width=200,
                                        height=50, text_color=colours[0], fg_color=colours[4], hover_color=colours[1])
        self.editbutton.place(relx=0.5, rely=0.25, anchor="center")


        self.custombutton = ctk.CTkButton(self.frames["sidebar"], text="Customisation", font=("Helvetica", 15), command=lambda:self.app.open_main(),
                                        anchor="w", image=self.imgB, width=200, height=50, text_color=colours[0],
                                        fg_color=colours[4], hover_color=colours[1])
        self.custombutton.place(relx=0.5, rely=0.35, anchor="center")


        self.progressbutton = ctk.CTkButton(self.frames["sidebar"], text="Progression", font=("Helvetica", 15), command=lambda:self.app.open_main(),
                                        anchor="w", image=self.imgC, width=200, height=50, text_color=colours[0],
                                        fg_color=colours[4], hover_color=colours[1])
        self.progressbutton.place(relx=0.5, rely=0.45, anchor="center")


        self.backbutton = ctk.CTkButton(self.frames["sidebar"], text="Return", font=("Helvetica", 15),
                                        command=lambda:self.app.open_main(), anchor="w", width=200, height=50, text_color=colours[0],
                                        fg_color=colours[4],hover_color=colours[1])
        self.backbutton.place(relx=0.5, rely=0.9, anchor="center")




        #Edit Page

        ctk.CTkLabel(self.frames["edit"], text="Edit Topic", font=("Helvetica", 25), width=100, height=50,
                     text_color=colours[0], anchor="w").place(relx=0.1, rely=0.1, anchor="w")
        

        ctk.CTkLabel(self.frames["edit"], text="Add a new card to this topic.", font=("Helvetica", 15), width=100, height=50,
                     text_color=colours[0], anchor="w").place(relx=0.1, rely=0.2, anchor="w")
        self.addbutton = ctk.CTkButton(self.frames["edit"], text="Add Card", font=("Helvetica", 15), width=150, height=40,
                                         text_color=colours[0], fg_color=colours[2], hover_color=colours[3])
        self.addbutton.place(relx=0.24, rely=0.28, anchor="center")


        ctk.CTkLabel(self.frames["edit"], text="Edit the existing cards in this topic.", font=("Helvetica", 15), width=100, height=50,
                     text_color=colours[0], anchor="w").place(relx=0.1, rely=0.45, anchor="w")
        self.editcardbutton = ctk.CTkButton(self.frames["edit"], text="Edit Cards", font=("Helvetica", 15), width=150, height=40,
                                         text_color=colours[0], fg_color=colours[2], hover_color=colours[3])
        self.editcardbutton.place(relx=0.24, rely=0.53, anchor="center")


        ctk.CTkLabel(self.frames["edit"], text="Delete the current topic. Once deleted this action cannot be \nundone.", font=("Helvetica", 15), width=100, height=50,
                     text_color=colours[0], anchor="w", justify="left").place(relx=0.1, rely=0.7, anchor="w")
        self.delbutton = ctk.CTkButton(self.frames["edit"], text="Delete Topic", font=("Helvetica", 15), width=150, height=40,
                                         text_color=colours[0], fg_color=colours[2], hover_color=colours[3])
        self.delbutton.place(relx=0.24, rely=0.8, anchor="center")


        #Customisation Page
        ctk.CTkLabel(self.frames["customisation"], text="Customise Topic", font=("Helvetica", 25), width=100, height=50,
                     text_color=colours[0], anchor="w").place(relx=0.1, rely=0.1, anchor="w")

        
        def choose_colour():
            """Open the color picker dialog and update the label."""
            self.colour = colorchooser.askcolor()[1]  # askcolor() returns a tuple, [1] gives the hex color value
            if self.colour:  # If the user selected a color
                self.colour_button.configure(fg_color=self.colour)  # Change background color of the button


        ctk.CTkLabel(self.frames["customisation"], text="Change the background colour of the cards.", font=("Helvetica", 15), width=100, height=50,
                     text_color=colours[0], anchor="w").place(relx=0.1, rely=0.2, anchor="w")
        # Button to trigger the color picker
        self.colour_button = ctk.CTkButton(self.frames["customisation"], text="", command=choose_colour, width=150, height=40)
        self.colour_button.place(relx=0.1, rely=0.28, anchor="w")


        ctk.CTkLabel(self.frames["customisation"], text="Rename this topic.", font=("Helvetica", 15), width=100, height=50,
                     text_color=colours[0], anchor="w").place(relx=0.1, rely=0.45, anchor="w")
        self.nameinput = ctk.CTkEntry(self.frames["customisation"], font=("Helvetica", 15), width=190, height=40,text_color=colours[0])
        self.nameinput.place(relx=0.1, rely=0.53, anchor="w")
        

        self.applybutton = ctk.CTkButton(self.frames["customisation"], text="Apply Changes", font=("Helvetica", 15), width=150, height=40,
                                         text_color=colours[0], fg_color=colours[2], hover_color=colours[3])
        self.applybutton.place(relx=0.1, rely=0.75, anchor="w")

        self.defaultbutton = ctk.CTkButton(self.frames["customisation"], text="Revert to Default", font=("Helvetica", 15), width=150, height=40,
                                         text_color=colours[0], fg_color=colours[2], hover_color=colours[3])
        self.defaultbutton.place(relx=0.42, rely=0.75, anchor="w")


        
        #Progress Page
        ctk.CTkLabel(self.frames["progression"], text="Topic Progress", font=("Helvetica", 25), width=100, height=50,
                     text_color=colours[0], anchor="w").place(relx=0.1, rely=0.1, anchor="w")

        ctk.CTkLabel(self.frames["progression"], text="Current Progress.", font=("Helvetica", 15), width=100, height=50,
                     text_color=colours[0], anchor="w").place(relx=0.1, rely=0.2, anchor="w")

        self.progressbar = ctk.CTkFrame(self.frames["progression"], border_width=5, border_color=colours[2], width=410, height=40)
        self.progressbar.place(relx=0.1, rely=0.28, anchor="w")


        ctk.CTkLabel(self.frames["progression"], text="Enable/Disable card feedback and less known card priority \nsorting.", font=("Helvetica", 15),
                     width=100, height=50, text_color=colours[0], anchor="w", justify="left").place(relx=0.1, rely=0.45, anchor="w")

        self.switch = ctk.CTkSwitch(self.frames["progression"], text="", border_width=1)
        self.switch.place(relx=0.1, rely=0.53, anchor="w")
        self.switch.select()

        self.applybutton2 = ctk.CTkButton(self.frames["progression"], text="Apply Changes", font=("Helvetica", 15), width=150, height=40,
                                         text_color=colours[0], fg_color=colours[2], hover_color=colours[3])
        self.applybutton2.place(relx=0.1, rely=0.75, anchor="w")



    def updateprogressbar(self, topic):

        self.bar1 = None
        self.bar2 = None
        self.bar3 = None

        if(len(topic.getcards()) > 0):
            counts = topic.getprogress()

            total = counts[0] + counts[1] + counts[2]

            hbar = (counts[0]/total) * 400
            nbar = ((counts[1]/total) * 400) + 1
            sbar = ((counts[2]/total) * 400) + 2

            self.bar1 = ctk.CTkLabel(self.progressbar, fg_color="#50C878", width=hbar, height=32, text="").place(x=5,y=5)
            self.bar2 = ctk.CTkLabel(self.progressbar, fg_color="#FFAA1D", width=nbar, height=32, text="").place(x=4+hbar,y=5)
            self.bar3 = ctk.CTkLabel(self.progressbar, fg_color="#FF6B6B", width=sbar, height=32, text="").place(x=3+hbar+nbar,y=5)
        
        



    def open_editframe(self, topic):
        self.hideall()
        self.frames["edit"].place(x=225,y=0)
        self.addbutton.configure(command=lambda: self.app.open_addcard(topic))
        self.editcardbutton.configure(command=lambda: self.app.open_edit(topic, True))
        self.delbutton.configure(command=lambda: self.app.open_delconfirm(topic))


    def open_customframe(self, topic):
        self.hideall()
        self.frames["customisation"].place(x=225,y=0)
        self.applybutton.configure(command=lambda: self.applycustomisation(topic))
        self.defaultbutton.configure(command=lambda: self.applydefault(topic))


    def open_progressframe(self, topic):
        self.hideall()
        self.frames["progression"].place(x=225,y=0)

        if(topic.getdofeedback() == False):
            self.switch.deselect()
        else:
            self.switch.select()
        
        self.updateprogressbar(topic)
        self.applybutton2.configure(command=lambda: self.applyfeedback(topic))



    def hideall(self):
        self.frames["edit"].place_forget()
        self.frames["customisation"].place_forget()
        self.frames["progression"].place_forget()



    def applycustomisation(self, topic):
        entry = self.nameinput.get().strip()
        if(len(entry) > 0):
            topic.setname(entry)
        topic.setbg(self.colour)
        self.nameinput.delete(0, "end")
        save_data()


    def applyfeedback(self, topic):
        choice = self.switch.get()
        if(choice == 0):
            topic.disablefeedback()
        else:
            topic.enablefeedback()
        save_data()


    def applydefault(self, topic):
        topic.setbg(colours[1])
        save_data()


    def show(self, topic):
        super().show()

        self.editbutton.configure(command=lambda: self.open_editframe(topic))
        self.custombutton.configure(command=lambda: self.open_customframe(topic))
        self.progressbutton.configure(command=lambda: self.open_progressframe(topic))
    

    
    def hide(self):
        super().hide()
        self.hideall()
