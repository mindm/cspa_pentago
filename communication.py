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
        self.codec_server = ServerPduCodec(self)
        self.codec_client = ClientPduCodec(self)
        ## variables
        self.save_game_id = None # Save game id between messages
        self.lock = threading.Lock()

    class State: # default actions
        
        def name(self): 
            return self.__class__.__name__

        # add methods with error-messages for each state

    class WAIT_UI_START(State):

        def look_game_req(self, ctx, address, port, game_id):
            ctx.save_game_id = game_id
            ctx.goto(ctx.WAIT_CONN_IND)
            ctx.port = ctx.tcp.port(addr,port,ctx)
            ctx.port.req_connect()

    class WAIT_CONN_IND(State):

        def new_connection_ind(self, ctx, port):
            assert ctx.port == port
            data = ctx.codec_server.look_game_pdu(ctx.game_id)
            ctx.port.req_send(data)
            ctx.goto(ctx.LOOK_GAME)

        def close_connection_ind(self, ctx, port):
            ctx.goto(ctx.WAIT_UI_START)

        def network_error_ind(self, ctx, port, code, reason):
            ctx.port = None
            ctx.goto(ctx.WAIT_UI_START)

    # waiting for game to starts
    class WAIT_UI_START(State):

        def look_game_req(self, ctx, address, port, game_id):
            ctx.save_game_id = game_id
            #data = ctx.codec_server.look_game_pdu(ctx.game_id)
            #ctx.port.req_send(data) - request tcp-connection
            ctx.goto(ctx.LOOK_GAME)

    # client waiting for connection to server
    class LOOK_GAME(State):

        # when second player found goto WAIT_MY_TURN
        def start_game_pdu(self, ctx):
            # start_game_ind() - tell controller to start game
            ctx.goto(ctx.WAIT_MYTURN)

    # player waiting for turn or server calculating changes
    class WAIT_MYTURN(State):

        # board is updated after opponent's m_place or rotate
        def update_board_pdu(self, ctx, board_info):
            # update_board_ind(board_info) - tell controller to update board
            ctx.goto(ctx.WAIT_MYTURN) 

        # player's turn starts or it's time to rotate
        def your_turn_pdu(self, ctx):
            # your_turn_ind() - tell controller to inform about new turn
            ctx.goto(ctx.WAIT_UI)

        # game tells that the move was invalid
        def invalid_move_pdu(self, ctx):
            # invalid_move_ind() - tell controller to inform about invalid move
            ctx.goto(ctx.WAIT_UI)

        # game ends - victory, loss, or draw
        def game_end_pdu(self, ctx, end_status):
            # game_end_ind(end_status) - tell controllet to inform about end
            ctx.goto(ctx.WAIT_UI_START)            

    # client waiting for user input
    class WAIT_UI(State):

        # user places marble
        def m_place_req(self, ctx, x, y):
            #data = ctx.codec_server.m_place_pdu(x, y)
            #port.req_send(data) - request tcp-transfer
            ctx.goto(ctx.WAIT_UI)

        # board is updated after current user's input
        def update_board_pdu(self, ctx, board_info):
            # update_board_ind(board_info) - tell controller to update board
            ctx.goto(ctx.WAIT_UI)

        # user rotates board
        def rotate_board_req(self, ctx, board, direction):
            #data = ctx.codec_server.rotate_board_pdu(x, y)
            #port.req_send(data) - request tcp-transfer
            ctx.goto(ctx.WAIT_MYTURN)

