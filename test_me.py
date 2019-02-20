from pydub import AudioSegment

def extract_audio_data(audio_path, file_type):
	if file_type != "wav" and file_type != "mp3":
		print("File type must either be mp3 or wav, returning nulls")
		return None, None, None
	else:
		sound = AudioSegment.from_file(audio_path, file_type)
		return sound.get_array_of_samples(), sound.frame_rate, sound.channels

raw_audio, sample_rate, num_channels = extract_audio_data("wilhelm.wav", "wav")
print("Number of samples in audio data = %d" % len(raw_audio))
print("Sample Rate = %d\nNumber of Channels = %d" % (sample_rate, num_channels))

