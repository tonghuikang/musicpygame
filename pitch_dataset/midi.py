from midiutil.MidiFile import MIDIFile
from itertools import combinations

scale = 4 #for scale=4 it means C4
no_of_notes = 4 #play 4 notes at the same time

pitch = range(12*(scale+1), 12*(scale+2))
comb = [x for x in combinations(pitch, no_of_notes)]
track = range(no_of_notes)
channel = 0
time = 0
duration = 2
tempo = 100
volume = 100

count = 0	
for com in comb:

    mf = MIDIFile(no_of_notes)

    for num in range(no_of_notes):
        mf.addNote(track[num], channel, com[num], time, duration, volume)

    with open("files\{:d}_notes_C{:d}_{:d}.mid".format(no_of_notes, scale, count), "wb") as outf:
        mf.writeFile(outf)

    count += 1
