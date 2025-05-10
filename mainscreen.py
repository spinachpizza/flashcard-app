import customtkinter as ctk
from topic import topic
from PIL import Image, ImageTk, ImageDraw
from data import colours, topics, paths, save_data, load_data
from screen import screen

class main(screen):

    def __init__(self, root, app):
        self.imgS = ctk.CTkImage(light_image=Image.open(paths[0]), size=(20,20))
        self.imgC = ctk.CTkImage(light_image=Image.open(paths[1]), size=(16,16))
        self.imgB = ctk.CTkImage(light_image=Image.open(paths[10]), size=(750,500))
        super().__init__(root,app)


    def setup(self):

        self.frame1 = ctk.CTkFrame(self.main, width=370, height=470, fg_color=colours[4],corner_radius=10)
        self.frame1.place(relx=0.5,rely=0.5,anchor="center")

        label = ctk.CTkLabel(self.frame1, text_color=colours[0], text="Flashcards", width=325, height=80,
                     font=("Helvetica", 40), corner_radius=10)
        label.place(relx=0.5, rely=0.1, anchor="center")


        self.topicframe = ctk.CTkScrollableFrame(self.frame1, width=350, height=370, fg_color=colours[4], corner_radius=10)
        self.topicframe.place(relx=0.5, rely=0.56, anchor="center")


        self.displaytopics()
        

    def setup1(self):
        
        ctk.CTkLabel(self.main, image=self.imgB, width=750, height=500, text="").place(x=0,y=0)
        
        self.frame1 = ctk.CTkFrame(self.main, width=300, height=75, fg_color=colours[4], bg_color="#000001", corner_radius=15)
        self.frame1.place(relx=0.5, rely=0.1, anchor="center")

        self.frame2 = ctk.CTkFrame(self.main, width=300, height=370, fg_color=colours[4], bg_color="#000001", corner_radius=15)
        self.frame2.place(relx=0.5, rely=0.56, anchor="center")

        self.topicframe = ctk.CTkScrollableFrame(self.frame2, width=255, height=350, fg_color=colours[4], corner_radius=5)
                                                 #bg_color="#000001")  # Set bg color
        #self.topicframe.pack(side="left", fill="both", expand=True, padx=225, pady=0)
        #self.topicframe.place(relx=0.5, rely=0.56, anchor="center")
        self.topicframe.place(x=20,y=5)

        label = ctk.CTkLabel(self.frame1, text_color=colours[0], text="Flashcards", width=250, height=60,
                     font=("Helvetica", 40))
        label.place(relx=0.5, rely=0.5, anchor="center")
        #label = ctk.CTkButton(self.main, fg=
        pywinstyles.set_opacity(self.frame2, value=0.5, color="#000001")
        pywinstyles.set_opacity(self.topicframe, value=2, color="#000001")
        pywinstyles.set_opacity(self.frame1, value=0.5, color="#000001")


        self.displaytopics()


    def show(self):
        super().show()
        self.displaytopics()



    def displaytopics(self):
    
        for widget in self.topicframe.winfo_children():
            widget.destroy()
        
        for i in range(len(topics)):
            if(i==0):
                pad = (10,5)
            else:
                pad = 5
            
            button = ctk.CTkButton(self.topicframe, text=topics[i].getname(), font=("Helvetica", 15),
                                   width=200, height=50, text_color=colours[0], fg_color=colours[1], hover_color=colours[2],
                                   command=lambda t=topics[i]: self.app.open_flashcard(t))
            button.grid(row=i, column=0, padx=(75,10), pady=pad)

            button2 = ctk.CTkButton(self.topicframe, image=self.imgS, width=30, height=30, fg_color=colours[1],
                                    hover_color=colours[2], text="", command=lambda t=topics[i]: self.app.open_options(t))
            button2.grid(row=i, column=1, pady=pad)



        self.new = ctk.CTkButton(self.topicframe, text="+", font=("Helvetica", 15), width=200, height=50, text_color=colours[0],
                            fg_color=colours[1], hover_color=colours[2], command=self.addnewtopic)
        self.new.grid(row=len(topics), column=0, padx=(75, 10), pady=5)





    def addnewtopic(self):
        self.nameinp = ctk.CTkEntry(self.topicframe, font=("Helvetica", 15), width=190, text_color=colours[0])
        self.nameinp.grid(row=len(topics), column=0, padx=(75, 10), ipadx=5, ipady=5)

        self.yes = ctk.CTkButton(self.topicframe, image=self.imgC, text="", command= self.addtopic,
                            width=30, height=30, fg_color=colours[1], hover_color=colours[2])
        self.yes.grid(row=len(topics), column=1, pady=(5, 5))

        self.new.destroy()



    def addtopic(self):
        text = self.nameinp.get()
        topics.append(topic(text))

        save_data()
        
        self.nameinp.destroy()
        self.yes.destroy()
        
        self.displaytopics()



    def deletetopic(self, topic):
        topics.remove(topic)
        save_data()

        self.app.open_main()
    
