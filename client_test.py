#!/usr/bin/python3.2
# -*- coding: iso-8859-15 -*-

from transport import TCPClient
import threading

def hello():
	pass

if __name__ == "__main__":

	tcp = TCPClient("localhost", 1719)

	tcp.start()

	


	t = threading.Timer(3, hello)
	t.start()
	t.join()
	# tcp.send(bytes("Ping", "utf-8"))
	#tcp.sock.send(bytes("Ping", "utf-8"))
	t = threading.Timer(3, hello)
	t.start()
	t.join()
	tcp.req_send(bytes("Ping", "utf-8"))
	# tcp.sock.send(bytes("Ping", "utf-8"))
	# tcp.sock.send(bytes("Ping", "utf-8"))
	t = threading.Timer(3, hello)
	t.start()
	t.join()
	tcp.req_send(bytes("Ping", "utf-8"))
	# tcp.sock.send(bytes("Ping", "utf-8"))
	# tcp.sock.send(bytes("Ping", "utf-8"))
	t = threading.Timer(3, hello)
	t.start()
	t.join()
	tcp.req_send(bytes("Ping", "utf-8"))
	# tcp.sock.send(bytes("Ping", "utf-8"))
	# tcp.sock.send(bytes("Ping", "utf-8"))
	t = threading.Timer(3, hello)
	t.start()
	t.join()
	tcp.close_connection()
