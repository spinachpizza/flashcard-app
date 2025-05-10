from PIL import Image
import customtkinter as ctk
import pickle
import threading
import time

from topic import topic
from card import card

import os, sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS  # temp folder PyInstaller uses
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


colour1 = '#36454f'
colour2 = '#536872'
colour3 = '#47555c'
tcolour = '#FFFFFF'


topics = []


filename = 'topics.pkl'

op = 0
editop = 0

cardindex = 0
editindex = 0
cards = None


canswaptext = True


def save_data():
    with open(filename, 'wb') as file:
        pickle.dump(topics, file)


def load_data():
    global topics
    with open(filename, 'rb') as file:
        topics = pickle.load(file)




#
# TOPIC OPTIONS
#

def displaytopics():
    
    for widget in frames["topics"].winfo_children():
        widget.destroy()
    
    for i in range(len(topics)):
        button = ctk.CTkButton(frames["topics"], text=topics[i].getname(), font=("Helvetica", 15), width=140, height=40, text_color=tcolour, fg_color=colour2, hover_color=colour3,
                               command=lambda t=topics[i]: open_flashcardframe(t))
        button.grid(row=i, column=0, padx=(280, 2), pady=5)

        button2 = ctk.CTkButton(frames["topics"], image=imgS, width=40, height=40, fg_color=colour2, hover_color=colour3, text="", command=lambda t=topics[i]: open_optionsframe(t))
        button2.grid(row=i, column=1)


    new = ctk.CTkButton(frames["topics"], text="+", font=("Helvetica", 15), width=140, height=40, text_color=tcolour, fg_color=colour2, hover_color=colour3,
                        command=lambda: addnewtopic(new))
    new.grid(row=len(topics), column=0, padx=(280, 2), pady=5)





def addnewtopic(new):
    nameinp = ctk.CTkEntry(frames["topics"], font=("Helvetica", 15), width=130, text_color='white')
    nameinp.grid(row=len(topics), column=0, padx=(280, 2), ipadx=5, ipady=5)

    yes = ctk.CTkButton(frames["topics"], image=imgC, text="", command=lambda: addtopic(nameinp, yes), width=40, height=40, fg_color=colour2, hover_color=colour3,)
    yes.grid(row=len(topics), column=1, pady=(5, 5))

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
    qtext = other["questionEntry"].get("1.0", "end-1c")
    atext = other["answerEntry"].get("1.0", "end-1c")
    other["questionEntry"].delete(1.0, ctk.END)
    other["answerEntry"].delete(1.0, ctk.END)
    if(len(atext) == 0 or len(qtext) == 0):
        print("Error: One or more input boxes are empty")
    else:
        topic.addcard(card(qtext,atext))
        print("Card added")
        save_data()
        open_optionsframe(topic)


def removecard(topic):
    global editindex
    print("attempting to delete")
    if(topic.removecard(editindex) == 1):
        print("Removed")
        if(editindex >= len(topic.getcards())):
            editindex -= 1
            if(editindex < 0):
                open_optionsframe(topic)
        display_editcard(topic)
    else:
        print("failed to delete")
    save_data()



def open_delconframe(topic):
    frames["option"].place_forget()
    frames["delcon"].place(x=0,y=0)

    buttons["delconfirm"].configure(command=lambda: deletetopic(topic))
    buttons["delcancel"].configure(command=lambda: open_optionsframe(topic))
    


def open_optionsframe(topic):
    frames["delcon"].place_forget()
    frames["main"].place_forget()
    frames["addcard"].place_forget()
    frames["edit"].place_forget()
    frames["option"].place(x=0,y=0)
    
    other["optitle"].configure(text=topic.getname() + " Options")
    text = f"{topic.getcardamount()} flash cards"
    other["cardcountdisplay"].configure(text=text)
    
    buttons["optionsadd"].configure(command=lambda: open_addcardframe(topic))
    buttons["optionsedit"].configure(command=lambda: open_editframe(topic))
    buttons["optionsdel"].configure(command=lambda: open_delconframe(topic))




