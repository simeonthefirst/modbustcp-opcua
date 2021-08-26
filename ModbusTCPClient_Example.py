#!/usr/bin/env python3

# source: https://pymodbus.readthedocs.io/en/latest/readme.html#example-code

from pymodbus.client.sync import ModbusTcpClient
import time

client = ModbusTcpClient('192.168.0.3',port=502)

while(True):
    result = client.read_holding_registers(528,1)
    if hasattr(result, 'message'):
        # communication error
        print (result.message)
    else:
        print(result.registers[0])
    time.sleep(2)

client.close()