#!/usr/bin/python3.2
# -*- coding: iso-8859-15 -*-

import inspect # http://docs.python.org/3/library/inspect.html
import threading # http://docs.python.org/3/library/threading.html
from model import GameLogic
from interfaces import *
from pdu_codecs import ClientPduCodec, ServerPduCodec

## EntityMix

class EntityMix:
    """ Entity Mixin - common functionalities for entities
    Required members::
    _state
    """
    def goto(self, new_state):
        caller = inspect.getframeinfo(inspect.stack()[1][0])
        input = caller.function
        self._state = new_state

    def name(self): 
        return self.__class__.__name__

# Communication layer client

class CommClient(IGameCommClientReq,IGameCommClientPdu, EntityMix):

    def __init__(self,tcp):
        ## create states
        self.WAIT_UI_START   = CommClient.WAIT_UI_START()
        self.LOOK_GAME       = CommClient.LOOK_GAME()
        self.WAIT_MYTURN     = CommClient.WAIT_MYTURN()
        self.WAIT_UI         = CommClient.WAIT_UI()
        ## state variable & initial state
        self._state = self.WAIT_UI_START
        ## layers
        self.tcp = tcp
        self.port = None
        #self.ui = None
        self.codec_server = ServerPduCodec(self)
        self.codec_client = ClientPduCodec(self)
        ## variables
        self.save_game_id = None # Save game id between messages
        self.lock = threading.Lock()

    class State: # default actions
        
        def name(self): 
            return self.__class__.__name__

        # add methods with error-messages for each state

    # waiting for game to starts
    class WAIT_UI_START(State):

        def look_game_req(self, address, port, game_id):
            save_game_id = game_id
            #data = codec_server.look_game_pdu(game_id)
            #port.req_send(data) - request tcp-connection
            goto(LOOK_GAME)

    # client waiting for connection to server
    class LOOK_GAME(State):

        # when second player found goto WAIT_MY_TURN
        def start_game_pdu(self):
            # start_game_ind() - tell controller to start game
            goto(WAIT_MYTURN)

    # player waiting for turn or server calculating changes
    class WAIT_MYTURN(State):

        # board is updated after opponent's m_place or rotate
        def update_board_pdu(self, board_info):
            # update_board_ind(board_info) - tell controller to update board
            goto(WAIT_MYTURN) 

        # player's turn starts or it's time to rotate
        def your_turn_pdu(self):
            # your_turn_ind() - tell controller to inform about new turn
            goto(WAIT_UI)

        # game tells that the move was invalid
        def invalid_move_pdu(self):
            # invalid_move_ind() - tell controller to inform about invalid move
            goto(WAIT_UI)

        # game ends - victory, loss, or draw
        def game_end_pdu(self, end_status):
            # game_end_ind(end_status) - tell controllet to inform about end
            goto(WAIT_UI_START)            

    # client waiting for user input
    class WAIT_UI(State):

        # user places marble
        def m_place_req(self, x, y):
            goto(WAIT_MYTURN)
            #data = codec_server.m_place_pdu(x, y)
            #port.req_send(data) - request tcp-transfer

        # user rotates board
        def rotate_board_req(self, board, direction):
            #data = codec_server.rotate_board_pdu(x, y)
            #port.req_send(data) - request tcp-transfer
            goto(WAIT_MYTURN)

        # board is updated after current user's input
        def update_board_pdu(self, board_info):
            # update_board_ind(board_info) - tell controller to update board
            goto(WAIT_UI)

# Inputs that are sent to states
  
  ## GUI inputs
  
    def look_game_req(self, addr, port, name):
        self._state.look_game_req(self, addr, port, name)
      
    def m_place_req(self, x, y): 
        self._state.m_place_req(self, x, y)

    def rotate_board_req(self, board, direction): 
        self._state.rotate_board_req(self, board, direction)

  ## peer inputs
  
    def start_game_pdu(self):
        self._state.start_game_pdu(self)

    def update_board_pdu(self, board_info):
        self._state.update_board_pdu(self, board_info)

    def invalid_move_pdu(self):
        self._state.invalid_move_pdu(self)

    def game_end_pdu(self, end_status):
        self._state.game_end_pdu(self, end_status)

    def your_turn_pdu(self):
        self._state.your_turn_pdu(self)

  ## tcp inputs

    def received_ind(self, port, data):
        self.codec_client.decode(data)

    def new_connection_ind(self, port): 
        self._state.ind_connect(self, port)

    def close_connection_ind(self, port): 
        self._state.ind_close(self, port)

    def networ_error_ind(self, port, code, reason): 
        self._state.ind_error(self, port, code, reason)

# Communication layer server

class CommServer(IGameCommServerReq, IGameCommServerPdu, EntityMix):
    pass

