import pyaudio
import argparse

import queue

import cmath
import math
import numpy as np
import time

chunksize = 2048

parser = argparse.ArgumentParser()
parser.add_argument("-input", required=False, type=int, help="Audio Input Device")
args = parser.parse_args()

if args.input is None:
	print("No input device specified. Printing list of input devices now: ")
	p = pyaudio.PyAudio()
	for i in range(p.get_device_count()):
		print("Device number (%i): %s" % (i, p.get_device_info_by_index(i).get('name')))
		print("Run this program with -input 1, or the number of the input you'd like to use.")
		exit()

p = pyaudio.PyAudio()

stream = p.open(format=pyaudio.paFloat32,
channels=1, rate=44100, input=True,
input_device_index=args.input, frames_per_buffer=chunksize)
time.sleep(1)

q = queue.Queue()

# to be called at the end of every 2048 entries
# the input is 2048 entry * 3
def detect_onset(signal, chunksize=2048, tempo_res=32):
    onset = -1
	
    difference = np.cumsum(np.add(np.absolute(signal[chunksize:-chunksize]), -np.absolute(signal[:-2*chunksize])))
    noise = 10*np.array(np.random.randn(len(difference)))
    difference = np.add(difference, noise)
    
    roceff = np.full(tempo_res, 0.)
    tempo_num = int(chunksize / tempo_res)
    for i in range(tempo_res):
        roceff[i] = np.corrcoef(difference[i * tempo_num:(i * tempo_num + chunksize)],
                                      np.arange(chunksize))[0, 1]
        if roceff[0] < 0.8 and roceff[i] > 0.8 and np.max(roceff[:i]) < 0.8:
            onset = i
    
    return onset # -1 or a value

def cqt_function(signal_to_ayse): # input in 4096 entries long
    length = len(signal_to_ayse)

    freq_domain = np.fft.fft(signal_to_ayse)

    bins = 36
    freq_ref_notes = [261.625565 * (2. ** (n/36. + 4./72.)) for n in range(bins)]


    bell_curves = []

    for note in range(len(freq_ref_notes)):
        
        bell_curve = np.exp(-((np.arange(-1.,1.,2./length))*(2. ** (note/36.)))**2.)
        
        bell_curves.append(bell_curve) 
		
    kernels = []

    for note in range(36):

        kernel = []

        kernels.append(np.multiply(np.exp((np.arange(length)-length/2.)*-1.j*2.*math.pi*freq_ref_notes[note]/44100.)
                                  ,bell_curves[note] ))

    fft_kernels = []

    for note in range(bins):
        fft_kernels.append(np.fft.fft(kernels[note]))

    cqt_resp_specs = []
    cqt_resp = []

    for note in range(bins):
        cqt_resp_spec = []
        for entry in range(length):
            cqt_resp_spec.append(fft_kernels[note][entry]*freq_domain[entry])
        cqt_resp_specs.append(cqt_resp_spec)
        cqt_resp.append(sum([abs(x) for x in cqt_resp_spec]))

    notesrum = cqt_resp

    notesrum_peak_only = [0.0]*len(notesrum)

    for index in range(bins-1)[1:]:
        if notesrum[index-1] < notesrum[index] and notesrum[index+1] < notesrum[index]:
            notesrum_peak_only[index]=notesrum[index]

    known_octave = notesrum_peak_only[:]
    
    notesrum_peak_only_sum = sum(notesrum_peak_only)

    for x in range(bins):
        if known_octave[x]/notesrum_peak_only_sum < 0.1: 
            known_octave[x] = 0
        
    known_octave_notes = []
    for notes in range(bins//3):
        known_octave_notes.append(known_octave[3*notes]
                             +known_octave[3*notes+1]
                             +known_octave[3*notes+2])

    notestrum_sum = sum(notesrum)
    notesrum_peak_only_sum = sum(notesrum_peak_only)

    output = []

    for x in range(12):
        if known_octave_notes[x]/notesrum_peak_only_sum > 0.1:
            output.append(x+1)

    return output

def note_detect(chunksize=2048, tempo_res=32):
	frames = []
	
	while True:
		# assume pyaudio clip mono sound
		data = stream.read(chunksize)
		data = np.fromstring(data, np.float32)
		frames.append(data)
		
		if len(frames) == 4:
			signal_3 = frames[0] + frames[1] + frames[2]
			
			# onset function
			onset = detect_onset(signal_3)

			# remove the oldest frame
			frames.pop(-1)
			
			# make an array consists of 4096 entries if there is an onset
			if onset != -1:
				signal_input = frames[2048+64*i, 4096+96*i]
				print("find onset")
				# cqt function 
				output = cqt_function(signal_input)
				print("output secured")
				# convert number into note
				for i in range(len(output)):
					if output[i] == 1:
						output[i] = "C"
					if output[i] == 2:
						output[i] = "Db"
					if output[i] == 3:
						output[i] = "D"
					if output[i] == 4:
						output[i] = "Eb"
					if output[i] == 5:
						output[i] = "E"
					if output[i] == 6:
						output[i] = "F"
					if output[i] == 7:
						output[i] = "Gb"
					if output[i] == 8:
						output[i] = "G"
					if output[i] == 9:
						output[i] = "Ab"
					if output[i] == 10:
						output[i] = "A"
					if output[i] == 11:
						output[i] = "Bb"
					if output[i] == 12:
						output[i] = "B"
					
				q.put({"Note": output})
