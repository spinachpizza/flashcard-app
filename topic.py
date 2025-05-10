class topic:

    def __init__(self, name):
        self.name = name
        self.cards = []
        self.dofeedback = True
        self.bg = "#36454f"

    def addcard(self, card):
        self.cards.append(card)

    def removecard(self, index):
        try:
            del self.cards[index]
            return 1
        except:
            return 0


    def setbg(self, new):
        self.bg = new


    def getbg(self):
        return self.bg
    

    def getcards(self):
        return self.cards


    def getcardamount(self):
        return len(self.cards)


    def setname(self, name):
        self.name = name


    def getname(self):
        return self.name


    def enablefeedback(self):
        self.dofeedback = True

    def disablefeedback(self):
        self.dofeedback = False


    def getdofeedback(self):
        return self.dofeedback


    def getprogress(self):
        counts = [0,0,0]
        for card in self.cards:
            if(card.getkval() == 0):
                counts[2] += 1
            elif(card.getkval() == 1):
                counts[1] += 1
            else:
                counts[0] += 1
        return counts

