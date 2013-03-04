#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

from tkinter import *
import math

#Quit method
def quit(root):
    root.destroy()

#Listens for button events
def rotate(id_):
    print("clicked btn {0}".format(id_))


#Class for the board, includes sub-boards
# and grids for those boards
class BoardGrid:

    def __init__(self, frame):
        self.arr = []
        self.f = []
        
        #initializing sub-boards
        for i in range(4):
            temp = Frame(frame, borderwidth=2, background="black")
            temp.grid(column=i%2, row=math.floor(i/2))
            self.f.append(temp)
        
        #initializing grids
        loop = 0
        for i in range(6):
            for j in range(6):
    
                s = str(loop)
                loop += 1
                
                #determine sub-board
                if(i in range(0,3) and j in range(0,3)):
                    sb = self.f[0]
                elif(i in range(0,3) and j in range(3,6)):
                    sb = self.f[1]
                elif(i in range(3,6) and j in range(0,3)):
                    sb = self.f[2]
                else:
                    sb = self.f[3]
                
                b = Button(sb, text=s, state=DISABLED, height=2, width=2)
                b.grid(row=i%3, column=j%3)
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

    def enable(self):
        self.enable_buttons(self.arr)
    
    def disable(self):
        self.disable_buttons(self.arr)

    def disable_buttons(self, arr):

        if type(arr) is not list:
            raise Exception("Argument should be a list!")
            
        for i in range(len(arr)):
            arr[i].config(state=DISABLED)
        
    def enable_buttons(self, arr):

        if type(arr) is not list:
            raise Exception("Argument should be a list!")
            
        for i in range(len(arr)):
            arr[i].config(state=NORMAL)



class View(Toplevel):
    def __init__(self, root):
        # creating menu
        self.menu = Menu(root)
        root.config(menu=self.menu)

        self.filemenu = Menu(self.menu)
        self.menu.add_cascade(label='File', menu=self.filemenu, background="#C4C4C4")
        self.filemenu.add_command(label='Exit', command=lambda root=root:quit(root))


        #creating rotate buttons

        self.btn_array = self.initbuttons(root)
        self.base = Frame(root)


        self.grid_item = BoardGrid(self.base)

        root.geometry("300x360+300+300")

        self.base.place(relx=0.5, rely=0.5, anchor=CENTER)

        #disable_buttons(btn_array)

    def enable_grid(self):
        self.grid_item.enable()

    def disable_grid(self):
        self.grid_item.disable()

    def enable_rotate(self):
        self.grid_item.enable_buttons(self.btn_array)

    def disable_rotate(self):
        self.grid_item.disable_buttons(self.btn_array)
        
    def update(self, array):
        self.grid_item.update(array)

    def buttonfactory(self, frame, label, x_, y_, id_):
        b = Button(frame, text=label, command=lambda: rotate(id_))
        b.place(x=x_, y=y_)
        return b

    def initbuttons(self, frame):

        x_array = [30,80,170,220,30,80,170,220]
        y_array = [15,15,15,15,316,316,316,316]
        text_array = ["<-", "->", "<-", "->", "<-", "->", "<-", "->"]
        btn_array = []
        
        for i in range(8):
            
            btn_array.append(self.buttonfactory(frame, text_array[i], x_array[i], y_array[i], i ))
        
        return btn_array

    
def main():
    global root
    root = Tk()
    view = View(root)
    view.disable_rotate()

    arr = []
    for i in range(36):
        arr.append("i")
    view.update(arr)

    root.mainloop()

if __name__ == "__main__":
    main()