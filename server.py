#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import socketserver
import sys


PORT = int(sys.argv[1])

if len(sys.argv) < 2:
    print("Usage: pyhton3 server.py PORT")


class SIPRegisterHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """

    dic_client = {}

    def handle(self):
        """
        handle method of the server class
        (all requests will be handled by this method)
        """
        self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
        for line in self.rfile:
            if line:
                if line.decode('utf-8')[:8] == 'REGISTER':
                    ip_user = line.decode('utf-8')[13:-10]
                    self.dic_client[ip_user] = self.client_address[0]
                elif line.decode('utf-8')[:7] == 'Expires':                
                    if line.decode('utf-8').split(' ')[1][0] == '0':
                        del self.dic_client[ip_user]
            print(line.decode('utf-8'), end="")
        print(self.dic_client)

if __name__ == "__main__":
    # Listens at localhost ('') port 6001 
    # and calls the EchoHandler class to manage the request
    serv = socketserver.UDPServer(('', PORT), SIPRegisterHandler) 

    print("Lanzando servidor UDP de eco...")
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Finalizado servidor")
