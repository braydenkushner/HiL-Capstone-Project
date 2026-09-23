
from opcua import Server
import time

server = Server()

server.set_endpoint("opc.tcp://0.0.0.0:4840")

uri = "NuclearSimulator"
idx = server.register_namespace(uri)

objects = server.get_objects_node()

power = objects.add_variable(idx, "ReactorPower", 0)
power.set_writable()

server.start()

value = 0

while True:
        power.set_value(value)

        print("Power =",value)

        value += 10

        if value > 100:
            value = 0

        time.sleep(2)

