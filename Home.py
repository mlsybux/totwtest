from tkinter import *

class Databanks:
    def __init__(self, ID):
        #[int x, int y, array script, sprite]
        #kuya, craft bench
        self.array = [[100, 100, ["Hey there.", "This is just a test script, but might as well do something fun.",
          "Uhhhh what kind of drink do you like?", "{", "{INSERT}", "I, personally, like hot cocoa."]],
                      [400, 200, ["Time to craft!", "{CRAFT}"]]]
        self.object = self.array[ID]
        self.x = self.object[0]
        self.y = self.object[1]
        self.script = self.object[2]
        self.sprite = PhotoImage(file='basic_sprite.png')

#class NPC will create NPC objects that have a text, a sprite, and coordinates
class NPC:
    def __init__(self, master, canvas, ID):
        self.master = master
        self.canvas = canvas
        self.data = Databanks(ID)
        self.excimage = PhotoImage(file='exclamation.png')
        self.npcsprite = self.canvas.create_image(self.data.x, self.data.y, image=self.data.sprite)
        self.excsprite = self.canvas.create_image(self.data.x, self.data.y-20,
                                                  image=self.excimage, state=HIDDEN)
        self.script = self.data.script
        #self.inrange = False

    def set_inrange(self, b):
        if b:
            self.canvas.itemconfig(self.excsprite, state=NORMAL)
        else:
            self.canvas.itemconfig(self.excsprite, state=HIDDEN)
        #self.inrange = bool



