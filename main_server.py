#!/usr/bin/python3.2
# -*- coding: iso-8859-15 -*-

import sys

from transport import TCPServer
from communication import CommServer
from model import GameLogic

def run():
    ## create transport
    tcp = TCPServer("localhost", 33345)
    print("Server is online")
    tcp.loop()
    ## close server by ctrl-c or eclipse red button
    #tcp.start()
  
if __name__ == '__main__':
    run()
