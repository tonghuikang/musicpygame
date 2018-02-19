#from threading import Thread
import pygame
import sys

## from cqt_function import cqt_function, fft
## from note_detection_function import detect_onset

pygame.init()

C = False
Db = False
D = False
Eb = False
E = False
F = False
Gb = False
G = False
Ab = False
A = False
Bb = False
B = False

objects = []

screen_width, screen_height = 512, 256
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Piano platform")

octave_blank = pygame.image.load("octave.png")
octave_blank.convert()
C_pressed = pygame.image.load("C_pressed.png")
C_pressed.convert()
D_pressed = pygame.image.load("D_pressed.png")
D_pressed.convert()
E_pressed = pygame.image.load("E_pressed.png")
E_pressed.convert()
sharp_pressed = pygame.image.load("sharp_pressed.png")
sharp_pressed.convert()
note_block = pygame.image.load("note_block.png")
note_block.convert
background = pygame.image.load("background.png")
background.convert

clock = pygame.time.Clock()

running = True

#title_font
#note_font

#t = Thread(target = cqt_function)
#t.daemon = True
#t.start()

note_list = ["C", "Gb"]

class autoMove_block():
	def __init__(self, position_x, position_y):
		self.pos_x = position_x
		self.pos_y = position_y
	
	def move(self):
		if self.pos_x <= 512:
			self.pos_x = self.pos_x + 4

screen.fill((0, 0, 0))

while running:
	for event in pygame.event.get():
		if (event.type == pygame.QUIT):
			running = False
		if (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
			running = False 
	
	screen.blit(background, (0, 0))
	screen.blit(octave_blank, (0, 0))
	
	if note_list == []:
		pass
		
	else:
		for note in note_list:
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
				screen.blit(note_block, (150, 36))
				auto_move(note_block)
				
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

	for o in objects:
		screen.blit(background, (o.pos_x, o.pos_y))
		
	for o in objects:
		o.move()
		screen.blit(note_block, (o.pos_x, o.pos_y))

		
	pygame.display.flip()
	clock.tick(40)

pygame.quit()
		