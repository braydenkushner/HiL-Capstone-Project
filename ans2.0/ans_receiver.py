import json
import socket
from datetime import datetime

HOST = "0.0.0.0"
PORT = 5000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen()

    print(f"Waiting for ANS JSON data on port {PORT}...")

    while True:
        connection, address = server.accept()

        with connection:
            buffer = ""

            while True:
                chunk = connection.recv(4096)

                if not chunk:
                    break

                buffer += chunk.decode("utf-8")

                while "\n" in buffer:
                    message, buffer = buffer.split("\n", 1)
                    message = message.strip()

                    if not message:
                        continue

                    try:
                        data = json.loads(message)

                        print("\n--- ANS Live Data ---")
                        print("Received:", datetime.now().isoformat(timespec="seconds"))
                        print("Station:", data.get("station"))
                        print("Rod position:", data.get("rod_position"))
                        print("Reactor power:", data.get("reactor_power"))
                        print("Reactor setpoint:", data.get("reactor_setpoint"))
                        print("Reactor pressure:", data.get("reactor_pressure"))
                        print("Fuel temperature:", data.get("fuel_temperature"))
                        print(
                            "Mean coolant temperature:",
                            data.get("mean_coolant_temperature"),
                        )

                    except json.JSONDecodeError as error:
                        print("Invalid JSON:", error)
                        print("Raw message:", message)
