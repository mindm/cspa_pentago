#!/usr/bin/python3.2
# -*- coding: iso-8859-15 -*-

import sys

from transport import TCPServer
from communication import CommServer
from model import GameLogic

def run():
  ## create transport
  tcp = TCP2()
  ## create server pool
  server = CommServer(tcp,10001)
  ## create game
  game = GameLogic(server)
  server.set_ind(game)
  ## close server by ctrl-c or eclipse red button
  tcp.start()
  
if __name__ == '__main__':
  run()
