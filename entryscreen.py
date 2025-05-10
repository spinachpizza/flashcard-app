import customtkinter as ctk
from data import colours, save_data, userimgs
from screen import screen
from tkinter import filedialog
from PIL import Image


class entryscreen(screen):

    def __init(self, root, app):
        super().__init__(root, app)
        self.imgselected = False


    def setup(self):

        self.qframe = ctk.CTkFrame(self.main, width=520, height=180, fg_color=colours[1])
        self.qframe.place(x=115,y=10)
        self.aframe = ctk.CTkFrame(self.main, width=520, height=270, fg_color=colours[1])
        self.aframe.place(x=115,y=190)
        

        ctk.CTkLabel(self.qframe, text_color=colours[0], text="Question", font=("Helvetica", 22), height=30).place(x=10,y=0)
        
        self.qEntry = ctk.CTkTextbox(self.qframe, font=("Helvetica", 17), height=90, width=520, fg_color=colours[2],text_color=colours[0],
                                     wrap="word")
        self.qEntry.place(x=0,y=30)

        self.enforce_line_limit(self.qEntry, 4, 200)





        ctk.CTkLabel(self.aframe, text_color=colours[0], text="Answer", font=("Helvetica", 22)).place(x=10,y=0)

        self.atbutton = ctk.CTkButton(self.aframe, font=("Helvetica", 18), text="Text", height=50, width=90, fg_color=colours[2],
                                      text_color=colours[0], hover_color=colours[2], anchor="n", corner_radius=20, command=self.selecttext)
        self.atbutton.place(x=10,y=30)

        self.aibutton = ctk.CTkButton(self.aframe, font=("Helvetica", 18), text="Image", height=50, width=90, fg_color=colours[4],
                                      text_color=colours[0], hover_color=colours[3], anchor="n", corner_radius=20, command=self.selectimg)
        self.aibutton.place(x=100,y=30)
        
        self.aEntry = ctk.CTkTextbox(self.aframe, font=("Helvetica", 17), height=180, width=520, fg_color=colours[2], text_color=colours[0],
                                     wrap="word")
        self.aEntry.place(x=0,y=60)

        self.imgframe = ctk.CTkFrame(self.aframe, fg_color=colours[2], width=520, height=180, corner_radius=6)

        self.loadbutton = ctk.CTkButton(self.imgframe, font=("Helvetica", 18), text="Load Image", command=self.loadimage, width=120, height=40,
                                        fg_color=colours[4], text_color=colours[0], hover_color=colours[3])
        self.loadbutton.place(x=197,y=70)

        self.enforce_line_limit(self.aEntry, 9, 500)


        


    def show(self, topic):
        super().show()
        self.file_path = None
        self.qEntry.delete("1.0", "end")
        self.aEntry.delete("1.0", "end")


    def hide(self):
        super().hide()
        self.selecttext()



    def selectimg(self):
        self.imgselected = True
        self.aEntry.place_forget()
        self.imgframe.place(x=0,y=60)
        self.atbutton.configure(fg_color=colours[4],  hover_color=colours[3])
        self.aibutton.configure(fg_color=colours[2], hover_color=colours[2])


    def selecttext(self):
        self.imgselected = False
        self.aEntry.place(x=0,y=60)
        self.imgframe.place_forget()
        self.atbutton.configure(fg_color=colours[2],  hover_color=colours[2])
        self.aibutton.configure(fg_color=colours[4],  hover_color=colours[3])


    def loadimage(self):

        self.file_path = filedialog.askopenfilename(title="Select an Image", filetypes=(("Image Files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp"),))





    def resizeimg(self, path):

        max_width = 650
        max_height = 340
        min_width = 300
        min_height = 200
        
        with Image.open(path) as img:

            or_width, or_height = img.size
            asp_ratio = or_width / or_height


            if or_width < min_width:
                width = min_width
                height = int(min_width / asp_ratio)
            elif or_height < min_height:
                height = min_height
                width = int(min_height * asp_ratio)
                
            

            if or_width > max_width or or_height > max_height:
                # Calculate scaling factors for width and height
                width_scale = max_width / or_width
                height_scale = max_height / or_height
                
                # Use the smaller scaling factor to fit within both constraints
                scale = min(width_scale, height_scale)
                
                # Apply scaling
                width = int(or_width * scale)
                height = int(or_height * scale)
            else:
                width, height = or_width, or_height


            resized = img.resize((width, height))
            resized.save(path)
            print(f"Image resized to {width}x{height}")


            

        


    def savecard(self, topic):
        qtext = self.qEntry.get("0.0", "end")
        atext = self.aEntry.get("0.0", "end")

        qtext = qtext.split("\n")
        text1 = []
        for string in qtext:
            string = self.addtextlines(string)
            for item in string:
                text1.append(item)
        qtext = "\n".join(text1)


        atext = atext.split("\n")
        text2 = []
        for string in atext:
            string = self.addtextlines(string)
            for item in string:
                text2.append(item)
        atext = "\n".join(text2)

        return [qtext,atext]



    def addtextlines(self, text):
        max_length = 70
        text = text.strip()
        words = text.split()
        lines = []
        current_line = ""

        for word in words:
            while len(word) > max_length:
                # Word is too long, split it across multiple lines
                if current_line:
                    lines.append(current_line)
                    current_line = ""

                lines.append(word[:max_length])
                word = word[max_length:]

            if len(current_line) + len(word) + (1 if current_line else 0) <= max_length:
                # Add the word to the current line
                if current_line:
                    current_line += " " + word
                else:
                    current_line = word
            else:
                # Current line is full, start a new line
                lines.append(current_line)
                current_line = word

        if current_line:
            lines.append(current_line)

        return lines
        #return "\n".join(lines)





    def enforce_line_limit(self, text_widget, max_lines=2, max_chars=100):
        line_height = 24  # Approximate height of one line in pixels
        max_height = line_height * max_lines

        def on_key_press(event):
            if event.keysym in ("BackSpace", "Delete", "Left", "Right", "Up", "Down"):
                return  # Allow navigation and deletions

            text_widget.update_idletasks()
            bbox = text_widget.bbox("end-1c")
            if not bbox:
                return
            current_height = bbox[1] + bbox[3]

            # If height exceeded, block
            if current_height >= max_height:
                return "break"

        def on_text_change(event):
            text_widget.update_idletasks()
            text = text_widget.get("0.0", "end-1c")

            # Enforce max lines
            lines = text.split("\n")
            if len(lines) > max_lines:
                # Trim to max lines
                lines = lines[:max_lines]
                text = "\n".join(lines)
                text_widget.delete("0.0", "end")
                text_widget.insert("0.0", text)

            # Enforce max characters
            if len(text) > max_chars:
                text = text[:max_chars]
                text_widget.delete("0.0", "end")
                text_widget.insert("0.0", text)

            text_widget.edit_modified(False)  # Reset the modified flag

        text_widget.bind("<Key>", on_key_press, add=True)
        text_widget.bind("<<Modified>>", on_text_change)
