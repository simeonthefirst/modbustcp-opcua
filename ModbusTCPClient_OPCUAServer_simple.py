#!/usr/bin/env python3

# used source: https://github.com/FreeOpcUa/python-opcua/blob/master/examples/server-minimal.py
# used source: https://pymodbus.readthedocs.io/en/latest/readme.html#example-code

import sys
sys.path.insert(0, "..")
import time

from opcua import ua, Server
from pymodbus.client.sync import ModbusTcpClient


opcua_ip_port="127.0.0.1:4841"
modbus_ip = "192.168.0.3"

if __name__ == "__main__":

    # setup our server
    opcua_server = Server()
    opcua_server.set_endpoint("opc.tcp://" + opcua_ip_port + "/freeopcua/server/")

    # setup our own namespace, not really necessary but should as spec
    uri = "http://examples.freeopcua.github.io"
    idx = opcua_server.register_namespace(uri)

    # get Objects node, this is where we should put our nodes
    objects = opcua_server.get_objects_node()

    # populating our address space
    object_node = objects.add_object(idx, "Siemens LOGO")
    variable_node = object_node.add_variable(idx, "Temperature", 0,ua.VariantType.Float)
    #variable_node.set_writable()    # Set MyVariable to be writable by clients

    # starting!
    opcua_server.start()
    print("OPC UA Server running on: "+ opcua_server.endpoint)
    

    # setup Modbus TCP Client
    modbustcp_client = ModbusTcpClient(modbus_ip, port=502)
    print("Modbus TCP Client running on: " + modbus_ip + ":502")

    try:
        while True:
            result = modbustcp_client.read_holding_registers(528, 1)

            if hasattr(result, 'message'):
                # modbus tcp communication error
                print (result.message)
            else:
                print("Temperature: ", result.registers[0]/10, " °C")

            variable_node.set_value(result.registers[0]/10)

            time.sleep(2)
    finally:
        #close connection, remove subscriptions, etc
        opcua_server.stop()
        modbustcp_client.close()