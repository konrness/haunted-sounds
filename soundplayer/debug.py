import soundcard as sc
import soundfile as sf
import time
import threading

# get a list of all speakers:
speakers = sc.all_speakers()

print("Speakers\n")
print(speakers)

speaker = sc.get_speaker("X-USB")
print("Speaker")
print(speaker)

channels = speaker.channels
print("Channels")
print(channels)

# load sound file
data, samplerate = sf.read('sounds/wolf2.wav')
print("Samplerate:")
print(samplerate)

player = speaker.player(samplerate=samplerate, channels=[0,2,4,6])
with speaker.player(samplerate=samplerate, channels=[0,2,4,6], blocksize=128) as player:
  player.play(data, wait=False)
  while(player._queue):
    time.sleep(0.001)

# player = speaker.player(samplerate=samplerate, channels=[0,2,4,6], blocksize=128)
# player.play(data, wait=False)

