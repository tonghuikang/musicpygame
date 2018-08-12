import numpy as np
import random

def generate_note_file():
    sound_id = ''.join(random.choice('0123456789ABCDEF') for i in range(16))
    
    t = 0
    note_time_array = []
    
    while t < 20:
        t += 0.3 + np.random.uniform(0.2)
        
        notes_in_this_chord = []
        
        if np.random.uniform() > 0.2:
            new_note = np.random.randint(24)
            if new_note not in notes_in_this_chord:
                note_time_array.append([t, new_note])
                notes_in_this_chord.append(new_note)
                
        if np.random.uniform() > 0.2:
            new_note = np.random.randint(24)
            if new_note not in notes_in_this_chord:
                note_time_array.append([t, new_note])
                notes_in_this_chord.append(new_note)
            
        if np.random.uniform() > 0.2:
            new_note = np.random.randint(24)
            if new_note not in notes_in_this_chord:
                note_time_array.append([t, new_note])
                notes_in_this_chord.append(new_note)
        
        if np.random.uniform() > 0.2 or (t > 18 and t < 20):
            new_note = np.random.randint(24)
            if new_note not in notes_in_this_chord:
                note_time_array.append([t, new_note])
                notes_in_this_chord.append(new_note)
                
#     print(note_time_array)
    np.save("./notes/" + sound_id, note_time_array)