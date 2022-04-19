from tkinter import *
from random import *
from Home import *
from Story import *


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
        #pcoords is the player coordinates in a list, given [x, y, direction]
        self.pcoords = [290, 350, 0]
        #Type, Max Health, Attack
        self.bestiarylist = [["Slime", 50, 1], ["Slime King", 150, 3]]
        for x in self.bestiarylist:
            if self.type == x[0]:
                self.attack = x[2]
                self.health, self.maxhealth = x[1], x[1]
        self.healthbarexists = False
        self.sprite = self.randomsprite()
        self.alive = True
        self.bouncing = False
        self.b_count = 0
        self.direction = 0
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
        if self.alive:
            self.direction = self.pcoords[2]
            self.bouncing = True


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
            self.differenceX = 0
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

        if self.bouncing:
            if self.b_count <= 3:
                self.b_count += 1
                if self.direction == 0:
                    self.x = 0
                    self.y = -10
                elif self.direction == 1:
                    self.x = 10
                    self.y = 0
                elif self.direction == 2:
                    self.x = 0
                    self.y = 10
                elif self.direction == 3:
                    self.x = -10
                    self.y = 0
            else:
                self.bouncing = False
                self.b_count = 0

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

    def getplayercoords(self, px, py, pd):
        self.pcoords[0] = px
        self.pcoords[1] = py
        self.pcoords[2] = pd


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
        else:
            self.canvas.enemies_alive -= 1


