import numpy as np
import soundfile as sf
import librosa
import matplotlib.pyplot as plt


def generate_spectrogram(filename):
    audio,sr = sf.read(filename)
    if type(audio[0]) != float or type(audio[0]) != int: 
        # if stereo (expected)
        signal = audio[:,0]  
    else:    
        # if mono (but I have yet to try this out)
        signal = audio[:]
    assert (signal[0] != float or signal[0] != int)
    
    
#     signal = signal[:44100*10]
    signal += 0.0001*np.random.randn(len(signal))  # Gaussian
    signal += np.cumsum(0.0005*np.random.randn(len(signal)))  # Brownian
    fmin = librosa.core.note_to_hz("B3")
    cqt_array = librosa.cqt(signal, 
                            sr=44100, 
                            hop_length=2**7, 
                            bins_per_octave=36, 
                            fmin=fmin, 
                            n_bins=108)
    CQT = librosa.magphase(cqt_array)[0]
#     assert np.shape(CQT) == (108,3446)
    
#     plt.figure(figsize=(15,4))
#     plt.imshow(CQT, cmap="YlOrBr")
#     plt.show()

    filename = (filename.split("/")[-1]).split(".")[0]
    np.save("./spectrogram/" + filename, CQT)