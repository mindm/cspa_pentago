#!/usr/bin/python3.2
# -*- coding: iso-8859-15 -*-
import numpy
import sys
from collections import defaultdict
from interfaces import IGameCommServerInd 

class Observable:
    def __init__(self):
        self.callbacks = {}
        self.pressed = None

    def addCallback(self, func):
        self.callbacks[func] = 1

    def del_callback(self, func):
        del self.callbacks[func]

    def _doCallbacks(self):
        for func in self.callbacks:
            func(self.pressed)

class GameLogic:
    def __init__(self, server): 
        self.board = numpy.array([[ 0,  0,  0,  0,  0, 0],
                    [ 0,  0,  0,  0,  0, 0],
                    [ 0,  0,  0,  0,  0, 0],
                    [ 0,  0,  0,  0,  0, 0],
                    [ 0,  0,  0,  0,  0, 0],
                    [ 0,  0,  0,  0,  0, 0]])

        self.server = server

    def reset_ind(self):
        ## init board 6x6
        self.board = list()
        for x in range(0,6):
            self.board.append(list())
            for y in range(0,6):
                self.board[x].append(0)

    def place_marble(self,x,y,color):
        if self.valid_move(y, x):
            self.board[y][x] = color
            self.server.update_board_req(self.board)
            ## check win condition
            winner = self.win_condition()
            if winner != 0:
                self.server.game_end_req(winner)
        else:
            self.server.invalid_move_req()
            return False
        return True

    def rotate_sub_board(self, sub_board, direction):
        #rotate upper left corner
        if sub_board == 0:
            #rotate right
            if direction == 0:
                #split array to 3x3
                rotate     = numpy.split(self.board,2,1)
                rotate2    = numpy.split(rotate[0],2)
                #rotate array -270 degrees
                rotate3    = numpy.rot90(rotate2[0],3)
                #merge array
                rotate2[0] = rotate3
                rotate2    = numpy.concatenate((rotate2[0], rotate2[1]),0)
                rotate[0]  = rotate2
                self.board = numpy.concatenate((rotate[0],rotate[1]),1)
                self.print_board()
            #rotate left
            elif direction == 1:
                #split array to 3x3
                rotate     = numpy.split(self.board,2,1)
                rotate2    = numpy.split(rotate[0],2)
                #rotate array -90 degrees
                rotate3    = numpy.rot90(rotate2[0],1)
                #merge array
                rotate2[0] = rotate3
                rotate2    = numpy.concatenate((rotate2[0], rotate2[1]),0)
                rotate[0]  = rotate2
                self.board = numpy.concatenate((rotate[0],rotate[1]),1)
                self.print_board()
        #rotate upper right corner
        elif sub_board == 1:
            #rotate right
            if direction == 0:
                #split array to 3x3
                rotate     = numpy.split(self.board,2,1)
                rotate2    = numpy.split(rotate[1],2)
                #rotate array -270 degrees
                rotate3    = numpy.rot90(rotate2[0],3)
                #merge array
                rotate2[0] = rotate3
                rotate2    = numpy.concatenate((rotate2[0], rotate2[1]),0)
                rotate[1]  = rotate2
                self.board = numpy.concatenate((rotate[0],rotate[1]),1)
                self.print_board()
            #rotate left
            elif direction == 1:
                #split array to 3x3
                rotate     = numpy.split(self.board,2,1)
                rotate2    = numpy.split(rotate[1],2)
                #rotate array -90 degrees
                rotate3    = numpy.rot90(rotate2[0],1)
                #merge array
                rotate2[0] = rotate3
                rotate2    = numpy.concatenate((rotate2[0], rotate2[1]),0)
                rotate[1]  = rotate2
                self.board = numpy.concatenate((rotate[0],rotate[1]),1)
                self.print_board()
                #rotate lower left corner
        elif sub_board == 2:
            #rotate right
            if direction == 0:
                #split array to 3x3
                rotate     = numpy.split(self.board,2,1)
                rotate2    = numpy.split(rotate[0],2)
                #rotate array -270 degrees
                rotate3    = numpy.rot90(rotate2[1],3)
                #merge array
                rotate2[1] = rotate3
                rotate2    = numpy.concatenate((rotate2[0], rotate2[1]),0)
                rotate[0]  = rotate2
                self.board = numpy.concatenate((rotate[0],rotate[1]),1)
                self.print_board()
            #rotate left
            elif direction == 1:
                #split array to 3x3
                rotate     = numpy.split(self.board,2,1)
                rotate2    = numpy.split(rotate[0],2)
                #rotate array -90 degrees
                rotate3    = numpy.rot90(rotate2[1],1)
                #merge array
                rotate2[1] = rotate3
                rotate2    = numpy.concatenate((rotate2[0], rotate2[1]),0)
                rotate[0]  = rotate2
                self.board = numpy.concatenate((rotate[0],rotate[1]),1)
                self.print_board()
        #rotate lower right corner
        elif sub_board == 3:
            #rotate right
            if direction == 0:
                #split array to 3x3
                rotate     = numpy.split(self.board,2,1)
                rotate2    = numpy.split(rotate[1],2)
                #rotate array -270 degrees
                rotate3    = numpy.rot90(rotate2[1],3)
                #merge array
                rotate2[1] = rotate3
                rotate2    = numpy.concatenate((rotate2[0], rotate2[1]),0)
                rotate[1]  = rotate2
                self.board = numpy.concatenate((rotate[0],rotate[1]),1)
                self.print_board()
            #rotate left
            elif direction == 1:
                #split array to 3x3
                rotate     = numpy.split(self.board,2,1)
                rotate2    = numpy.split(rotate[1],2)
                #rotate array -90 degrees
                rotate3    = numpy.rot90(rotate2[1],1)
                #merge array
                rotate2[1] = rotate3
                rotate2    = numpy.concatenate((rotate2[0], rotate2[1]),0)
                rotate[1]  = rotate2
                self.board = numpy.concatenate((rotate[0],rotate[1]),1)
                self.print_board()
            else:
                self.server.error_req()

        ## check win condition
        self.server.update_board_req(self.board)
        winner = self.win_condition()
        if winner != 0:
            self.server.game_end_req(winner)
        elif not self.is_full():
            self.server.game_end_req(0)
        else:
            self.server.nextturn_req()
            
    def win_condition(self):
        #when five marbles of same color aling
        #check after each place_marble and rotate_sub_board
        win = 0
        temp = defaultdict(int)

        #checking vertical and horizontal
        for i in range(6):
            temp = defaultdict(int)
            if win != 0:
                return win
            for j in range(2):
                if self.board[i][j] != 0:
                    for k in range(5):
                        temp[self.board[i][j+k]] += 1
                    if temp[self.board[i][j]] == 5:
                        win = self.board[i][j]
                        break
                    else:
                        temp = defaultdict(int)
            
            for j in range(2):
                if self.board[j][i] != 0:
                    for k in range(5):
                        temp[self.board[j+k][i]] += 1
                    if temp[self.board[j][i]] == 5:
                        win = self.board[j][i]
                        break
                    else:
                        temp = defaultdict(int)

        #checking diagonals
        t_points = [[0,0], [1, 1], [0,1], [1,0]]
        b_points = [[0,5], [1, 4], [0,4], [1,5]]

        for [i, j] in t_points:
            if win != 0:
                return win
            if self.board[i][j] != 0:
                for c in range(5):
                    temp[self.board[i+c][j+c]] += 1
                if temp[self.board[i][j]] == 5:
                        win = self.board[i][j]
                        break
                else:
                    temp = defaultdict(int)

        for [i, j] in b_points:
            if win != 0:
                return win
            if self.board[i][j] != 0:
                for c in range(5):
                    temp[self.board[i+c][j-c]] += 1
                if temp[self.board[i][j]] == 5:
                        win = self.board[i][j]
                        break
                else:
                    temp = defaultdict(int)

        return win


    def valid_move(self, x, y):
        #if place is not 0 it's taken and the move is invalid
        if self.board[x][y] != 0:
            #print("Invalid move")
            return False
            # implement error_req
        else:
            return True
        
    def is_full(self):
        for x in range(0,6):
            for y in range(0,6):
                if self.board[x][y] is 0:
                    return False
        return True

    def print_board(self):
        print (self.board)
