import librosa
import pydub

print("something")


def main():
    file = librosa.util.example_audio_file()
    waveform, samplerate = librosa.load(file)
    tempo, beat_frames = librosa.beat.beat_track(waveform, samplerate)
    print(f"Estimated tempo: {tempo}")
    beat_times = librosa.frames_to_time(beat_frames, samplerate)
    print(beat_times)

if __name__ == "__main__":
    main()
