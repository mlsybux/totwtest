from tkinter import *
from Items import *
from Home import *
from Morgan import *

root = Tk()
root.title("Take Over The World!!")
root.iconphoto(False, PhotoImage(file='assets/ako_portrait.png'))
#root.geometry("1200x800")
root.geometry("600x400")
root.grid_propagate(False)

ind = 0
player = Databanks("Player", 0)
#wood, stone, coal, trees, swords, axes
#playerInventory = [10, 10, 10, 0, 10, 50]
player.loadinventory([15, 9, 0, 0, 0, 50])
stats = 100
chosen_envi = "Forest"
unlockedstages = 1
stagelevels = 0

higheststagelevel = 0
newhighestcutscene = 0

testscript = ["Hello there.", "What's your name?", "ENTERNAME", "That's a nice name.", "What title will you go by?",
              "ENTERTITLE", "Lovely title.", "What about your kingdom?", "ENTERKINGDOM", "Lovely.",
              "Thank you for your responses.", "REPEAT"]
script = ["There are so many kingdoms…", "Full of so many types of people.", "Scientists, soldiers, artists, bakers…",
          "How can anyone choose to be just one thing like that?", "How can anyone choose just one kingdom?",
          "Not that that matters to me.", "Because I’m gonna rule them all!",
          "Who needs to know how to cook when you’ve got a royal chef? Or fight if you’ve got your own army?",
          "I don't need any of that if I'm the ruler!", "My name is...", "ENTERNAME", "And I'm gonna be...",
          "ENTERTITLE",  "of the whole wide world!", "...eventually, at least.",
          "For now, I've just got my humble kingdom of...", "ENTERKINGDOM",
          "But hey, {playerTitle} {playerName} of {playerKingdom} Kingdom sounds pretty cool, doesn't it?", "REPEAT",
          "???::Heh, {playerTitle}, huh? You're gonna need a few more people before you can call {playerKingdom} a "
          "proper kingdom", "Player::Well, duh! But it's a start, don't you think, Kuya?",
          "Kuya::Sure, kiddo. Just don't try taking over the Coven or anything when all {playerKingdom}’s got is a "
          "couple sticks and stones.",
          "Player::T-That’s not all we have! We have manpower, that’s the most important thing about "
          "kingdoms-- the citizens!", "Kuya::Yep. {playerKingdom} Kingdom: population of two.",
          "Player::Twoooo very amazing individuals with lots of talent and grit?",
          "Kuya::Heh. Yeah, a start indeed. Well, no kingdom’s going to build itself. Why don’t you go get resources "
          "to get this ball rolling?"]
tscript = ["Kuya::Hey, what's up?",
           "Player::Not much, actually. I'm not really sure what I'm supposed to be doing right now.",
           "Kuya::Yeahhh, this place is a work in progress. For now, how about you keep on making axes? "
           "Those'll be helpful soon.", "Player::Okay? I guess?",
           "Player::But, um, can we go back to the 'work in progress' thing? What does that mean?",
           "Kuya::Haha. It's not that important, don't worry."]
escript = ["Player::Huh, this is the farthest out I've ever been... ", "Player::Hm? What's that over there?",
           "Player::Woah! A cave system! Looks like it runs pretty deep.",
           "Player::Hmm, maybe I'll come back and explore here next time!", "Area: Cave Unlocked!", "EXPLORE"]
