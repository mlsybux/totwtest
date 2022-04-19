from tkinter import *
from sqlite3 import *


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
        self.menu_stats_frame = Frame(self.master, width=300, height=150)
        self.menu_stats_frame.grid_propagate(False)
        self.menu_stats_frame.grid_columnconfigure(0, weight=1)
        self.player_label = Label(self.menu_stats_frame, text=self.player.player_data[1] + " " +
                                                              self.player.player_data[0] + " of " +
                                                              self.player.player_data[2] + " Kingdom")
        self.stats_label = Label(self.menu_stats_frame, text="Health: " + str(self.player.player_data[3]) +
                                                             "\nStrength: " + str(self.player.player_data[4]) +
                                                             "\nFurthest Level: " + str(self.player.player_data[5]) +
                                                             "\nCrowns: " + str(self.player.player_data[6]) + "\n")
        self.save_button = Button(self.menu_stats_frame, text="Save Game", command=lambda: self.save())
        self.player_label.grid(row=0)
        self.stats_label.grid(row=1)
        self.save_button.grid(row=3)
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


    def save(self):
        self.conn = connect('totw_save.db')
        self.cur = self.conn.cursor()
        self.cur.execute("""UPDATE player SET
                name = :name,
                title = :title,
                kingdom = :kingdom,
                health = :health,
                attack = :attack,
                flevel = :flevel,
                crowns = :crowns,
                chealth = :chealth,
                wood = :wood,
                stone = :stone,
                coal = :coal,
                tree = :tree,
                sword = :sword,
                axe = :axe
                WHERE oid = 1""",
                {
                    'name': self.player.player_data[0],
                    'title': self.player.player_data[1],
                    'kingdom': self.player.player_data[2],
                    'health': self.player.player_data[3],
                    'attack': self.player.player_data[4],
                    'flevel': self.player.player_data[5],
                    'crowns': self.player.player_data[6],
                    'chealth': self.player.current_data[0],
                    'wood': self.player.inventory[0],
                    'stone': self.player.inventory[1],
                    'coal': self.player.inventory[2],
                    'tree': self.player.inventory[3],
                    'sword': self.player.inventory[4],
                    'axe': self.player.inventory[5]

                })
        #self.cur.execute("SELECT *, oid FROM player")
        self.conn.commit()
        self.conn.close()

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

class Scripts:
    def __init__(self, id):
        #dictionary of scripts. remember: key: value
        self.archive = {}
        #every dang script bc idk how else to do this
        self.archive["Kuya"] = ["Kuya: Hey there, kiddo.", "Kuya: You doing alright?"]
        self.archive["Craft"] = ["Time to make some more stuff!", "{CRAFT}"]
        self.archive["Parchment"] = ["There are records of your kingdom's activities lying on the table.",
                                     "{PARCHMENT}"]
        self.archive["Sleep"] = ["Go to sleep?", "{SLEEP}"]
        self.archive["Azretta"] = ["Player: Huh? Who is that?",
                                   "Player: She looks like a deer... is she a centaur?", "Azretta: ..?",
                                   "Azretta: Who goes there? Show yourself.", "Player: Uh, just me! Hi?",
                                   "Azretta: Why are you this deep in the forest? You are not one of the citizens.",
                                   "Azretta: Don't tell me...",
                                   "Azretta: Are you the little pest who has been terrorizing the residents of my "
                                   "forest?", "Player: Um.", "Player: Well, 'pest' is a little harsh...",
                                   "Player: Wait, 'my forest'? Are you the Queen here?",
                                   "Player: That means if I beat you, I get this forest, right?",
                                   "Azretta: Me? Queen? No, the queen is much more powerful than me.",
                                   "Azretta: But as her knight and protector of this forest, I'm afraid I can't"
                                   " allow you to pass.", "Azretta: En garde!"]
        self.archive["Ekorre"] = ["Ekorre: Hm?", "Ekorre: Hm, hm, hm? Who's this?", "Player: Uh. Hello there?",
                                  "Player: I'm--", "Ekorre: The intruder, right?",
                                  "Ekorre: Shame, shame. For you, that is.", "Ekorre: For me, it's no shame at all!",
                                  "Ekorre: It's been a while since I've had to chase someone out of my forest.",
                                  "Player: Wait, you're the queen?!", "Ekorre: The one and only! I hear you defeated my"
                                                                      " knight already, so it's time for me to kick you "
                                                                      "out myself.", "Ekorre: Try not to bore me!"]
        self.archive["Permata"] = ["Player: Kuya??", "Player: What the heck are you doing here?", "Kuya: Well...",
                                   "Kuya: The one who was supposed to be here simply hasn't been created yet.",
                                   "Kuya: So you're stuck with me.", "Player: I--", "Player: What????",
                                   "Kuya: Never mind all that, just fight me."]

        self.archive["Batu"] = ["Player: Kuya, again????", "Kuya: Yyyyyep", "Kuya: Ready to fight?", "Player: I guess?"]
        self.archive["Dobhran"] = ["Dobhran: Ooh, who are you?", "Dobhran: Who are you, who are you?",
                                   "Dobhran: Friend or enemy?", "Dobhran: Land or sea?",
                                   "Dobhran: A bit of both, maybe?", "Player: I'm here to take over the ocean!",
                                   "Player: The whole world, eventually.", "Dobhran: Ooh, sounds fun, sounds fun!",
                                   "Dobhran: But that makes you an enemy."]
        self.archive["Seileach"] = ["Player: Seriously?", "Kuya: Heyyyyy", "Player: Fine! Fine.",
                                    "Player: I know how this goes already. Let's fight."]
        self.archive["Terkun"] = ["Terkun: HONK", "Terkun: HOOONK HONK HONK", "Player: Woah that scarf looks comfy.",
                                  "Terkun: HONK HONK HONKNOHONK", "Player: uuuuuh okay? Fight it is?",
                                  "Terkun: h o n k"]
        self.archive["Nahla"] = ["Player: ughhhhhh", "Kuya: Hi!", "Player: UGGGGHHHH"]
        self.archive["Dreki"] = ["Player: Why", "Player: Just.", "Player: Why?",
                                 "Kuya: ERROR 404. Reason doesn't exist."]
        self.archive["Eldi"] = ["Player: KUYA", "Player: THIS IS THE FINAL BOSS", "Player: WHY ARE YOU HERE",
                                "Kuya: The laziness and hubris of god himself"]


        self.archive["End"] = ["Hey.", "I don't know if anyone is going to read this, but...", "Did you have fun?",
                               "...", "I guess it doesn't matter that much.", "I hope you did, though.", "After all...",
                               "Kuya: Isn't that the point of a game?", "Kuya: Though, I guess...",
                               "Kuya: The point was to take over the world, wasn't it?", "Kuya: Congrats, by the way.",
                               "Kuya: You took over the world!", "Kuya: You beat the game.", "Kuya: ...",
                               "Kuya: Yeah, I figured you wouldn't be too satisfied with this kind of ending.",
                               "Kuya: Sorry, but...", "Kuya: There isn't any more 'world' to take over.",
                               "Kuya: This is the end.",
                               "Kuya: But what's the point of a game when there isn't anything left to do?",
                               "Kuya: Just a heads up, but...",
                               "Kuya: If you really wanna hold onto this 'world', you'd better close out now.",
                               "Kuya: No?", "Kuya: Well, alright then.", "Kuya: See you back at the start!", "{END}"]

        self.script = self.archive[id]

