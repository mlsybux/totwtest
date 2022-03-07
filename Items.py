from tkinter import *
from random import *
from Home import *


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

    def getsprite(self):
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

    def getid(self):
        return self.id

    def makesprite(self):
        self.sprite = self.randomsprite()

    def removesprite(self):
        self.canvas.delete(self.sprite)
        #print("Sprite removed!")


class Bestiary:
    def __init__(self, can, rtype, rid, obs):
        self.canvas = can
        self.type = rtype
        self.id = rid
        self.obstacles = obs
        #pcoords is the player coordinates in a list, given [x, y]
        self.pcoords = [290, 350]
        #Type, Max Health, Attack
        self.bestiarylist = [["Slime", 50, 1], ["Slime King", 150, 3]]
        for x in self.bestiarylist:
            if self.type == x[0]:
                self.attack = x[2]
                self.health, self.maxhealth = x[1], x[1]
        self.healthbarexists = False
        self.sprite = self.randomsprite()
        self.alive = True
        self.x = 0
        self.y = 0
        self.differenceX = 0
        self.differenceY = 0
        self.currentx1 = self.canvas.coords(self.sprite)[0]
        self.currenty1 = self.canvas.coords(self.sprite)[1]
        self.currentx2 = self.canvas.coords(self.sprite)[2]
        self.currenty2 = self.canvas.coords(self.sprite)[3]
        #self.health, self.maxhealth = 50, 50
        #self.attack = 1
        self.move()

    def randomsprite(self):
        self.rand1 = randint(50, 400)
        self.rand2 = randint(30, 300)
        while self.hasobstacle(self.rand1, self.rand2, self.rand1+25, self.rand2+25):
            self.rand1 = randint(50, 400)
            self.rand2 = randint(30, 300)
        if self.type == "Slime":
            return self.canvas.create_rectangle(self.rand1, self.rand2, self.rand1+25, self.rand2+25, fill="red")
        elif self.type == "Slime King":
            self.healthbarexists = True
            self.healthbar()
            return self.canvas.create_rectangle(self.rand1, self.rand2, self.rand1+50, self.rand2+50, fill="pink")


    def healthbar(self):
        self.healthbarexists = True
        self.emptyhealthbar = self.canvas.create_rectangle(20, 365, 180, 385, fill="white")
        self.fullhealthbar = self.canvas.create_rectangle(20, 365, (self.health / self.maxhealth) * 160 + 20, 385,
                                                          fill="red")

    def changehealth(self, change):
        self.health = self.health + change

        if self.health > self.maxhealth:
            self.health = self.maxhealth
        if self.health <= 0:
            self.canvas.delete(self.fullhealthbar)
        else:
            self.canvas.coords(self.fullhealthbar, 20, 365, (self.health / self.maxhealth) * 160 + 20, 385)

    def damage(self, n):
        self.health = self.health - n
        #print(self.health)
        if self.health <= 0:
            self.health = 0
            self.defeat()
        if self.healthbarexists:
            self.changehealth(-n)

    def specialdamage(self, n):
        if n > (self.health/2):
            self.damage(self.health/2)
        else:
            self.damage(n)

    def hasobstacle(self, x1, y1, x2, y2):
        if y2 >= 385:
            return True
        self.c_object = self.canvas.find_overlapping(x1, y1, x2, y2)
        for k, v in self.obstacles.items():  # iterates over obstacles dict
            if v in self.c_object:
                return True
        return False

    def move(self):
        if not self.alive:
            return

        # checks where the player is in relation to it, moves in the direction that's currently the furthest
        if self.currentx1-2 > self.pcoords[0]:
            self.differenceX = self.currentx2 - self.pcoords[0]
            self.x = -2
        elif self.currentx1+2 < self.pcoords[0]:
            self.differenceX = self.pcoords[0] - self.currentx1+2
            self.x = 2
        else:
            self.differenceX=0
            self.x = 0
        if self.currenty1-2 > self.pcoords[1]:
            self.differenceY = self.currenty1-2 - self.pcoords[1]
            self.y = -2
        elif self.currenty1+2 < self.pcoords[1]:
            self.differenceY = self.pcoords[1] - self.currenty1+2
            self.y = 2
        else:
            self.differenceY = 0
            self.y = 0
        if self.differenceX > self.differenceY:
            self.y = 0
        else:
            self.x = 0

        # checks if there's an obstacle in the direction it's trying to move
        if self.x < 0 and self.hasobstacle(self.currentx1 - 5, self.currenty1, self.currentx2 - 5, self.currenty2):
            self.x = 0
        if self.x > 0 and self.hasobstacle(self.currentx1 + 5, self.currenty1, self.currentx2 + 5, self.currenty2):
            self.x = 0
        if self.y < 0 and self.hasobstacle(self.currentx1, self.currenty1 - 5, self.currentx2, self.currenty2 - 5):
            self.y = 0
        if self.y > 0 and self.hasobstacle(self.currentx1, self.currenty1 + 5, self.currentx2, self.currenty2 + 5):
            self.y = 0

        # moves the sprite
        self.canvas.move(self.sprite, self.x, self.y)
        # sets the current coords to whatever the new coords are
        self.currentx1 = self.canvas.coords(self.sprite)[0]
        self.currenty1 = self.canvas.coords(self.sprite)[1]
        self.currentx2 = self.canvas.coords(self.sprite)[2]
        self.currenty2 = self.canvas.coords(self.sprite)[3]

        self.canvas.after(70, self.move)

    def getplayercoords(self, px, py):
        self.pcoords[0] = px
        self.pcoords[1] = py


    def getattack(self):
        return self.attack

    def gettype(self):
        return self.type

    def getid(self):
        return self.id

    def getsprite(self):
        return self.sprite

    def makesprite(self):
        self.alive = True
        self.sprite = self.randomsprite()

    def defeat(self):
        self.alive = False
        self.canvas.delete(self.sprite)
        if self.type == "Slime King":
            self.canvas.bosswin = True


