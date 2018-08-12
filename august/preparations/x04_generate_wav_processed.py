from pyo import *
import glob
# Installation of pyo on MacOS
# https://github.com/lupyanlab/lab-computer/wiki/Installing-pyo

def generate_wav_processed(save_location, files):
    s = Server(duplex=0, audio='offline', winhost="asio")

    for i in files:
        info = sndinfo(i)
        dur, sr, chnls = info[1], info[2], info[3]
        fformat = ['WAVE', 'AIFF', 'AU', 'RAW', 'SD2', 'FLAC', 'CAF', 'OGG'].index(info[4])
        samptype = ['16 bit int', '24 bit int', '32 bit int', '32 bit float',
                    '64 bits float', 'U-Law encoded', 'A-Law encoded'].index(info[5])
        s.setSamplingRate(sr)
        s.setNchnls(chnls)
        s.boot()
        s.recordOptions(dur=dur, filename=save_location+i[-20:], fileformat=fformat, sampletype=samptype)
        sound = SfPlayer(i)
        b = Freeverb(sound, size=0.8, damp=.3, bal=.5).out()
        s.start()
        s.shutdown()