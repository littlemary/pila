import base64

from pyModbusTCP.client import ModbusClient
from pyModbusTCP.utils import encode_ieee, long_list_to_word

c = ModbusClient(host='10.0.6.10', port=502, unit_id=1, auto_open=True)
if not c.is_open():
    if not c.open():
        print("unable to connect to host:port")
    if c.is_open():
       print("connect ok")
if c.is_open():
    reg_val = 0x1e0f3
    res = [243, 224]
    c.wr
    c.write_multiple_registers(6, res)
