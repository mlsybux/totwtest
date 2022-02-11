from tkinter import *
from random import *
#from time import *


class Resource:
    def __init__(self, can, rtype, rid):
        self.canvas = can
        self.type = rtype
        self.id = rid
        self.sprite = self.randomsprite()

    def randomsprite(self):
        self.rand1 = randint(50, 400)
        self.rand2 = randint(30, 300)
        if self.type == "Wood":
            return self.canvas.create_rectangle(self.rand1, self.rand2, self.rand1+20, self.rand2+10, fill="brown")
        elif self.type == "Stone":
            return self.canvas.create_rectangle(self.rand1, self.rand2, self.rand1+20, self.rand2+20, fill="gray")
        elif self.type == "Coal":
            return self.canvas.create_rectangle(self.rand1, self.rand2, self.rand1+5, self.rand2+5, fill="black")
        elif self.type == "Tree":
            return self.canvas.create_rectangle(self.rand1, self.rand2, self.rand1+25, self.rand2+25, fill="green")

    def setlocation(self, x1, y1, x2, y2):
        self.removesprite()
        self.sprite = self.canvas.create_rectangle(x1, y1, x2, y2, fill="green")

    def getitem(self):
        return self.sprite

    def getitemcoords(self):
        #print(self.canvas.coords(self.sprite))
        self.ox1 = self.canvas.coords(self.sprite)[0]
        self.oy1 = self.canvas.coords(self.sprite)[1]
        self.ox2 = self.canvas.coords(self.sprite)[2]
        self.oy2 = self.canvas.coords(self.sprite)[3]
        return [self.ox1, self.oy1, self.ox2, self.oy2]

    def gettype(self):
        return self.type

    def getitemid(self):
        return self.id

    def makesprite(self):
        self.sprite = self.randomsprite()

    def removesprite(self):
        self.canvas.delete(self.sprite)
        #print("Sprite removed!")


