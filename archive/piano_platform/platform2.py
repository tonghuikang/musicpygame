import pygame
import sys
# from note_detect import q, note_detect
from threading import Thread

# pygame initiate
pygame.init()
pygame.mixer.init()

# initiate threading
#t = Thread(target=get_current_note)
#t.daemon = True
#t.start()

# sprite groups
all_sprites = pygame.sprite.Group()
keys = pygame.sprite.Group()
blocks = pygame.sprite.Group()  

# setting up screen 
screen_width, screen_height = 512, 256
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Piano platform")

# import images
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

clock = pygame.time.Clock()

running = True

#title_font
#note_font

#if not q.empty():
	#b = q.get()
	#note_list = b["Note"]

#if q.empty():
	#note_list = []

# test
note_list = ["C", "D"]

class autoMove_block(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = note_block
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
	def update(self):
		if (self.rect.x > 512):
			self.kill()
		self.rect.x += 2

class Octave(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = octave_blank
		self.rect = self.image.get_rect()
		self.rect.x = 0
		self.rect.y = 0

class C_key(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = C_pressed
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.time = None
	def update(self):
		if (self.time != None):
			if pygame.time.get_ticks() - self.time >= 200:
				self.kill()
		
class D_key(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = D_pressed
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.time = None
	def update(self):
		if (self.time != None):
			if pygame.time.get_ticks() - self.time >= 200:
				self.kill()

class E_key(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = E_pressed
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.time = None
	def update(self):
		if (self.time != None):
			if pygame.time.get_ticks() - self.time >= 200:
				self.kill()

class sharp_key(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = sharp_pressed
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.time = None
	def update(self):
		if (self.time != None):
			if pygame.time.get_ticks() - self.time >= 200:
				self.kill()

while running:
	for event in pygame.event.get():
		if (event.type == pygame.QUIT):
			running = False
		if (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
			running = False 
	
	octave = Octave()
	all_sprites.add(octave)
	
	if note_list == []:
		pass
		
	else:
		for note in note_list:
			if (note == "C"):
				o = autoMove_block(150, 0)
				c_key = C_key(2, 0)
				blocks.add(o)
				keys.add(c_key)
		
			elif (note == "Db"):
				o = autoMove_block(150, 24)
				Csharp_key = sharp_key(63, 24)
				blocks.add(o)
				keys.add(Csharp_key)
				
			elif (note == "D"):
				o = autoMove_block(150, 36)
				d_key = D_key(2, 36)
				blocks.add(o)
				keys.add(d_key)

			elif (note == "Eb"):
				o = autoMove_block(150, 66)
				Dsharp_key = sharp_key(63, 66)
				blocks.add(o)
				keys.add(Dsharp_key)
				
			elif (note == "E"):
				o = autoMove_block(150, 73)
				e_key = E_key(2, 73)
				blocks.add(o)
				keys.add(e_key)
				
			elif (note == "F"):
				o = autoMove_block(150, 109)
				f_key = C_key(2, 109)
				blocks.add(o)
				keys.add(f_key)
				
			elif (note == "Gb"):
				o = autoMove_block(150, 133)
				Fsharp_key = sharp_key(63, 133)
				blocks.add(o)
				keys.add(Fsharp_key)

			elif (note == "G"):
				o = autoMove_block(150, 144)
				g_key = D_key(2, 144)
				blocks.add(o)
				keys.add(g_key)
				
			elif (note == "Ab"):
				o = autoMove_block(150, 173)
				Gsharp_key = sharp_key(63, 173)
				blocks.add(o)
				keys.add(Gsharp_key)
				
			elif (note == "A"):
				o = autoMove_block(150, 181)
				a_key = D_key(2, 181)
				blocks.add(o)
				keys.add(a_key)
				
			elif (note == "Bb"):
				o = autoMove_block(150, 211)
				Asharp_key = sharp_key(63, 211)
				blocks.add(o)
				keys.add(Asharp_key)
				
			elif (note == "B"):
				o = autoMove_block(150, 220)
				b_key = E_key(2, 220)
				blocks.add(o)
				keys.add(b_key)
				
	all_sprites.update()
	keys.update()
	blocks.update()

	screen.fill((0, 0, 0))
	all_sprites.draw(screen)
	keys.draw(screen)
	blocks.draw(screen)
	pygame.display.flip()
	clock.tick(40)

pygame.quit()
