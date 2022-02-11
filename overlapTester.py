from tkinter import *


class Test:

    def __init__(self, master):
        self.a = master
        self.resources = {}
        self.table = Canvas(self.a, width=500, height=500, bg='white')
        self.table.grid(row=0, column=0)
        #self.rect = self.table.create_rectangle(30, 30, 70, 70)
        #self.wood = Resource(self.a, self.rect, "Wood", "Wood-A")
        #self.oval_a = self.table.create_oval(40, 40, 80, 80)
        #self.resources['oval_a'] = self.oval_a
        #self.resources[self.wood.getitemid()] = self.wood.getitem()
        self.rectangle = self.table.create_rectangle(30, 30, 70, 70)

    def overlaps(self, x1, y1, x2, y2):
        '''returns overlapping object ids in dict'''
        self.overlap_list = []
        self.c_object = self.table.find_overlapping(x1, y1, x2, y2)
        for k, v in self.resources.items():  # iterates over resources dict
            print("The list works")
            if v in self.c_object:
                print("Why here!")
                self.overlap_list.append(k)
        return self.overlap_list

    def testoverlaps(self, x1, y1, x2, y2):
        '''returns overlapping object ids in dict'''
        self.overlap_list = []
        self.c_object = self.table.find_overlapping(x1, y1, x2, y2)
        print(self.c_object)
        for k, v in self.resources.items():
            print("second part")
            print(v)

            if v in self.c_object:
                print("third part works")
                self.overlap_list.append(k)
        return self.overlap_list
        """
        for k, v in self.wood.resources.items():  # iterates over resources dict
            print("The list works")
            if v in self.c_object:
                print(" here!")
                self.overlap_list.append(k)
        return self.overlap_list
        """


    # make a dictionary to hold object ids

    # create oval_a and assign a name for it as a key and
    # a reference to it as a value in the ovals dict.
    # the key can be whatever you want to call it
    # create the other ovals as well, adding each to the dict
    # after it's made

    def spawnwood(self, amount):
        self.i = 0
        #print("spawnwood has been called")
        self.woodstack = []
        while self.i < amount:
            #print("The loop's been called")
            self.woodsprite = self.table.create_rectangle(50, 50, 60, 60, fill="red")
            self.woodstack.append(Resource(self.a, self.woodsprite, "Wood", "Wood" + str(self.i)))
            self.woodstack[self.i].resources[self.woodstack[self.i].getitemid()] = self.woodstack[self.i].getitem()
            #self.resources[self.woodstack[self.i].getitemid()] = self.woodstack[self.i].getitem()
            self.i = self.i + 1

    def makeitems(self):
        # draw a rectangle
        self.spawnwood(3)
        #self.rect = self.table.create_rectangle(20, 20, 70, 70)
        #self.wood = Resource(self.a, self.rect, "Wood", "Wood-A")
        #self.resources[self.wood.getitemid()] = self.wood.getitem()

        # print the return value of the overlaps function
        # using the coords of the rectangle as a bounding box
        print(self.testoverlaps(30, 30, 70, 70))


class Resource:
    def __init__(self, can, shape, rtype, rid):
        self.canvas = can
        self.sprite = shape
        self.type = rtype
        self.id = rid
        self.resources = {self.id: self.sprite}

    def getitem(self):
        return self.sprite

    def getitemid(self):
        return self.id

    def getresoucedict(self):
        return self.resources

    def removesprite(self):
        self.canvas.delete(self.sprite)


#main running stuff
root = Tk()
o = Test(root)
o.makeitems()
root.mainloop()
