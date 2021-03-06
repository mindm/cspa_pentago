#!/usr/bin/python3.2
# -*- coding: iso-8859-15 -*-

import inspect # http://docs.python.org/3/library/inspect.html
import threading # http://docs.python.org/3/library/threading.html
from model import GameLogic
from interfaces import *
from pdu_codecs import ClientPduCodec, ServerPduCodec
import sys

def wait():
    print("debug wait")

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
        self.ui = None
        self.codec_server = ServerPduCodec(self)
        self.codec_client = ClientPduCodec(self)
        ## variables
        self.lock = threading.Lock()
        tcp.set_ind(self)

    def set_ui(self,ui):
        self.ui = ui

    class State: # default actions
        
        def name(self): 
            return self.__class__.__name__

        # add methods with error-messages for each state

    # waiting for game to starts
    class WAIT_UI_START(State):

        def look_game_req(self, ctx):
            #ctx.port = ctx.tcp.port(addr,port,ctx)
            data = ctx.codec_server.look_game_pdu()
            ctx.goto(ctx.LOOK_GAME)
            ctx.tcp.req_send(data)

        def game_end_pdu(self, ctx, player):
            sys.exit(0)

#    class WAIT_CONN_IND(State):

#        def new_connection_ind(self, ctx, port):
#            assert ctx.port == port
#            data = ctx.codec_server.look_game_pdu()
#            ctx.port.req_send(data)
#            ctx.goto(ctx.LOOK_GAME)

#        def close_connection_ind(self, ctx, port):
#            ctx.goto(ctx.WAIT_UI_START)

#        def network_error_ind(self, ctx, port, code, reason):
#            ctx.port = None
#            ctx.goto(ctx.WAIT_UI_START)

    # client waiting for connection to server
    class LOOK_GAME(State):

        # when second player found goto WAIT_MY_TURN
        def start_game_pdu(self, ctx):
            ctx.ui.start_game_ind()
            ctx.goto(ctx.WAIT_MYTURN)

    # player waiting for turn or server calculating changes
    class WAIT_MYTURN(State):

        # board is updated after opponent's m_place or rotate
        def update_board_pdu(self, ctx, board_info):
            ctx.ui.update_board_ind(board_info)
            ctx.goto(ctx.WAIT_MYTURN) 

        # player's turn starts or it's time to rotate
        def your_turn_pdu(self, ctx):
            ctx.ui.your_turn_ind()
            ctx.goto(ctx.WAIT_UI)

        # game tells that the move was invalid
        def invalid_move_pdu(self, ctx):
            ctx.ui.invalid_move_ind()
            ctx.goto(ctx.WAIT_UI)

        # game ends - victory, loss, or draw
        def game_end_pdu(self, ctx, end_status):
            ctx.ui.game_end_ind(end_status)
            #ctx.goto(ctx.WAIT_UI_START)            

    # client waiting for user input
    class WAIT_UI(State):

        # user places marble
        def m_place_req(self, ctx, x, y):
            data = ctx.codec_server.m_place_pdu(x, y)
            ctx.tcp.req_send(data)
            ctx.goto(ctx.WAIT_UI)

        # board is updated after current user's input
        def update_board_pdu(self, ctx, board_info):
            ctx.ui.update_board_ind(board_info)
            ctx.goto(ctx.WAIT_UI)

        # user rotates board
        def rotate_board_req(self, ctx, board, direction):
            ctx.goto(ctx.WAIT_MYTURN)
            data = ctx.codec_server.rotate_board_pdu(board, direction)
            ctx.tcp.req_send(data)

        # game tells that the move was invalid
        def invalid_move_pdu(self, ctx):
            ctx.ui.invalid_move_ind()
            ctx.goto(ctx.WAIT_UI)

        # game ends - victory, loss, or draw
        def game_end_pdu(self, ctx, end_status):
            ctx.ui.game_end_ind(end_status)
            ctx.goto(ctx.WAIT_UI_START) 

# Inputs that are sent to states
  
  ## GUI inputs
  
    def look_game_req(self): # STATES
        self._state.look_game_req(self)
      
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
        self._state.close_connection_ind(self, port)

    def networ_error_ind(self, port, code, reason): 
        self._state.ind_error(self, port, code, reason)

