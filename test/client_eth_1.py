"""
Filename: client_eth_1.py
Description: OPC UA client that communicates with Windows PC server via Ethernet and lights up an LED
Author: Copilot (User Brayden Kushner)
Date: 2026-09-22
"""
from opcua import Client
from gpiozero import LED
from time

# TODO: User sets these variables
SERVER_IP = "192.168.56.1"
NAMESPACE_IDX = 2
LED_PIN = 17

led = LED(LED_PIN)
client = Client(f"opc.tcp://{SERVER_IP}:4840/freeopcua/server/")

# Connect to the server
try:
    client.connect()
    print("Connected to OPC UA server")

    objects = client.get_objects_node()
    power_var = objects.get_child([f"{NAMESPACE_IDX}:Power"])

    while True:
        power = power_var.get_value()
        print(f"Power: {power}")

        if power > 50:
            led.on()
        else:
            led.off()

        time.sleep(1)

except KeyboardInterrupt:
    print("\nStopping Client...")

except Exception as e:
    print(f"Connection error: {e}")

finally:
    led.off()
    client.disconnect()
