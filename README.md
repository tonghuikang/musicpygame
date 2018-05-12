# Vision
We hope to make an open-source music education game based on Python so that developers can prototype and test their algorithms and advance music education.

# About
In the general transcription problem is much more difficult and some advanced work has been done on it already. However, we would like to focus on audio that is easier to be transcribed, and we want to do it live on something portable like a Raspberry Pi. With such an example, I hope it is easier for the music information retrieval community to develop more advanced open source games for music education.

# Functions and Terminologies
In the definition of the methods we also use introduce terminologies that we will standardise in this project - they are in bold.

#### Onset Detection `onset_dection`
Given a long audio recording *soundfile*, which is typically a stereo `.wav` file a sampling rate of 44100Hz, or a stereo live microphone audio of the same typical sampling rate, produce the *snippets* for note evaluation right after times when it determines a new note is detected. <BR>
We assume that the instrument has a distinct and significant onset - therefore our focus on plucked string instruments or tuned percussion instruments. Also, we assume that there are little or no sustained notes from previous times - which could be displayed in the note.

#### Note Evaluation `note_evaluation`
Given a *snippet* of an audio, for now a mono signal of `4096` to analyse, determine the notes present in the sound. <BR>
We assume that 

# Folder Structure

## [/game_platform](/game_platform) 
Contains files for the note detection game to run. It has been proven to work with the live microphone. Right now it requires better note evaluation algorithms. We hope to deliver a game that could be run on RPi at the end of the project.

- [ ] Write installation requirements
- [ ] Decide whether to use the terminology `chunk` and how often do we calculate rcoeff.
- [ ] 

## [/note_evaluation](/note_evaluation) 
Contains the test for the different evaluation functions that we propose. We also have `note_evaluation_helper.ipynb` containing the helper functions and that generates midi file and soundfiles (through fluidsynth) and deletes them later by default. The candidate note evaluation functions are inside `note_evaluation_accuracy.ipynb` and 

- [ ] Make make LG's regression into a function
- [ ] Make a function to calculate accuracy in `soundfile_generator.ipynb`
- [ ] Copy and make a `note_evaluation_helper.py`

### [/../midifile_sch](/note_evaluation/midifile_sch)
A folder to contain midifiles `.mid` that is generated and destroyed after generation. 

### [/../soundfile_sch](/note_evaluation/soundfile_sch)
A folder to contain soundfiles `.wav` that is generated and destroyed after generation. 

### [/../soundfile_template](/note_evaluation/soundfile_template)
A folder to contain soundfiles `.wav` with one note only. These are necessary for Lin Geng's regression algorithm.

## [/meeting_notes](/meeting_notes)
Contains the recordings of the meeting, and perhaps email updates. 
- [ ] Find more of them

## [/archive](/archive) 
Contains old files. It is there because we are still beginners at using git and we do not know how to navigate to the older files efficiently.

# Cloning this repository
Due to our bad project management practices, we have committed our production of all possible 1-2-3-4 combinations notes from an octave. Please use `git clone --depth 1 https://github.com/tonghuikang/musicpygame/` to avoid downloading large amounts of data.