# Communication layer server

class CommServer(IGameCommServerReq, IGameCommServerPdu, EntityMix):
    def __init__(self,tcp, p1, p2):
        ## server data
        self.tcp = tcp
        #self.listen = tcp.listen(tcpport,self)
        self.player1_port = p1
        self.player2_port = p2
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

        def close_connection_ind(self, ctx, port):
            if port == ctx.player1_port:
                if ctx.player2_port:
                    data = ctx.codec_client.game_end_pdu(2)
                    ctx.tcp.req_send(data, ctx.player2_port)
            else:
                if ctx.player1_port:
                    data = ctx.codec_client.game_end_pdu(1)
                    ctx.tcp.req_send(data, ctx.player1_port)

        def m_place_pdu(self, ctx, port, x, y):
            print("Wrong state")

        # add methods with error-messages for each state

    class GAME_END(State):

        def close_connection_ind(self, ctx, port):
            pass



    class WAIT_PLAYER1(State):
    
        def look_game_pdu(self, ctx):
            ctx.goto(ctx.WAIT_PLAYER2)
    
    class WAIT_PLAYER2(State):
    
        def look_game_pdu(self, ctx):
            ##
            data = ctx.codec_client.start_game_pdu()
            ctx.tcp.req_send(data, ctx.player1_port)
            ##
            data = ctx.codec_client.start_game_pdu()
            ctx.tcp.req_send(data, ctx.player2_port)
            ##
            data = ctx.codec_client.your_turn_pdu()
            ctx.tcp.req_send(data, ctx.player1_port)
            ctx.goto(ctx.WAIT_P1_M_PLACE)
    
    class WAIT_COMMAND(State):

        def game_end_req(self, ctx, end_status):
            data = ctx.codec_client.game_end_pdu(end_status)
            ctx.tcp.req_send(data, ctx.player1_port)
            data = ctx.codec_client.game_end_pdu(end_status)
            ctx.tcp.req_send(data, ctx.player2_port)
            #elif end_status == 2: # player 2 won
               #data = ctx.codec_client.game_end_pdu(end_status)
                #ctx.player1_port.req_send(data)
                #data = ctx.codec_client.game_end_pdu(end_status)
                #ctx.player2_port.req_send(data)
            #else: # draw
                #data = ctx.codec_client.game_end_pdu(end_status)
                #ctx.player1_port.req_send(data)
                #data = ctx.codec_client.game_end_pdu(end_status)
                #ctx.player2_port.req_send(data)

            # reset game
            #ctx.ind.reset_ind()
            # close connections
            #ctx.close_connection_ind(None) - IMPLEMENT THIS  
            # new game
            ctx.goto(ctx.GAME_END)
            print("Game end")

        def update_board_req(self, ctx, board_info):
            data = ctx.codec_client.update_board_pdu(board_info)
            ctx.tcp.req_send(data, ctx.player1_port)
            ctx.tcp.req_send(data, ctx.player2_port)

      
        # def close_connection_ind(self, ctx, port):
        #     if port == ctx.player1_port: # p1 disconnected, p2 won
        #         data = ctx.codec_client.game_end_pdu(2)
        #         ctx.tcp.req_send(data, ctx.player2_port)
        #     else: # p2 disconnected, p1 won
        #         data = ctx.codec_client.game_end_pdu(1)
        #         ctx.tcp.req_send(data, ctx.player1_port)
        #     ctx.ind.reset_ind() # reset game
        #     ctx.goto(ctx.WAIT_PLAYER1) # new game     
    
    class WAIT_P1_M_PLACE(WAIT_COMMAND):

        def m_place_pdu(self, ctx, port, x, y):
            #if port != ctx.player1_port: # if not your turn send error
                #data = ctx.codec_client.invalid_move_pdu()
                #ctx.tcp.req_send(data, ctx.player1_port)
            check = ctx.ind.place_marble(x,y,1)
            if check == True: # move to next state if move was valid
                ctx.goto(ctx.WAIT_P1_ROTATE)

        def rotate_board_pdu(self, ctx, port, board, direction):
            #if port != ctx.player1_port:
                #data = ctx.codec_client.invalid_move_pdu()
                #ctx.tcp.req_send(data, ctx.player1_port)
            #ctx.ind.rotate_sub_board(board,direction)
            self.invalid_move_req(ctx)

        def invalid_move_req(self, ctx):
            data = ctx.codec_client.invalid_move_pdu()
            ctx.tcp.req_send(data, ctx.player1_port)
            ctx.goto(ctx.WAIT_P1_M_PLACE)

    class WAIT_P1_ROTATE(WAIT_COMMAND):

        def rotate_board_pdu(self, ctx, port, board, direction):
            #if port != ctx.player1_port:
                #data = ctx.codec_client.invalid_move_pdu()
                #ctx.tcp.req_send(data, ctx.player1_port)
            ctx.ind.rotate_sub_board(board,direction)

        def nextturn_req(self,ctx):
            data = ctx.codec_client.your_turn_pdu()
            ctx.tcp.req_send(data, ctx.player2_port)
            ctx.goto(ctx.WAIT_P2_M_PLACE)

        def invalid_move_req(self, ctx):
            data = ctx.codec_client.invalid_move_pdu()
            ctx.tcp.req_send(data, ctx.player1_port)
            ctx.goto(ctx.WAIT_P1_ROTATE)

    class WAIT_P2_M_PLACE(WAIT_COMMAND):

        def m_place_pdu(self, ctx, port, x, y):
            #if port != ctx.player2_port:
                #data = ctx.codec_client.invalid_move_pdu()
                #ctx.tcp.req_send(data, ctx.player2_port)
            check = ctx.ind.place_marble(x,y,2)
            if check == True: # move to next state if move was valid
                ctx.goto(ctx.WAIT_P2_ROTATE)

        def rotate_board_pdu(self, ctx, port, board, direction):    
            self.invalid_move_req(ctx)

        def invalid_move_req(self, ctx):
            data = ctx.codec_client.invalid_move_pdu()
            ctx.tcp.req_send(data, ctx.player2_port)
            ctx.goto(ctx.WAIT_P2_M_PLACE)

    class WAIT_P2_ROTATE(WAIT_COMMAND):

        def rotate_board_pdu(self, ctx, port, board, direction):
            #if port != ctx.player2_port:
                #data = ctx.codec_client.invalid_move_pdu()
                #ctx.tcp.req_send(data, ctx.player2_port)
            ctx.ind.rotate_sub_board(board,direction)

        def nextturn_req(self,ctx):
            data = ctx.codec_client.your_turn_pdu()
            ctx.tcp.req_send(data, ctx.player1_port)
            ctx.goto(ctx.WAIT_P1_M_PLACE)

        def invalid_move_req(self, ctx):
            data = ctx.codec_client.invalid_move_pdu()
            ctx.tcp.req_send(data, ctx.player2_port)
            ctx.goto(ctx.WAIT_P2_ROTATE)

# Inputs that are sent to states

    ## from game

    def update_board_req(self, board_info):
        self._state.update_board_req(self, board_info)

    def invalid_move_req(self):
        self._state.invalid_move_req(self)

    def game_end_req(self, end_status):
        self._state.game_end_req(self, end_status)

    def nextturn_req(self):
        self._state.nextturn_req(self)

    ## from client

    def look_game_pdu(self):
        self._state.look_game_pdu(self)

    def m_place_pdu(self, port, x, y):
        self._state.m_place_pdu(self, port, x, y)

    def rotate_board_pdu(self, port, board, direction):
        self._state.rotate_board_pdu(self, port, board, direction)

    ## tcp indications

    def received_ind(self, data, port):
        self.codec_server.decode(data, port)

    #not in use
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
            self._state.close_connection_ind(self, port)
        #self.tcp.req_close_connection()
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

    def received_ind(self, port, data):
        pass

    def new_connection_ind(self, port):
        self.server.ind_connect(port)

    def close_connection_ind(self, port):
        pass

    def network_error_ind(self, port, code, reason):
        pass
