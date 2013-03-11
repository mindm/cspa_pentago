#!/usr/bin/python3.2
# -*- coding: iso-8859-15 -*-

import sys

from transport import TCPClient
from communication import CommClient
from controller import GameController

def run():
    ## create transport
    tcp = TCPClient("localhost", 33345)
    ## create game communication
    client = CommClient(tcp)
    ## create UI
    ui = GameController(client,tcp)  
    client.set_ui(ui)
    ## main loop
    tcp.start()
    ui.new_game_ind()
  
if __name__ == '__main__':
    run()