class Boss:
    def __init__(self, master, canvas, player, id, obs):
        self.master = master
        self.canvas = canvas
        self.player = player
        self.obstacles = obs
        # pcoords is the player coordinates in a list, given [x, y, direction]
        self.pcoords = [290, 350, 0]
        #self.bosses = ["Azretta", "Ekorre", "Permata", "Batu", "Dobhran", "Seileach", "Terkun", "Nahla",
                       #"Dreki", "Eldi"]
        #name, health, attack, size/2
        self.bosses = [["Azretta", 150, 3, 40], ["Ekorre", 175, 4, 25], ["Permata", 150, 3, 60], ["Batu", 150, 3, 40],
                       ["Dobhran", 150, 3, 25], ["Seileach", 150, 3, 40], ["Terkun", 150, 3, 25], ["Nahla", 150, 3, 40],
                       ["Dreki", 150, 3, 60], ["Eldi", 150, 3, 60]]

        self.name = self.bosses[id][0]
        self.health, self.maxhealth = self.bosses[id][1], self.bosses[id][1]
        self.attack = self.bosses[id][2]
        self.size = self.bosses[id][3]
        self.sprite_set = [['assets/radjur_front.png', 'assets/radjur_left.png', 'assets/radjur_back.png',
                            'assets/radjur_right.png'], #azretta
                           ['assets/ekorre_front.png', 'assets/ekorre_left.png', 'assets/ekorre_back.png',
                            'assets/ekorre_right.png'], #ekorre
                           ['assets/kuya_front.png', 'assets/kuya_left.png', 'assets/kuya_back.png',
                            'assets/kuya_right.png'], #permata
                           ['assets/kuya_front.png', 'assets/kuya_left.png', 'assets/kuya_back.png',
                            'assets/kuya_right.png'], #batu
                           ['assets/dobhran_front.png', 'assets/dobhran_left.png', 'assets/dobhran_back.png',
                            'assets/dobhran_right.png'], #dobhran
                           ['assets/kuya_front.png', 'assets/kuya_left.png', 'assets/kuya_back.png',
                            'assets/kuya_right.png'], #seileach
                           ['assets/alba_front.png', 'assets/alba_left.png', 'assets/alba_back.png',
                            'assets/alba_right.png'], #terkun
                           ['assets/kuya_front.png', 'assets/kuya_left.png', 'assets/kuya_back.png',
                            'assets/kuya_right.png'], #nahla
                           ['assets/kuya_front.png', 'assets/kuya_left.png', 'assets/kuya_back.png',
                            'assets/kuya_right.png'], #dreki
                           ['assets/kuya_front.png', 'assets/kuya_left.png', 'assets/kuya_back.png',
                            'assets/kuya_right.png']] #eldi
        self.front = PhotoImage(file=self.sprite_set[id][0])
        self.left = PhotoImage(file=self.sprite_set[id][1])
        self.back = PhotoImage(file=self.sprite_set[id][2])
        self.right = PhotoImage(file=self.sprite_set[id][3])
        self.directions = [self.back, self.right, self.front, self.left]
        #0=back, 1=right, 2=front, 3=left
        self.facing = 2
        self.current_facing = 2
        self.x = 0
        self.y = 0
        self.sprite = self.canvas.create_image(300, 100, image=self.front)
        self.canvas.bosswin = False
        self.alive = True
        self.bouncing = False
        self.b_count = 0
        self.direction = 0
        self.differenceX = 0
        self.differenceY = 0
        self.currentx1 = 300 - self.size
        self.currenty1 = 100 - self.size
        self.currentx2 = 300 + self.size
        self.currenty2 = 100 + self.size
        self.healthbar()
        self.cutscene_over = False
        self.label_on = False
        #self.move()
        self.cutscene()

    def cutscene(self):
        if not self.cutscene_over:
            if not self.label_on:
                self.label_on = True
                self.story = Story(self.master, self.canvas, self.player, self.name)
            elif self.story.text_on:
                self.story.continue_text()
                if not self.story.text_on:
                    self.label_on = False
                    self.cutscene_over = True
                    self.move()
            else:
                self.label_on = False
                self.cutscene_over = True
                self.move()

    def healthbar(self):
        self.healthbarexists = True
        self.emptyhealthbar = self.canvas.create_rectangle(20, 365, 180, 385, fill="white")
        self.fullhealthbar = self.canvas.create_rectangle(20, 365, (self.health / self.maxhealth) * 160 + 20, 385,
                                                          fill="dark red")

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
        if self.alive:
            self.direction = self.pcoords[2]
            self.bouncing = True

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
        if self.canvas.coords(self.sprite)[0]-2 > self.pcoords[0]:
            self.differenceX = self.canvas.coords(self.sprite)[0] - self.pcoords[0]
            self.x = -2
        elif self.canvas.coords(self.sprite)[0]+2 < self.pcoords[0]:
            self.differenceX = self.pcoords[0] - self.canvas.coords(self.sprite)[0]
            self.x = 2
        else:
            self.differenceX = 0
            self.x = 0
        if self.canvas.coords(self.sprite)[1]-2 > self.pcoords[1]:
            self.differenceY = self.canvas.coords(self.sprite)[1]-2 - self.pcoords[1]
            self.y = -2
        elif self.canvas.coords(self.sprite)[1]+2 < self.pcoords[1]:
            self.differenceY = self.pcoords[1] - self.canvas.coords(self.sprite)[1]+2
            self.y = 2
        else:
            self.differenceY = 0
            self.y = 0
        if self.differenceX > self.differenceY:
            self.y = 0
        else:
            self.x = 0

        if self.x < 0:
            self.change_direction(3)
        elif self.x > 0:
            self.change_direction(1)
        elif self.y < 0:
            self.change_direction(0)
        elif self.y > 0:
            self.change_direction(2)

        if self.bouncing:
            if self.b_count <= 3:
                self.b_count += 1
                if self.direction == 0:
                    self.x = 0
                    self.y = -10
                elif self.direction == 1:
                    self.x = 10
                    self.y = 0
                elif self.direction == 2:
                    self.x = 0
                    self.y = 10
                elif self.direction == 3:
                    self.x = -10
                    self.y = 0
            else:
                self.bouncing = False
                self.b_count = 0

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

        #if not self.facing == self.current_facing:
          #  self.change_direction(self.facing)
        # sets the current coords to whatever the new coords are
        self.currentx1 = self.canvas.coords(self.sprite)[0] - self.size + 10
        self.currenty1 = self.canvas.coords(self.sprite)[1] - self.size + 10
        self.currentx2 = self.canvas.coords(self.sprite)[0] + self.size - 10
        self.currenty2 = self.canvas.coords(self.sprite)[1] + self.size - 10

        self.canvas.after(70, self.move)

    def getsprite(self):
        return self.sprite

    def getattack(self):
        return self.attack

    def getid(self):
        return self.name

    def gettype(self):
        return "Boss"

    def getplayercoords(self, px, py, pd):
        self.pcoords[0] = px
        self.pcoords[1] = py
        self.pcoords[2] = pd

    def change_direction(self, dir):
        self.current_facing = dir
        self.canvas.itemconfig(self.sprite, image=self.directions[dir])

    def defeat(self):
        self.player.set_player_data(6, self.player.player_data[6] + 1)
        self.alive = False
        self.canvas.delete(self.sprite)
        self.canvas.bosswin = True
        self.canvas.enemies_alive -= 1


