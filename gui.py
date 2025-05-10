import tkinter as tk
from tkinter import ttk
import pickle
import threading
import time

from topic import topic
from card import card


colour1 = '#36454f'
colour2 = '#536872'


topics = []


filename = 'topics.pkl'

op = 0

cardindex = 0
cards = None


canswaptext = True


def save_data():
    with open(filename, 'wb') as file:
        pickle.dump(topics, file)


def load_data():
    global topics
    with open(filename, 'rb') as file:
        topics = pickle.load(file)



def create_scrollable_frame(root):
    canvas = tk.Canvas(root, bg=colour1, highlightthickness=0, bd=0)
    scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg=colour1, highlightthickness=0, bd=0)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    return scrollable_frame  # You add widgets to this





#
# TOPIC OPTIONS
#

def displaytopics():

    for widget in frame.winfo_children():
        widget.destroy()
    
    for i in range(len(topics)):
        button = tk.Button(frame, text=topics[i].getname(), font=("Helvetica", 15),width=w, height=1, bg=colour2, fg='white',
                           command=lambda t=topics[i]: open_flashcardframe(t))
        button.grid(row=i,column=0,padx=(140,2),pady=5)
        
        button2 = tk.Button(frame, image=imgS, width=33, height=33,bg=colour2, command=lambda t=topics[i]: open_optionsframe(t))
        button2.grid(row=i,column=1)

    new = tk.Button(frame, fg='white', bg=colour2, text="+", font=("Helvetica", 15), width=w, height=1, command=lambda: addnewtopic(new))
    new.grid(row=len(topics),column=0,padx=(140,2), pady=5)




def addnewtopic(new):
    nameinp = tk.Entry(frame, fg='white', bg=colour2, font=("Helvetica", 15),width=w)
    nameinp.grid(row=len(topics),column=0,padx=(140,2), ipadx=5, ipady=5)
    
    yes = tk.Button(frame, bg=colour2, image=imgC, command=lambda: addtopic(nameinp,yes),width=32,height=32)
    yes.grid(row=len(topics),column=1,pady=(5,5))
    
    new.destroy()



def addtopic(nameinp, yes):
    text = nameinp.get()
    topics.append(topic(text))

    save_data()
    
    nameinp.destroy()
    yes.destroy()
    
    displaytopics()



def deletetopic(topic):
    topics.remove(topic)
    save_data()

    open_mainframe()


 
def addcard(topic):
    qtext = questionEntry.get("1.0", "end-1c")
    atext = answerEntry.get("1.0", "end-1c")
    questionEntry.delete(1.0, tk.END)
    answerEntry.delete(1.0, tk.END)
    if(len(atext) == 0 or len(qtext) == 0):
        print("Error: One or more input boxes are empty")
    else:
        topic.addcard(card(qtext,atext))
        print("Card added")
        save_data()
        open_optionsframe(topic)


def removecard(topic):
    try:
        topic.removecard()
    except:
        pass
    save_data()



def open_delconframe(topic):
    optionframe.place_forget()
    delconframe.place(x=0,y=0,width=500,height=350)

    delconfirmbutton.config(command=lambda: deletetopic(topic))
    delcancelbutton.config(command=lambda: open_optionsframe(topic))
    


def open_optionsframe(topic):
    delconframe.place_forget()
    mainframe.place_forget()
    addcardframe.place_forget()
    optionframe.place(x=0,y=0, width=500, height=350)
    
    optitle.config(text=topic.getname() + " Options")
    text = f"This topic has: {topic.getcardamount()} cards"
    cardcountdisplay.config(text=text)
    optionsaddbutton.config(command=lambda: open_addcardframe(topic))
    optionsrembutton.config(command=lambda: removecard(topic))
    optionsdelbutton.config(command=lambda: open_delconframe(topic))




def open_addcardframe(topic):
    optionframe.place_forget()
    addcardframe.place(x=0,y=0, width=500, height=350)

    addcardbutton.config(command=lambda: addcard(topic))
    addcardcancelbutton.config(command=lambda: open_optionsframe(topic))