class Home:
    def __init__(self, master):
        self.master = master
        self.x = 0
        self.y = 0
        # just saying that all the keys are released by default
        self.leftpressed = False
        self.rightpressed = False
        self.uppressed = False
        self.downpressed = False
        # 0 = front, 1 = right, 2 = down, 3 = left
        self.facing = 0
        # this is the canvas NOT THE TK
        self.canvas = Canvas(master, width=600, height=400, bg="light green")
        # the player's sprite and its coordinates :)
        # self.playersprite = self.canvas.create_rectangle(290, 350, 310, 370, fill="purple")
        self.psprite = PhotoImage(file='beta_sprite.png')
        self.pback = PhotoImage(file='beta_back.png')
        self.pleft = PhotoImage(file='beta_left.png')
        self.pright = PhotoImage(file='beta_right.png')
        self.bsprite = PhotoImage(file='basic_sprite.png')
        self.playersprite = self.canvas.create_image(290, 350, image=self.pback)
        self.npc_list = (NPC(self.master, self.canvas, 0), NPC(self.master, self.canvas, 1))
        self.currentx1 = self.canvas.coords(self.playersprite)[0] - 10
        self.currenty1 = self.canvas.coords(self.playersprite)[1] - 10
        self.currentx2 = self.currentx1 + 20
        self.currenty2 = self.currenty1 + 20
        self.canvas.grid(row=0, column=0, rowspan=5, columnspan=5)
        self.craft = Canvas(master, width=400, height=300, bg="light gray")
        self.label = Label(master, bg="white", width=80, height=3)
        self.label_on = False
        self.button_up = False
        self.picup = True
        self.inv = Canvas(master, width=300, height=200, bg="gray")
        self.inventoryup = False
        # wood, stone, coal, tree, gems, axes
        self.inventory = [0, 0, 0, 0, 0, 0]
        self.script = []
        self.index = 0
        self.movement()


    def interaction(self):
        if self.picup and not self.button_up:
            if not self.label_on:
                self.label_on = True
                self.label.configure(text=self.script[self.index])
                self.label.grid(row=4, column=2, rowspan=4)
            elif len(self.script) > self.index + 1:
                self.index = self.index + 1
                if self.script[self.index] == "{":
                    self.label_on = False
                    self.label.grid_forget()
                    self.index = self.index + 1
                    self.choice(["Coffee", "Tea", "Water"])
                elif self.script[self.index] == "{CRAFT}":
                    self.label_on = True
                    self.label.grid_forget()
                    self.index = self.index + 1
                    self.craft.grid(row=1, column=1, rowspan=3, columnspan=3)
                    self.exitB = Button(self.master, text="X", command=lambda:self.close_popup([self.craft, self.exitB]))
                    self.exitB.grid(row=1, column=3, sticky=NE)
                else:
                    self.label.configure(text=self.script[self.index])
            else:
                self.label_on = False
                self.index = 0
                self.label.grid_forget()
                self.movement()


    def close_popup(self, array):
        self.label_on = False
        for x in array:
            x.grid_forget()


    def choicemade(self, n, list):
        #global index, script, button_up
        self.button_up = False
        for l in list:
            l.grid_forget()
        self.answer_list = ["Coffee? You got a caffeine addiction?", "Tea, huh? You sound old.", "Water? Seriously?"]
        self.script[self.index] = self.answer_list[n]
        self.interaction()

    def choice(self, choices):
        self.button_up = True
        b0 = Button(self.master, command=lambda: self.choicemade(0, gridded_list))
        b1 = Button(self.master, command=lambda: self.choicemade(1, gridded_list))
        b2 = Button(self.master, command=lambda: self.choicemade(2, gridded_list))
        b3 = Button(self.master, command=lambda: self.choicemade(3, gridded_list))
        button_list = [b0, b1, b2, b3]
        gridded_list = []
        i = 0
        for c in choices:
            button_list[i].configure(text=c)
            button_list[i].grid(row=i, column=2)
            gridded_list.append(button_list[i])
            i = i + 1





    def movement(self):
        if not self.label_on:
            #moves the sprite
            self.canvas.move(self.playersprite, self.x, self.y)
            #sets the current coords to whatever the new coords are
            self.currentx1 = self.canvas.coords(self.playersprite)[0] - 10
            self.currenty1 = self.canvas.coords(self.playersprite)[1] - 10
            self.currentx2 = self.currentx1 + 20
            self.currenty2 = self.currenty1 + 20

            #checks if you're near an npc to interact with
            for npc in self.npc_list:
                if npc.data.x - 30 < self.currentx1 < npc.data.x + 30 and npc.data.y - 30 < self.currenty1 \
                        < npc.data.y + 30:
                    self.picup = True
                    npc.set_inrange(True)
                    self.script = npc.data.script
                    break
                else:
                    npc.set_inrange(False)
                    self.picup = False

            #after 70 ticks, it calls itself again
            self.canvas.after(70, self.movement)

    # navigation
    def back(self):
        self.canvas.grid_forget()

    def left(self, event):
        if not (self.label_on or self.button_up):
            self.leftpressed = True
            self.canvas.itemconfig(self.playersprite, image=self.pleft)
            self.facing = 3
            self.x = -5
        # self.y = 0

    def right(self, event):
        if not (self.label_on or self.button_up):
            self.rightpressed = True
            self.canvas.itemconfig(self.playersprite, image=self.pright)
            self.facing = 1
            self.x = 5
        # self.y = 0

    def up(self, event):
        if not (self.label_on or self.button_up):
            self.uppressed = True
            self.canvas.itemconfig(self.playersprite, image=self.pback)
            self.facing = 0
            # self.x = 0
            self.y = -5

    def down(self, event):
        if not (self.label_on or self.button_up):
            self.downpressed = True
            self.canvas.itemconfig(self.playersprite, image=self.psprite)
            self.facing = 2
            # self.x = 0
            self.y = 5


    def stop(self, event, released):
        if released == "L":
            self.leftpressed = False
        elif released == "R":
            self.rightpressed = False
        elif released == "U":
            self.uppressed = False
        elif released == "D":
            self.downpressed = False
        if not (self.leftpressed or self.rightpressed):
            self.x = 0
            if self.uppressed:
                self.facing = 0
                self.canvas.itemconfig(self.playersprite, image=self.pback)
            elif self.downpressed:
                self.facing = 2
                self.canvas.itemconfig(self.playersprite, image=self.psprite)
        if not (self.uppressed or self.downpressed):
            self.y = 0
            if self.leftpressed:
                self.facing = 3
                self.canvas.itemconfig(self.playersprite, image=self.pleft)
            elif self.downpressed:
                self.facing = 1
                self.canvas.itemconfig(self.playersprite, image=self.pright)

    # inventory stuff
    def showinventory(self):
        self.inventoryup = True
        self.inv.grid(row=1, column=1, rowspan=3, columnspan=3)
        self.backB = Button(self.master, text="X", command=lambda: self.hideinventory())
        self.invLabel = Label(self.master, text="Inventory: \nWood: " + str(self.inventory[0]) + "\nStone: "
                                                + str(self.inventory[1]) + "\nCoal: " + str(self.inventory[2]) +
                                                "\nAxes: " + str(self.inventory[5]))
        self.invLabel.grid(row=2, column=2)
        self.backB.grid(row=2, column=3)

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