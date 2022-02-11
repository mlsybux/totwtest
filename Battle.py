from tkinter import *
from time import *

class Fighter:
    def __init__(self, name, servants, power):
        self.name = name
        self.servants = servants
        self.power = power

class Battle:
    def __init__(self, master):
        # Tk
        self.master = master
        self.spaces = 2
        self.characters = [Fighter("Ako", 5, 10), Fighter("Kuya", 10, 7)]