class Items:
    def __init__(self, master, l, player):
        #Tk
        self.master = master
        self.player = player
        #x and y are the movement
        self.x = 0
        self.y = 0
        self.level = l
        if self.level <= 20:
            self.environment = "Forest"
            self.color1 = "DarkOliveGreen3"
            self.color2 = "forest green"
        elif self.level <= 40:
            self.environment = "Cave"
            self.color1 = "gray16"
            self.color2 = "gray50"
        elif self.level <= 60:
            self.environment = "Ocean"
            self.color1 = "cyan3"
            self.color2 = "DodgerBlue4"
        elif self.level <= 80:
            self.environment = "Tundra"
            self.color1 = "snow2"
            self.color2 = "slate gray"
        elif self.level <= 100:
            self.environment = "Volcano"
            self.color1 = "firebrick3"
            self.color2 = "brown4"
        if self.level % 10 == 0:
            self.environment = "Boss Fight"
        if self.level >= 101:
            self.environment = "End"
            self.color1 = "snow1"
            self.color2 = "snow3"
        self.cutscene_over = True
        #just saying that all the keys are released by default
        self.leftpressed = False
        self.rightpressed = False
        self.uppressed = False
        self.downpressed = False
        #0 = front, 1 = right, 2 = down, 3 = left
        self.facing = 0
        #this is the canvas NOT THE TK
        self.canvas = Canvas(master, width=600, height=400, bg=self.color1)
        #the player's sprite and its coordinates :)
        self.psprite = PhotoImage(file='assets/ako_front.png')
        self.pback = PhotoImage(file='assets/ako_back.png')
        self.pleft = PhotoImage(file='assets/ako_left.png')
        self.pright = PhotoImage(file='assets/ako_right.png')
        self.playersprite = self.canvas.create_image(290, 350, image=self.pback)
        self.currentx1 = self.canvas.coords(self.playersprite)[0] - 25
        self.currenty1 = self.canvas.coords(self.playersprite)[1] - 25
        self.currentx2 = self.currentx1 + 50
        self.currenty2 = self.currenty1 + 50
        self.bladebool = False
        self.hit_list = []
        self.canvas.bosswin = False
        self.canvas.enemies_alive = 0
        self.boss_checked = False
        self.ending = False
        self.inventoryup = False
        self.canvas.grid(row=0, column=0, rowspan=5, columnspan=5)
        self.resources = {}
        self.obstacles = {}
        self.enemies = {}
        self.dictionaries = [self.resources, self.obstacles, self.enemies]
        self.stack = []
        self.loadborders()
        self.level_text = self.canvas.create_text(50, 10, text="Stage Level: " + str(self.level), fill="white")
        if self.environment == "Forest":
            if self.level <= 3:
                self.spawnitems([5, 3, 2, 2])
                self.loadenemies(1)
            elif 5 > self.level > 3:
                self.spawnitems([3, 5, 4, 1])
                self.loadenemies(1)
            elif self.level >= 5:
                self.spawnitems([3, 3, 3, 3])
                self.loadenemies(2)
        elif self.environment == "Cave":
            self.spawnitems([0, 6, 5, 0])
            self.loadenemies(1)
        elif self.environment.startswith("Boss Fight"):
            #self.boss = self.bosses[self.environment[:]]
            self.bossfight()
        elif self.environment == "End":
            self.ending = True
            self.cutscene_over = False
            self.end_cutscene()



        self.emptyhealthbar = self.canvas.create_rectangle(420, 365, 580, 385, fill="white")
        self.fullhealthbar = self.canvas.create_rectangle(420, 365, (self.player.current_data[0] /
                                                                     self.player.player_data[3]) * 160 + 420, 385,
                                                          fill="red")
        self.movement()

    def getbosswin(self):
        return self.canvas.bosswin

    def loadborders(self):
        self.leftborder = self.canvas.create_rectangle(0, 0, 17, 400, fill=self.color2)
        self.rightborder = self.canvas.create_rectangle(583, 0, 600, 400, fill=self.color2)

        self.lowerborderL = self.canvas.create_rectangle(0, 353, 200, 400, fill=self.color2)
        self.lowerborderR = self.canvas.create_rectangle(400, 353, 600, 400, fill=self.color2)
        self.upperborder = self.canvas.create_rectangle(0, 0, 600, 20, fill=self.color2)
        self.obstacles["UpperBorder"] = self.upperborder

        self.obstacles["LeftBorder"] = self.leftborder
        self.obstacles["RightBorder"] = self.rightborder
        self.obstacles["LowerBorderL"] = self.lowerborderL
        self.obstacles["LowerBorderR"] = self.lowerborderR

    def bossfight(self):
        self.cutscene_over = False
        self.boss = Boss(self.master, self.canvas, self.player, (int)(self.level/10)-1, self.obstacles)
        self.stack.append(self.boss)
        self.enemies[self.boss.getid()] = self.boss.getsprite()
        self.canvas.enemies_alive += 1

    def end_cutscene(self):
        self.story = Story(self.master, self.canvas, self.player, "End")

    def interaction(self):
        if not self.cutscene_over:
            if self.ending:
                if self.story.text_on:
                    self.story.continue_text()
                    if not self.story.text_on:
                        #self.label_on = False
                        self.cutscene_over = True
                else:
                    #self.label_on = False
                    self.cutscene_over = True
            else:
                self.boss.cutscene()
                self.cutscene_over = self.boss.cutscene_over


    def loadenemies(self, a):
        self.acounter = 0
        while self.acounter < a:
            self.enemy = Bestiary(self.canvas, "Slime", "Slime" + str(self.acounter), self.obstacles)
            self.stack.append(self.enemy)
            self.enemies["Slime" + str(self.acounter)] = self.enemy.getsprite()
            self.acounter = self.acounter + 1
            self.canvas.enemies_alive += 1

    #changes the player's health
    def changehealth(self, change):
        self.player.change_current_health(change)
        self.canvas.coords(self.fullhealthbar, 420, 365,
                           (self.player.current_data[0] / self.player.player_data[3]) * 160 + 420, 385)
        if self.player.current_data[0] <= 0:
            self.back()


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

        for x in self.overlaps(self.canvas.coords(self.blade)[0], self.canvas.coords(self.blade)[1],
                               self.canvas.coords(self.blade)[2], self.canvas.coords(self.blade)[3]):
            for a in self.stack:
                if a.gettype() == "Tree" and a.getid() == x and self.player.inventory[5] >= 1:
                    self.player.additem(0, 5)
                    self.player.subtractitem(5, 1)
                    a.removesprite()
                elif a.gettype() == "Slime" and a.getid() == x:
                    if not a in self.hit_list:
                        self.hit_list.append(a)
                        a.damage(self.player.player_data[4])
                elif a.gettype() == "Boss" and a.getid() == x:
                    if not a in self.hit_list:
                        self.hit_list.append(a)
                        a.damage(self.player.player_data[4])

        if (self.facing == 2 and self.bx1 <= self.currentx1+15) or (self.facing == 0 and self.bx2 >= self.currentx2-15)\
                or (self.facing == 3 and self.by1 <= self.currenty1+15) or (self.facing == 1 and self.by2 >= self.currenty2-15):
            self.bx = 0
            self.by = 0
            self.canvas.delete(self.blade)
            self.bladebool = False
            self.hit_list = []
            return
        self.canvas.move(self.blade, self.bx, self.by)
        if (self.canvas.bosswin or self.canvas.enemies_alive == 0) and not self.boss_checked:
            self.boss_checked = True
            self.canvas.delete(self.upperborder)
            self.upperborderL = self.canvas.create_rectangle(0, 0, 255, 20, fill=self.color2)
            self.upperborderR = self.canvas.create_rectangle(340, 0, 600, 20, fill=self.color2)
            self.obstacles["UpperBorderL"] = self.upperborderL
            self.obstacles["UpperBorderR"] = self.upperborderR
            self.canvas.lift(self.level_text)
        self.canvas.after(70, self.swingblade)

    def cuttree(self):
        if not self.bladebool:
            if self.facing == 0:
                self.blade = self.canvas.create_rectangle(self.currentx1+5, self.currenty1 - 25, self.currentx1 + 10, self.currenty1)
            elif self.facing == 1:
                self.blade = self.canvas.create_rectangle(self.currentx2, self.currenty1+5, self.currentx2 + 25, self.currenty1 + 10)
            elif self.facing == 2:
                self.blade = self.canvas.create_rectangle(self.currentx2-10, self.currenty2, self.currentx2-5, self.currenty2+25)
            else:
                self.blade = self.canvas.create_rectangle(self.currentx1-25, self.currenty2 - 10, self.currentx1, self.currenty2-5)

            self.swingblade()


    def overlaps(self, x1, y1, x2, y2):
        self.overlap_list = []
        self.c_object = self.canvas.find_overlapping(x1, y1, x2, y2)
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


    def hasobstacle(self, x1, y1, x2, y2):
        self.c_object = self.canvas.find_overlapping(x1, y1, x2, y2)
        for k, v in self.obstacles.items():  # iterates over obstacles dict
            if v in self.c_object:
                return True
        return False

    def movement(self):
        if not self.inventoryup:
            if self.cutscene_over:
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
                self.currentx1 = self.canvas.coords(self.playersprite)[0] - 25
                self.currenty1 = self.canvas.coords(self.playersprite)[1] - 25
                self.currentx2 = self.currentx1 + 50
                self.currenty2 = self.currenty1 + 50

                #let enemies know where player is
                for x in self.stack:
                    if x.gettype() == "Slime" or x.gettype() == "Boss":
                        x.getplayercoords(self.canvas.coords(self.playersprite)[0],
                                          self.canvas.coords(self.playersprite)[1], self.facing)

                #gets the list of whatever it's overlapping, then iterates through it to either get it or get hurt
                self.o_list = self.overlaps(self.currentx1, self.currenty1, self.currentx2, self.currenty2)
                for x in self.o_list:
                    for a in self.stack:
                        if a.getid() == x and x in self.resources:
                            if a.gettype() == "Wood":
                                self.player.additem(0, 3)
                            elif a.gettype() == "Stone":
                                self.player.additem(1, 3)
                            elif a.gettype() == "Coal":
                                self.player.additem(2, 2)
                            a.removesprite()
                        elif a.getid() == x and x in self.enemies:
                            if a.gettype() == "Slime" or a.gettype() == "Boss":
                                self.changehealth(-a.getattack())
            #after 70 ticks, it calls itself again
            self.canvas.after(70, self.movement)

    # navigation
    def back(self):
        self.canvas.grid_forget()

    def left(self, event):
        if not self.bladebool and self.cutscene_over:
            self.leftpressed = True
            self.canvas.itemconfig(self.playersprite, image=self.pleft)
            self.facing = 3
            self.x = -5
            self.y = 0

    def right(self, event):
        if not self.bladebool and self.cutscene_over:
            self.rightpressed = True
            self.canvas.itemconfig(self.playersprite, image=self.pright)
            self.facing = 1
            self.x = 5
            self.y = 0

    def up(self, event):
        if not self.bladebool and self.cutscene_over:
            self.uppressed = True
            self.canvas.itemconfig(self.playersprite, image=self.pback)
            self.facing = 0
            self.x = 0
            self.y = -5

    def down(self, event):
        if not self.bladebool and self.cutscene_over:
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