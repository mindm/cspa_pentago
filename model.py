# -*- coding: iso-8859-15 -*-
import numpy

class GameLogic:
	def __init__(self): 
		self.board = numpy.array([[ 0,  0,  0,  0,  0, 0],
					[ 0,  0,  0,  0,  0, 0],
					[ 0,  0,  0,  0,  0, 0],
					[ 0,  0,  0,  0,  0, 0],
					[ 0,  0,  0,  0,  0, 0],
					[ 0,  0,  0,  0,  0, 0]])

	def place_marble(self,x,y,color):
		if self.board[x,y] == 0:
			self.board[x,y] = color
			self.print_board()
			self.win_condition()
		else:
			self.invalid_move()

	def rotate_sub_board(self, sub_board, direction):
		#rotate upper left corner
		if sub_board == 0:
			#rotate right
			if direction == 0:
				#split array to 3x3
				rotate = numpy.split(self.board,2,1)
				rotate2 = numpy.split(rotate[0],2)
				#rotate array -270 degrees
				rotate3 = numpy.rot90(rotate2[0],3)
				#merge array
				rotate2[0] = rotate3
				rotate2 = numpy.concatenate((rotate2[0], rotate2[1]),0)
				rotate[0] = rotate2
				self.board = numpy.concatenate((rotate[0],rotate[1]),1)
				self.print_board()
			#rotate left
			elif direction == 1:
				#split array to 3x3
				rotate = numpy.split(self.board,2,1)
				rotate2 = numpy.split(rotate[0],2)
				#rotate array -90 degrees
				rotate3 = numpy.rot90(rotate2[0],1)
				#merge array
				rotate2[0] = rotate3
				rotate2 = numpy.concatenate((rotate2[0], rotate2[1]),0)
				rotate[0] = rotate2
				self.board = numpy.concatenate((rotate[0],rotate[1]),1)
				self.print_board()
		#rotate upper right corner
		elif sub_board == 1:
			#rotate right
			if direction == 0:
				#split array to 3x3
				rotate = numpy.split(self.board,2,1)
				rotate2 = numpy.split(rotate[1],2)
				#rotate array -270 degrees
				rotate3 = numpy.rot90(rotate2[0],3)
				#merge array
				rotate2[0] = rotate3
				rotate2 = numpy.concatenate((rotate2[0], rotate2[1]),0)
				rotate[1] = rotate2
				self.board = numpy.concatenate((rotate[0],rotate[1]),1)
				self.print_board()
			#rotate left
			elif direction == 1:
				#split array to 3x3
				rotate = numpy.split(self.board,2,1)
				rotate2 = numpy.split(rotate[1],2)
				#rotate array -90 degrees
				rotate3 = numpy.rot90(rotate2[0],1)
				#merge array
				rotate2[0] = rotate3
				rotate2 = numpy.concatenate((rotate2[0], rotate2[1]),0)
				rotate[1] = rotate2
				self.board = numpy.concatenate((rotate[0],rotate[1]),1)
				self.print_board()
		#rotate lower left corner
		elif sub_board == 2:
			#rotate right
			if direction == 0:
				#split array to 3x3
				rotate = numpy.split(self.board,2,1)
				rotate2 = numpy.split(rotate[0],2)
				#rotate array -270 degrees
				rotate3 = numpy.rot90(rotate2[1],3)
				#merge array
				rotate2[1] = rotate3
				rotate2 = numpy.concatenate((rotate2[0], rotate2[1]),0)
				rotate[0] = rotate2
				self.board = numpy.concatenate((rotate[0],rotate[1]),1)
				self.print_board()
			#rotate left
			elif direction == 1:
				#split array to 3x3
				rotate = numpy.split(self.board,2,1)
				rotate2 = numpy.split(rotate[0],2)
				#rotate array -90 degrees
				rotate3 = numpy.rot90(rotate2[1],1)
				#merge array
				rotate2[1] = rotate3
				rotate2 = numpy.concatenate((rotate2[0], rotate2[1]),0)
				rotate[0] = rotate2
				self.board = numpy.concatenate((rotate[0],rotate[1]),1)
				self.print_board()
		#rotate lower right corner
		elif sub_board == 3:
			#rotate right
			if direction == 0:
				#split array to 3x3
				rotate = numpy.split(self.board,2,1)
				rotate2 = numpy.split(rotate[1],2)
				#rotate array -270 degrees
				rotate3 = numpy.rot90(rotate2[1],3)
				#merge array
				rotate2[1] = rotate3
				rotate2 = numpy.concatenate((rotate2[0], rotate2[1]),0)
				rotate[1] = rotate2
				self.board = numpy.concatenate((rotate[0],rotate[1]),1)
				self.print_board()
			#rotate left
			elif direction == 1:
				#split array to 3x3
				rotate = numpy.split(self.board,2,1)
				rotate2 = numpy.split(rotate[1],2)
				#rotate array -90 degrees
				rotate3 = numpy.rot90(rotate2[1],1)
				#merge array
				rotate2[1] = rotate3
				rotate2 = numpy.concatenate((rotate2[0], rotate2[1]),0)
				rotate[1] = rotate2
				self.board = numpy.concatenate((rotate[0],rotate[1]),1)
				self.print_board()
		self.win_condition()
	def win_condition(self):
		#when five marbles of same color aling
		#check after each place_marble and rotate_sub_board
		pass

	def invalid_move(self):
		#if place is not 0 it's taken and the move is invalid
		print("Invalid move")

	def print_board(self):
		print (self.board)

def main():

	game = GameLogic()
	game.place_marble(3,3,1)
	print ("")
	game.rotate_sub_board(3,1)

if __name__ == "__main__":
	main()