escript2 = ["Player::I'm out pretty far now, huh?", "Player::Hey, wait, isn't that...", "Player::Kuya?",
            "Kuya::Hm? Oh hey kiddo, what're you doing all the way out here?",
            "Player::Just exploring. Hey, what's that behind you?", "Kuya::Oh, just the Slime King's cave",
            "Player::T-", "Player::The what?", "Kuya::Oh, you know, big slime boss, kill it and you're essentially the"
                                               " biggest threat around these parts.",
            "Player:: What???", "Player::Wait, so, if I kill it, I'm basically conquering this forest?",
            "Kuya::Mmmmyeah.", "Player::Cool! Lemme go fight it right now--","Kuya::Nnnnonononono, hold on.",
            "Player::What now?", "Kuya::Your arms are literally full of materials and you look exhausted. "
                                 "Why don't you go back to the camp and drop those off?", "Kuya::Oh, and...",
            "Player::?", "Kuya::It'll probably be easier if we both take it down, yeah? Make me some swords and I "
                         "can beat it down enough for you to finish it!", "Player::Really? Cool! Heck yeah,"
                                                                          "let's kill that Slime King!",
            "Area: Slime King's Cave Unlocked!", "EXPLORE"]
bossscript1 = ["Player::We're almost to the end!",
               "Kuya::I'll use the {s} swords we have to knock the Slime King back! You go finish it off!",
               "Player::Got it!", "BOSS"]
bossscript2 = ["Player::We're almost to the end!", "Player::There's the Slime King! Time to finish him!", "BOSS"]
winscript = ["Player::Whoa! We did it!!", "Player::Does-- does that mean I'm {playerTitle} of this cave now?",
             "Kuya::Heck yeah you are.", "Player::Sweet!! Now I can keep--", "Kuya::Now you can wait until the next"
                                                                             " update",
             "Player::Wait, what's that supposed to mean--"]

titleChoices = ["TITLES", "King", "Queen", "Overlord"]
repeatChoices = ["YESNO", "Sounds good!", "No, something's off...", "Repeater"]

playerName = "Ako"
playerKingdom = "Kaharian"
playerTitle = "Overlord"
#boolean to make sure that functions don't get called multiple times before keys can be unbound
stopkeys = False

#the function to clear the old screen and call the new
def changescreen(arr, new):
    global nameon, stagelevels, chosen_envi, unlockedstages
    nameon = False
    for x in arr[0]:
        root.grid_rowconfigure(x, weight=0)
    for x in arr[1]:
        root.grid_columnconfigure(x, weight=0)
    for x in arr[2]:
        x.grid_forget()
    if new == "Title":
        title()
    elif new == "Credits":
        credits()
    elif new == "Home":
        home()
    elif new == "Castle":
        castle()
    elif new == "Explore":
        gameover()
        explore()
        #stagelevels = 0
        #e_options()

    elif new == "Explore Continue":
        explore()
    elif new == "Explore Forest":
        chosen_envi = "Forest"
        stagelevels = 0
        explore()
    elif new == "Explore Cave":
        chosen_envi = "Cave"
        stagelevels = 0
        explore()
    elif new == "Boss Text":
        if player.inventory[4] > 0:
            displaytext(bossscript1)
        else:
            displaytext(bossscript2)
    elif new == "Boss Fight":
        chosen_envi = "Boss Fight"
        stagelevels = 0
        explore()
    elif new == "Win":
        displaytext(winscript)
    elif new == "Opening Cutscene":
        displaytext(script)
    elif new == "Talk":
        displaytext(tscript)
    elif new == "ETalk":
        unlockedstages = 2
        displaytext(escript)
    elif new == "ETalk2":
        unlockedstages = 3
        displaytext(escript2)
    elif new == "Set Name":
        enterchoice("Name")
    elif new == "Set Title":
        make3choice(titleChoices)
    elif new == "Set Kingdom":
        enterchoice("Kingdom")
    elif new == "":
        pass
    else:
        print("This has not been made in yet!")

#functions for making choices with buttons/entries for the screens to call on
def setchoice(a, t):
    global playerTitle, currentArray, b1, b2, b3, ind, player

    if a[0] == "TITLES":
        #playerTitle = t
        player.set_player_data(1, t)
        if ind == 0:
            changescreen([[], [], [b1, b2, b3]], "Menu")
        else:
            changescreen([[], [], [b1, b2, b3]], "")
            buttonclicked(currentArray)
            displaytext(currentArray)
    elif a[0] == "YESNO":
        changescreen([[], [], [b1, b2]], "")
        if t == "Y":
            setynchoice(a, True)
        elif t == "N":
            setynchoice(a, False)


