#!/usr/bin/python3.2
# -*- coding: iso-8859-15 -*-

import sys
from collections import defaultdict
#from model import GameLogic
from GUI import View
#from states import GameState
from tkinter import *
from interfaces import *

class GameController:
    def __init__(self, client, tcp):

        self.client = client 
        # create game board

        self.rotate_params = {  0: [0, 1],
                                1: [0, 0],
                                2: [1, 1],
                                3: [1, 0],
                                4: [2, 1],
                                5: [2, 0],
                                6: [3, 1],
                                7: [3, 0] }
    
    # start new game
    def new_game_ind():
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
        root.mainloop()

    # your turn notification
    def your_turn_ind():
        self.view.set_infotext("Your turn")

    # receive invalid move notification
    def invalid_move_ind():
        self.view.set_infotext("Invalid move")

    # receive game end result
    def game_end_ind(end_status):
        self.view.popup("Player {} won!".format(win))

    # update board with data received from communication layer
    def update_board_ind(board_info):
        self.view.update(board_info)

    # place marble and send the data to communication layer
    def callback(self, id):
        x = id % 6
        y = int(id / 6)
        print("Clicked grid button {}, {}".format(x, y))
        self.client.m_place_req(x, y)

    # click rotate button and send the data to communication layer
    def rotate_callback(self, id):
        print("Clicked btn {}".format(id))
        self.client.m_place_req(x, y)
    
    # make callback for exit-button
    #def closeEvent(self,event):
        #self.client.tcp.shutdown()
        #sys.exit()
