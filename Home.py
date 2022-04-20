from tkinter import *
from Story import *

#classes Databanks, NPC, Home

class Databanks:
    def __init__(self, type, ID):
        #[int x, int y, array script, sprite, size/2]
        #kuya, craft bench, record table, bed
        if type == "NPC":
            self.array = [[100, 100, "Kuya",
                           'assets/kuya_front.png', 40],
                          [400, 200, "Craft", 'assets/ekorre_left.png', 25],
                          [300, 200, "Parchment",
                           'assets/ekorre_front.png', 25],
                          [150, 150, "Sleep", 'assets/alba_front.png', 25]]
            self.object = self.array[ID]
            self.x = self.object[0]
            self.y = self.object[1]
            self.script = self.object[2]
            self.sprite = PhotoImage(file=self.object[3])
            self.size = self.object[4]
        elif type == "Player":
            #name, title, kingdom, health, attack, furthest level, crowns
            self.player_data = ["Ako", "Overlord", "Kaharian", 300, 10, 0, 0]
            #current health
            self.current_data = [300]
            #wood, stone, coal, trees, swords, axe
            self.inventory = [0, 0, 0, 0, 0, 0]

    def set_player_data(self, x, n):
        #name, title, kingdom, health, attack, furthest level, crowns
        self.player_data[x] = n

    def get_current_health(self):
        return self.current_data[0]

    def reset_health(self):
        self.current_data[0] = self.player_data[3]

    def set_current_health(self, c):
        self.current_data[0] = c

    def change_current_health(self, n):
        self.current_data[0] = self.current_data[0] + n

        if self.current_data[0] > self.player_data[3]:
            self.current_data[0] = self.player_data[3]
        if self.current_data[0] < 0:
            self.current_data[0] = 0


    def loadinventory(self, arr):
        self.ind = 0
        for x in arr:
            self.inventory[self.ind] = x
            self.ind += 1

    def additem(self, n, a):
        self.inventory[n] = self.inventory[n] + a
        if n == 4:
            self.player_data[4] += a

    def subtractitem(self, n, a):
        self.inventory[n] = self.inventory[n] - a
        if self.inventory[n] < 0:
            self.inventory[n] = 0

    def getinventory(self):
        return self.inventory


#class NPC will create NPC objects that have a text, a sprite, and coordinates
class NPC:
    def __init__(self, master, canvas, ID):
        self.master = master
        self.canvas = canvas
        self.data = Databanks("NPC", ID)
        self.excimage = PhotoImage(file='assets/exclamation.png')
        self.npcsprite = self.canvas.create_image(self.data.x, self.data.y, image=self.data.sprite)
        self.excsprite = self.canvas.create_image(self.data.x, self.data.y-(self.data.size+10),
                                                  image=self.excimage, state=HIDDEN)
        self.script = self.data.script


    def set_inrange(self, b):
        if b:
            self.canvas.itemconfig(self.excsprite, state=NORMAL)
        else:
            self.canvas.itemconfig(self.excsprite, state=HIDDEN)