def setynchoice(a, b):
    global currentArray, ind, textbox
    if a[3] == "Repeater":
        if b == True:
            displaytext(currentArray)
            buttonclicked(currentArray)
        else:
            displaytext(currentArray)
            textbox.config(text=lineprocess("Oops, I misspoke. I'm actually..."))
            ind = (currentArray.index("ENTERNAME"))-1


def make2choice(a):
    global b1
    global b2
    b1=Button(root, text=a[1], command=lambda: setchoice(a, "Y"))
    b2=Button(root, text=a[2], command=lambda: setchoice(a, "N"))
    b1.grid(row=2, column=0)
    b2.grid(row=2, column=1)


def make3choice(a):
    global b1
    global b2
    global b3
    b1 = Button(root, text=a[1], command=lambda: setchoice(a, a[1]))
    b2 = Button(root, text=a[2], command=lambda: setchoice(a, a[2]))
    b3 = Button(root, text=a[3], command=lambda: setchoice(a, a[3]))
    b1.grid(row=1, column=0)
    b2.grid(row=1, column=1)
    b3.grid(row=1, column=2)

    # THE ENTRY FUNCTIONS


def setplayername(t):
    global userEnter
    global enterB
    global playerName, player
    global currentArray
    if not t == "":
        player.set_player_data(0, t)
        #playerName = t
    if not ind == 0:
        changescreen([[], [], [userEnter, enterB]], "")
        displaytext(currentArray)
        buttonclicked(currentArray)
    else:
        changescreen([[], [], [userEnter, enterB]], "Menu")


def setkingdomname(t):
    global userEnter
    global enterB
    global playerKingdom
    global currentArray
    if not t == "":
        #playerKingdom = t
        player.set_player_data(2, t)
    if not ind == 0:
        changescreen([[], [], [userEnter, enterB]], "")
        displaytext(currentArray)
        buttonclicked(currentArray)
    else:
        changescreen([[], [], [userEnter, enterB]], "Menu")


def enterchoice(x):
    global userEnter
    global enterB
    userEnter = Entry(root)
    if x == "Name":
        enterB = Button(root, text="Enter Your Name", command=lambda: setplayername(userEnter.get()))
    elif x == "Kingdom":
        enterB = Button(root, text="Enter Kingdom Name", command=lambda: setkingdomname(userEnter.get()))
    userEnter.grid(row=0, column=0)
    enterB.grid(row=1, column=0)

    # THE BASE FUNCTIONS


def lineprocess(text):
    global namebox, player
    global nameon
    if '::' in text:
        if not nameon:
            nameon = True
            namebox.grid(row=0, column=0)
        cind = text.index('::')
        namebox.config(text=text[:cind])
        if text[:cind] == "Player":
            namebox.config(text=player.player_data[0])
        proText = text[cind+2:]
    else:
        if nameon:
            nameon = False
            namebox.grid_forget()
        proText = text
    proText = proText.replace("{playerName}", player.player_data[0])
    proText = proText.replace("{playerTitle}", player.player_data[1])
    proText = proText.replace("{playerKingdom}", player.player_data[2])
    proText = proText.replace("{s}", str(player.inventory[4]))
    proText = linebreaker(proText)
    return proText


def linebreaker(text):
    initI = 45
    breakerI = initI
    tempI = 0
    if len(text) > initI:
        for x in text:
            tempI += 1
            if (x == " ") and tempI <= initI:
                breakerI = tempI
        substringA = text[:breakerI]
        substringB = text[breakerI:]
        if len(substringB) >= initI:
            substringB = linebreaker(substringB)
        newtext = substringA + "\n" + substringB
    else:
        newtext = text
    return newtext


