from time import sleep
import subprocess

def convert_midi_to_signal(filename):
    '''
    Given filename, create soundfile.
    It uses fluidsynth to convert the midifile from the directory 
    into a soundfile in another directory.
    Installation of fluidsynth is necessary to run this.
    https://github.com/FluidSynth/fluidsynth/wiki/BuildingWithCMake
    returns mono signal - could we use stereo information for evaluation someday?
    '''
    soundfont_dir = "~/soundfonts/Sonatina_Symphonic_Orchestra.sf2"
    
    subprocess.run("fluidsynth -F ./wav/{}.wav {} {}"
                   .format(filename[-20:-4],
                           soundfont_dir,
                           filename),
                   shell=True)