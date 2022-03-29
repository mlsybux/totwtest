from tkinter import *
from Story import *

class Popups:
    def __init__(self, master, ID, player):
        self.master = master
        self.canvas = Canvas(self.master, width=400, height=300, bg="light gray")
        self.canvas.grid_propagate(False)
        self.header = self.canvas.create_text(190, 15)
        self.player = player
        #self.inventory = self.player.inventory
        self.frames_up = []
        if ID == 0:
            self.craft_screen()
            self.craft_change(0)
        elif ID == 1:
            self.menu_screen()
            self.change_menu(0)
        elif ID == 2:
            self.parchment_screen()
        elif ID == 3:
            self.yes_no_screen()
        self.canvas.grid(row=1, column=1, rowspan=3, columnspan=3)

    def menu_screen(self):
        self.canvas.itemconfigure(self.header, text="Menu")
        self.menu_bottom_frame = Frame(self.master, width=360, height=20)
        self.menu_bottom_frame.grid_propagate(False)
        self.menu_bottom_frame.grid_columnconfigure(0, weight=1)
        self.menu_bottom_frame.grid_columnconfigure(1, weight=1)
        self.menu_bottom_frame.grid_columnconfigure(2, weight=1)
        self.menu_bottom_frame.grid_rowconfigure(0, weight=1)
        self.menu_button = Button(self.menu_bottom_frame, text="Menu", width=13, command=lambda: self.change_menu(0))
        self.inv_button = Button(self.menu_bottom_frame, text="Inventory", width=13, command=lambda: self.change_menu(1))
        self.settings_button = Button(self.menu_bottom_frame, text="Settings", width=13, command=lambda: self.change_menu(2))
        self.controls_button = Button(self.menu_bottom_frame, text="Controls", width=13, command=lambda: self.change_menu(6))
        self.menu_button.grid(row=0, column=0)
        self.inv_button.grid(row=0, column=1)
        self.settings_button.grid(row=0, column=2)
        self.controls_button.grid(row=0, column=3)
        self.menu_bottom = self.canvas.create_window(5, 230, anchor=NW, window=self.menu_bottom_frame)
        #menu specific frames
        self.menu_stats_frame = Frame(self.master, width=300, height=100)
        self.menu_stats_frame.grid_propagate(False)
        self.menu_stats_frame.grid_columnconfigure(0, weight=1)
        #self.player_label = Label(self.menu_stats_frame, text="Overlord Ako of Kaharian")
        self.player_label = Label(self.menu_stats_frame, text=self.player.player_data[1] + " " +
                                                              self.player.player_data[0] + " of " +
                                                              self.player.player_data[2] + " Kingdom")
        #self.stats_label = Label(self.menu_stats_frame, text="Health: 100\nStrength: 10\nFurthest Level: #\nCrowns: 1")
        self.stats_label = Label(self.menu_stats_frame, text="Health: " + str(self.player.player_data[3]) +
                                                             "\nStrength: " + str(self.player.player_data[4]) +
                                                             "\nFurthest Level: " + str(self.player.player_data[5]) +
                                                             "\nCrowns: " + str(self.player.player_data[6]))
        self.player_label.grid(row=0)
        self.stats_label.grid(row=1)
        #inventory specific frames
        self.inv_frame = Frame(self.master, width=300, height=150)
        self.inv_frame.grid_propagate(False)
        self.inv_frame.grid_columnconfigure(0, weight=1)
        self.inv_label = Label(self.inv_frame, text="Inventory: \nWood: " + str(self.player.inventory[0]) + "\nStone: "
                                                + str(self.player.inventory[1]) + "\nCoal: " + str(self.player.inventory[2]) +
                                                "\nAxes: " + str(self.player.inventory[5]) + "\nSwords: "
                                                    + str(self.player.inventory[4]))
        self.inv_label.grid(row=0)
        #settings specific frames
        self.settings_frame = Frame(self.master, width=300, height=150)
        self.settings_frame.grid_propagate(False)
        self.settings_frame.grid_columnconfigure(0, weight=1)
        self.name_button = Button(self.settings_frame, text="Change Your Name", command=lambda: self.change_menu(3))
        self.title_button = Button(self.settings_frame, text="Change Your Title", command=lambda: self.change_menu(4))
        self.kingdom_button = Button(self.settings_frame, text="Change Your Kingdom's Name", command=lambda: self.change_menu(5))
        self.name_button.grid(row=0)
        self.title_button.grid(row=1)
        self.kingdom_button.grid(row=2)
        #controls specific frames
        self.controls_frame = Frame(self.master, width=300, height=150)
        self.controls_frame.grid_propagate(False)
        self.controls_frame.grid_columnconfigure(0, weight=1)
        self.controls_label = Label(self.controls_frame, text="Home:\nReturn to Title = Q\nOpen Menu = X\nInteract = Z"
                                                              "\n\nExplore:\nReturn to Home = Q\nCut = V\nOpen Menu = X")
        self.controls_label.grid(column=0)
        #changing player name stuff
        self.back_b = Button(self.master, text="Go Back", command=lambda: self.change_menu(2))
        self.name_frame = Frame(self.master, width=300, height=150)
        self.name_frame.grid_propagate(False)
        self.name_frame.grid_columnconfigure(0, weight=1)
        self.entry = Entry(self.name_frame)
        self.enterB = Button(self.name_frame, text="Confirm", command=lambda: self.change_player_aspect(0, self.entry.get()))
        self.entry.grid(row=0)
        self.enterB.grid(row=1)
        # changing kingdom stuff
        self.kname_frame = Frame(self.master, width=300, height=150)
        self.kname_frame.grid_propagate(False)
        self.kname_frame.grid_columnconfigure(0, weight=1)
        self.kentry = Entry(self.kname_frame)
        self.kenterB = Button(self.kname_frame, text="Confirm",
                             command=lambda: self.change_player_aspect(2, self.kentry.get()))
        self.kentry.grid(row=0)
        self.kenterB.grid(row=1)
        #changing title stuff
        self.title_frame = Frame(self.master, width=300, height=150)
        self.title_frame.grid_propagate(False)
        self.title_frame.grid_columnconfigure(0, weight=1)
        self.king_b = Button(self.title_frame, text="King", command=lambda: self.change_player_aspect(1, "King"))
        self.queen_b = Button(self.title_frame, text="Queen", command=lambda: self.change_player_aspect(1, "Queen"))
        self.over_b = Button(self.title_frame, text="Overlord", command=lambda: self.change_player_aspect(1, "Overlord"))
        self.king_b.grid(row=0)
        self.queen_b.grid(row=1)
        self.over_b.grid(row=2)


    def change_menu(self, id):
        for x in self.frames_up:
            self.canvas.delete(x)
        if id == 0:
            self.canvas.itemconfigure(self.header, text="Menu")
            self.menu_center = self.canvas.create_window(40, 60, anchor=NW, window=self.menu_stats_frame)
            self.frames_up.append(self.menu_center)
        elif id == 1:
            self.canvas.itemconfigure(self.header, text="Inventory")
            self.inv_center = self.canvas.create_window(40, 40, anchor=NW, window=self.inv_frame)
            self.frames_up.append(self.inv_center)
        elif id == 2:
            self.canvas.itemconfigure(self.header, text="Settings")
            self.settings_center = self.canvas.create_window(40, 40, anchor=NW, window=self.settings_frame)
            self.frames_up.append(self.settings_center)
        elif id == 3:
            self.canvas.itemconfigure(self.header, text="Change Your Name")
            self.name_center = self.canvas.create_window(40, 40, anchor=NW, window=self.name_frame)
            self.back_frame = self.canvas.create_window(160, 195, anchor=NW, window=self.back_b)
            self.frames_up.append(self.back_frame)
            self.frames_up.append(self.name_center)
        elif id == 4:
            self.canvas.itemconfigure(self.header, text="Change Your Title")
            self.title_center = self.canvas.create_window(40, 40, anchor=NW, window=self.title_frame)
            self.back_frame = self.canvas.create_window(160, 195, anchor=NW, window=self.back_b)
            self.frames_up.append(self.back_frame)
            self.frames_up.append(self.title_center)
        elif id == 5:
            self.canvas.itemconfigure(self.header, text="Change Your Kingdom's Name")
            self.kname_center = self.canvas.create_window(40, 40, anchor=NW, window=self.kname_frame)
            self.back_frame = self.canvas.create_window(160, 195, anchor=NW, window=self.back_b)
            self.frames_up.append(self.back_frame)
            self.frames_up.append(self.kname_center)
        elif id == 6:
            self.canvas.itemconfigure(self.header, text="Controls")
            self.controls_center = self.canvas.create_window(40, 40, anchor=NW, window=self.controls_frame)
            self.frames_up.append(self.controls_center)


    def change_player_aspect(self, n, new):
        self.player.set_player_data(n, new)
        self.player_label.configure(text=self.player.player_data[1] + " " +
                                                              self.player.player_data[0] + " of " +
                                                              self.player.player_data[2] + " Kingdom")
        self.stats_label.configure(text="Health: " + str(self.player.player_data[3]) +
                                                             "\nStrength: " + str(self.player.player_data[4]) +
                                                             "\nFurthest Level: " + str(self.player.player_data[5]) +
                                                             "\nCrowns: " + str(self.player.player_data[6]))
        self.change_menu(2)