def open_addcardframe(topic):
    frames["option"].place_forget()
    frames["addcard"].place(x=0,y=0)

    buttons["addcard"].configure(command=lambda: addcard(topic))
    buttons["addcardcancel"].configure(command=lambda: open_optionsframe(topic))



def open_mainframe():
    frames["delcon"].place_forget()
    frames["option"].place_forget()
    frames["addcard"].place_forget()
    frames["flashcard"].place_forget()
    frames["main"].place(x=0,y=0)

    displaytopics()



def open_flashcardframe(topic):
    global cards
    global cardindex
    
    frames["main"].place_forget()
    frames["flashcard"].place(x=0,y=0)

    cards = None
    cardindex = 0


    cards = topic.getcards()
    if(len(cards) > 0):
        card = cards[0]
        displaycard()
    
    

    string = ("This is a question, what do you think is the maximum amount of chicken you can store within a box about 30cm wide and 30cm high, also why do you think that some chickens have big legs and others not this is definitely a question to be considered")


def open_editframe(topic):
    frames["option"].place_forget()
    frames["edit"].place(x=0,y=0)

    other["editflashtext"].configure(command=lambda: editswaptext(topic))
    buttons["editreturn"].configure(command=lambda: open_optionsframe(topic))
    buttons["editdelcard"].configure(command=lambda: removecard(topic))
    buttons["editcard"]
    buttons["editnextcard"].configure(command=lambda: nexteditcard(topic))
    buttons["editprevcard"].configure(command=lambda: preveditcard(topic))
    display_editcard(topic)


def open_editcardframe(topic):
    frames["edit"].place_forget()
    frames["editcard"].place(x=0,y=0)
    



def display_editcard(topic):
    cards = topic.getcards()
    card = cards[editindex]

    if(editop == 0):
        other["editflashtext"].configure(text=addtextlines(card.getquestion()))
    else:
        other["editflashtext"].configure(text=addtextlines(card.getanswer()))


def editswaptext(topic):
    global editop
    if(len(topic.getcards()) > 0):
        editop += 1
        if(editop>1):
            editop = 0
        display_editcard(topic)


def nexteditcard(topic):
    global editindex
    editop = 0
    if(editindex < len(topic.getcards()) -1):
        editindex += 1
        display_editcard(topic)

def preveditcard(topic):
    global editindex
    editop = 0
    if(editindex > 0):
        editindex -= 1
        display_editcard(topic)
            




def displaycard():
    global cards
    global cardindex

    qtext = cards[cardindex].getquestion()
    atext = cards[cardindex].getanswer()

    if(len(cards) > 0):
        if(op==0):
            other["flashtext"].configure(text=qtext)
        else:
            other["flashtext"].configure(text=atext)


def swaptext():
    global op
    if(len(cards) > 0):
        op = op + 1
        if(op > 1):
            op = 0
        displaycard()


def swaptimer():
    global canswaptext
    time.sleep(0.25)
    canswaptext = True



def nextcard():
    global op
    global cardindex
    global cards
    op = 0
    if(len(cards) > 0):
        if(cardindex < len(cards) - 1):
            cardindex = cardindex + 1
        displaycard()


def prevcard():
    global op
    global cardindex
    global cards
    op = 0
    if(len(cards) > 0):
        if(cardindex > 0):
            cardindex = cardindex - 1
        displaycard()
    