class Items:
    def __init__(self, master, l, player):
        #Tk
        self.master = master
        self.player = player
        #wood, stone, coal, tree, gems, axes
        self.inventory = [0, 0, 0, 0, 0, 0]
        #x and y are the movement
        self.x = 0
        self.y = 0
        self.level = l
        if self.level <= 7:
            self.environment = "Forest"
        elif 12 >= self.level > 7:
            self.environment = "Cave"
        elif self.level > 12:
            self.environment = "Boss Fight"
        #just saying that all the keys are released by default
        self.leftpressed = False
        self.rightpressed = False
        self.uppressed = False
        self.downpressed = False
        #0 = front, 1 = right, 2 = down, 3 = left
        self.facing = 0
        #this is the canvas NOT THE TK
        self.canvas = Canvas(master, width=600, height=400)
        self.inv = Canvas(master, width=300, height=200, bg="gray")
        #the player's sprite and its coordinates :)
        #self.playersprite = self.canvas.create_rectangle(290, 350, 310, 370, fill="purple")
        self.psprite = PhotoImage(file='beta_sprite.png')
        self.pback = PhotoImage(file='beta_back.png')
        self.pleft = PhotoImage(file='beta_left.png')
        self.pright = PhotoImage(file='beta_right.png')
        self.playersprite = self.canvas.create_image(290, 350, image=self.pback)
        self.currentx1 = self.canvas.coords(self.playersprite)[0] - 10
        self.currenty1 = self.canvas.coords(self.playersprite)[1] - 10
        self.currentx2 = self.currentx1 + 20
        self.currenty2 = self.currenty1 + 20
        self.bladebool = False
        self.hit = False
        self.canvas.bosswin = False
        self.inventoryup = False
        self.health = 100
        self.maxhealth = 100
        self.canvas.grid(row=0, column=0, rowspan=5, columnspan=5)
        self.resources = {}
        self.obstacles = {}
        self.enemies = {}
        self.dictionaries = [self.resources, self.obstacles, self.enemies]
        self.stack = []
        #self.maketree()
        self.loadborders()
        self.level_text = self.canvas.create_text(50, 10, text="Stage Level: " + str(self.level), fill="white")
        if self.environment == "Forest":
            if self.level <= 3:
                self.spawnitems([5, 3, 2, 2])
            elif 5 > self.level > 3:
                self.spawnitems([3, 5, 4, 1])
                self.loadenemies(1)
            elif self.level >= 5:
                self.spawnitems([3, 3, 3, 3])
                self.loadenemies(2)
        elif self.environment == "Cave":
            self.spawnitems([0, 6, 5, 0])
            self.loadenemies(1)
        elif self.environment == "Boss Fight":
            #self.loadenemies(5)
            self.bossfight()

        self.emptyhealthbar = self.canvas.create_rectangle(420, 365, 580, 385, fill="white")
        self.fullhealthbar = self.canvas.create_rectangle(420, 365, (self.health / self.maxhealth) * 160 + 420, 385,
                                                          fill="red")
        self.movement()

    def getbosswin(self):
        return self.canvas.bosswin

    def loadborders(self):
        if self.environment == "Forest":
            self.color = "green"
        else:
            self.color = "gray"
        self.leftborder = self.canvas.create_rectangle(0, 0, 17, 400, fill=self.color)
        self.rightborder = self.canvas.create_rectangle(583, 0, 600, 400, fill=self.color)

        self.lowerborderL = self.canvas.create_rectangle(0, 353, 200, 400, fill=self.color)
        self.lowerborderR = self.canvas.create_rectangle(400, 353, 600, 400, fill=self.color)

        if self.environment == "Boss Fight":
            self.upperborder = self.canvas.create_rectangle(0, 0, 600, 20, fill=self.color)
            self.obstacles["UpperBorder"] = self.upperborder
        else:
            self.upperborderL = self.canvas.create_rectangle(0, 0, 280, 20, fill=self.color)
            self.upperborderR = self.canvas.create_rectangle(315, 0, 600, 20, fill=self.color)
            self.obstacles["UpperBorderL"] = self.upperborderL
            self.obstacles["UpperBorderR"] = self.upperborderR

        self.obstacles["LeftBorder"] = self.leftborder
        self.obstacles["RightBorder"] = self.rightborder
        self.obstacles["LowerBorderL"] = self.lowerborderL
        self.obstacles["LowerBorderR"] = self.lowerborderR

    def bossfight(self):
        self.boss = Bestiary(self.canvas, "Slime King", "Slime King", self.obstacles)
        self.stack.append(self.boss)
        self.enemies["Slime King"] = self.boss.getsprite()



    def kuya(self, swords):
        if swords <= 5:
            self.boss.specialdamage(5*swords)
        else:
            self.boss.specialdamage(25)

    def loadenemies(self, a):
        self.acounter = 0
        while self.acounter < a:
            self.enemy = Bestiary(self.canvas, "Slime", "Slime" + str(self.acounter), self.obstacles)
            self.stack.append(self.enemy)
            self.enemies["Slime" + str(self.acounter)] = self.enemy.getsprite()
            self.acounter = self.acounter + 1

    def changehealth(self, change):
        self.health = self.health + change

        if self.health <= 0:
            self.health = 0
            self.back()
        elif self.health > self.maxhealth:
            self.health = self.maxhealth

        self.canvas.coords(self.fullhealthbar, 420, 365, (self.health/self.maxhealth)*160 + 420, 385)

    def swingblade(self):
        self.bladebool = True
        self.x = 0
        self.y = 0
        if self.facing == 0:
            self.bx = 5
            self.by = 0
        elif self.facing == 1:
            self.bx = 0
            self.by = 5
        elif self.facing == 2:
            self.bx = -5
            self.by = 0
        else:
            self.bx = 0
            self.by = -5
        self.bx1 = self.canvas.coords(self.blade)[0]
        self.by1 = self.canvas.coords(self.blade)[1]
        self.bx2 = self.canvas.coords(self.blade)[2]
        self.by2 = self.canvas.coords(self.blade)[3]
        if self.inventory[5] >= 1:
            for x in self.overlaps(self.canvas.coords(self.blade)[0], self.canvas.coords(self.blade)[1],
                                   self.canvas.coords(self.blade)[2], self.canvas.coords(self.blade)[3]):
                for a in self.stack:
                    if a.gettype() == "Tree" and a.getid() == x:
                        self.additem(0, 5)
                        self.subtractitem(5, 1)
                        a.removesprite()
                    elif a.gettype() == "Slime" and a.getid() == x:
                        if not self.hit:
                            self.hit = True
                            a.damage(10)
                    elif a.gettype() == "Slime King" and a.getid() == x:
                        if not self.hit:
                            self.hit = True
                            a.damage(10)


        if (self.facing == 2 and self.bx1 <= self.currentx1) or (self.facing == 0 and self.bx2 >= self.currentx2)\
                or (self.facing == 3 and self.by1 <= self.currenty1) or (self.facing == 1 and self.by2 >= self.currenty2):
            self.bx = 0
            self.by = 0
            self.canvas.delete(self.blade)
            self.bladebool = False
            self.hit = False
            return
        self.canvas.move(self.blade, self.bx, self.by)
        self.canvas.after(70, self.swingblade)

    def cuttree(self):
        if not self.bladebool:
            if self.facing == 0:
                self.blade = self.canvas.create_rectangle(self.currentx1, self.currenty1 - 15, self.currentx1 + 5, self.currenty1)
            elif self.facing == 1:
                self.blade = self.canvas.create_rectangle(self.currentx2, self.currenty1, self.currentx2 + 15, self.currenty1 + 5)
            elif self.facing == 2:
                self.blade = self.canvas.create_rectangle(self.currentx2-5, self.currenty2, self.currentx2, self.currenty2+15)
            else:
                self.blade = self.canvas.create_rectangle(self.currentx1-15, self.currenty2 - 5, self.currentx1, self.currenty2)

            self.swingblade()

    def overlaps(self, x1, y1, x2, y2):
        self.overlap_list = []
        self.c_object = self.canvas.find_overlapping(x1, y1, x2, y2)
        """
        for k, v in self.resources.items(): #iterates over resources dict
            if v in self.c_object:
                self.overlap_list.append(k)
        #delete under this if it doesn't work
        for k, v in self.obstacles.items():
            if v in self.c_object:
                self.overlap_list.append(k)
                """
        for x in self.dictionaries:
            for k, v in x.items():
                if v in self.c_object:
                    self.overlap_list.append(k)
       # print(self.overlap_list)
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
                if self.typearray[self.penisboi] == "Tree":
                    self.obstacles[self.stack[self.i].getid()] = self.stack[self.i].getsprite()
                else:
                    self.resources[self.stack[self.i].getid()] = self.stack[self.i].getsprite()
                self.ind = self.ind + 1
                self.i = self.i + 1
            self.penisboi = self.penisboi + 1
        self.stack.append(Resource(self.canvas, "Tree", "BorderTree"))
        self.stack[self.i].setlocation(285, 2, 310, 27)
        self.obstacles[self.stack[self.i].getid()] = self.stack[self.i].getsprite()

    def hasobstacle(self, x1, y1, x2, y2):
        self.c_object = self.canvas.find_overlapping(x1, y1, x2, y2)
        for k, v in self.obstacles.items():  # iterates over obstacles dict
            if v in self.c_object:
                return True
        return False

    def movement(self):
        if not self.inventoryup:
            #checks if there's an obstacle in the direction it's trying to move
            if self.x < 0 and self.hasobstacle(self.currentx1-5, self.currenty1, self.currentx2-5, self.currenty2):
                #print("obstacle to the left")
                self.x = 0
            if self.x > 0 and self.hasobstacle(self.currentx1+5, self.currenty1, self.currentx2+5, self.currenty2):
                #print("obstacle to the right")
                self.x = 0
            if self.y < 0 and self.hasobstacle(self.currentx1, self.currenty1-5, self.currentx2, self.currenty2-5):
                self.y = 0
            if self.y > 0 and self.hasobstacle(self.currentx1, self.currenty1+5, self.currentx2, self.currenty2+5):
                self.y = 0
            #moves the sprite
            self.canvas.move(self.playersprite, self.x, self.y)
            #sets the current coords to whatever the new coords are
            self.currentx1 = self.canvas.coords(self.playersprite)[0] - 10
            self.currenty1 = self.canvas.coords(self.playersprite)[1] - 10
            self.currentx2 = self.currentx1 + 20
            self.currenty2 = self.currenty1 + 20

            #let enemies know where player is
            for x in self.stack:
                if x.gettype() == "Slime":
                    x.getplayercoords(self.currentx1, self.currenty1)

            #gets the list of whatever it's overlapping, then iterates through it to either get it or get hurt
            self.o_list = self.overlaps(self.currentx1, self.currenty1, self.currentx2, self.currenty2)
            for x in self.o_list:
                for a in self.stack:
                    if a.getid() == x and x in self.resources:
                        if a.gettype() == "Wood":
                            self.additem(0, 3)
                        elif a.gettype() == "Stone":
                            self.additem(1, 3)
                        elif a.gettype() == "Coal":
                            self.additem(2, 2)
                        a.removesprite()
                    elif a.getid() == x and x in self.enemies:
                        if a.gettype() == "Slime" or a.gettype() == "Slime King":
                            self.changehealth(-a.getattack())
            #after 70 ticks, it calls itself again
            self.canvas.after(70, self.movement)

    # navigation
    def back(self):
        self.canvas.grid_forget()


    def left(self, event):
        self.leftpressed = True
        self.canvas.itemconfig(self.playersprite, image=self.pleft)
        self.facing = 3
        self.x = -5
        self.y = 0

    def right(self, event):
        self.rightpressed = True
        self.canvas.itemconfig(self.playersprite, image=self.pright)
        self.facing = 1
        self.x = 5
        self.y = 0


    def up(self, event):
        self.uppressed = True
        self.canvas.itemconfig(self.playersprite, image=self.pback)
        self.facing = 0
        self.x = 0
        self.y = -5

    def down(self, event):
        self.downpressed = True
        self.canvas.itemconfig(self.playersprite, image=self.psprite)
        self.facing = 2
        self.x = 0
        self.y = 5


    def stop(self, event):
        if event.keysym == "Left":
            self.leftpressed = False
        elif event.keysym == "Right":
            self.rightpressed = False
        elif event.keysym == "Up":
            self.uppressed = False
        elif event.keysym == "Down":
            self.downpressed = False
        if not (self.leftpressed or self.rightpressed):
            self.x = 0
            if self.uppressed:
                self.y = -5
                self.facing = 0
                self.canvas.itemconfig(self.playersprite, image=self.pback)
            elif self.downpressed:
                self.y = 5
                self.facing = 2
                self.canvas.itemconfig(self.playersprite, image=self.psprite)
        if not (self.uppressed or self.downpressed):
            self.y = 0
            if self.leftpressed:
                self.x = -5
                self.facing = 3
                self.canvas.itemconfig(self.playersprite, image=self.pleft)
            elif self.rightpressed:
                self.x = 5
                self.facing = 1
                self.canvas.itemconfig(self.playersprite, image=self.pright)