#all the crafting stuff
    def craft_screen(self):
        self.inv_val = 0
        self.canvas.itemconfigure(self.header, text="Craft")
        self.craft_right_frame = Frame(self.master, width=120, height=210)
        self.craft_right_frame.grid_propagate(False)
        self.craft_right_frame.grid_columnconfigure(0, weight=1)
        self.axe_button = Button(self.craft_right_frame, text="Axe", width=20, command=lambda: self.craft_change(0))
        self.sword_button = Button(self.craft_right_frame, text="Sword", width=20, command=lambda: self.craft_change(1))
        self.axe_button.grid(row=0)
        self.sword_button.grid(row=1)
        self.craft_options = self.canvas.create_window(275, 135, window=self.craft_right_frame)
        self.craft_left_frame = Frame(self.master, width=180, height=210)
        self.craft_left_frame.grid_propagate(False)
        self.craft_left_frame.grid_columnconfigure(0, weight=1)
        self.craft_left_frame.grid_rowconfigure(0, weight=1)
        self.craft_left_frame.grid_rowconfigure(1, weight=2)
        self.craft_left_frame.grid_rowconfigure(2, weight=2)
        self.craft_left_frame.grid_rowconfigure(3, weight=1)
        # array: name, description, ingredients array
        # ing. array: id, needed
        self.ingredient_id = ["Wood", "Stone", "Coal"]
        self.craft_info = [["Axe", "Used to chop down trees.", [[0, 5], [1, 3]]],
                           ["Sword", "A classic weapon.", [[0, 3], [1, 7], [2, 1]]]]
        self.current_item = Label(self.craft_left_frame)
        self.item_desc = Label(self.craft_left_frame)
        self.ingredients = Label(self.craft_left_frame)
        self.craft_button = Button(self.craft_left_frame, text="CRAFT", width=20, command=lambda: self.crafting())
        self.current_item.grid(row=0)
        self.item_desc.grid(row=1)
        self.ingredients.grid(row=2)
        self.craft_button.grid(row=3)
        self.craft_left = self.canvas.create_window(110, 135, window=self.craft_left_frame)

    def crafting(self):
        #x = [[0, 5],[1, 3]]
        if self.can_craft:
            for x in self.craft_info[self.current_id][2]:
                self.player.subtractitem(x[0], x[1])
            self.player.additem(self.inv_val, 1)
            self.craft_change(self.current_id)

    def craft_change(self, id):
        self.current_item.config(text=self.craft_info[id][0])
        self.can_craft = False
        self.checked = False
        self.current_id = id
        #axe: 5, sword:4
        if id == 0:
            self.inv_val = 5
        elif id == 1:
            self.inv_val = 4

        self.item_desc.config(text="Held: " + str(self.player.inventory[self.inv_val]) + "\n\n" + self.craft_info[id][1])
        self.ing_text = ""
        for x in self.craft_info[id][2]:
            self.ing_text += self.ingredient_id[x[0]] + ": " + str(self.player.inventory[x[0]]) + "/" + str(x[1]) + "\n"
            if self.player.inventory[x[0]] < x[1] and not self.checked:
                self.can_craft = False
                self.checked = True
            elif not self.checked:
                self.can_craft = True
        self.ingredients.config(text=self.ing_text)

