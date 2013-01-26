#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

from tkinter import *
import math

def quit():
    root.quit()

class BoardGrid:

    def __init__(self, frame):
        self.arr = []
        loop = 0
        for i in range(6):
            for j in range(6):
    
                s = str(loop)
                loop += 1
                
                b = Button(frame, text=s, state=DISABLED, height=2, width=2)
                b.grid(row=i, column=j)
                self.arr.append(b)
    
    def update(self, array):
        if len(array) != 36:
            raise Exception('Array length should be 36!')
        else: 
            loop = 0
            for i in range(6):
                for j in range(6):
                    self.arr[loop].config(text=array[loop])
                    loop += 1
            print("done")
        



root = Tk()

# creating menu
menu = Menu(root)
root.config(menu=menu)

filemenu = Menu(menu)
menu.add_cascade(label='File', menu=filemenu, background="#C4C4C4")
filemenu.add_command(label='Exit', command=quit)

base = Frame(root)

grid_item = BoardGrid(base)
####
arrtest=[]
for i in range(36):
    arrtest.append("X")
grid_item.update(arrtest)
####
base.pack()

mainloop()
