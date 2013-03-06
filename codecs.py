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
5 – join_game_pdu
6 – m_place_pdu
7 – rotate_board_pdu
"""

# copied from example; names, variables and values need fixing

class ClientPduCodec(IGameCommClientPdu):

  def __init__(self,entity):
    self.entity = entity
    self.rbuf = bytes()# read buffer
  
  def new_game_pdu(self,peer_name, mark): # => return encoded binary data
    msgtype = struct.pack("<h",0)
    strdata = peer_name.encode("iso8859_15")
    strsize = struct.pack("<h",len(strdata))
    markdata = mark.encode("iso8859_15")
    size = len(msgtype) + len(strdata) + len(strsize) + len(markdata) + 2 # as msgsize
    msgsize = struct.pack("<h",size)
    return msgsize + msgtype + strsize + strdata + markdata
  
  def board_info_pdu(self, board):
    msgtype = struct.pack("<h",1)
    boarddata = bytes()
    for x in range(0,3):
      for y in range(0,3):
        boarddata += board[x][y].encode("iso8859_15")
    size = 2 + len(msgtype) + len(boarddata)   
    msgsize = struct.pack("<h",size)
    return msgsize + msgtype + boarddata
  
  def error_pdu(self, code, reason):
    msgtype = struct.pack("<h",2)
    codedata = struct.pack("<h",code)
    strdata = reason.encode("iso8859_15")
    strsize = struct.pack("<h",len(strdata))
    size = 2 + len(msgtype) + len(codedata) + len(strsize) + len(strdata)   
    msgsize = struct.pack("<h",size)
    return msgsize + msgtype + codedata + strsize + strdata
  
  def win_pdu(self, result):
    msgtype = struct.pack("<h",3)
    resultdata = struct.pack("<h",result)
    size = 2 + len(msgtype) + len(resultdata)   
    msgsize = struct.pack("<h",size)
    return msgsize + msgtype + resultdata    
  
  def your_turn_pdu(self):
    msgtype = struct.pack("<h",6)
    size = 2 + len(msgtype)   
    msgsize = struct.pack("<h",size)
    return msgsize + msgtype
  
  def decode(self,data): # => decode binary data and call resolved message
    log.debug("decode({})".format(buf_debug(data)))
    ## handle read buffer
    self.rbuf = self.rbuf + data
    data = self.rbuf
    ## decode header 
    point = 0 
    msgsize, = struct.unpack("<h", data[point:point+2]) # Remember tuple return
    point += 2 
    msgtype, = struct.unpack("<h", data[point:point+2])
    log.debug("decode(msgsize={},msgtype={})".format(msgsize,msgtype))
    point += 2
    ## no we know message size, can remove it from read buffer
    self.rbuf = self.rbuf[msgsize:] # rest data
    
    ## 0 new_game_pdu
    if msgtype == 0: 
      strsize, = struct.unpack("<h", data[point:point+2])
      point += 2
      strdata = data[point:point+strsize]
      point += strsize
      peer_name = strdata.decode("iso8859_15")
      markdata = data[point:point+1]
      mark = markdata.decode("iso8859_15")
      self.entity.new_game_pdu(peer_name,mark)
      
    ## 1 board_info_odu
    elif msgtype == 1: 
      board = list()
      for x in range(0,3):
        board.append(list())
        for y in range(0,3):
          board[x].append(None)
      for i,byte in enumerate(data[point:point+9]):
        y = i % 3
        x = int(i / 3)
        #log.debug("{}x{}".format(x,y))
        board[x][y] = chr(byte)
      self.entity.board_info_pdu(board)
      
    ## 2 error_pdu(self, code, reason):
    elif msgtype == 2:
      code, = struct.unpack("<h", data[point:point+2])
      point += 2
      strsize, = struct.unpack("<h", data[point:point+2])
      point += 2
      reason = data[point:point+strsize].decode("iso8859_15")
      self.entity.error_pdu(code, reason)
      
    ## 3 win_pdu(self, result):
    elif msgtype == 3:
      result, = struct.unpack("<h", data[point:point+2])
      point += 2
      self.entity.win_pdu(result)

    ## 6 your_turn_pdu(self):
    elif msgtype == 6:
      self.entity.your_turn_pdu()

    ## X unknown
    else:
      raise RuntimeError("Bad message coding {}".format(msgtype))

class ServerPduCodec(IGameCommServerPdu):
  
  def __init__(self,entity):
    self.entity = entity  
  
  def look_game_pdu(self, name):
    msgtype = struct.pack("<h",4)
    namedata = name.encode("iso8859_15")
    strsize = struct.pack("<h",len(namedata))
    size = len(msgtype) + len(strsize) + len(namedata)
    msgsize = struct.pack("<h",size)
    return msgsize + msgtype + strsize + namedata
 
  def move_pdu(self, x, y):
    msgtype = struct.pack("<h",5)
    xdata = struct.pack("<h",x)
    ydata = struct.pack("<h",y)
    size = len(msgtype) + len(xdata) + len(ydata)
    msgsize = struct.pack("<h",size)
    return msgsize + msgtype + xdata + ydata

  def decode(self, cid, data): # => decode binary data and call resolved message
    log.debug("decode({})".format(buf_debug(data)))
    point = 0 
    msgsize, = struct.unpack("<h", data[point:point+2]) # Remember tuple return
    point += 2 
    msgtype, = struct.unpack("<h", data[point:point+2])
    log.debug("decode(msgsize={},msgtype={})".format(msgsize,msgtype))
    point += 2
    
    # look_game_pdu(self, name):
    if msgtype == 4:
      strsize, = struct.unpack("<h", data[point:point+2])
      point += 2
      name = data[point:point+strsize].decode("iso8859_15")
      point += strsize
      self.entity.look_game_pdu(cid, name)
    
    # move_pdu(self, x, y):
    elif msgtype == 5:
      x, = struct.unpack("<h", data[point:point+2])
      point += 2
      y, = struct.unpack("<h", data[point:point+2])
      point += 2
      self.entity.move_pdu(cid, x, y)

    ## X unknown
    else:
      raise RuntimeError("Bad message coding {}".format(msgtype))
