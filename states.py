#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

class GameState:
"""A class for game's various states"""

    def __init__(self):
        self.state = "START"
        
    def setState(self, state):
        self.state = state
    
    def getState(self):
        return self.state
