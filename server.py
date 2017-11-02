#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import json
import socketserver
import sys
import time


PORT = int(sys.argv[1])

if len(sys.argv) < 2:
    print("Usage: pyhton3 server.py PORT")


class SIPRegisterHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """
    dic_client = {}

    def json2registered(self):
        """
        compruebe si hay un fichero llamado
        registered.json. Si existe, se leer ́a su contenido y se usará como
        diccionario de usuarios registrados.
        """
        try:
            with open('registered.json', 'r') as archivo:
                self.dic_client = json.load(archivo)
                self.expired()
        except (NameError, FileNotFoundError):
            pass

    def register2json(self):
        """
        Cada vez que un usuario se registre o se dé de baja,
        se imprimirá en el fichero registered.json con información
        sobre el usuario, su dirección y la hora de expiración.
        """
        self.expired()
        json.dump(self.dic_client, open('registered.json', "w"))

    def expired(self):
        """
        Darse de baja en el servidor.
        """
        expirados = []
        time_act = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))
        for usuarios in self.dic_client:
            if self.dic_client[usuarios][1] < time_act:
                expirados.append(usuarios)
        for usuarios in expirados:
            del self.dic_client[usuarios]

    def handle(self):
        """
        handle method of the server class
        (all requests will be handled by this method)
        """
        self.json2registered()
        self.expired()
        for line in self.rfile:
            mensaje = line.decode('utf-8').split()
            if mensaje:
                if mensaje[0] == 'REGISTER':
                    user = mensaje[1][4:]
                    direccion = self.client_address[0]
                if mensaje[0] == 'Expires:':
                    if mensaje[1] != '0':
                        expire = time.strftime('%Y-%m-%d %H:%M:%S+%Z',
                                               time.gmtime(time.time() +
                                                           int(mensaje[1])))
                        self.dic_client[user] = ['address: ' + direccion,
                                                 'expires: ' + expire]
                        self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
                    elif mensaje[1] == '0':
                        try:
                            del self.dic_client[user]
                            self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
                        except KeyError:
                            self.wfile.write(b"SIP/2.0 404 USER"
                                             b"NOT FOUND\r\n\r\n")
            print(line.decode('utf-8'), end="")
        print(self.dic_client)
        self.register2json()
if __name__ == "__main__":
    # Listens at localhost ('') port 6001
    # and calls the EchoHandler class to manage the request
    serv = socketserver.UDPServer(('', PORT), SIPRegisterHandler)

    print("Lanzando servidor UDP de eco...")
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Finalizado servidor")
