# Modbus TCP Client - OPC UA Server Example

```ModbusTCPClient_OPCUAServer_simple.py``` is an example how an adapter between a Modbus TCP Server (Master) and an OPC CLient could be realised with python.
Therefore the adapter contains a Modbus TCP Client and a OPC UA Server.
For tests of the script a Siemens LOGO with a Modbus TCP Server and a PT100 Temperature Sensor was used.
As a OPC UA Client UaExpert was used: <https://www.unified-automation.com/de/produkte/entwicklerwerkzeuge/uaexpert.html>

## Libraries

python-opcua: <https://github.com/FreeOpcUa/python-opcua>

pymodbus: <https://github.com/riptideio/pymodbus>