#stats stuff
    def loadstats(self, n):
        self.health = n
        self.changehealth(0)

    def getstats(self):
        return self.health

#inventory stuff

    def open_popup(self, id):
        self.inventoryup = True
        self.popup = Popups(self.master, id, self.player)
        self.exitB = Button(self.master, text="X",
                            command=lambda: self.close_popup([self.popup.canvas, self.exitB]))
        self.exitB.grid(row=1, column=3, sticky=NE)

    def close_popup(self, array):
        self.inventoryup = False
        for x in array:
            x.grid_forget()
        self.movement()


    def showinventory(self):
        self.inventoryup = True
        self.inv.grid(row=1, column=1, rowspan=3, columnspan=3)
        self.backB = Button(self.master, text="X", command=lambda:self.hideinventory())
        self.invLabel = Label(self.master, text="Inventory: \nWood: " + str(self.inventory[0]) + "\nStone: "
                                                + str(self.inventory[1]) + "\nCoal: " + str(self.inventory[2]) +
                                                "\nAxes: " + str(self.inventory[5]))
        self.invLabel.grid(row=2, column=2)
        self.backB.grid(row=3, column=3)

    def hideinventory(self):
        self.inventoryup = False
        self.inv.grid_forget()
        self.invLabel.grid_forget()
        self.backB.grid_forget()

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