from pyo import *
import glob

s = Server(duplex=0, audio='offline', winhost="asio")
files = glob.glob('E:/notes_database/soundfiles/*')
save = 'E:/notes_database/soundfiles_3'
for i in files:
    info = sndinfo(i)
    dur, sr, chnls = info[1], info[2], info[3]
    fformat = ['WAVE', 'AIFF', 'AU', 'RAW', 'SD2', 'FLAC', 'CAF', 'OGG'].index(info[4])
    samptype = ['16 bit int', '24 bit int', '32 bit int', '32 bit float',  '64 bits float', 'U-Law encoded', 'A-Law encoded'].index(info[5])
    s.setSamplingRate(sr)
    s.setNchnls(chnls)
    s.boot()
    s.recordOptions(dur=dur, filename=save+'\\'+i.split('\\')[1], fileformat=fformat, sampletype=samptype)
    sound = SfPlayer(i)
    b = Freeverb(sound, size=0.8, damp=.3, bal=.5).out()
    s.start()
    s.shutdown()