def buttonclicked(a):
    global textbox, ind, advButton, namebox
    thisarr = [[], [], [textbox, namebox, advButton]]
    if ind + 1 < len(a):
        ind = ind + 1
        if a[ind] == "ENTERTITLE":
            changescreen(thisarr, "")
            make3choice(titleChoices)
        elif a[ind] == "ENTERNAME":
            changescreen(thisarr, "")
            enterchoice("Name")
        elif a[ind] == "ENTERKINGDOM":
            changescreen(thisarr, "")
            enterchoice("Kingdom")
        elif a[ind] == "REPEAT":
            changescreen(thisarr, "")
            make2choice(repeatChoices)
        elif a[ind] == "BOSS":
            ind = 0
            changescreen(thisarr, "Boss Fight")
        elif a[ind] == "EXPLORE":
            ind = 0
            changescreen(thisarr, "Explore")
        else:
            textbox.config(text=lineprocess(currentArray[ind]))
    else:
        ind = 0
        changescreen(thisarr, "Home")


def displayname(t):
    global namebox
    namebox.config(text=t)


def displaytext(a):
    global textbox, namebox, nameon, advButton, ind, currentArray
    currentArray = a
    namebox = Label(root, text="", width=20, height=1, anchor=NW, justify=LEFT, relief=RIDGE)
    #namebox.grid(row=0, column=0)
    textbox = Label(root, text=lineprocess(currentArray[ind]), width=40, height=4, anchor=NW, justify=LEFT,
                    relief=RIDGE)
    textbox.grid(row=1, column=0)
    advButton = Button(root, text=">", command=lambda: buttonclicked(currentArray))
    advButton.grid(row=2, column=0)


#all the different GUIs
def title():
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(4, weight=1)

    titleCard = Label(root, text = "Take Over\nThe\nWorld!!", font = ("Arial", 20), pady=25)
    newGameButton = Button(root, text="New Game", borderwidth = 3, command=lambda: changescreen(thisArray,
                                                                                                "Opening Cutscene"))
    loadGameButton = Button(root, text="Load Game", borderwidth = 3, command=lambda: changescreen(thisArray, "Home"))
    creditsButton = Button(root, text="Credits", borderwidth=3, command=lambda: changescreen(thisArray, "Credits"))

    titleCard.grid(row=0, column=2)
    newGameButton.grid(row=2, column=1)
    loadGameButton.grid(row=2, column=2)
    creditsButton.grid(row=2, column=3)

    thisArray= [[],
                [0,4],
                [newGameButton, loadGameButton, creditsButton, titleCard]]

def credits():
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(4, weight=1)
    creditHead = Label(root, text="This Thing Was Made By:", font = ("Comic Sans", 20), pady=20)
    backButton = Button(root, text="Back", command=lambda: changescreen(thisArray, "Title"))
    l1 = Label(root, text = "Jadzia, a cool dude\nMorgan, the cooler one\n\nAND WITH THE HELP OF:\n\nUMW Ladies:"
                            "\nSarah & Bella\n\n(and mr arnold i guess)\n")

    creditHead.grid(row=0, column=1)
    l1.grid(row=1, column=1)
    backButton.grid(row=4, column=1)

    thisArray = [[],
                 [0, 4],
                 [creditHead, l1, backButton]]

def oldhome():

    root.grid_rowconfigure(0, weight=1)
    root.grid_rowconfigure(2, weight=1)
    root.grid_rowconfigure(4, weight=1)
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(2, weight=1)
    root.grid_columnconfigure(4, weight=1)
    exploreB = Button(root, text="Explore!", command=lambda: changescreen(thisArray, "Explore"))
    craftB = Button(root, text="Craft", command=lambda: changescreen(thisArray, "Craft"))
    talkB = Button(root, text="Talk", command=lambda: changescreen(thisArray, "Talk"))
    menuB = Button(root, text="Menu", command=lambda: changescreen(thisArray, "Menu"))

    exploreB.grid(row=1, column=1)
    craftB.grid(row=1, column=3)
    talkB.grid(row=3, column=1)
    menuB.grid(row=3, column=3)

    thisArray = [[0, 2, 4],
                 [0, 2, 4],
                 [exploreB, craftB, talkB, menuB]]
    """
    homecanvas = Canvas(root, width=600, height=400, bg="gray")
    homecanvas.grid(row=0, column=0, rowspan=3, columnspan=2)
    x = 0
    y = 0

    sprite = canvas.create_rectangle(25, 25, 50, 50, fill="purple")

    downp = False
    upp = False
    leftp = False
    rightp = False
    picup = False


    thisArray = [[], [], [homecanvas]]
    """
