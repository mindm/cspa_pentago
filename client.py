#!/usr/bin/python3.2
# -*- coding: iso-8859-15 -*-

from transport import TCPClient
import threading

def hello():
	pass



if __name__ == "__main__":

	tcp = TCPClient("localhost", 1719)

	tcp.connect(("localhost", 1719))

	while 1:
		data = tcp.recv(1024)
		if data:
			print(data)

		t = threading.Timer(10, hello)
		t.start()
		t.join()
		tcp.send(bytes("Ping", "utf-8"))
