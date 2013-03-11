#!/usr/bin/python3.2
# -*- coding: iso-8859-15 -*-

import struct # http://docs.python.org/3/library/struct.html
from interfaces import IGameCommClientPdu, IGameCommServerPdu

""" Message type coding
0 – start_game_pdu
1 – update_board_pdu
2 – game_end_pdu
3 – invalid_move_pdu
4 – your_turn_pdu
5 – look_game_pdu
6 – m_place_pdu
7 – rotate_board_pdu
"""

class ClientPduCodec(IGameCommClientPdu):

    def __init__(self,entity):
        self.entity = entity
        self.rbuf = bytes()# read buffer
  
    def start_game_pdu(self):
        msgtype = struct.pack("<h",0)
        size = 2 + len(msgtype)
        msgsize = struct.pack("<h",size)
        return msgsize + msgtype
  
    def update_board_pdu(self, board_info):
        msgtype = struct.pack("<h",1)
        boarddata = bytes()
        for x in range(0,6):
          for y in range(0,6):
              boarddata += str(board_info[x][y]).encode("iso8859_15")
        size = 2 + len(msgtype) + len(boarddata)   
        msgsize = struct.pack("<h",size)
        return msgsize + msgtype + boarddata
  
    def game_end_pdu(self, end_status):
        msgtype = struct.pack("<h",2)
        resultdata = struct.pack("<h",end_status)
        size = 2 + len(msgtype) + len(resultdata)   
        msgsize = struct.pack("<h",size)
        return msgsize + msgtype + resultdata

    def invalid_move_pdu(self):
        msgtype = struct.pack("<h",3)
        size = 2 + len(msgtype)   
        msgsize = struct.pack("<h",size)
        return msgsize + msgtype

    def your_turn_pdu(self):
        msgtype = struct.pack("<h",4)
        size = 2 + len(msgtype)   
        msgsize = struct.pack("<h",size)
        return msgsize + msgtype
  
    def decode(self,data): # => decode binary data and call resolved message
        ## handle read buffer
        self.rbuf = self.rbuf + data
        data = self.rbuf
        ## decode header 
        point = 0 
        msgsize, = struct.unpack("<h", data[point:point+2]) # Remember tuple return
        point += 2 
        msgtype, = struct.unpack("<h", data[point:point+2])
        point += 2
        ## no we know message size, can remove it from read buffer
        self.rbuf = self.rbuf[msgsize:] # rest data

        ## 0 start_game_pdu
        if msgtype == 0: 
            self.entity.start_game_pdu()
      
        ## 1 update_board_pdu
        elif msgtype == 1: 
            board_info = list()
            for x in range(0,6):
                board_info.append(list())
                for y in range(0,6):
                    board_info[x].append(None)
            for i,byte in enumerate(data[point:point+36]):
                y = i % 6
                x = int(i / 6)
                board_info[x][y] = chr(byte)
            self.entity.update_board_pdu(board_info)

        ## 2 game_end_pdu(self, end_status):
        elif msgtype == 2:
            end_status, = struct.unpack("<h", data[point:point+2])
            point += 2
            self.entity.game_end_pdu(end_status)
      
        ## 3 invalid_move_pdu(self):
        elif msgtype == 3:
            self.entity.invalid_move_pdu()

        ## 4 your_turn_pdu(self):
        elif msgtype == 4:
            self.entity.your_turn_pdu()

        ## X unknown
        else:
            raise RuntimeError("Bad message coding {}".format(msgtype))

class ServerPduCodec(IGameCommServerPdu):
  
    def __init__(self,entity):
        self.entity = entity  
  
    def look_game_pdu(self):
        msgtype = struct.pack("<h",5)
        size = 2 + len(msgtype)
        msgsize = struct.pack("<h",size)
        return msgsize + msgtype
 
    def m_place_pdu(self, x, y):
        msgtype = struct.pack("<h",6)
        xdata = struct.pack("<h",x)
        ydata = struct.pack("<h",y)
        size = 2 + len(msgtype) + len(xdata) + len(ydata)
        msgsize = struct.pack("<h",size)
        return msgsize + msgtype + xdata + ydata

    def rotate_board_pdu(self, board, direction):
        msgtype = struct.pack("<h",7)
        subboarddata = struct.pack("<h",board)
        directiondata = struct.pack("<h",direction)
        size = 2 + len(msgtype) + len(subboarddata) + len(directiondata)
        msgsize = struct.pack("<h",size)
        return msgsize + msgtype + subboarddata + directiondata

    def decode(self, data, port): # => decode binary data and call resolved message
        point = 0 
        msgsize, = struct.unpack("<h", data[point:point+2]) # Remember tuple return
        point += 2 
        msgtype, = struct.unpack("<h", data[point:point+2])
        point += 2
    
        # look_game_pdu(self):
        if msgtype == 5:
            self.entity.look_game_pdu()
        
        # m_place_pdu(self, x, y):
        elif msgtype == 6:
            x, = struct.unpack("<h", data[point:point+2])
            point += 2
            y, = struct.unpack("<h", data[point:point+2])
            point += 2
            self.entity.m_place_pdu(port, x, y)

        # rotate_board_pdu(self, board, direction):
        elif msgtype == 7:
            board, = struct.unpack("<h", data[point:point+2])
            point += 2
            direction, = struct.unpack("<h", data[point:point+2])
            point += 2
            self.entity.rotate_board_pdu(port, board, direction)

        ## X unknown
        else:
            raise RuntimeError("Bad message coding {}".format(msgtype))