"""
def craftitem(itemname, itemlabel):
    if itemname == "Axe" and playerInventory[0] >= 5 and playerInventory[1] >= 3:
        playerInventory[0] = playerInventory[0] - 5
        playerInventory[1] = playerInventory[1] - 3
        playerInventory[5] = playerInventory[5] + 1
        itemlabel.config(text="Axe: Used for cutting down trees.\nMaterials:\nWood: " + str(playerInventory[0]) +
                                "/5\nStone: " + str(playerInventory[1]) + "/3\nCurrent Amount: " + str(playerInventory
                                                                                                       [5]))
    elif itemname == "Sword" and playerInventory[0] >= 2 and playerInventory[1] >= 10 and playerInventory[2] >= 5:
        playerInventory[0] = playerInventory[0] - 2
        playerInventory[1] = playerInventory[1] - 10
        playerInventory[2] = playerInventory[2] - 5
        playerInventory[4] = playerInventory[4] + 1
        itemlabel.config(text="Sword: A WEAPON\nMaterials:\nWood: " + str(playerInventory[0]) + "/2\nStone: " +
                         str(playerInventory[1]) + "/10\nCoal: " + str(playerInventory[2]) +
                              "/5\n Current Amount: " + str(playerInventory[4]))

def crafttext(itemname, itemlabel):
    global selectedcraft
    if itemname == "Sword":
        itemlabel.config(text="Sword: A WEAPON\nMaterials:\nWood: " + str(playerInventory[0]) + "/2\nStone: " +
                              str(playerInventory[1]) + "/10\nCoal: " + str(playerInventory[2]) +
                              "/5\n Current Amount: " + str(playerInventory[4]))
    elif itemname == "Axe":
        itemlabel.config(text="Axe: Used for cutting down trees.\nMaterials:\nWood: " + str(playerInventory[0]) +
                              "/5\nStone: " + str(playerInventory[1]) + "/3\nCurrent Amount: " + str(playerInventory
                                                                                                     [5]))
    selectedcraft = itemname

def craft():
    global selectedcraft
    selectedcraft = "Axe"
    backB = Button(root, text="Back", command=lambda: changescreen(thisArray, "Home"))
    craftLabel = Label(root, text="Axe: Used for cutting down trees.\nMaterials:\nWood: " + str(playerInventory[0]) +
                                "/5\nStone: " + str(playerInventory[1]) + "/3\nCurrent Amount: " + str(playerInventory
                                                                                                       [5]))
    craftButton = Button(root, text="Craft", command=lambda: craftitem(selectedcraft, craftLabel))

    axeButton = Button(root, text="Axe", command=lambda: crafttext("Axe", craftLabel))

    swordButton = Button(root, text="Sword", command=lambda: crafttext("Sword", craftLabel))

    #invLabel.grid(row=1, column=2)
    backB.grid(row=3, column=1)
    craftLabel.grid(row=1, column=2)
    craftButton.grid(row=2, column=2)
    swordButton.grid(row=2, column=3)
    axeButton.grid(row=1, column=3)

    thisArray = [[],
                 [],
                 [backB, craftButton, craftLabel, swordButton, axeButton]]

def menu():
    global higheststagelevel
    playerLabel = Label(root, text=lineprocess("{playerTitle} {playerName} of {playerKingdom} Kingdom"))
    invLabel = Label(root, text="Inventory: \nWood: " + str(playerInventory[0]) + "\nStone: " + str(playerInventory[1])
                                + "\nCoal: " + str(playerInventory[2]) + "\nAxes: " + str(playerInventory[5]))
    levLabel = Label(root, text="Furthest Level: " + str(higheststagelevel))
    backB = Button(root, text="Back", command=lambda: changescreen(thisArray, "Home"))
    optionsB = Button(root, text="Options", command=lambda: changescreen(thisArray, "Options"))
    returnB = Button(root, text="Return to Title", command=lambda: changescreen(thisArray, "Title"))

    playerLabel.grid(row=1, column=1)
    invLabel.grid(row=1, column=2)
    levLabel.grid(row=2, column=2)
    backB.grid(row=2, column=1)
    optionsB.grid(row=3, column=1)
    returnB.grid(row=4, column=1)

    thisArray = [[],
                 [],
                 [playerLabel, invLabel, levLabel, backB, returnB, optionsB]]

def options():
    changeName = Button(root, text="Change Your Name", command=lambda: changescreen(thisArray, "Set Name"))
    changeTitle = Button(root, text= "Change Your Title", command=lambda: changescreen(thisArray, "Set Title"))
    changeKingdom = Button(root, text="Change Your Kingdom's Name", command=lambda: changescreen(thisArray,
                                                                                                 "Set Kingdom"))
    backB = Button(root, text="Go Back", command=lambda:changescreen(thisArray, "Menu"))


    changeName.grid(row=0, column=0)
    changeTitle.grid(row=1, column=0)
    changeKingdom.grid(row=2, column=0)
    backB.grid(row=3, column=0)

    thisArray = [[],
                 [],
                 [changeName, changeTitle, changeKingdom, backB]]


def choosefighter():
    removeB = Button(root, text="Remove")
    

def prepwar():
    # Labels/GUI
    head = Label(root, text="Set your fighters!")
    slot1 = Label(root, text="Front")
    slot2 = Label(root, text="Rear")
    slot1F = Label(root, text="None Selected")
    slot2F = Label(root, text="None Selected")
    slot1B = Button(root, text="Change")
    slot2B = Button(root, text="Change")
    backB = Button(root, text="Back", command=lambda: changescreen(thisArr, "Home"))

    head.grid(row=0, column=1)
    backB.grid(row=0, column=0)
    slot1.grid(row=1, column=0)
    slot2.grid(row=1, column=2)
    slot1F.grid(row=2, column=0)
    slot2F.grid(row=2, column=0)
    root.grid_rowconfigure(2, weight=1)
    slot1B.grid(row=3, column=0)
    slot2B.grid(row=3, column=2)

    thisArr = [[2], [], [head, slot1, slot2, slot1F, slot2F, slot1B, slot2B, backB]]
    """
