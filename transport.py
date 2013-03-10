#!/usr/bin/python3.2
# -*- coding: iso-8859-15 -*-

import socket
import threading
#from interfaces import ITransReq
# from communication import CommClient
import queue
import select

SIZE = 1024

class ITransReq:

    def received_ind(self, port, data):
        print("{}: {}".format(port, data))




class TCPServer():
    def __init__(self, address, port):
        self.address = address
        self.port    = port
        self.sock    = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.backlog = 5
        self.game    = None
        
        self.sock.bind((address, port))
        self.sock.listen(self.backlog)
        
    # def accept(self):
    #     self.client, self.address = self.sock.accept()

    def loop(self):
        while 1:
            # client = ClientThread(*self.sock.accept()).start()
            client1 = self.sock.accept()
            print(client1)
            client2 = self.sock.accept()
            print(client2)

            self.game = ClientThread(client1, client2)
            self.game.start()
            self.game.req_send(bytes("from server", "utf-8"), 1)
            self.game.req_send(bytes("from server", "utf-8"), 2)



class TCPClient(ITransReq, threading.Thread):
    def __init__(self, address, port):
        self.address = address
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ind = None
        self.inputs  = []
        self.outputs = []
        self.message_queues = {}
        super().__init__()

    def open_connection(self, host):
        self.sock.connect(host)

    def req_send(self, data):
        self.message_queues[self.sock].put(data)
        self.outputs.append(self.sock)

    def close_connection(self):
        self.inputs.remove(self.sock)
        self.sock.close()

    def recv(self, size):
        return self.sock.recv(size)

    def set_ind(self, commclient):
        self.ind = commclient


    # Uses select-module to distinguish if socket is readable or writable
    # source: http://pymotw.com/2/select/
    def run(self):
        self.open_connection((self.address, self.port))
        self.sock.setblocking(0)
        self.inputs.append(self.sock)
        self.message_queues[self.sock] = queue.Queue()
        self.set_ind(ITransReq())

        while self.inputs:
            try:
                readable, writable, exceptional = select.select(self.inputs, self.outputs, self.inputs, 0)
            except select.error:
                pass
            for s in readable:
                data = s.recv(1024)
                if data:
                    print("received data '{}' from {}".format(data, s.getpeername()))
                    self.ind.received_ind(self.port, data)
                else:
                    print("closing connection {}".format(s.getpeername()))
                    self.inputs.remove(s)
                    if s in self.outputs:
                        self.outputs.remove(s)
                    s.close()
                    del self.message_queues[s]

            for s in writable:
                try:
                    next_msg = self.message_queues[s].get_nowait()
                except queue.Empty:
                    print("Error, queue empty")
                    pass
                else:
                    print("sending message '{}' to {}".format(next_msg, s.getpeername()))
                    self.outputs.remove(s)
                    s.send(next_msg)









class ClientThread(ITransReq, threading.Thread): #A server thread

    def __init__(self, client1, client2):
        self.client1      = client1[0]
        self.client2      = client2[0]
        self.client1_info = client1[1]
        self.client2_info = client2[1]
        self.ind = None
        self.inputs  = []
        self.outputs = []
        self.message_queues = {}
        super().__init__()


    def run(self):

        self.inputs.append(self.client1)
        self.inputs.append(self.client2)
        self.message_queues[self.client1] = queue.Queue()
        self.message_queues[self.client2] = queue.Queue()
        self.set_ind(ITransReq())

        while self.inputs:
            try:
                readable, writable, exceptional = select.select(self.inputs, self.outputs, self.inputs, 0)
            except select.error:
                pass
            for s in readable:
                data = s.recv(1024)
                if data:
                    print("received data '{}' from {}".format(data, s.getpeername()))
                    self.ind.received_ind(s.getpeername()[1], data)
                else:
                    print("closing connection {}".format(s.getpeername()))
                    self.inputs.remove(s)
                    if s in self.outputs:
                        self.outputs.remove(s)
                    s.close()
                    del self.message_queues[s]

            for s in writable:
                try:
                    next_msg = self.message_queues[s].get_nowait()
                except queue.Empty:
                    print("Error, queue empty")
                    pass
                else:
                    print("sending message '{}' to {}".format(next_msg, s.getpeername()))
                    self.outputs.remove(s)
                    s.send(next_msg)


    def set_ind(self, commserver):
        self.ind = commserver

    def req_send(self, data, player):
        if player == 1:
            self.message_queues[self.client1].put(data)
            self.outputs.append(self.client1)
        elif player == 2:
            self.message_queues[self.client2].put(data)
            self.outputs.append(self.client2)

    def close_connection(self):
        self.client1.close()
        self.client2.close()
        self.inputs.remove(self.client1)
        self.inputs.remove(self.client2)