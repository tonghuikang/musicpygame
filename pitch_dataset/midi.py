from midiutil.MidiFile import MIDIFile
from itertools import combinations

scales = range(1,5) #C1 to C4
no_of_notes = range(2, 5) #2 notes to 4 notes

channel = 0
time = 0
duration = 2
tempo = 100
volume = 100

for scale in scales:
	for no_ in no_of_notes:
		pitch = range(12*(scale+1), 12*(scale+2))
		comb = [x for x in combinations(pitch, no_)]
		track = range(no_)
		
		count = 0	
		for com in comb:

			mf = MIDIFile(no_)

			for num in range(no_):
				mf.addNote(track[num], channel, com[num], time, duration, volume)
    
			code = []
			for num in com:
				code.append(num)
			while len(code) < 4:
				code.append("x")
				
			with open("files\C{}_{}_{}_{}_{}.mid".format(scale, code[0], code[1], code[2], code[3]), "wb") as outf:
				mf.writeFile(outf)

			count += 1