#explore game


def gameover():
    global goArray
    root.grid_rowconfigure(0, weight=1, uniform="a")
    root.grid_rowconfigure(2, weight=1, uniform="a")
    root.grid_rowconfigure(4, weight=1, uniform="a")
    root.grid_rowconfigure(1, weight=1, uniform="a")
    root.grid_rowconfigure(3, weight=1, uniform="a")
    root.grid_columnconfigure(0, weight=1, uniform="b")
    root.grid_columnconfigure(4, weight=1, uniform="b")
    root.grid_columnconfigure(1, weight=1, uniform="b")
    root.grid_columnconfigure(2, weight=1, uniform="b")
    root.grid_columnconfigure(3, weight=1, uniform="b")
    root.unbind("<KeyPress-Down>")
    root.unbind("<KeyPress-Up>")
    root.unbind("<KeyPress>")
    gameoverlabel = Label(root, text="GAME OVER")
    gameoverlabel.grid(row=1, column=2)
    backB = Button(root, text="Back to Home", command=lambda: changescreen(goArray, "Home"))
    titleB = Button(root, text="Quit to Title", command=lambda: changescreen(goArray, "Title"))
    backB.grid(row=2, column=2)
    titleB.grid(row=3, column=2)
    goArray = [[0, 1, 2, 3, 4], [0, 1, 2, 3, 4], [gameoverlabel, backB, titleB]]


