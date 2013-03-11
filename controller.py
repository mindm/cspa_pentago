#!/usr/bin/python3.2
# -*- coding: iso-8859-15 -*-

import sys
from collections import defaultdict
from GUI import View
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
        self.trans_array = {"0" : " ", "1" : "X", "2" : "O"}
    # start new game
    def new_game_ind(self):
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
        self.client.look_game_req()
        root.mainloop()

    def start_game_ind(self):
        self.view.set_infotext("Game starting")

    # your turn notification
    def your_turn_ind(self):
        self.view.set_infotext("Your turn - place mark")

    # receive invalid move notification
    def invalid_move_ind(self):
        self.view.set_infotext("Invalid move")

    # receive game end result
    def game_end_ind(self, end_status):
        if end_status == 0:
            self.view.popup("Draw!")
        else:
            self.view.popup("Player {} won!".format(end_status))

    # update board with data received from communication layer
    def update_board_ind(self, board_info):
        board = list()
        for row in board_info:
            board.extend(row)
        for i in range(len(board)):
            board[i] = self.trans_array[board[i]]
        self.view.update(board)

    # place marble and send the data to communication layer
    def callback(self, id):
        x = id % 6
        y = int(id / 6)
        print("Clicked grid button {}, {}".format(x, y))
        self.client.m_place_req(x, y)

    # click rotate button and send the data to communication layer
    def rotate_callback(self, id):
        print("Clicked btn {}".format(id))
        self.client.rotate_board_req(*self.rotate_params[id])
    
    # make callback for exit-button
    #def closeEvent(self,event):
        #self.client.tcp.shutdown()
        #sys.exit()
