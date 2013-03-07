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

        self.rotate_params = {  0: [0, 1],
                                1: [0, 0],
                                2: [1, 1],
                                3: [1, 0],
                                4: [2, 1],
                                5: [2, 0],
                                6: [3, 1],
                                7: [3, 0] }
	    # create GUI
        root = Tk()
        self.view = View(root)

        grid_btn_array = self.view.get_grid_btns()
        i = 0
        for btn in grid_btn_array:
            btn.config(command=lambda x=i: self.callback(x))
            i += 1

        rotate_btn_array = self.view.get_rotate_btns()
        i=0
        for btn in rotate_btn_array:
            btn.config(command=lambda x=i: self.rotate_callback(x))
            i += 1

        self.view.enable_grid()
        self.view.set_infotext("Player 1 place marble")
        root.mainloop()

    # call from rotate button, rotate board on model and update GUI
    def rotate_call(self, board):
        self.rotate_sub_board(0, 0) #upper left sub-board to right - for testing

    def callback(self, id):
        x = id % 6
        y = int(id / 6)
        print("Clicked grid button {}, {}".format(x, y))

        if self.state.getState() == "WAIT_P1_M_PLACE":
            self.game.place_marble(x, y, 1)
            self.state.setState("WAIT_P1_ROTATE")
            self.view.set_infotext("Player 1 rotate")
            win = self.game.win_condition()
            if win != 0:
                print ("Player {} won!".format(win))
                self.state.setState("STOP")
        elif self.state.getState() == "WAIT_P2_M_PLACE":
            self.game.place_marble(x, y, 2)
            self.state.setState("WAIT_P2_ROTATE")
            self.view.set_infotext("Player 2 rotate")
            win = self.game.win_condition()
            if win != 0:
                print ("Player {} won!".format(win))
                self.state.setState("STOP")
        

        board = self.game.get_board()
        self.view.update(board)

    def rotate_callback(self, id):
        print("Clicked btn {}".format(id))
        if self.state.getState() == "WAIT_P1_ROTATE":
            try:
                self.game.rotate_sub_board(*self.rotate_params[id])
                self.state.setState("WAIT_P2_M_PLACE")
                self.view.set_infotext("Player 2 place marble")
            except Exception as e:
                print(e)
            win = self.game.win_condition()
            if win != 0:
                print ("Player {} won!".format(win))
                self.state.setState("STOP")
        if self.state.getState() == "WAIT_P2_ROTATE":
            try:
                self.game.rotate_sub_board(*self.rotate_params[id])
                self.state.setState("WAIT_P1_M_PLACE")
                self.view.set_infotext("Player 1 place marble")
            except Exception as e:
                print(e)
            win = self.game.win_condition()
            if win != 0:
                print ("Player {} won!".format(win))
                self.state.setState("STOP")

        board = self.game.get_board()
        self.view.update(board)



def main():
    newgame = GameController()

if __name__ == "__main__":
   main()
