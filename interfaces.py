#!/usr/bin/python3.2
# -*- coding: iso-8859-15 -*-

from abc import ABCMeta, abstractmethod # http://docs.python.org/3/library/abc.html

# Client interfaces

class IGameCommClientReq(metaclass=ABCMeta):

    @abstractmethod
    def look_game_req(self):
        """ Player is looking for game.
        address as str as ip/dns address
        port as int
        """
      
    @abstractmethod
    def m_place_req(self, x, y):
        """ Player places a game piece.
        x as uint32 
        y as uint32
        """

    @abstractmethod
    def rotate_board_req(self, board, direction):
        """ Player rotates sub-board
        board as uint32
        direction as uint8 
        """
        
class IGameCommClientInd(metaclass=ABCMeta):
  
    @abstractmethod
    def start_game_ind(self):
        """ Player is informed of starting game.
        """

    @abstractmethod
    def update_board_ind(self, board_info):
        """ Board update from server.
        board_info as list  
        """

    @abstractmethod
    def game_end_ind(self, end_status):
        """ Game ends; win, lose or draw.
        end_status as uint32
        """       

    @abstractmethod
    def invalid_move_ind(self):
        """ Game logic error.
        """

    @abstractmethod
    def your_turn_ind(self):
        """ Player's turn now. 
        """
        
class IGameCommClientPdu(metaclass=ABCMeta):

    @abstractmethod
    def start_game_pdu(self):
        """ PDU for player looking a new game.
        """

    @abstractmethod
    def update_board_pdu(self, board_info):
        """ PDU for player move.
        board_info as list
        """

    @abstractmethod
    def game_end_pdu(self, end_status):
        """ PDU for end game information.
        end_status as uint32
        """

    @abstractmethod
    def invalid_move_pdu(self):
        """ PDU for move againsta game logic.
        """

    @abstractmethod
    def your_turn_pdu(self):
        """ PDU for players turn.
        """

# Server interfaces     

class IGameCommServerReq(metaclass=ABCMeta):

    @abstractmethod
    def game_end_req(self, end_status):
        """ End condition is met  
        end_status as uint32
        """

    @abstractmethod
    def update_board_req(self, board_info):
        """ Game logic tells the server to send new board to client.
        board_info as list
        """

    @abstractmethod
    def invalid_move_req(self):
        """ Game logic tells the server that the move was invalid  
        """

class IGameCommServerInd(metaclass=ABCMeta):

    @abstractmethod
    def new_game_ind(self):
        """ Server asks game logic for a new game
        """
    
    @abstractmethod
    def m_place_ind(self, x, y):
        """ Server tells game logic about new game piece placement.  
        x as uint32
        y as uint32
        """

    @abstractmethod
    def rotate_board_ind(self, board, direction):
        """ Server tells game logic about sub-board rotation.
        board as uint32
        direction as uint8
        """

class IGameCommServerPdu(metaclass=ABCMeta):
  
    @abstractmethod
    def look_game_pdu(self):
        """ Client looking for game.
        """

    @abstractmethod
    def m_place_pdu(self, x, y):
        """ Client sends placement data.
        x as uint32 
        y as uint32 
        """

    @abstractmethod
    def rotate_board_pdu(self, board, direction):
        """ Client sends rotation data.
        board as uint32
        direction as uint8
        """

# Transport, TCP Interfaces    

class ITransReq(metaclass=ABCMeta):
  
    @abstractmethod
    def req_send(self, data):
        """ Send data to peer.
        """
    
    @abstractmethod
    def req_open_connection(self, address, port):
        """ Open connection.
        """

    @abstractmethod
    def req_close_connection(self):
        """ Close connection.
        """
    
class ITransInd(metaclass=ABCMeta):  
  
    @abstractmethod
    def received_ind(self, port, data):
        """ Received data from connection
        """

    @abstractmethod
    def new_connection_ind(self, port):
        """ New connection 
        """

    @abstractmethod
    def close_connection_ind(self, port):
        """ Connection has closed.
        """

    @abstractmethod
    def network_error_ind(self, port, errno, why):
        """ Error in connection.
        """
