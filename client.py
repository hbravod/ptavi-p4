#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Programa cliente UDP que abre un socket a un servidor
"""

import socket
import sys


if len(sys.argv) < 4:
    print("Usage: pyhton3 client.py SERVER PORT LINE")

# Constantes. Dirección IP del servidor y contenido a enviar
SERVER = sys.argv[1] #'localhost'
PORT = int(sys.argv[2]) #puerto
LINE = ' '.join(sys.argv[4:]) #'¡Hola mundo!'

# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket:
    my_socket.connect((SERVER, int(PORT)))
    print("Enviando:", LINE)
    if sys.argv[3] == "register":
        my_socket.send(bytes('REGISTER sip:'+LINE +' SIP/2.0\r\n\r\n',                                                                                          'utf-8') + b'\r\n')
    data = my_socket.recv(1024)
    print('Recibido -- ', data.decode('utf-8'))

print("Socket terminado.")
