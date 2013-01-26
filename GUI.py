#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

from tkinter import *

def quit():
    root.quit()

root = Tk()

# creating menu
menu = Menu(root)
root.config(menu=menu)

filemenu = Menu(menu)
menu.add_cascade(label='File', menu=filemenu)
filemenu.add_command(label='Exit', command=quit)

mainloop()
