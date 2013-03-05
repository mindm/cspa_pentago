#!/usr/bin/python3.2
# -*- coding: iso-8859-15 -*-

import sys
from collections import defaultdict
from model import GameLogic
from GUI import View
from states import GameState
from tkinter import *

class GameController:
    def __init__(self):
        # create game board
        self.game = GameLogic()
        self.state = GameState()

        

	    # create GUI
        root = Tk()
        self.view = View(root)

        grid_btn_array = self.view.get_grid_btns()
        i = 0
        for btn in grid_btn_array:
            btn.config(command=lambda x=i: self.callback(x))
            i += 1

        self.view.enable_grid()
        root.mainloop()

    # call from rotate button, rotate board on model and update GUI
    def rotate_call(self, board):
        self.rotate_sub_board(0, 0) #upper left sub-board to right - for testing

    def callback(self, id):
        x = id % 6
        y = int(id / 6)
        print("Clicked grid button {}, {}".format(x, y))

        if self.state.getState() == "P1":
            self.game.place_marble(x, y, 1)
            self.state.setState("P2")
        elif self.state.getState() == "P2":
            self.game.place_marble(x, y, 2)
            self.state.setState("P1")
        

        board = self.game.get_board()
        self.view.update(board)

def main():
    newgame = GameController()

if __name__ == "__main__":
   main()
