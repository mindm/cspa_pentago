#!/usr/bin/python3.2
# -*- coding: iso-8859-15 -*-

from abc import ABCMeta, abstractmethod # http://docs.python.org/3/library/abc.html

# Client interfaces

class IGameCommClientReq(metaclass=ABCMeta):
  
  # game name not in specs, add there or remove?
  @abstractmethod
  def look_game_req(self, addr:str, port:int, name:str):
    """ Player is looking for game.
    addr as str as ip/dns address
    port as int 
    name as str 
    """
      
  @abstractmethod
  def m_place_req(self, x, y):
    """ Player places a game piece.
    x and y as int 
    """

  @abstractmethod
  def rotate_board_req(self, board, direction):
    """ Player rotates sub-board
    subboard and direction as int 
    """
        
class IGameCommClientInd(metaclass=ABCMeta):
  
  @abstractmethod
  def start_game_ind(self, peer_name, mark):
    """ Player is informed of starting game.
    peer_name as str
    mark as str 
    """

  @abstractmethod
  def game_end_ind(self, result):
    """ Game ends; win, lose or draw.
    result as int 
    """       
 
  @abstractmethod
  def update_board_ind(self, board):
    """ Board update from server.
    board as int  
    """
    # should the board be sent as list?
        
  @abstractmethod
  def invalid_move_ind(self, code, reason):
    """ Game logic error.
    code as int where
      100 out of board bounds
      101 unit already in position
    reason as string 
    """

  @abstractmethod
  def your_turn_ind(self):
    """ Player's turn now. 
    """
        
class IGameCommClientPdu(metaclass=ABCMeta):

  @abstractmethod
  def look_game_pdu(self,peer_name, mark):
    """ Client looking for game.
    peer_name as str
    mark as str  
    """

  @abstractmethod
  def m_place_pdu(self, x, y):
    """ Client sends placement data.
    x and y as int 
    """

  @abstractmethod
  def rotate_board_pdu(self, subboard, direction):
    """ Client sends rotation data.
    board and direction as int 
    """

# Server interfaces     

class IGameCommServerReq(metaclass=ABCMeta):

  @abstractmethod
  def game_end_req(self, result):
    """ End condition is met  
    result as int
    """

  @abstractmethod
  def update_board_req(self, board):
    """ Game logic tells the server to send new board to client.
    board as int
    """

  @abstractmethod
  def invalid_move_req(self, code, reason):
    """ Game logic tells the server that the move was invalid  
    code as int
    reason as string
    """
    
class IGameCommServerInd(metaclass=ABCMeta):

  @abstractmethod
  def new_game_ind(self):
    """ Server asks game logic for a new game
    """
    
  @abstractmethod
  def m_place_ind(self, x, y, color):
    """ Server tells game logic about new game piece placement.  
    x as int
    y as int
    color as int
    """

  @abstractmethod
  def rotate_board_ind(self, subboard, direction):
    """ Server tells game logic about sub-board rotation.
    subboard and direction as int
    """

class IGameCommServerPdu(metaclass=ABCMeta):
  
  @abstractmethod
  def start_game_pdu(self, name):
    """ PDU for player looking a new game.
    name as string 
    """

  @abstractmethod
  def game_end_pdu(self, result):
    """ PDU for end game information.
    result as int
    """

  @abstractmethod
  def update_board_pdu(self, board):
    """ PDU for player move.
    board as int
    """

  @abstractmethod
  def invalid_move_pdu(self, code, reason):
    """ PDU for move againsta game logic.
    code as int
    reason as string
    """

  @abstractmethod
  def your_turn_pdu(self):
    """ PDU for players turn.
    """

# Transport, Tcp Interfaces    
    
class ITransReq(metaclass=ABCMeta):
  
  @abstractmethod
  def send(self, cid, data):
    """ Send data to peer.
    is as int -- connection cid
    data as bytes
    """
    
  @abstractmethod
  def open_connection(self, address, port):
    """ Open connection.
    address as str
    port as int 
    """

  @abstractmethod
  def close_connection(self, cid):
    """ Close connection.
    cid as int -- connection id
    """
    
class ITransInd(metaclass=ABCMeta):

  @abstractmethod
  def receive(self, cid, data):
    """ Receive data from connection
    cid as int -- connection id
    data as byte
    """

  @abstractmethod
  def new_connection_ind(self, cid):
    """ New connection 
    cid as int -- connection id
    """
    
  @abstractmethod
  def close_connection_ind(self, cid):
    """ Connection has closed.
    cid as int -- connection id
    """

  @abstractmethod
  def network_error(self, cid, code, reason):
    """ Error in network.
    cid as int -- connection id
    code as int
    reason as str
    """

  # do we need two errors?
  @abstractmethod
  def transport_error(self, cid, code, reason):
    """ 
    cid as int -- connection id
    code as int
    reason as str
    """
