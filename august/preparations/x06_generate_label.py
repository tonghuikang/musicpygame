import numpy as np
import matplotlib.pyplot as plt


def generate_label(filename):
    sound_id = filename[-20:-4]
    time_note_array = np.load(filename)
    time_array, note_array = np.transpose(time_note_array)    
    
#     time_note_array = np.array(sorted(time_note_array, key=lambda x: x[0]))
    
    labels = np.zeros((140,24))
    for i,entry in enumerate(time_note_array):
        time, note = entry
        time_slice = int((time/2*44100/(27*2**7))//1)  # divide 2 because bpm is 120
        labels[time_slice, int(note)] = 1
        
#     plt.figure(figsize=(12,12))
#     plt.imshow(labels)
    
    np.save("label/" + filename[-20:-4], labels)