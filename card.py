import os

class card:

    def __init__(self, question, answer):
        self.question = question
        self.answer = answer
        self.imagenum = None
        self.displayimage = False
        self.providedfeedback = False
        self.kval = 1



    def changetext(self, qtext, atext):
        self.question = qtext
        self.answer = atext



    def displayimg(self, x):
        self.displayimage = x
        if(self.displayimage == False and self.imagenum):
            os.remove(f"images/user/img{self.imagenum}.png")



    def getimgnum(self):
        try:
            return self.imagenum
        except:
            return None


    def getdisplayimg(self):
        try:
            return self.displayimage
        except:
            self.displayimage = False
            return self.displayimage


    def changeimage(self, image):
        if image:
            self.displayimage = True
            self.imagenum = image



    def providefeedback(self, num):
        self.providedfeedback = True
        self.kval = num


    def resetprovidefeedback(self):
        self.providedfeedback = False


    def getprovidedfeedback(self):
        return self.providedfeedback


    def getkval(self):
        return self.kval


    def getquestion(self):
        return self.question


    def getanswer(self):
        return self.answer



