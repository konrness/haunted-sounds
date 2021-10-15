import threading

import soundcard as sc
import soundfile as sf

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
      print("Playing")
      player.play(data, wait=True)


thread1 = myPlayer('sounds/wolf2.wav', channels=[0,2,4])
thread1.start()

thread2 = myPlayer('sounds/heartbeat.wav', channels=[1,3,5])
thread2.start()

input("Waiting...")
# player = speaker.player(samplerate=samplerate, channels=[0,2,4,6], blocksize=128)
# player.play(data, wait=False)

