#!/usr/bin/python3.2
# -*- coding: iso-8859-15 -*-

import sys
from collections import defaultdict
from model import GameLogic
from GUI import *

class GameController:
    def __init__(self):
        # create game board
        self.game = GameLogic()
        self.game.place_marble(2,2,1)

	    # create GUI
        root = Tk()

	    # creating menu
        menu = Menu(root)
        root.config(menu=menu)

        filemenu = Menu(menu)
        menu.add_cascade(label='File', menu=filemenu, background="#C4C4C4")
        filemenu.add_command(label='Exit', command=quit)

	    #creating rotate buttons
        btn_array = initbuttons(root)
        base = Frame(root)

        grid_item = BoardGrid(base)

        root.geometry("300x360+300+300")

        base.place(relx=0.5, rely=0.5, anchor=CENTER)

        # disable sub-board rotation and enable grid buttons
        #disable_buttons(btn_array)
        grid_item.enable()
        mainloop()

    # call from rotate button, rotate board on model and update GUI
    def rotate_call(self, board):
        self.rotate_sub_board(0, 0) #upper left sub-board to right - for testing

def main():
    newgame = GameController()

if __name__ == "__main__":
   main()
