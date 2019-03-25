"Takes samples and creates a chromagram, from which a sequence of notes is extracted and returned"

import librosa
import librosa.display as ld
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import rc


THRESHOLD = 0.9

def main():
	y, sr = librosa.load("./music.wav", mono=True)
	notes = get_notes(y, sr)


def get_notes(y, sr):
	y_harmonic = librosa.effects.harmonic(y)
	chroma = librosa.feature.chroma_cqt(y=y_harmonic, sr=sr, threshold=THRESHOLD)
	duration = librosa.get_duration(y=y, sr=sr)
	num_columns = len(chroma[0])
	num_rows = len(chroma)

	new_chroma = chroma.copy()

	# Zeros out everything that is below 0.75 for clarity purposes
	for i in range(num_rows):
		for j in range(num_columns):
			if (chroma[i][j] < THRESHOLD):
				chroma[i][j] = 0
				
			new_chroma[i][j] = 0

	tuple_list = []
	note_row = 0 # 0,1,2,3,... ---> C,C#,D,D#,...

	for n in range(num_rows):

		num_zeros = 0
		note_length = 0
		start_index = 0
		current_index = 0
		i = 0

		while (i < num_columns):

			# Found a value that could lead to possible note
			if (chroma[note_row][i] > 0.0):
				num_zeros = 0
				note_length = 0

				# By incrementing the current_index and checking for zeros,
				# we allow only 3 zeros in the middle of notes and continue
				# to increment note_length until 3 zeros are found.
				while (num_zeros != 2):
					if (current_index > (num_columns) - 1):
						break
					if (chroma[note_row][current_index] == 0.0):
						num_zeros += 1
					note_length += 1
					current_index += 1

				# satisfied note_length...add note to list
				if (note_length > 12):

					note_name = get_name(note_row)
					beg_time = (float(start_index) / (float(num_columns) / duration))
					length_time = (float(current_index) / (float(num_columns) / duration)) - beg_time
					tuple_list.append((note_name, beg_time, length_time))
					for i in range(start_index, current_index):
						new_chroma[note_row][i] = 1

				# Loop stuff, to make sure we are
				# scanning the correct portion of the chroma.
				start_index = current_index
				i = current_index
			else:
				i += 1
				start_index += 1
				current_index += 1

		note_row += 1

	tuple_list.sort(key=lambda x: x[1])

	for i in tuple_list:
		print(i)

	# plot_title_style = {"size": 8}
	# rc("font", **plot_title_style)
	# plt.style.use("dark_background")
	# plt.subplot(211)
	# plt.title("Chromagram")
	# librosa.display.specshow(chroma, x_axis="time", y_axis="chroma")
	# plt.colorbar()
	# plt.subplot(212)
	# plt.title("after processing")
	# librosa.display.specshow(new_chroma, x_axis="time", y_axis="chroma")
	# plt.colorbar()
	# plt.show()
	# plt.tight_layout()

	return tuple_list

def get_name(x):
	return {
		0: "C", 1: "C#", 2: "D", 3: "D#", 4: "E", 5: "F",
		6: "F#", 7: "G", 8: "G#", 9: "A", 10: "A#", 11: "B",
	}[x]


if __name__ == "__main__":
	main()