# Inputs that are sent to states
  
  ## GUI inputs
  
    def look_game_req(self, addr, port, name): # STATES
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
    def __init__(self,tcp,tcpport):
        ## server data
        self.tcp = tcp
        self.listen = tcp.listen(tcpport,self)
        self.player1_port = None
        self.player2_port = None
        self.ind = None
        ## states
        self.WAIT_PLAYER1 = CommServer.WAIT_PLAYER1()
        self.WAIT_PLAYER2 = CommServer.WAIT_PLAYER2()
        self.WAIT_P1_M_PLACE = CommServer.WAIT_P1_M_PLACE()
        self.WAIT_P2_M_PLACE = CommServer.WAIT_P2_M_PLACE()
        self.WAIT_P1_ROTATE = CommServer.WAIT_P1_ROTATE()
        self.WAIT_P2_ROTATE = CommServer.WAIT_P2_ROTATE()
        ## state variable and initial state
        self._state = self.WAIT_PLAYER1
        ##
        self.codec_server = ServerPduCodec(self)
        self.codec_client = ClientPduCodec(self)

    def set_ind(self,ind):
        self.ind = ind

    class State: # default actions
        
        def name(self): 
            return self.__class__.__name__

        def close_connection_ind(self, port):
            #ind.reset_ind() # reset game, not yet implemented
            goto(WAIT_PLAYER1)

        # add methods with error-messages for each state

    class WAIT_PLAYER1(State):
    
        def look_game_pdu(self, ctx, game_id):
            ctx.goto(ctx.WAIT_PLAYER2)
    
    class WAIT_PLAYER2(State):
    
        def look_game_pdu(self, ctx, game_id):
            ##
            data = ctx.codec_client.start_game_pdu()
            ctx.player1_port.req_send(data)
            ##
            data = ctx.codec_client.start_game_pdu()
            ctx.player2_port.req_send(data)
            ##
            data = ctx.codec_client.your_turn_pdu()
            ctx.player1_port.req_send(data)
            ctx.goto(ctx.WAIT_P1_M_PLACE)
    
    class WAIT_COMMAND(State):

        def game_end_req(self, ctx, end_status):
            if end_status == 1: # player 1 won
                data = ctx.codec_client.win_pdu(end_status)
                ctx.player1_port.req_send(data)
                data = ctx.codec_client.win_pdu(end_status)
                ctx.player2_port.req_send(data)
            elif end_status == 2: # player 2 won
                data = ctx.codec_client.win_pdu(end_status)
                ctx.player1_port.req_send(data)
                data = ctx.codec_client.win_pdu(end_status)
                ctx.player2_port.req_send(data)
            else: # draw
                data = ctx.codec_client.win_pdu(end_status)
                ctx.player1_port.req_send(data)
                data = ctx.codec_client.win_pdu(end_status)
                ctx.player2_port.req_send(data)

            # reset game
            # ctx.ind.reset_ind() - not yet implemented
            # close connections
            ctx.close_connection_ind(None)  
            # new game
            ctx.goto(ctx.WAIT_PLAYER1)    

        def update_board_req(self, ctx, board_info):
            data = ctx.codec_client.board_info_pdu(board_info)
            ctx.player1_port.req_send(data)
            ctx.player2_port.req_send(data)
      
        def close_connection_ind(self, ctx, port):
            if port == ctx.player1_port: # p1 disconnected, p2 won
                data = ctx.codec_client.game_end_pdu(2)
                ctx.player2_port.req_send(data)
            else: # p2 disconnected, p1 won
                data = ctx.codec_client.game_end_pdu(1)
                ctx.player1_port.req_send(data)
            #ctx.ind.reset_ind() # reset game - not yet implemented
            ctx.goto(ctx.WAIT_PLAYER1) # new game     
    
    class WAIT_P1_M_PLACE(WAIT_COMMAND):

        def m_place_pdu(self, ctx, port, x, y):
            if port != ctx.player1_port: # if not your turn send error
                data = ctx.codec_client.invalid_move_pdu()
                ctx.player1_port.req_send(data)
            ctx.ind.place_marble(x,y,1)
            ctx.goto(ctx.WAIT_P1_ROTATE)

        def error_req(self, ctx):
            data = ctx.codec_client.invalid_move_pdu()
            ctx.player1_port.req_send(data)
            ctx.goto(ctx.WAIT_P1_M_PLACE)

    class WAIT_P1_ROTATE(WAIT_COMMAND):

        def rotate_board_pdu(self, ctx, port, board, direction):
            if port != ctx.player1_port:
                data = ctx.codec_client.invalid_move_pdu()
                ctx.player1_port.req_send(data)
            ctx.ind.rotate_sub_board(board,direction)

        def nextturn_req(self,ctx): # controller calls
            data = ctx.codec_client.your_turn_pdu()
            ctx.player2_port.req_send(data)
            ctx.goto(ctx.WAIT_P2_M_PLACE)

        def error_req(self, ctx):
            data = ctx.codec_client.invalid_move_pdu()
            ctx.player1_port.req_send(data)
            ctx.goto(ctx.WAIT_P1_ROTATE)

    class WAIT_P2_M_PLACE(WAIT_COMMAND):

        def m_place_pdu(self, ctx, port, x, y):
            if port != ctx.player2_port:
                data = ctx.codec_client.invalid_move_pdu()
                ctx.player2_port.req_send(data)
            ctx.ind.place_marble(x,y,2)
            ctx.goto(ctx.WAIT_P2_ROTATE)

        def error_req(self, ctx):
            data = ctx.codec_client.invalid_move_pdu()
            ctx.player2_port.req_send(data)
            ctx.goto(ctx.WAIT_P2_M_PLACE)

    class WAIT_P2_ROTATE(WAIT_COMMAND):

        def rotate_board_pdu(self, ctx, port, board, direction):
            if port != ctx.player2_port:
                data = ctx.codec_client.invalid_move_pdu()
                ctx.player2_port.req_send(data)
            ctx.ind.rotate_sub_board(board,direction)

        def nextturn_req(self,ctx): # controller calls
            data = ctx.codec_client.your_turn_pdu()
            ctx.player1_port.req_send(data)
            ctx.goto(ctx.WAIT_P1_M_PLACE)

        def error_req(self, ctx):
            data = ctx.codec_client.invalid_move_pdu()
            ctx.player2_port.req_send(data)
            ctx.goto(ctx.WAIT_P2_ROTATE)

