#!/usr/bin/python3.2
# -*- coding: iso-8859-15 -*-

import sys

from transport import TCPServer
from communications import CommClient
from controller import GameController

def run():
  ## create transport
  tcp = TCPServer()
  ## create game communication
  client = CommClient(tcp)
  ## create UI
  ui = GameController(client,tcp)  
  client.set_ui(ui)
  ## main loop
  tcp.start()
  app.exec_()
  
if __name__ == '__main__':
  logging.basicConfig(level=logging.DEBUG)
  run()
