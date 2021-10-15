import logging
import math
from socketserver import TCPServer
from collections import defaultdict

from umodbus import conf
from umodbus.server.tcp import RequestHandler, get_server
from umodbus.utils import log_to_stream

# Add stream handler to logger 'uModbus'.
log_to_stream(level=logging.DEBUG)

# A very simple data store which maps addresss against their values.
data_store = defaultdict(int)

# Enable values to be signed (default is False).
conf.SIGNED_VALUES = True

print("Starting ModBus Server...")
TCPServer.allow_reuse_address = True
app = get_server(TCPServer, ('192.168.86.34', 1502), RequestHandler)
print ("Server: ", app)

@app.route(slave_ids=[2], function_codes=[5], addresses=list(range(0, 1500)))
def play_sound(slave_id, function_code, address, value):
  print("Address: ", address)
  soundId, channel = decodeAddress(address)
  print("Playing sound: ", soundId, "to channel: ", channel)



def decodeAddress(address):
    offset = 1001
    blockSize = 16

    address -= offset
    soundId = address % blockSize
    channel = math.floor(address / blockSize)

    return soundId, channel


print("Decode test:")

print("1001: ", decodeAddress(1001)) # should be soundId 0, channel 0
print("1033: ", decodeAddress(1033)) # should be soundId 0, channel 2
print("1076: ", decodeAddress(1076)) # should be soundId 11, channel 4


if __name__ == '__main__':
    try:
        app.serve_forever()
    finally:
        app.shutdown()
        app.server_close()