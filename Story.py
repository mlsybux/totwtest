from tkinter import *

class Scripts:
    def __init__(self, id):
        #list of scripts
        self.archive = []
        #every dang script bc idk how else to do this
        self.archive.append(["Player: hehe check this out", "Kuya: I like the colors on this one",
                             "Dobhran: this one makes me happy but i might redo some colors",
                             "Terkun: penguiiiiiin", "Ekorre: Looks like neopolitan ice cream",
                             "Azretta: bonsai antlers lol"])
        self.archive.append(["Player: Hey, what's up?", "Player: keeeeep on rolling", "Player: i'm tired",
                             "Kuya: oh time to go"])
        self.script = self.archive[id]

class Story:
    def __init__(self, master, canvas, player, id):
        self.master = master
        self.canvas = canvas
        self.player = player
        self.script = Scripts(id).script
        self.index = -1
        self.text_on = True
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
        if self.index < len(self.script):
            if (not self.script[self.index].startswith(self.name)) and ':' in self.script[self.index]:
                self.name = self.script[self.index][:self.script[self.index].index(":") + 2]
                self.canvas.itemconfig(self.portrait, image=self.characters[self.name], state=NORMAL)
            if self.name == "Player: ":
                self.textbox.config(text=self.player.player_data[0] +
                                         self.script[self.index][self.script[self.index].index(":"):])
            else:
                self.textbox.config(text=self.script[self.index])
        else:
            self.text_on = False
            self.canvas.delete(self.portrait)
            self.textbox.grid_forget()

