import glob
import json
import subprocess
import time
from datetime import datetime, timezone

from opcua import Client


OPCUA_ENDPOINT = "opc.tcp://10.10.1.10:53530"

PI_TAILSCALE_IP = "100.93.20.9"
PI_PORT = 5000

READ_INTERVAL_SECONDS = 1

NODES = {
    "rod_position": "ns=5;s=CR_Position",
    "reactor_power": "ns=5;s=RX_ReactorPower",
    "reactor_setpoint": "ns=5;s=CTRL_RXPowerSetpoint",
    "reactor_pressure": "ns=5;s=RX_ReactorPress",
    "fuel_temperature": "ns=5;s=RX_FuelTemp",
    "mean_coolant_temperature": "ns=5;s=RX_MeanCoolTemp",
}


def find_tailscale_binary():
    matches = glob.glob(
        "/home/kqk5924/tailscale_*/tailscale"
    )

    if not matches:
        raise FileNotFoundError(
            "Could not find the Tailscale executable"
        )

    return matches[0]


def start_pi_connection(tailscale_binary):
    print("Connecting to Raspberry Pi...")

    return subprocess.Popen(
        [
            tailscale_binary,
            "--socket=/home/kqk5924/tailscaled.sock",
            "nc",
            PI_TAILSCALE_IP,
            str(PI_PORT),
        ],
        stdin=subprocess.PIPE,
        text=True,
        bufsize=1,
    )


def connect_to_ans():
    print("Connecting to ANS OPC UA server...")

    client = Client(OPCUA_ENDPOINT)
    client.connect()

    print("Connected to ANS OPC UA server")
    return client


def read_ans_data(client):
    payload = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "station": "01",
    }

    for field_name, node_id in NODES.items():
        value = client.get_node(node_id).get_value()
        payload[field_name] = float(value)

    return payload


def main():
    tailscale_binary = find_tailscale_binary()
    opcua_client = None
    pi_connection = None

    while True:
        try:
            if opcua_client is None:
                opcua_client = connect_to_ans()

            if (
                pi_connection is None
                or pi_connection.poll() is not None
            ):
                pi_connection = start_pi_connection(
                    tailscale_binary
                )

            payload = read_ans_data(opcua_client)
            message = json.dumps(payload)

            pi_connection.stdin.write(message + "\n")
            pi_connection.stdin.flush()

            print(message)

            time.sleep(READ_INTERVAL_SECONDS)

        except KeyboardInterrupt:
            print("\nStopping ANS-to-Pi bridge...")
            break

        except Exception as error:
            print(f"Bridge error: {error}")
            print("Reconnecting in 5 seconds...")

            if opcua_client is not None:
                try:
                    opcua_client.disconnect()
                except Exception:
                    pass
                opcua_client = None

            if pi_connection is not None:
                try:
                    pi_connection.terminate()
                except Exception:
                    pass
                pi_connection = None

            time.sleep(5)

    if opcua_client is not None:
        try:
            opcua_client.disconnect()
        except Exception:
            pass

    if pi_connection is not None:
        try:
            pi_connection.terminate()
        except Exception:
            pass


if __name__ == "__main__":
    main()
