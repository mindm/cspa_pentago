#!/usr/bin/python3.2
# -*- coding: iso-8859-15 -*-

import socket
import threading


SIZE = 1024

class TCPServer:
    def __init__(self, address, port):
        self.address = address
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.backlog = 5
        
        self.sock.bind((address, port))
        self.sock.listen(self.backlog)
        
    # def accept(self):
    #     self.client, self.address = self.sock.accept()

    def loop(self):
        while 1:
            client = ClientThread(*self.sock.accept()).start()


class TCPClient():
    def __init__(self, address, port):
        self.address = address
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, host):
        self.sock.connect(host)

    def send(self, data):
        self.sock.send(data)

    def close(self):
        self.sock.close()

class ClientThread(threading.Thread):

    def __init__(self, client, address):
        self.client = client
        self.address = address
        super().__init__()

    def run(self):
        while 1:
            data = self.client.recv(1024)
            if data:
                print(data)