class Story:
    def __init__(self, master, canvas, player, id):
        self.master = master
        self.canvas = canvas
        self.player = player
        self.script = Scripts(id).script
        self.index = -1
        self.text_on = True
        self.canvas.popup_up = False
        #characters dictionary
        self.characters = {}
        self.characters["Player: "] = PhotoImage(file='assets/ako_portrait.png')
        self.characters["Kuya: "] = PhotoImage(file='assets/kuya_portrait.png')
        self.characters["Ekorre: "] = PhotoImage(file='assets/ekorre_portrait.png')
        self.characters["Azretta: "] = PhotoImage(file='assets/radjur_portrait.png')
        self.characters["Dobhran: "] = PhotoImage(file='assets/dobhran_portrait.png')
        self.characters["Terkun: "] = PhotoImage(file='assets/alba_portrait.png')
        self.portrait = self.canvas.create_image(160, 150, image=self.characters["Player: "], state=HIDDEN)
        self.name = " "
        self.textbox = Label(self.master, width=80, height=4)
        self.textbox.grid(row=4, column=0, columnspan=5)
        self.continue_text()

    def continue_text(self):
        self.index += 1
        if self.index < len(self.script) and not self.canvas.popup_up:
            if (not self.script[self.index].startswith(self.name)) and ':' in self.script[self.index]:
                self.name = self.script[self.index][:self.script[self.index].index(":") + 2]
                self.canvas.itemconfig(self.portrait, image=self.characters[self.name], state=NORMAL)
            elif not ': ' in self.script[self.index]:
                self.canvas.itemconfig(self.portrait, state=HIDDEN)
            if self.script[self.index] == "{CRAFT}":
                self.open_popup(0)
            elif self.script[self.index] == "{PARCHMENT}":
                self.open_popup(2)
            elif self.script[self.index] == "{SLEEP}":
                self.open_popup(3)
            elif self.script[self.index] == "{END}":
                self.reset()
                return
            if self.name == "Player: ":
                self.textbox.config(text=self.player.player_data[0] +
                                         self.script[self.index][self.script[self.index].index(":"):])
            else:
                self.textbox.config(text=self.script[self.index])
        else:
            self.text_on = False
            self.canvas.delete(self.portrait)
            self.textbox.grid_forget()


    def open_popup(self, id):
        self.text_on = False
        self.canvas.popup_up = True
        self.textbox.grid_forget()
        self.popup = Popups(self.master, id, self.player)
        self.exitB = Button(self.master, text="X",
                            command=lambda: self.close_popup([self.popup.canvas, self.exitB]))
        self.exitB.grid(row=1, column=3, sticky=NE)

    def close_popup(self, array):
        self.label_on = False
        self.canvas.popup_up = False
        self.index = 0
        for x in array:
            x.grid_forget()

    def reset(self):
        self.conn = connect('totw_save.db')
        self.cur = self.conn.cursor()
        self.cur.execute("""UPDATE player SET
                    name = :name,
                    title = :title,
                    kingdom = :kingdom,
                    health = :health,
                    attack = :attack,
                    flevel = :flevel,
                    crowns = :crowns,
                    wood = :wood,
                    stone = :stone,
                    coal = :coal,
                    tree = :tree,
                    sword = :sword,
                    axe = :axe                   
                    WHERE oid = 1""",
                    {
                        'name': self.player.player_data[0],
                        'title': self.player.player_data[1],
                        'kingdom': self.player.player_data[2],
                        'health': 300,
                        'attack': 10,
                        'flevel': 0,
                        'crowns': 0,
                        'wood': 0, 'stone': 0, 'coal': 0, 'tree': 0, 'sword': 0, 'axe': 0
                    })
        self.cur.execute("SELECT *, oid FROM player")
        self.conn.commit()
        self.conn.close()
        self.master.destroy()