def goback(c, e):
    global stagelevels, goArray
    global stats
    if e == "q" or e.char == "q":
        """
        i = 0
        stats = 100
        while i < len(player.inventory):
            player.inventory[i] = c.getinventory()[i]
            i = i + 1
        """
        c.back()
        stagelevels = 0
        player.reset_health()
        #root.unbind("<KeyPress-Down>")
        #root.unbind("<KeyPress-Up>")
        root.unbind("<KeyPress>")
        changescreen(goArray, "Home")
    elif e.char == "v":
        c.cuttree()
    elif e.char == "x" and not c.inventoryup:
        c.open_popup(1)


def checkdown(c, e):
    if c.currenty2 > 410:
        goback(c, "q")
    else:
        c.down(e)

def checkup(c, e):
    #global stats, newhighestcutscene, chosen_envi
    if c.currenty1 < -10:
        """
        i = 0
        stats = c.getstats()
        while i < len(player.inventory):
            player.inventory[i] = c.getinventory()[i]
            i = i + 1
        """
        c.back()
        explore()
    else:
        c.up(e)

def e_options():
    global unlockedstages, stopkeys
    stopkeys = True
    e_label = Label(root, text="Where are you going?")
    forestB = Button(root, text="Forest", command=lambda: changescreen(thisArr, "Explore Forest"))
    caveB = Button(root, text="Cave", command=lambda: changescreen(thisArr, "Explore Cave"))
    bossB = Button(root, text="Slime King's Cave", command=lambda: changescreen(thisArr, "Boss Text"))
    backB = Button(root, text="Go Back", command=lambda: changescreen(thisArr, "Home"))
    if unlockedstages >= 1:
        e_label.grid(row=0, column=1)
        forestB.grid(row=2, column=0)
        backB.grid(row=3, column=2)
        thisArr = [[], [], [e_label, forestB, backB]]
    if unlockedstages >= 2:
        caveB.grid(row=2, column=1)
        thisArr = [[], [], [e_label, forestB, caveB, backB]]
    if unlockedstages >= 3:
        bossB.grid(row=2, column=2)
        thisArr = [[], [], [e_label, forestB, caveB, bossB, backB]]


def explore():
    #global stagelevels, higheststagelevel, newhighestcutscene, stats, goArray, player
    global stagelevels, stopkeys, higheststagelevel, player
    stopkeys = True
    stagelevels = stagelevels + 1
    test = Items(root, stagelevels, player)
    if player.player_data[5] < stagelevels:
        player.set_player_data(5, stagelevels)
    """
    if higheststagelevel < stagelevels:
        higheststagelevel = stagelevels
   
    if chosen_envi == "Boss Fight":
        test.kuya(player.inventory[4])
    if higheststagelevel < stagelevels:
        higheststagelevel = stagelevels
        if higheststagelevel == 5:
            test.back()
            changescreen(goArray, "ETalk")
    if stagelevels == 5 and chosen_envi == "Cave":
        test.back()
        changescreen(goArray, "ETalk2")
    else:
        newhighestcutscene = 0
    #test.loadinventory(player.inventory)
    #test.loadstats(stats)
    """
    root.bind("<KeyPress-Left>", lambda e: test.left(e))
    root.bind("<KeyPress-Right>", lambda e: test.right(e))
    #root.bind("<KeyPress-Up>", lambda e: test.up(e))
    root.bind("<KeyPress-Up>", lambda e: checkup(test, e))
    #root.bind("<KeyPress-Down>", lambda e: test.down(e))
    root.bind("<KeyPress-Down>", lambda e: checkdown(test, e))
    root.bind("<KeyRelease-Left>", lambda e: test.stop(e))
    root.bind("<KeyRelease-Right>", lambda e: test.stop(e))
    root.bind("<KeyRelease-Up>", lambda e: test.stop(e))
    root.bind("<KeyRelease-Down>", lambda e: test.stop(e))
    root.bind("<KeyPress>", lambda e: goback(test, e))