def open_mainframe():
    delconframe.place_forget()
    optionframe.place_forget()
    addcardframe.place_forget()
    flashcardframe.place_forget()
    mainframe.place(x=0,y=0, width=500, height=350)

    displaytopics()



def open_flashcardframe(topic):
    global cards
    global cardindex
    mainframe.place_forget()
    flashcardframe.place(x=0,y=0, width=500, height=350)

    cards = None
    cardindex = 0


    cards = topic.getcards()
    if(len(cards) > 0):

        card = cards[0]
        displaycard()
    
    

    string = ("This is a question, what do you think is the maximum amount of chicken you can store within a box about 30cm wide and 30cm high, also why do you think that some chickens have big legs and others not this is definitely a question to be considered")



def displaycard():
    global cards
    global cardindex

    qtext = cards[cardindex].getquestion()
    atext = cards[cardindex].getanswer()

    if(op==0):
        flashtext.config(text=qtext)
    else:
        flashtext.config(text=atext)


def swaptext():
    global op
    global canswaptext
    if(canswaptext):
        canswaptext = False
        op = op + 1
        if(op > 1):
            op = 0
        displaycard()
        timer = threading.Thread(target=swaptimer)
        timer.start()


def swaptimer():
    global canswaptext
    time.sleep(0.25)
    canswaptext = True



def nextcard():
    global op
    global cardindex
    global cards
    op = 0
    if(cardindex < len(cards) - 1):
        cardindex = cardindex + 1
    displaycard()


def prevcard():
    global op
    global cardindex
    global cards
    op = 0
    if(cardindex > 0):
        cardindex = cardindex - 1
    displaycard()
    




def addtextlines(text):
    max_length = 50
    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        # Check if adding the word would exceed the max length
        if len(current_line) + len(word) + 1 <= max_length:  # +1 for the space
            # Add the word to the current line
            if current_line:
                current_line += " " + word
            else:
                current_line = word
        else:
            # If the current line exceeds max_length, start a new line
            lines.append(current_line)
            current_line = word
    
    # Append the last line
    if current_line:
        lines.append(current_line)
    
    return "\n".join(lines)
    



