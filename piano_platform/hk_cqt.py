import math
import cmath
import numpy as np


# def fft(x):
#     N = len(x)
#     if N <= 1: return x
#     even = fft(x[0::2])
#     odd =  fft(x[1::2])
#     T= [cmath.exp(-2j*math.pi*k/N)*odd[k] for k in range(N//2)]
#     return [even[k] + T[k] for k in range(N//2)] + \
#        [even[k] - T[k] for k in range(N//2)]
            
def cqt_function(signal_to_ayse): # input in 4096 entries long
    length = len(signal_to_ayse)

    freq_domain = np.fft.fft(signal_to_ayse)

    bins = 36
    freq_ref_notes = [261.625565 * (2. ** (n/36. + 4./72.)) for n in range(bins)]


    bell_curves = []
#     window_iv = [2.*x/length - 1. for x in range(length)]
    for note in range(len(freq_ref_notes)):
#         bell_curve = [0]*length
#         for entry in range(length):
#             bell_curve[entry] = math.exp(-((window_iv[entry])*(2. ** (note/36.)))**2.)
        
        bell_curve = np.exp(-((np.arange(-1.,1.,2./length))*(2. ** (note/36.)))**2.)
        
        bell_curves.append(bell_curve) 

    # indexes_centred = [x for x in range(length)]

    kernels = []

    for note in range(36):

        kernel = []

        kernels.append(np.multiply(np.exp((np.arange(length)-length/2.)*-1.j*2.*math.pi*freq_ref_notes[note]/44100.)
                                  ,bell_curves[note]  # windowing
                            ))

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

    # known_octave = notesrum_peak_only[12:12+36]
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
