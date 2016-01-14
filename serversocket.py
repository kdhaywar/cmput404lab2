#!/usr/bin/env python

import socket
import os
import sys
import select

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


serverSocket.bind(("0.0.0.0",12346))  #0.0.0.0 listen on all of them

serverSocket.listen(5)

while True:
    print "waiting for a fucking connection..."
    (incomingSocket, address) = serverSocket.accept()
    print "WE got a Mother fucking connection %s" % (str (address))

    pid = os.fork()

    if (pid == 0):
        #child
        outgoingSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        outgoingSocket.connect(("www.google.com", 80))

        response = bytearray()
        while True:
            incomingSocket.setblocking(0)
            try:
                part = incomingSocket.recv(1024)
            except IOError, exception:
                if exception.errno == 11:
                    part = None
                else:
                    raise
            if(part):
                response.extend(part)
                outgoingSocket.sendall(part)


            outgoingSocket.setblocking(0)
            try:
                part = outgoingSocket.recv(1024)
            except IOError, exception:
                if exception.errno == 11:
                    part = None
                else:
                    raise

            if(part):
                incomingSocket.sendall(part)
            select.select(
                [incomingSocket, outgoingSocket],
                [],
                [incomingSocket, outgoingSocket],
                1)
                

        print response
        sys.exit(0)
        
    else:
        #parent
        pass


