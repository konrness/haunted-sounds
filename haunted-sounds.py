import logging
import math
from socketserver import TCPServer
from collections import defaultdict

from umodbus import conf
from umodbus.server.tcp import RequestHandler, get_server
from umodbus.utils import log_to_stream

import threading

import soundcard as sc
import soundfile as sf


# Add stream handler to logger 'uModbus'.
log_to_stream(level=logging.DEBUG)

# Enable values to be signed (default is False).
conf.SIGNED_VALUES = True

TCPServer.allow_reuse_address = True
app = get_server(TCPServer, ('192.168.86.34', 1502), RequestHandler)
print ("Server: ", app)

@app.route(slave_ids=[2], function_codes=[5], addresses=list(range(0, 1500)))
def play_sound(slave_id, function_code, address, value):
  print("Address: ", address)
  soundId, channel = decodeAddress(address)
  print("Playing sound: ", soundId, "to channel: ", channel)
  thread1 = myPlayer('soundplayer/sounds/' + str(soundId) + '.wav', channels=[channel, channel+1])
  thread1.start()


def decodeAddress(address):
    offset = 1001
    blockSize = 16

    address -= offset
    soundId = address % blockSize
    channel = math.floor(address / blockSize)

    return soundId, channel


speaker = sc.get_speaker("X-USB")
print("Speaker")
print(speaker)

class myPlayer(threading.Thread):
   def __init__(self, soundFile, channels):
      threading.Thread.__init__(self)
      self.soundFile = soundFile
      self.channels = channels
   def run(self):
      playSound(self.soundFile, self.channels)


def playSound(soundFile, channels):
   print("Playing " + soundFile + "to channels: ", channels)

   # load sound file
   data, samplerate = sf.read(soundFile)

   with speaker.player(samplerate=samplerate, channels=channels, blocksize=128) as player:
      player.play(data, wait=True)


if __name__ == '__main__':
    try:
        print("Starting ModBus Server...")
        app.serve_forever()
    finally:
        app.shutdown()
        app.server_close()