# Inputs that are sent to states

    ## from game

    def update_board_req(self, board_info):
        self._state.update_board_req(self, board_info)

    def invalid_move_req(self):
        self._state.error_req(self)

    def game_end_req(self, end_status):
        self._state.game_end_req(self, end_status)

    def nextturn_req(self):
        self._state.nextturn_req(self)

    ## from client

    def look_game_pdu(self, game_id):
        self._state.look_game_pdu(self, game_id)

    def m_place_pdu(self, port, x, y):
        self._state.m_place_pdu(self, port, x, y)

    def rotate_board_pdu(self, port, board, direction):
        self._state.rotate_board_pdu(self, port, board, direction)

    ## tcp indications

    def received_ind(self, port, data):
        self.codec_server.decode(data, port)

    def new_connection_ind(self, port):
        port.set_ind(self)
        if self.player1_port is None:
            self.player1_port = port
            return
        if self.player2_port is None:
            self.player2_port = port
            return

    def close_connection_ind(self, port):
        if port is not None:
            self._state.ind_close(self, port)
        if self.player1_port:
            self.player1_port.req_close()
        if self.player2_port:
            self.player2_port.req_close()
        self.player1_port = None
        self.player2_port = None

    def network_error_ind(self, port, code, reason):
        print("ind_error({}, {}, {}):".format(port, code, reason))

class CommServers(ITransInd):
    """ Connection multiplexer to servers.
    Support only one server/game at the time. 
    """
  
    def __init__(self,tcp):
        self.tcp = tcp
        self.server = CommServer(self,self.tcp)
        self.game = GameLogic(self.server)
        self.server.set_ind(self.game)

    def ind_recv(self, port, data):
        pass

    def ind_connect(self, port):
        self.server.ind_connect(port)

    def ind_close(self, port):
        pass

    def ind_error(self, port, code, reason):
        pass
