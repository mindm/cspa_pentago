#!/usr/bin/python3.2
# -*- coding: iso-8859-15 -*-

from transport import TCPServer, ClientThread



if __name__ == "__main__":

    tcp = TCPServer("localhost", 1719)

    # tcp.accept()
    tcp.loop()
    
            

