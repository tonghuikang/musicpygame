# to be called at the end of every 2048 entries
# the input is 2048 entry * 3
def detect_onset(signal, chunksize=2048, tempo_res=32):
    
    onset = -1
#     plt.figure(figsize = (16,2))
#     plt.plot(signal)
    
    difference = np.cumsum(np.add(np.absolute(signal[chunksize:-chunksize]), -np.absolute(signal[:-2*chunksize])))
    noise = 10*np.array(np.random.randn(len(difference)))
    difference = np.add(difference, noise)
    
#     plt.plot(np.arange(chunksize, chunksize*3),np.array(difference)/np.max(np.absolute(difference)))
    
    roceff = np.full(tempo_res, 0.)
    tempo_num = int(chunksize / tempo_res)
    for i in range(tempo_res):
        roceff[i] = np.corrcoef(difference[i * tempo_num:(i * tempo_num + chunksize)],
                                      np.arange(chunksize))[0, 1]
        if roceff[0] < 0.8 and roceff[i] > 0.8 and np.max(roceff[:i]) < 0.8:
            onset = i
            
#     plt.plot(np.arange(chunksize*2, chunksize*3, tempo_num),roceff)
#     plt.axhline(y=0.8)
#     plt.show()

