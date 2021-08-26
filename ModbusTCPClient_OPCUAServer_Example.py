#!/usr/bin/env python3

# source: https://github.com/FreeOpcUa/python-opcua/blob/master/examples/server-minimal.py
# source: https://pymodbus.readthedocs.io/en/latest/readme.html#example-code

import sys
sys.path.insert(0, "..")
import time


from opcua import ua, Server
from pymodbus.client.sync import ModbusTcpClient


if __name__ == "__main__":

    # setup our server
    opcuaserver = Server()
    opcuaserver.set_endpoint("opc.tcp://127.0.0.1:4841/freeopcua/server/")

    # setup our own namespace, not really necessary but should as spec
    uri = "http://examples.freeopcua.github.io"
    idx = opcuaserver.register_namespace(uri)

    # get Objects node, this is where we should put our nodes
    objects = opcuaserver.get_objects_node()

    # populating our address space
    myobj = objects.add_object(idx, "Siemens LOGO")
    myvar = myobj.add_variable(idx, "Temperature", 0,ua.VariantType.Float)
    #myvar.set_writable()    # Set MyVariable to be writable by clients

    # starting!
    opcuaserver.start()
    

    # setup Modbus TCP Client
    modbustcpclient = ModbusTcpClient('192.168.0.3',port=502)

    try:
        while True:
            result = modbustcpclient.read_holding_registers(528,1)

            if hasattr(result, 'message'):
                # modbus tcp communication error
                print (result.message)
            else:
                print("Temperature: ",result.registers[0]/10, " °C")

            myvar.set_value(result.registers[0]/10)

            time.sleep(2)
    finally:
        #close connection, remove subcsriptions, etc
        opcuaserver.stop()
        modbustcpclient.close()