class Items:
    def __init__(self, master):
        #Tk
        self.master = master
        #wood, stone, coal, tree, gems, axes
        self.inventory = [0, 0, 0, 0, 0, 50]
        #x and y are the movement
        self.x = 0
        self.y = 0
        #just saying that all the keys are released by default
        self.leftpressed = False
        self.rightpressed = False
        self.uppressed = False
        self.downpressed = False
        #this is the canvas NOT THE TK JADZIA YOU DUMB THOT
        self.canvas = Canvas(master, width=600, height=400)
        #the player's sprite and its coordinates :)
        self.playersprite = self.canvas.create_rectangle(290, 350, 310, 370, fill="purple")
        self.currentx1 = self.canvas.coords(self.playersprite)[0]
        self.currenty1 = self.canvas.coords(self.playersprite)[1]
        self.currentx2 = self.canvas.coords(self.playersprite)[2]
        self.currenty2 = self.canvas.coords(self.playersprite)[3]

        self.canvas.grid(row=0, column=0)
        self.resources = {}
        self.obstacles = {}
        self.stack = []
        self.spawnitems([0, 0, 0, 2])

        self.loadborders()
        self.movement()

    def loadborders(self):
        self.leftborder = self.canvas.create_rectangle(0, 0, 17, 400, fill="green")
        self.rightborder = self.canvas.create_rectangle(583, 0, 600, 400, fill="green")
        #self.upperborder = self.canvas.create_rectangle(0, 0, 600, 17, fill="green")
        self.upperborderL = self.canvas.create_rectangle(0, 0, 280, 20, fill="green")
        self.upperborderR = self.canvas.create_rectangle(315, 0, 600, 20, fill="green")
        self.lowerborderL = self.canvas.create_rectangle(0, 383, 200, 400, fill="green")
        self.lowerborderR = self.canvas.create_rectangle(400, 383, 600, 400, fill="green")
        self.obstacles["LeftBorder"] = self.leftborder
        self.obstacles["RightBorder"] = self.rightborder
        #self.obstacles["UpperBorder"] = self.upperborder

        self.obstacles["LowerBorderL"] = self.lowerborderL
        self.obstacles["LowerBorderR"] = self.lowerborderR

    def swingblade(self):
        self.bx = 5
        self.by = 0
        self.bx2 = self.canvas.coords(self.blade)[2]
        if self.inventory[5] >= 1:
            #print("HEWWO")
            for x in self.overlaps(self.canvas.coords(self.blade)[0], self.canvas.coords(self.blade)[1],
                                   self.canvas.coords(self.blade)[2], self.canvas.coords(self.blade)[3]):
                for a in self.stack:
                    if a.gettype() == "Tree" and a.getitemid() == x:
                        self.additem(0, 5)
                        self.subtractitem(5, 1)
                        a.removesprite()
        if self.bx2 >= self.currentx2:
            self.bx = 0
            self.canvas.delete(self.blade)
            return
        self.canvas.move(self.blade, self.bx, self.by)
        self.canvas.after(70, self.swingblade)

    def cuttree(self):
        self.blade = self.canvas.create_rectangle(self.currentx1, self.currenty1 - 10, self.currentx1 + 5, self.currenty1)
        self.swingblade()



    def overlaps(self, x1, y1, x2, y2):
        self.overlap_list = []
        self.c_object = self.canvas.find_overlapping(x1, y1, x2, y2)
        for k, v in self.resources.items(): #iterates over resources dict
            if v in self.c_object:
                self.overlap_list.append(k)
        #delete under this if it doesn't work
        for k, v in self.obstacles.items():
            if v in self.c_object:
                self.overlap_list.append(k)
        return self.overlap_list


    def overlapsbool(self, item):
        self.itemcoordinates = item.getitemcoords()

        self.ox1 = self.itemcoordinates[0]
        self.oy1 = self.itemcoordinates[1]
        self.ox2 = self.itemcoordinates[2]
        self.oy2 = self.itemcoordinates[3]

        self.c_object = self.canvas.find_overlapping(self.ox1, self.oy1, self.ox2, self.oy2)
        for k, v in self.resources.items(): #iterates over resources dict
            if v in self.c_object:
                return True
        for k, v in self.obstacles.items():
            if v in self.c_object:
                return True
        return False

    def spawnitems(self, amountarray):
        self.i = 0
        self.penisboi = 0
        self.typearray = ["Wood", "Stone", "Coal", "Tree"]
        for amount in amountarray:
            self.ind = 0
            while self.ind < amount:
                self.stack.append(Resource(self.canvas, self.typearray[self.penisboi], self.typearray[self.penisboi] + str(self.ind)))
                while self.overlapsbool(self.stack[self.i]):
                    self.stack[self.i].removesprite()
                    self.stack[self.i].makesprite()
                    #print(self.stack[self.i].getitemid())
                #self.resources[self.stack[self.i].getitemid()] = self.stack[self.i].getitem()
                if self.typearray[self.penisboi] == "Tree":
                    self.obstacles[self.stack[self.i].getitemid()] = self.stack[self.i].getitem()
                else:
                    self.resources[self.stack[self.i].getitemid()] = self.stack[self.i].getitem()
                self.ind = self.ind + 1
                self.i = self.i + 1
            self.penisboi = self.penisboi + 1
        self.stack.append(Resource(self.canvas, "Tree", "BorderTree"))
        self.stack[self.i].setlocation(285, 2, 310, 27)
        #self.resources[self.stack[self.i].getitemid()] = self.stack[self.i].getitem()
        self.obstacles[self.stack[self.i].getitemid()] = self.stack[self.i].getitem()

    def hasobstacle(self, x1, y1, x2, y2):
        self.c_object = self.canvas.find_overlapping(x1, y1, x2, y2)
        for k, v in self.obstacles.items():  # iterates over obstacles dict
            if v in self.c_object:
                return True
        return False

    def movement(self):
        if self.x < 0 and self.hasobstacle(self.currentx1-5, self.currenty1, self.currentx2, self.currenty2):
            self.x = 0
        if self.x > 0 and self.hasobstacle(self.currentx1, self.currenty1, self.currentx2+5, self.currenty2):
            self.x = 0
        if self.y < 0 and self.hasobstacle(self.currentx1, self.currenty1-5, self.currentx2, self.currenty2):
            self.y = 0
        if self.y > 0 and self.hasobstacle(self.currentx1, self.currenty1, self.currentx2, self.currenty2+5):
            self.y = 0

        self.canvas.move(self.playersprite, self.x, self.y)

        self.currentx1 = self.canvas.coords(self.playersprite)[0]
        self.currenty1 = self.canvas.coords(self.playersprite)[1]
        self.currentx2 = self.canvas.coords(self.playersprite)[2]
        self.currenty2 = self.canvas.coords(self.playersprite)[3]

        self.o_list = self.overlaps(self.currentx1, self.currenty1, self.currentx2, self.currenty2)
        for x in self.o_list:
            for a in self.stack:
                if a.getitemid() == x:
                    if a.gettype() == "Wood":
                        self.additem(0, 3)
                    elif a.gettype() == "Stone":
                        self.additem(1, 3)
                    elif a.gettype() == "Coal":
                        self.additem(2, 2)
                    a.removesprite()
        self.canvas.after(70, self.movement)


