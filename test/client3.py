"""
Filename: client3.py
Description: Read and output ReactorPower variable from OPCUA Server
Author: Copilot (User Brayden Kushner)
Date: 2026-09-22
"""

from opcua import Client
import time

# TODO: input PC IP
client = Client("opc.tcp://10.0.0.102:4840")

client.connect()

# Get power
power = client.get_node(
        "ns=2;i=1"
        )

# Print power value
while True:
    value = power.get_value()
    print("Power =",value)

    time.sleep(1)
