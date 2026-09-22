"""
Filename: client2.py
Description: Connect to OPCUA Server on PC and get nodes
Author: Copilot (User Brayden Kushner)
Date: 2026-09-22
"""


from opcua import Client

# TODO: update PC IP
client = Client("opc.tcp://10.0.0.102:4840")

client.connect()

root = client.get_root_node()

# Print the children
for child in root.get_children():
    print(child)

client.disconnect()