"""
def homeup(c, e):
    global stopkeys, stagelevels, player
    if c.currenty1 < 0 and not stopkeys:
        print("homeup's if was called")
        stopkeys = True
        c.back()
        player.reset_health()
        stagelevels = 0
        changescreen([[], [], []], "Explore")
    else:
        c.up(e)
        """

def e_movement(c, e):
    if c.currenty1 <= 0:
        c.back()
        explore()
    elif c.currenty2 > 410:
        goback(c, "q")


def movement(c, e, press):
    global stopkeys
    if c.currenty1 <= 0 and not stopkeys:
        stopkeys = True
        c.back()
        changescreen([[], [], []], "Explore")
    elif c.currentx1 <= 0 and not stopkeys:
        #go all the way left to enter the castle
        stopkeys = True
        c.back()
        changescreen([[], [], []], "Castle")
    elif c.currentx1 >= 600 and not stopkeys:
        #go all the way right to leave the castle
        stopkeys = True
        c.back()
        changescreen([[], [], []], "Home")
    if press:
        if e.keysym == "Up":
            c.up(e)
        elif e.keysym == "Down":
            c.down(e)
        elif e.keysym == "Left":
            c.left(e)
        elif e.keysym == "Right":
            c.right(e)
    else:
        c.stop(e)

def home_keypress(c, e):
    if e.char == "z":
        c.interaction()
    elif e.char == "x" and not c.button_up and not c.label_on:
        c.open_popup(1)
    elif e.char == "q" and not c.button_up and not c.label_on:
        c.back()
        changescreen([[], [], []], "Title")



def home():
    global player, stopkeys
    stopkeys = False
    home = Home(root, player)
    #home.loadinventory(player.inventory)
    root.bind("<KeyPress-Left>", lambda e: movement(home, e, True))
    root.bind("<KeyPress-Right>", lambda e: movement(home, e, True))
    # root.bind("<KeyPress-Up>", lambda e: test.up(e))
    root.bind("<KeyPress-Up>", lambda e: movement(home, e, True))
    # root.bind("<KeyPress-Down>", lambda e: test.down(e))
    root.bind("<KeyPress-Down>", lambda e: movement(home, e, True))
    root.bind("<KeyRelease-Left>", lambda e: movement(home, e, False))
    root.bind("<KeyRelease-Right>", lambda e: movement(home, e, False))
    root.bind("<KeyRelease-Up>", lambda e: movement(home, e, False))
    root.bind("<KeyRelease-Down>", lambda e: movement(home, e, False))
    root.bind("<KeyPress>", lambda e: home_keypress(home, e))

def castle_keypress(c, e):
    if e.char == "z":
        c.interaction()
    elif e.char == "x" and not c.parchmentup:
        c.open_popup(1)
    elif e.char == "q" and not c.parchmentup:
        c.back()
        changescreen([[], [], []], "Title")

def castle():
    global player, stopkeys
    stopkeys = False
    castle = Morgan(root, player)
    root.bind("<KeyPress-Left>", lambda e: movement(castle, e, True))
    root.bind("<KeyPress-Right>", lambda e: movement(castle, e, True))
    root.bind("<KeyPress-Up>", lambda e: movement(castle, e, True))
    root.bind("<KeyPress-Down>", lambda e: movement(castle, e, True))
    root.bind("<KeyRelease-Left>", lambda e: movement(castle, e, False))
    root.bind("<KeyRelease-Right>", lambda e: movement(castle, e, False))
    root.bind("<KeyRelease-Up>", lambda e: movement(castle, e, False))
    root.bind("<KeyRelease-Down>", lambda e: movement(castle, e, False))
    root.bind("<KeyPress>", lambda e: castle_keypress(castle, e))

#main running stuff
#title()
gameover()
explore()
#home()

#castle()
root.mainloop()
