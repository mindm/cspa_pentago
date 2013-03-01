#!/usr/bin/python3.2
# -*- coding: iso-8859-15 -*-
import numpy
import sys
from collections import defaultdict

class GameLogic:
    def __init__(self): 
        self.board = numpy.array([[ 0,  0,  0,  0,  0, 0],
                    [ 0,  0,  0,  0,  0, 0],
                    [ 0,  0,  0,  0,  0, 0],
                    [ 0,  0,  0,  0,  0, 0],
                    [ 0,  0,  0,  0,  0, 0],
                    [ 0,  0,  0,  0,  0, 0]])

    def place_marble(self,x,y,color):
        if self.valid_move(x, y):
            self.board[x,y] = color
            self.print_board()
            if self.win_condition() != 0:
                print("{} has won!".format(self.win_condition()))
                sys.exit(0)
        else:
            pass
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
        if self.win_condition():
            pass
            
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
                        temp[self.board[i][j]] = 0
            
            for j in range(2):
                if self.board[j][i] != 0:
                    for k in range(5):
                        temp[self.board[j+k][i]] += 1
                    if temp[self.board[j][i]] == 5:
                        win = self.board[j][i]
                        break
                    else:
                        temp[self.board[j][i]] = 0

        #checking diagonals
        t_points = [[0,0], [1, 1], [0,1], [1,0]]
        u_points = [[0,5], [1, 4], [0,4], [1,5]]

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
                    temp[self.board[i][j]] = 0

        for [i, j] in u_points:
            if win != 0:
                return win
            if self.board[i][j] != 0:
                for c in range(5):
                    temp[self.board[i+c][j-c]] += 1
                if temp[self.board[i][j]] == 5:
                        win = self.board[i][j]
                        break
                else:
                    temp[self.board[i][j]] = 0

                

        return win


    def valid_move(self, x, y):
        #if place is not 0 it's taken and the move is invalid
        if self.board[x][y] != 0:
            print("Invalid move")            
            return False
        else:
            return True
        

    def print_board(self):
        print (self.board)

def main():

    game = GameLogic()
    game.place_marble(4,0,1)
    #game.rotate_sub_board(3,1)
    game.place_marble(3,1,1)
    game.place_marble(2,2,1)
    game.place_marble(1,3,1)
    game.place_marble(0,4,1)
    #game.place_marble(5,5,1)
if __name__ == "__main__":
    main()