#navigation
    def back(self):
        self.canvas.grid_forget()

    def left(self, event):
        self.leftpressed = True
        self.x = -5
        self.y = 0

    def right(self, event):
        self.rightpressed = True
        self.x = 5
        self.y = 0

    def up(self, event):
        self.uppressed = True
        self.x = 0
        self.y = -5

    def down(self, event):
        self.downpressed = True
        self.x = 0
        self.y = 5

    def stop(self, event, released):
        #print(self.o_list)
        #print(self.canvas.coords(self.playersprite))
        if released == "L":
            self.leftpressed = False
        elif released == "R":
            self.rightpressed = False
        elif released == "U":
            self.uppressed = False
        elif released == "D":
            self.downpressed = False
        if not (self.leftpressed or self.rightpressed or self.uppressed or self.downpressed):
            self.x = 0
            self.y = 0



#inventory stuff
    def loadinventory(self, arr):
        self.ind = 0
        for x in arr:
            self.inventory[self.ind] = x
            self.ind += 1

    def additem(self, n, a):
        self.inventory[n] = self.inventory[n] + a

    def subtractitem(self, n, a):
        self.inventory[n] = self.inventory[n] - a
        if self.inventory[n] < 0:
            self.inventory[n] = 0

    def getinventory(self):
        return self.inventory


#GUI functions


root = Tk()
playerInventory = [50, 50, 50, 0, 0, 0]
stagelevels = 0
higheststagelevel = 0

def changescreen(arr, new):
    global nameon
    global stagelevels
    nameon = False
    for x in arr[0]:
        root.grid_rowconfigure(x, weight=0)
    for x in arr[1]:
        root.grid_columnconfigure(x, weight=0)
    for x in arr[2]:
        x.grid_forget()
    if new == "Home":
        print("Not doing this right now")
    elif new == "Explore":
        stagelevels = 0
        explore()
    elif new == "":
        pass
    else:
        print("This has not been made in yet!")


def goback(c, e):
    if e == "x" or e.char == "x":
        i = 0
        while i < len(playerInventory):
            playerInventory[i] = c.getinventory()[i]
            i = i + 1
        c.back()
        root.unbind("<KeyPress-Down>")
        root.unbind("<KeyPress-Up>")
        root.unbind("<KeyPress>")
        arr = [[],[],[]]
        changescreen(arr, "Home")
    elif e.char == "y":
        #c.swingblade()
        c.cuttree()


def checkdown(c, e):
    if c.currenty2 > 410:
        goback(c, "x")
    else:
        c.down(e)

def checkup(c, e):
    if c.currenty1 < -10:
        i = 0
        while i < len(playerInventory):
            playerInventory[i] = c.getinventory()[i]
            i = i + 1
        c.back()
        explore()
    else:
        c.up(e)


def explore():
    global stagelevels
    global higheststagelevel
    stagelevels = stagelevels + 1
    if higheststagelevel < stagelevels:
        higheststagelevel = stagelevels
    test = Items(root)
    test.loadinventory(playerInventory)
    root.bind("<KeyPress-Left>", lambda e: test.left(e))
    root.bind("<KeyPress-Right>", lambda e: test.right(e))
    #root.bind("<KeyPress-Up>", lambda e: test.up(e))
    root.bind("<KeyPress-Up>", lambda e: checkup(test, e))
    #root.bind("<KeyPress-Down>", lambda e: test.down(e))
    root.bind("<KeyPress-Down>", lambda e: checkdown(test, e))
    root.bind("<KeyRelease-Left>", lambda e: test.stop(e, "L"))
    root.bind("<KeyRelease-Right>", lambda e: test.stop(e, "R"))
    root.bind("<KeyRelease-Up>", lambda e: test.stop(e, "U"))
    root.bind("<KeyRelease-Down>", lambda e: test.stop(e, "D"))
    root.bind("<KeyPress>", lambda e: goback(test, e))

explore()
#btest = Items(root)
#btest.swingblade()
root.mainloop()