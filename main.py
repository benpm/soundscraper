from random import randint
from time import sleep, time
import sched
from hueInterface import createBridgeConn, setLight, flashLight
import librosa
from audioStream import AudioStream

def main():
    print("Loading file...")
    audioStream = AudioStream("test.wav")
    waveform, samplerate = librosa.load("test.wav")
    
    print("Detecting beats...")
    tempo, beat_frames = librosa.beat.beat_track(waveform, samplerate)
    
    print("Converting beat sample idices to times...")
    beat_times = librosa.frames_to_time(beat_frames, samplerate)

    # check for a credential file / create conn
    bridge = createBridgeConn("auth.txt", "10.0.0.91")

    # create a lights resource
    lights = bridge.lights

    # Turn on all lights, set brightness to max, min transition time
    for index in range(1, 4):
        setLight(lights[index], bri=254, transitiontime=0, on=True)

    scheduler = sched.scheduler(time, sleep)

    for sec, index in zip(beat_times, range(len(beat_times))):
        scheduler.enter(sec, 1, flashLight, argument=(lights, index % 3 + 1), kwargs={'hue': randint(0, 65535)})

    print("Starting track and running events...")
    audioStream.start()
    scheduler.run()

if __name__ == "__main__":
    main()