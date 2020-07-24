import pygame as pg
import numpy as np

black = (0, 0, 0)
white = (255, 255, 255)

width = 1000
height = 1000
screen_dimension = (width, height)
pg.init()
screen = pg.display.set_mode(screen_dimension)
pg.display.set_caption("Ideal Gas")
number_of_atoms = 1000
atoms = []

class atom:
	def __init__(self, x, y, v_x, v_y):
		self.r = 2
		self.x = round(x)
		self.y = round(y)
		self.v_x = round(v_x)
		self.v_y = round(v_y)
	def move(self):
		self.x += round(self.v_x)
		self.y += round(self.v_y)
	def check_collision(self):
		if (self.x >= width and self.v_x > 0) or (self.x <= 0 and self.v_x < 0):
			self.v_x *= -1
		if (self.y >= height and self.v_y > 0) or (self.y <= 0 and self.v_y < 0):
			self.v_y *= -1
	def show(self):
		self.center = (self.x, self.y)
		pg.draw.circle(screen, white, self.center, self.r)

def make_atoms():
	for ind in range(number_of_atoms):
		atoms.append(atom(width//2+100*np.random.randn(),height//2+100*np.random.randn(),5*np.random.randn(),5*np.random.randn()))

def show_atoms():
	for atom in atoms:
		atom.show()
		atom.check_collision()
		atom.move()

def initialize():
	make_atoms()
	running = True
	time_step = 0
	while running:
		for event in pg.event.get():
			if event.type == pg.QUIT:
				running = False
		screen.fill(black)
		show_atoms()
		pg.display.update()

initialize()