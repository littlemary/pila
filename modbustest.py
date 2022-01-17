from pyModbusTCP.client import ModbusClient
from pyModbusTCP.utils import encode_ieee, long_list_to_word

c = ModbusClient(host='10.0.6.10', port=502, unit_id=1, auto_open=True)
if not c.is_open():
    if not c.open():
        print("unable to connect to host:port")
    if c.is_open():
       print("connect ok")
if c.is_open():

    c.write_single_register(3,3)

