#! /usr/local/bin/python

import time
from threading import Thread, Lock
import numpy as np
import cv2
import sys
import socket

ROWS = 320
COLS = 240
CLRS = 3
SIZE = ROWS*COLS*CLRS

cap = cv2.VideoCapture(0)
cap.set(3,ROWS)
cap.set(4,COLS)

go = True
lock = Lock()

def setGo(val):
	global go
	global lock
	lock.acquire()
	go = val
	lock.release()

def getGo():
	global go
	global lock
	lock.acquire()
	val = go
	lock.release()
	return val


def setUpServer(ip,port):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         # Create a socket object
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.bind((ip, port))        # Bind to the port
	s.listen(1)                 # Now wait for client connection.
	c, addr = s.accept()
	return c

def setUpClient(ip, port):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         # Create a socket object
	s.connect((ip, port))
	return s

def displayThread(ip, port):
	s = setUpClient(ip, port)
	while(True):
		raw = str()
		for i in range(ROWS):
			raw += s.recv(COLS*CLRS)
		trash = [ord(x) for x in raw]
		npraw = np.array(trash)
		data = npraw.reshape((COLS,ROWS,CLRS))
		data = data.astype(np.uint8)
		cv2.imshow('crappy skype', data)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			setGo(False)
			break

def captureThread(ip, port):
	c = setUpServer(ip,port)
	global cap
	global go
	while(getGo()):
    # Capture frame-by-frame
		ret, raw = cap.read()
    # Our operations on the frame come here
		flipped = cv2.flip(raw, 1)
		
		flat = np.reshape(flipped,(ROWS,COLS*CLRS))
		try:
			for i in range(ROWS):
				bytes = flat[i,:].tobytes()
				c.send(bytes)
		except:
			print 'there was a frame dropped'
	return


def main():
	serverIP = socket.gethostbyname(socket.gethostname())
	if len(sys.argv) == 1 :
		clientIP = serverIP
	else:
		clientIP = sys.argv[1]

	port = 5002
	
	t1 = Thread(target=captureThread, args=(serverIP, port))
	t1.start()
	time.sleep(.1)
	displayThread(clientIP,port)
	t1.join()
	global cap
	cap.release()
	cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