class Home:
    def __init__(self, master, player):
        self.master = master
        self.player = player
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
        self.canvas = Canvas(master, width=600, height=400, bg="DarkOliveGreen3")
        # the player's sprite and its coordinates :)
        # self.playersprite = self.canvas.create_rectangle(290, 350, 310, 370, fill="purple")
        self.psprite = PhotoImage(file='assets/ako_front.png')
        self.pback = PhotoImage(file='assets/ako_back.png')
        self.pleft = PhotoImage(file='assets/ako_left.png')
        self.pright = PhotoImage(file='assets/ako_right.png')
        self.bsprite = PhotoImage(file='assets/basic_sprite.png')
        self.playersprite = self.canvas.create_image(290, 350, image=self.pback)
        self.npc_list = [NPC(self.master, self.canvas, 0), NPC(self.master, self.canvas, 1)]
        #self.npc_list = [NPC(self.master, self.canvas, 1)]
        self.currentx1 = self.canvas.coords(self.playersprite)[0] - 25
        self.currenty1 = self.canvas.coords(self.playersprite)[1] - 25
        self.currentx2 = self.currentx1 + 50
        self.currenty2 = self.currenty1 + 50
        self.canvas.grid(row=0, column=0, rowspan=5, columnspan=5)
        # wood, stone, coal, tree, swords, axes
        self.inventory = self.player.inventory
        #textbox
        self.label = Label(master, bg="white", width=80, height=3)
        self.label_on = False
        #self.button_up = False
        self.canvas.popup_up = False
        self.picup = True
        self.inv = Canvas(master, width=300, height=200, bg="gray")
        self.inventoryup = False
        self.obstacles = {}
        self.script = ""
        self.index = 0
        self.loadborders()
        self.movement()


    def interaction(self):
        if self.picup and not self.canvas.popup_up:
            if not self.label_on:
                self.label_on = True
                self.story = Story(self.master, self.canvas, self.player, self.script)
            elif self.story.text_on:
                self.story.continue_text()
                if not self.story.text_on:
                    self.label_on = False
                    self.movement()
            else:
                self.label_on = False
                self.movement()


    def open_popup(self, id):
        self.label_on = False
        #self.button_up = True
        self.canvas.popup_up = True
        self.label.grid_forget()
        """
        if self.index < len(self.script) - 1:
            self.index = self.index + 1
        else:
            self.index = 0
            """
        self.popup = Popups(self.master, id, self.player)
        self.exitB = Button(self.master, text="X",
                            command=lambda: self.close_popup([self.popup.canvas, self.exitB]))
        self.exitB.grid(row=1, column=3, sticky=NE)

    def close_popup(self, array):
        self.label_on = False
        #self.button_up = False
        self.canvas.popup_up = False
        self.index = 0
        for x in array:
            x.grid_forget()
        #self.movement()


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


    def hasobstacle(self, x1, y1, x2, y2):
        self.c_object = self.canvas.find_overlapping(x1, y1, x2, y2)
        for k, v in self.obstacles.items():  # iterates over obstacles dict
            if v in self.c_object:
                return True
        return False

    def movement(self):
        if self.label_on:
            return
        if not self.canvas.popup_up:
            # checks if there's an obstacle in the direction it's trying to move
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
            self.currentx1 = self.canvas.coords(self.playersprite)[0] - 25
            self.currenty1 = self.canvas.coords(self.playersprite)[1] - 25
            self.currentx2 = self.currentx1 + 50
            self.currenty2 = self.currenty1 + 50

            #checks if you're near an npc to interact with
            for npc in self.npc_list:
                if npc.data.x - (npc.data.size*2 + 35) < self.currentx1 < npc.data.x + (npc.data.size + 15) \
                        and npc.data.y - (npc.data.size*2 + 35) < self.currenty1 < npc.data.y + (npc.data.size + 20):
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
        if not (self.label_on or self.canvas.popup_up):
            self.leftpressed = True
            self.canvas.itemconfig(self.playersprite, image=self.pleft)
            self.facing = 3
            self.x = -5
            self.y = 0

    def right(self, event):
        if not (self.label_on or self.canvas.popup_up):
            self.rightpressed = True
            self.canvas.itemconfig(self.playersprite, image=self.pright)
            self.facing = 1
            self.x = 5
            self.y = 0


    def up(self, event):
        if not (self.label_on or self.canvas.popup_up):
            self.uppressed = True
            self.canvas.itemconfig(self.playersprite, image=self.pback)
            self.facing = 0
            self.x = 0
            self.y = -5

    def down(self, event):
        if not (self.label_on or self.canvas.popup_up):
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


    def loadborders(self):
        self.color = "green"
        self.leftborder1 = self.canvas.create_rectangle(0, 0, 17, 200, fill=self.color)
        self.leftborder2 = self.canvas.create_rectangle(0, 350, 17, 400, fill=self.color)
        self.rightborder = self.canvas.create_rectangle(583, 0, 600, 400, fill=self.color)
        self.lowerborder = self.canvas.create_rectangle(0, 383, 600, 400, fill=self.color)
        self.upperborderL = self.canvas.create_rectangle(0, 0, 350, 20, fill=self.color)
        self.upperborderR = self.canvas.create_rectangle(440, 0, 600, 20, fill=self.color)
        self.obstacles["UpperBorderL"] = self.upperborderL
        self.obstacles["UpperBorderR"] = self.upperborderR
        self.obstacles["LeftBorder1"] = self.leftborder1
        self.obstacles["LeftBorder2"] = self.leftborder2
        self.obstacles["RightBorder"] = self.rightborder
        self.obstacles["LowerBorder"] = self.lowerborder
