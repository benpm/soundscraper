import mido

port = mido.open_output()

midi_file = mido.MidiFile("test.mid")
for msg in midi_file.play():
    port.send(msg)