def setup():
    global frame, mainframe, optionframe, addcardframe, flashcardframe, delconframe
    global addcardbutton, optionsaddbutton, optionsrembutton, optionsdelbutton, optionsbackbutton, addcardcancelbutton, addcardbutton
    global returnbutton, prevcardbutton, nextcardbutton, delconfirmbutton, delcancelbutton
    global questionEntry, answerEntry, flashtext, cardcountdisplay, optitle
    global imgS, imgC
    global w

    try:
        load_data()
    except:
        pass

    #Config
    w = 15
    w2 = 18

    root = tk.Tk()
    root.title("FlashCards")
    root.geometry("500x350")
    root.resizable(False, False)
    root.configure(bg=colour1)

    imgS = tk.PhotoImage(file="images/settings.png")
    imgC = tk.PhotoImage(file="images/check.png")

    #Pages
    mainframe = tk.Frame(root, bg=colour1)
    mainframe.place(x=0,y=0, width=500, height=350)

    optionframe = tk.Frame(root, bg=colour1)

    addcardframe = tk.Frame(root)

    flashcardframe = tk.Frame(root)

    delconframe = tk.Frame(root)
    

    #Main Frame
    frame1 = tk.Frame(mainframe, bg=colour1)# bd=2, relief="solid")
    frame1.place(x=10, y=10, width=480, height=80)

    frame2 = tk.Frame(mainframe, bg=colour1)# bd=2, relief="solid")
    frame2.place(x=10, y=100, width=480, height=240)

    frame = create_scrollable_frame(frame2)

    tk.Label(frame1, bg=colour1, fg='white', text="Simple Flashcards", font=("Helvetica", 26)).pack(side="top",pady=(20,0))
    displaytopics()


    #Option Frame
    optitle = tk.Label(optionframe, bg=colour1, fg='white', text="Options", font=("Helvetica", 20))
    optitle.pack(side="top", pady=(20,5), anchor="n", padx=100)

    cardcountdisplay = tk.Label(optionframe, bg=colour1, fg='white', text="", font=("Helvetica", 14))
    cardcountdisplay.pack(side="top",pady=(5,15),anchor="n")

    optionsaddbutton = tk.Button(optionframe, bg=colour2, fg='white', text="Add Card", font=("Helvetica", 15), width=w2)
    optionsaddbutton.pack(side="top", pady=5, anchor="n", padx=100)

    optionsrembutton = tk.Button(optionframe, bg=colour2, fg='white', text="Remove Last Card", font=("Helvetica", 15), width=w2)
    optionsrembutton.pack(side="top", pady=5, anchor="n", padx=100)

    optionsdelbutton = tk.Button(optionframe, bg=colour2, fg='white', text="Delete Topic", font=("Helvetica", 15), width=w2)
    optionsdelbutton.pack(side="top", pady=5, anchor="n", padx=100)

    optionsbackbutton = tk.Button(optionframe, bg=colour2, fg='white', text="Return", font=("Helvetica", 15), command=lambda:open_mainframe(), width=w2)
    optionsbackbutton.pack(side="bottom", pady=(30,30), anchor="s", padx=100)


    #Add Card Frame
    frame3 = tk.Frame(addcardframe)
    frame3.place(x=10,y=10,width=480,height=310)
    
    tk.Label(frame3, text="Question", font=("Helvetica", 12)).pack(side="top",anchor="nw", pady=(0,2), padx=70)
    questionEntry = tk.Text(frame3, font=("Helvetica", 11), height=3, width=42)
    questionEntry.pack(side="top", pady=(0,10), anchor="n")

    tk.Label(frame3, text="Answer", font=("Helvetica", 12)).pack(side="top",anchor="nw", pady=(0,2), padx=70)
    answerEntry = tk.Text(frame3, font=("Helvetica", 11), height=10, width=42)
    answerEntry.pack(side="top", anchor="n")
    
    addcardcancelbutton = tk.Button(addcardframe, text="Cancel", font=("Helvetica", 12), width=10,height=1)
    addcardcancelbutton.place(x=80,y=310)

    addcardbutton = tk.Button(addcardframe, text="Enter", font=("Helvetica",12), width=10, height=1)
    addcardbutton.place(x=320,y=310)


    #Flashcard Frame

    flashtext = tk.Button(flashcardframe, bg=colour1, activebackground=colour1, highlightcolor=colour1, fg='white', font=("Helvetica", 12), height=20, width=56, relief="flat", command=swaptext)
    flashtext.place(x=-10,y=-10)

    returnbutton = tk.Button(flashcardframe, text="Return", font=("Helvetica", 11), width=6, command=open_mainframe)
    returnbutton.place(x=10,y=310)

    prevcardbutton = tk.Button(flashcardframe, text="<", font=("Helvetica", 11), width=4, command=prevcard)
    prevcardbutton.place(x=380,y=310)
    
    nextcardbutton = tk.Button(flashcardframe, text=">", font=("Helvetica", 11), width=4, command=nextcard)
    nextcardbutton.place(x=430,y=310)


    #Delete confirmation frame
    frame5 = tk.Frame(delconframe)
    frame5.place(x=100,y=50,width=300,height=200)
    
    tk.Label(frame5, text="Are you sure you want to \n delete this topic?", font=("Helvetica", 15)).place(x=40,y=20)

    delconfirmbutton = tk.Button(frame5, text="Confirm", font=("Helvetica", 15), width=7)
    delconfirmbutton.place(x=40,y=100)

    delcancelbutton = tk.Button(frame5, text="Cancel", font=("Helvetica", 15), width=7)
    delcancelbutton.place(x=170,y=100)


    


    root.mainloop()


mainthread = threading.Thread(target=setup)
mainthread.start()

