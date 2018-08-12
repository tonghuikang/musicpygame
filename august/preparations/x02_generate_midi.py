from midiutil.MidiFile import MIDIFile
import numpy as np

def generate_midi_file(sound_id, time_array, note_array):
    
    # create your MIDI object
    num_tracks = 5
    mf = MIDIFile(num_tracks)     # only 1 track
    track = 0   # the only track

    time = 0    # start at the beginning
#     mf.addTrackName(track, time, "Sample Track")
    mf.addTempo(track, time, 120)

    # add some notes
    channel = 0
    volume = 100
    
    for i in range(len(time_array)):
        track = (track + 1) % 5
        
        pitch = 60 + note_array[i]             # C4 (middle C)
        time = time_array[i]                   # start on beat 0
        duration = np.random.uniform(0.8,0.9)
        volume = np.random.randint(50,100)     # 1 beat long
        mf.addNote(track, channel, pitch, time, duration, volume)
    
    with open("./midi/{}.mid".format(sound_id), 'wb') as outf:
        mf.writeFile(outf)