#all the parchment stuff
    def parchment_screen(self):
        self.canvas.itemconfigure(self.header, text="Kingdom Report:")

    def yes_no_screen(self):
        self.yes_button = Button(self.master, text="YES")
        self.no_button = Button(self.master, text="NO")
        #self.canvas.itemconfigure(self.header, text="")


class Databanks:
    def __init__(self, type, ID):
        #[int x, int y, array script, sprite, size/2]
        #kuya, craft bench, record table, bed
        if type == "NPC":
            self.array = [[100, 100, ["Hey there.", "This is just a test script, but might as well do something fun.",
              "Uhhhh what kind of drink do you like?", "{", "{INSERT}", "I, personally, like hot cocoa."],
                           'assets/kuya_front.png', 40],
                          [400, 200, ["Time to craft!", "{CRAFT}"], 'assets/ekorre_left.png', 25],
                          [300, 200, ["There are kingdom records lying on the table", "{PARCHMENT}"],
                           'assets/ekorre_front.png', 25],
                          [150, 150, ["Rest until tomorrow?", "{SLEEP}"], 'assets/alba_front.png', 25]]
            self.object = self.array[ID]
            self.x = self.object[0]
            self.y = self.object[1]
            self.script = self.object[2]
            self.sprite = PhotoImage(file=self.object[3])
            self.size = self.object[4]
        elif type == "Player":
            #name, title, kingdom, health, attack, furthest level, crowns
            self.player_data = ["Ako", "Overlord", "Kaharian", 100, 10, 0, 1]
            #current health
            self.current_data = [100]
            #wood, stone, coal, trees, swords, axe
            self.inventory = [0, 0, 0, 0, 0, 0]

    def set_player_data(self, x, n):
        #name, title, kingdom, health
        self.player_data[x] = n

    def get_current_health(self):
        return self.current_data[0]

    def reset_health(self):
        self.current_data[0] = self.player_data[3]

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
        self.button_up = False
        self.picup = True
        self.inv = Canvas(master, width=300, height=200, bg="gray")
        self.inventoryup = False
        self.obstacles = {}
        self.script = []
        self.index = 0
        self.loadborders()
        self.movement()

    """
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
                elif self.script[self.index] == "{CRAFT}": #and not self.button_up:
                    self.open_popup(0)
                else:
                    self.label.configure(text=self.script[self.index])
            else:
                self.label_on = False
                self.script = []
                self.index = 0
                self.label.grid_forget()
                self.movement()
                
        """

    def interaction(self):
        if self.picup and not self.button_up:
            if not self.label_on:
                self.label_on = True
                self.story = Story(self.master, self.canvas, self.player, 0)
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
        self.button_up = True
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
        self.button_up = False
        self.index = 0
        for x in array:
            x.grid_forget()
        self.movement()


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
        if not (self.label_on or self.button_up):
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
        if not (self.label_on or self.button_up):
            self.leftpressed = True
            self.canvas.itemconfig(self.playersprite, image=self.pleft)
            self.facing = 3
            self.x = -5
            self.y = 0

    def right(self, event):
        if not (self.label_on or self.button_up):
            self.rightpressed = True
            self.canvas.itemconfig(self.playersprite, image=self.pright)
            self.facing = 1
            self.x = 5
            self.y = 0


    def up(self, event):
        if not (self.label_on or self.button_up):
            self.uppressed = True
            self.canvas.itemconfig(self.playersprite, image=self.pback)
            self.facing = 0
            self.x = 0
            self.y = -5

    def down(self, event):
        if not (self.label_on or self.button_up):
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
