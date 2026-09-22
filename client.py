"""
Filename: client.py
Description: test connection with OPCUA server on another PC over TCP/IP
Author: Copilot (User: Brayden Kushner)
Date: 2026-09-22

"""

from opcua import Client

# TODO: put in proper IP of PC
url = "opc.tcp://10.0.0.102:4840"

client = Client(url)

# Attempt to connect to server & get root node
try:
    client.connect()

    print("Connected")

    root = client.get_root_node()

    print(root)

finally:
    client.disconnect()