def addtextlines(text):
    max_length = 50
    text = text.strip()
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
    global imgS, imgC
    global frames, buttons, other

    frames = {}
    buttons = {}
    other = {}

    try:
        load_data()
    except:
        pass


    root = ctk.CTk()
    root.title("FlashCards")
    root.geometry("750x500")
    root.resizable(False, False)

    root.iconbitmap(resource_path("images/icon.ico"))

    imgS = ctk.CTkImage(light_image=Image.open(resource_path("images/settings.png")), size=(16,16))
    imgC = ctk.CTkImage(light_image=Image.open(resource_path("images/check.png")), size=(16,16))

    #Frames
    frames["main"] = ctk.CTkFrame(root, width=750, height=500, fg_color=colour1)
    frames["main"].place(x=0,y=0)

    frames["option"] = ctk.CTkFrame(root, width=750, height=500, fg_color=colour1)

    frames["addcard"] = ctk.CTkFrame(root, width=750, height=500, fg_color=colour1)

    frames["flashcard"] = ctk.CTkFrame(root, width=750, height=500, fg_color=colour1)

    frames["delcon"] = ctk.CTkFrame(root, width=750, height=500, fg_color=colour1)

    frames["edit"] = ctk.CTkFrame(root, width=750, height=500, fg_color=colour1)

    frames["editcard"] = ctk.CTkFrame(root, width=750, height=500, fg_color=colour1)
    

    #Main Frame
    frame1 = ctk.CTkFrame(frames["main"], width=730, height=90, fg_color=colour1)# bd=2, relief="solid")
    frame1.place(x=10, y=10)

    frame2 = ctk.CTkFrame(frames["main"], width=730, height=380, fg_color=colour1)# bd=2, relief="solid")
    frame2.place(x=10, y=100)

    frames["topics"] = ctk.CTkScrollableFrame(frame2, width=720, height=380, fg_color=colour1)  # Set bg color
    frames["topics"].pack(side="left", fill="both", expand=True, padx=0, pady=0)

    ctk.CTkLabel(frame1, fg_color=colour1, text_color=tcolour, text="Simple Flashcards", font=("Helvetica", 42)).place(relx=0.5, rely=0.5, anchor="center")
    displaytopics()


    #Option Frame
    other["optitle"] = ctk.CTkLabel(frames["option"], fg_color=colour1, text_color=tcolour, text="Options", font=("Helvetica", 32))
    other["optitle"].place(relx=0.5, rely=0.1, anchor="center")

    other["cardcountdisplay"] = ctk.CTkLabel(frames["option"], text="", font=("Helvetica", 19))
    other["cardcountdisplay"].place(relx=0.5, rely=0.25, anchor="center")


    buttons["optionsadd"] = ctk.CTkButton(frames["option"], text="Add Card", font=("Helvetica", 15), width=200, height=50,
                                     text_color=tcolour, fg_color=colour2, hover_color=colour3)
    buttons["optionsadd"].place(relx=0.5, rely=0.35, anchor="center")


    buttons["optionsedit"] = ctk.CTkButton(frames["option"], text="Edit Cards", font=("Helvetica", 15), width=200, height=50,
                                     text_color=tcolour, fg_color=colour2, hover_color=colour3)
    buttons["optionsedit"].place(relx=0.5, rely=0.48, anchor="center")


    buttons["optionsdel"] = ctk.CTkButton(frames["option"], text="Delete Topic", font=("Helvetica", 15), width=200, height=50,
                                     text_color=tcolour, fg_color=colour2, hover_color=colour3)
    buttons["optionsdel"].place(relx=0.5, rely=0.65, anchor="center")


    buttons["optionsback"] = ctk.CTkButton(frames["option"], text="Return", font=("Helvetica", 15), command=lambda:open_mainframe(),
                                      width=200, height=50, text_color=tcolour, fg_color=colour2, hover_color=colour3)
    buttons["optionsback"].place(relx=0.5, rely=0.9, anchor="center")
    


    #Add Card Frame
    def enforce_line_limit(text_widget, max_lines=2):

        line_height = 23 # Approximate height of one line in pixels (adjust if needed)
        max_height = line_height * max_lines

        def on_key_press(event):
            # Allow deletions (BackSpace, Delete) and navigation keys
            if event.keysym in ("BackSpace", "Delete", "Left", "Right", "Up", "Down"):
                return

            # Get current widget height (in pixels)
            text_widget.update_idletasks()
            bbox = text_widget.bbox("end-1c")
            if not bbox:  # Edge case: empty widget
                return
            current_height = bbox[1] + bbox[3]  # y-position + height of last line

            # Block if adding text would exceed max height
            if current_height >= max_height:
                return "break"

        text_widget.bind("<Key>", on_key_press, add=True)
        
    frame3 = ctk.CTkFrame(frames["addcard"], width=730, height=480, fg_color=colour1)
    frame3.place(x=10,y=10)
    
    ctk.CTkLabel(frame3, text_color=tcolour, text="Question", font=("Helvetica", 19)).place(x=105,y=10)
    other["questionEntry"] = ctk.CTkTextbox(frame3, font=("Helvetica", 15), height=90, width=500, fg_color=colour2, text_color=tcolour)
    other["questionEntry"].place(x=100,y=40)

    enforce_line_limit(other["questionEntry"], 4)


    ctk.CTkLabel(frame3, text_color=tcolour, text="Answer", font=("Helvetica", 19)).place(x=105,y=160)
    other["answerEntry"] = ctk.CTkTextbox(frame3, font=("Helvetica", 15), height=180, width=500, fg_color=colour2, text_color=tcolour)
    other["answerEntry"].place(x=100,y=190)

    enforce_line_limit(other["answerEntry"], 9)

    buttons["addcardcancel"] = ctk.CTkButton(frames["addcard"], text="Cancel", font=("Helvetica", 15), width=80,height=40, text_color=tcolour, fg_color=colour2, hover_color=colour3)
    buttons["addcardcancel"].place(x=110,y=410)

    buttons["addcard"] = ctk.CTkButton(frames["addcard"], text="Enter", font=("Helvetica",15), width=80, height=40, text_color=tcolour, fg_color=colour2, hover_color=colour3)
    buttons["addcard"].place(x=530,y=410)



    #Flashcard Frame

    other["flashtext"] = ctk.CTkButton(frames["flashcard"], text="", text_color=tcolour, fg_color=colour1, hover_color=colour1,
                              font=("Helvetica", 20), height=520, width=770, command=swaptext)
    other["flashtext"].place(x=-10,y=-10)


    buttons["cardreturn"] = ctk.CTkButton(frames["flashcard"], text_color=tcolour, fg_color=colour2, hover_color=colour3,
                                 text="Return", font=("Helvetica", 14), width=100, height=40, command=open_mainframe)
    buttons["cardreturn"].place(x=10,y=450)


    buttons["prevcard"] = ctk.CTkButton(frames["flashcard"], text_color=tcolour, fg_color=colour2, hover_color=colour3,
                                   text="<", font=("Helvetica", 14), width=40, height=40, command=prevcard)
    buttons["prevcard"].place(x=655,y=450)

    
    buttons["nextcard"] = ctk.CTkButton(frames["flashcard"], text_color=tcolour, fg_color=colour2, hover_color=colour3,
                                   text=">", font=("Helvetica", 14), width=40, height=40, command=nextcard)
    buttons["nextcard"].place(x=700,y=450)


    #Delete confirmation frame
    frame5 = ctk.CTkFrame(frames["delcon"], width=300, height=200)
    frame5.place(x=225,y=140)
    
    ctk.CTkLabel(frame5, text="Are you sure you want to \n delete this topic?", font=("Helvetica", 24)).place(relx=0.5, rely=0.25, anchor="center")

    buttons["delconfirm"] = ctk.CTkButton(frame5, text="Confirm", font=("Helvetica", 15), width=80, height=40,
                                          text_color=tcolour, fg_color=colour2, hover_color=colour3)
    buttons["delconfirm"].place(relx=0.7, rely=0.65, anchor="center")

    buttons["delcancel"] = ctk.CTkButton(frame5, text="Cancel", font=("Helvetica", 15), width=80, height=40,
                                         text_color=tcolour, fg_color=colour2, hover_color=colour3)
    buttons["delcancel"].place(relx=0.3, rely=0.65, anchor="center")


    #Edit Card Frame
    frame6 = ctk.CTkFrame(frames["edit"], width=460, height=310, border_width=5, border_color=colour2)
    frame6.place(x=145,y=70)

    other["editflashtext"] = ctk.CTkButton(frame6, text_color=tcolour, fg_color=colour1, hover_color=colour1,
                                   text="", font=("Helvetica", 14), width=450, height=300)
    other["editflashtext"].place(x=5,y=5)


    buttons["editreturn"] = ctk.CTkButton(frames["edit"], width=85, height=40, text="Return", font=("Helvetica", 15),
                                          text_color=tcolour, fg_color=colour2, hover_color=colour3)
    buttons["editreturn"].place(x=145,y=420)


    buttons["editdelcard"] = ctk.CTkButton(frames["edit"], width=100, height=40, text="Delete", font=("Helvetica", 15),
                                          text_color=tcolour, fg_color=colour2, hover_color=colour3)
    buttons["editdelcard"].place(x=270,y=420)


    buttons["editcard"] = ctk.CTkButton(frames["edit"], width=100, height=40, text="Edit Text", font=("Helvetica", 15),
                                          text_color=tcolour, fg_color=colour2, hover_color=colour3)
    buttons["editcard"].place(x=380,y=420)


    buttons["editprevcard"] = ctk.CTkButton(frames["edit"], width=40, height=40, text="<", font=("Helvetica", 15),
                                          text_color=tcolour, fg_color=colour2, hover_color=colour3)
    buttons["editprevcard"].place(x=520,y=420)


    buttons["editnextcard"] = ctk.CTkButton(frames["edit"], width=40, height=40, text=">", font=("Helvetica", 15),
                                          text_color=tcolour, fg_color=colour2, hover_color=colour3)
    buttons["editnextcard"].place(x=565,y=420)



    #Edit card text frame
    def enforce_line_limit(text_widget, max_lines=2):

        line_height = 23 # Approximate height of one line in pixels (adjust if needed)
        max_height = line_height * max_lines

        def on_key_press(event):
            # Allow deletions (BackSpace, Delete) and navigation keys
            if event.keysym in ("BackSpace", "Delete", "Left", "Right", "Up", "Down"):
                return

            # Get current widget height (in pixels)
            text_widget.update_idletasks()
            bbox = text_widget.bbox("end-1c")
            if not bbox:  # Edge case: empty widget
                return
            current_height = bbox[1] + bbox[3]  # y-position + height of last line

            # Block if adding text would exceed max height
            if current_height >= max_height:
                return "break"

        text_widget.bind("<Key>", on_key_press, add=True)
        
    frame7 = ctk.CTkFrame(frames["editcard"], width=730, height=480, fg_color=colour1)
    frame7.place(x=10,y=10)
    
    ctk.CTkLabel(frame7, text_color=tcolour, text="Question", font=("Helvetica", 19)).place(x=105,y=10)
    other["editquestionEntry"] = ctk.CTkTextbox(frame7, font=("Helvetica", 15), height=90, width=500, fg_color=colour2, text_color=tcolour)
    other["editquestionEntry"].place(x=100,y=40)

    enforce_line_limit(other["editquestionEntry"], 4)


    ctk.CTkLabel(frame3, text_color=tcolour, text="Answer", font=("Helvetica", 19)).place(x=105,y=160)
    other["editanswerEntry"] = ctk.CTkTextbox(frame7, font=("Helvetica", 15), height=180, width=500, fg_color=colour2, text_color=tcolour)
    other["editanswerEntry"].place(x=100,y=190)

    enforce_line_limit(other["editanswerEntry"], 9)

    buttons["editcancel"] = ctk.CTkButton(frames["editcard"], text="Cancel", font=("Helvetica", 15), width=80,height=40, text_color=tcolour, fg_color=colour2, hover_color=colour3)
    buttons["editcancel"].place(x=110,y=410)

    buttons["editsave"] = ctk.CTkButton(frames["editcard"], text="Save Changes", font=("Helvetica",15), width=80, height=40, text_color=tcolour, fg_color=colour2, hover_color=colour3)
    buttons["editsave"].place(x=530,y=410)

    


    root.mainloop()


mainthread = threading.Thread(target=setup)
mainthread.start()
mainthread.join()

