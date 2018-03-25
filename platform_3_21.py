import pyaudio
import argparse

from note_detect_3_25 import detect_onset, cqt_function

import numpy as np
import time
# import matplotlib.pyplot as plt

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

import pygame

screen_width, screen_height = 512, 256
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Piano platform")

clock = pygame.time.Clock()

octave_blank = pygame.image.load("image/octave.png")
octave_blank.convert()
C_pressed = pygame.image.load("image/C_pressed.png")
C_pressed.convert()
D_pressed = pygame.image.load("image/D_pressed.png")
D_pressed.convert()
E_pressed = pygame.image.load("image/E_pressed.png")
E_pressed.convert()
sharp_pressed = pygame.image.load("image/sharp_pressed.png")
sharp_pressed.convert()
note_block = pygame.image.load("image/note_block.png")
note_block.convert

running = True

#title_font
#note_font

class autoMove_block():
	def __init__(self, position_x, position_y):
		self.pos_x = position_x
		self.pos_y = position_y

	def move(self):
		self.pos_x += 4

frames = []
i = 0
objects = []

while running:
	note_list = []
	i += 1
	data = stream.read(chunksize, exception_on_overflow=False)
	data = np.fromstring(data, np.float32)
	frames.append(data)
	# print(len(frames))

	# start listening only after there is a certain number of "frames"
	if i > 10 and len(frames) > 4:
		frames[:] = frames[-5:]
		signal = np.concatenate((frames[-5], frames[-4], frames[-3], frames[-2]))

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
			# print("onset DETECTED")
			signal_ = np.concatenate((frames[-4], frames[-3], frames[-2], frames[-1]))
			signal_input = signal_[2048 + 64 * onset:6144 + 64 * onset]
			onset = -1  # set onset back to negative one - but necessary?

			# cqt function
			output = cqt_function(signal_input)
			print(output)
			# convert number into note - why not just give numbers to your game?
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
			note_list = output

	for event in pygame.event.get():
		if (event.type == pygame.QUIT):
			running = False
		if (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
			running = False

	screen.fill((0, 0, 0))
	screen.blit(octave_blank, (0, 0))

	if note_list == []:
		pass

	else:
		for note in note_list:
			print (note)
			if (note == "C"):
				screen.blit(C_pressed, (2, 0))
				o = autoMove_block(150, 0)
				objects.append(o)

			elif (note == "Db"):
				screen.blit(sharp_pressed, (63, 24))
				o = autoMove_block(150, 24)
				objects.append(o)

			elif (note == "D"):
				screen.blit(D_pressed, (2, 36))
				o = autoMove_block(note_block, (150, 36))
				objects.append(o)

			elif (note == "Eb"):
				screen.blit(sharp_pressed, (63, 66))
				o = autoMove_block(150, 66)
				objects.append(o)

			elif (note == "E"):
				screen.blit(E_pressed, (2, 73))
				o = autoMove_block(150, 73)
				objects.append(o)

			elif (note == "F"):
				screen.blit(C_pressed, (2, 109))
				o = autoMove_block(150, 109)
				objects.append(o)

			elif (note == "Gb"):
				screen.blit(sharp_pressed, (63, 133))
				o = autoMove_block(150, 133)
				objects.append(o)

			elif (note == "G"):
				screen.blit(D_pressed, (2, 144))
				o = autoMove_block(150, 144)
				objects.append(o)

			elif (note == "Ab"):
				screen.blit(sharp_pressed, (63, 173))
				o = autoMove_block(150, 173)
				objects.append(o)

			elif (note == "A"):
				screen.blit(D_pressed, (2, 181))
				o = autoMove_block(150, 181)
				objects.append(o)

			elif (note == "Bb"):
				screen.blit(sharp_pressed, (63, 211))
				o = autoMove_block(150, 211)
				objects.append(o)

			elif (note == "B"):
				screen.blit(E_pressed, (2, 220))
				o = autoMove_block(150, 220)
				objects.append(o)

			else:
				pass

	for j in objects:
		j.move()
		screen.blit(note_block, (j.pos_x, j.pos_y))
		if j.pos_x > 512:
			del j

	pygame.display.flip()
	clock.tick(40)
	pygame.display.update()

stream.stop_stream()
stream.close()
pygame.display.quit()
		