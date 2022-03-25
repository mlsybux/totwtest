from tkinter import *
from Home import Popups, NPC

class Morgan:
    def __init__(self, master, player):
        self.master = master
        self.player = player
        # just saying that all the keys are released by default
        self.leftpressed = False
        self.rightpressed = False
        self.uppressed = False
        self.downpressed = False
        # 0 = front, 1 = right, 2 = down, 3 = left
        self.facing = 0
        # this is the canvas NOT THE TK
        self.canvas = Canvas(master, width=600, height=400, bg="goldenrod")
        # the player's sprite and its coordinates :)
        self.psprite = PhotoImage(file='beta_sprite.png')
        self.pback = PhotoImage(file='beta_back.png')
        self.pleft = PhotoImage(file='beta_left.png')
        self.pright = PhotoImage(file='beta_right.png')
        self.bsprite = PhotoImage(file='basic_sprite.png')
        self.playersprite = self.canvas.create_image(290, 350, image=self.pleft)
        self.x = 0
        self.y = 0
        self.currentx1 = self.canvas.coords(self.playersprite)[0] - 10
        self.currenty1 = self.canvas.coords(self.playersprite)[1] - 10
        self.currentx2 = self.currentx1 + 20
        self.currenty2 = self.currenty1 + 20
        self.canvas.grid(row=0, column=0, rowspan=5, columnspan=5)
        # wood, stone, coal, tree, swords, axes
        self.inventory = self.player.inventory
        self.obstacles = {}
        self.script = []
        self.index = 0
        self.npc_list = [NPC(self.master, self.canvas, 2), NPC(self.master, self.canvas, 3)]
        self.picup = False
        self.parchmentup = False
        self.label = Label(master, bg="white", width=80, height=3)
        self.label_on = False
        self.loadborders()
        self.movement()

    #FRONT END: Jadzia
    #everything under HERE is just user interface/GUI/visual stuff that gets put up on screen :)


    def hasobstacle(self, x1, y1, x2, y2):
        self.c_object = self.canvas.find_overlapping(x1, y1, x2, y2)
        for k, v in self.obstacles.items():  # iterates over obstacles dict
            if v in self.c_object:
                return True
        return False

    def loadborders(self):
        self.color = "brown"
        self.leftborder = self.canvas.create_rectangle(0, 0, 17, 400, fill=self.color)
        self.rightborder1 = self.canvas.create_rectangle(583, 0, 600, 200, fill=self.color)
        self.rightborder2 = self.canvas.create_rectangle(583, 350, 600, 400, fill=self.color)
        self.lowerborder = self.canvas.create_rectangle(0, 383, 600, 400, fill=self.color)
        self.upperborder = self.canvas.create_rectangle(0, 0, 600, 20, fill=self.color)
        self.obstacles["UpperBorder"] = self.upperborder
        self.obstacles["LeftBorder"] = self.leftborder
        self.obstacles["RightBorder1"] = self.rightborder1
        self.obstacles["RightBorder2"] = self.rightborder2
        self.obstacles["LowerBorder"] = self.lowerborder

    def interaction(self):
        if self.picup and not self.parchmentup:
            if not self.label_on:
                self.label_on = True
                self.label.configure(text=self.script[self.index])
                self.label.grid(row=4, column=2, rowspan=4)
            elif len(self.script) > self.index + 1:
                self.index = self.index + 1
                if self.script[self.index] == "{PARCHMENT}":
                    self.open_popup(2)
                elif self.script[self.index] == "{SLEEP}":
                    self.open_popup(3)
                else:
                    self.label.configure(text=self.script[self.index])
            else:
                self.label_on = False
                self.script = []
                self.index = 0
                self.label.grid_forget()
                self.movement()

    def open_popup(self, id):
        self.parchmentup = True
        self.label_on = False
        self.label.grid_forget()
        self.popup = Popups(self.master, id, self.player)
        self.exitB = Button(self.master, text="X",
                            command=lambda: self.close_popup([self.popup.canvas, self.exitB]))
        self.exitB.grid(row=1, column=3, sticky=NE)

    def close_popup(self, array):
        self.label_on = False
        self.parchmentup = False
        self.index = 0
        for x in array:
            x.grid_forget()
        self.movement()

    def movement(self):
        if not self.parchmentup:
            #checks for obstacles
            if self.currenty1 <= 0:
                self.y = 0
            if self.x < 0 and self.hasobstacle(self.currentx1 - 5, self.currenty1, self.currentx2 - 5, self.currenty2):
                # print("obstacle to the left")
                self.x = 0
            if self.x > 0 and self.hasobstacle(self.currentx1 + 5, self.currenty1, self.currentx2 + 5, self.currenty2):
                # print("obstacle to the right")
                self.x = 0
            if self.y < 0 and self.hasobstacle(self.currentx1, self.currenty1 - 5, self.currentx2, self.currenty2 - 5):
                self.y = 0
            if self.y > 0 and self.hasobstacle(self.currentx1, self.currenty1 + 5, self.currentx2, self.currenty2 + 5):
                self.y = 0
            #moves the sprite
            self.canvas.move(self.playersprite, self.x, self.y)
            #sets the current coords to whatever the new coords are
            self.currentx1 = self.canvas.coords(self.playersprite)[0] - 10
            self.currenty1 = self.canvas.coords(self.playersprite)[1] - 10
            self.currentx2 = self.currentx1 + 20
            self.currenty2 = self.currenty1 + 20
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
            #calls itself again
            self.canvas.after(70, self.movement)
    # navigation
    def back(self):
        self.canvas.grid_forget()


    def left(self, event):
        if not self.parchmentup:
            self.leftpressed = True
            self.canvas.itemconfig(self.playersprite, image=self.pleft)
            self.facing = 3
            self.x = -5
            self.y = 0

    def right(self, event):
        if not self.parchmentup:
            self.rightpressed = True
            self.canvas.itemconfig(self.playersprite, image=self.pright)
            self.facing = 1
            self.x = 5
            self.y = 0


    def up(self, event):
        if not self.parchmentup:
            self.uppressed = True
            self.canvas.itemconfig(self.playersprite, image=self.pback)
            self.facing = 0
            self.x = 0
            self.y = -5

    def down(self, event):
        if not self.parchmentup:
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


    #This is where the front end ends

    #BACK END: Morgan
    #everything under here is just calculations
    def test_wood(self, days):
        return (days*5)