#!/usr/bin/env python3


import socket

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_obj:
    socket.setdefaulttimeout(1)
    result = socket_obj.connect_ex((addr, port))
