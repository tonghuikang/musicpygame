import pyaudio
import argparse

import numpy as np
import time


# this is the size of each individual block of audio, we call this "chunk"
chunksize = 2048

parser = argparse.ArgumentParser()
parser.add_argument("-input", required=False, type=int, help="Audio Input Device")
args = parser.parse_args()

# this is here so you can choose the default audio input
if args.input is None:
    print("No input device specified. Printing list of input devices now: ")
    p = pyaudio.PyAudio()
    for i in range(p.get_device_count()):
        print("Device number (%i): %s" % (i, p.get_device_info_by_index(i).get('name')))
        print("Run this program with -input 1, or the number of the input you'd like to use.")
        exit()

# starting audio channel?
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paFloat32,
channels=1, rate=44100, input=True,
input_device_index=args.input, frames_per_buffer=chunksize)
time.sleep(1)

def detect_onset(signal, chunksize=2048, tempo_res=32):
    '''
    # this is to be called at the end of every chunk (2048 entries), starting from 4th chunk
    # the input to this function is four chunks
    '''
    onset = -1 # default, overwritten if onset is detected

    # to detect difference
    difference = np.cumsum(np.add(np.absolute(signal[chunksize:-chunksize]), -np.absolute(signal[:-2*chunksize])))
    
    # noise is added to desensitise detection of noise
    noise = 10*np.array(np.random.randn(len(difference)))
    difference = np.add(difference, noise)

    # calculation of r-coefficient
    # -1 is negatively correlated
    # +1 is positively correlated
    # onset is when r-coefficient cuts above 0.8
    roceff = np.full(tempo_res, 0.)
    tempo_num = int(chunksize / tempo_res)
    for i in range(tempo_res):
        roceff[i] = np.corrcoef(difference[i * tempo_num:(i * tempo_num + chunksize)],
                                      np.arange(chunksize))[0, 1]
        if i == 0 and roceff[0] > 0.8:
            onset = i
        if roceff[0] < 0.8 and roceff[i] > 0.8 and np.max(roceff[:i]) < 0.8:
            onset = i
    # print(np.max(roceff))
    return onset # none, or a value
            
def cqt_function(signal_to_ayse): 
    # input to this function is 4096 entries long
    length = len(signal_to_ayse)
    print(length)

    # fast fourier transform
    freq_domain = np.fft.fft(signal_to_ayse)

    # defining the 36 notes bins
    bins = 36
    freq_ref_notes = [261.625565 * (2. ** (n/36. - 1./72.)) for n in range(bins)]

    # defining the time kernel
    bell_curves = []
    for note in range(len(freq_ref_notes)):
        bell_curve = np.exp(-((np.arange(-1.,1.,2./length))*(2. ** (note/36.)))**2.)
        bell_curves.append(bell_curve) 

    # what was this for?
    kernels = []
    for note in range(36):
        kernels.append(np.multiply(np.exp((np.arange(length)-length/2.)*-1.j*2.*np.pi*freq_ref_notes[note]/44100.)
                                  ,bell_curves[note]  # windowing
                            ))

    # fourier transform for the frequency kernel
    fft_kernels = []
    for note in range(bins):
        fft_kernels.append(np.fft.fft(kernels[note]))

    # creating arrays to populate for each one-third-semitone
    cqt_resp_specs = []
    cqt_resp = []

    # populating the arrays
    for note in range(bins):
        cqt_resp_spec = []
        for entry in range(length):
            cqt_resp_spec.append(fft_kernels[note][entry]*freq_domain[entry])
        cqt_resp_specs.append(cqt_resp_spec)
        cqt_resp.append(sum([abs(x) for x in cqt_resp_spec]))

    # finding peaks in the cqt response
    notesrum = cqt_resp
    notesrum_peak_only = [0.0]*len(notesrum)
    notesrum_sum = sum(notesrum)

    for index in range(bins-1)[1:]:
        if notesrum[index-1] < notesrum[index] and notesrum[index+1] < notesrum[index]:
            notesrum_peak_only[index]=notesrum[index]

    # known_octave = notesrum_peak_only[12:12+36] # don't know what is this for
    known_octave = notesrum_peak_only[:]
    print(np.round(known_octave,5)/notesrum_sum)
    
    notesrum_peak_only_sum = sum(notesrum_peak_only)

    for x in range(bins):
        # if known_octave[x]/notesrum_sum < 0.1: 
        if known_octave[x]/notesrum_peak_only_sum < 0.2: 
            known_octave[x] = 0
        
    known_octave_notes = []
    for notes in range(bins//3):
        known_octave_notes.append(known_octave[3*notes]
                             +known_octave[3*notes+1]
                             +known_octave[3*notes+2])

    # notestrum_sum = sum(notesrum)  # alternate demoninator to calc threshold
    print(np.round(known_octave_notes,5)/notesrum_peak_only_sum)
    print("check")

    notesrum_peak_only_sum = sum(notesrum_peak_only)

    output = []

    for x in range(12):
        if known_octave_notes[x]/notesrum_peak_only_sum > 0.1:
            output.append(x+1)

    return output

def note_detect(chunksize=2048, tempo_res=32):
    print("opening")
    frames = []
    i = 0

    while True:
        # assume pyaudio clip mono sound
        # use assert?
        
        i += 1
        data = stream.read(chunksize, exception_on_overflow=False)
        data = np.fromstring(data, np.float32)
        frames.append(data)
        # print(len(frames))
        
        if i > 10 and len(frames)>4:
            frames[:] = frames[-4:]
            signal = np.concatenate((frames[-4],frames[-3],frames[-2],frames[-1]))

            # onset function
            # print(np.sum(abs(signal)))
            # print(len(signal))
            # print("finding onset")
            onset = detect_onset(signal)
            # print("onset detection complete")
            # print(onset)
            
            # remove the older frames
            
            
            # make an array consists of 4096 entries if there is an onset
            if onset != -1:
                print("onset DETECTED")
                signal_input = signal[2048+64*onset:6144+64*onset]
                onset = -1 # set onset back to negative one - but necessary?

                # cqt function 
                output = cqt_function(signal_input)
                print(output)
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
                print(output)    
    
    # don't you need to return something?

note_detect()