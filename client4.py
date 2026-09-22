"""
Filename: client4.py
Description: Read ReactorPower values from OPCUA server and change LED value based on them
"""

from opcua import Client
from gpiozero import LED
from time import sleep

led = LED(17)

# TODO: input proper PC IP
client = Client("opc.tcp://10.0.0.102:4840")

client.connect()

# Get ReactorPower
power = client.get_node(
    "ns=2;i=1"
    )

# Get power value and update LED value
try:
    while True:
        value = power.get_value()

        print("Power =", value)

        if value > 50:
            led.on()
        else:
            led.off()

        sleep(1)

finally:
    led.off()
    client.disconnect()
