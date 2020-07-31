import pygame as pg
import numpy as np

black = (0, 0, 0)
white = (255, 255, 255)
blue = (0, 0, 255)
green = (0, 255, 0)

width = 1000
height = 1000
screen_dimension = (width, height)
pg.init()
screen = pg.display.set_mode(screen_dimension)
pg.display.set_caption("Brownian Motion")
number_of_atoms = 10000
trail_length = 8000
atoms = []

class Particle:
	def __init__(self, x, y, v_x, v_y):
		self.x = x
		self.y = y
		self.v_x = v_x
		self.v_y = v_y
	def move(self):
		self.x += self.v_x
		self.y += self.v_y
	def collision_with_wall(self):
		if (self.x + self.r >= width and self.v_x > 0) or (self.x - self.r <= 0 and self.v_x < 0):
			self.v_x *= -1
		if (self.y + self.r >= height and self.v_y > 0) or (self.y - self.r<= 0 and self.v_y < 0):
			self.v_y *= -1
	def show(self):
		self.center = (round(self.x), round(self.y))
		pg.draw.circle(screen, self.color, self.center, self.r)

class Atom(Particle):
	def __init__(self, x, y, v_x, v_y):
		Particle.__init__(self, x, y, v_x, v_y)
		self.r = 2
		self.m = 1
		self.color = white

class Grain(Particle):
	def __init__(self, x, y, v_x, v_y):
		Particle.__init__(self, x, y, v_x, v_y)
		self.r = 10
		self.m = 20
		self.color = blue
	def collision_with_atom(self, atom):
		d0 = ((self.x-atom.x)**2+(self.y-atom.y)**2)**0.5
		d1 = self.r+atom.r
		if d0<=d1 and (self.x-atom.x)*(self.v_x-atom.v_x)<0 and (self.y-atom.y)*(self.v_y-atom.v_y)<0:
			diff = self.m-atom.m
			total = self.m+atom.m
			self.v_x = (diff*self.v_x+2*atom.m*atom.v_x)/total
			atom.v_x = (2*self.m*self.v_x-diff*atom.v_x)/total
			self.v_y = (diff*self.v_y+2*atom.m*atom.v_y)/total
			atom.v_y = (2*self.m*self.v_y-diff*atom.v_y)/total

def make_atoms():
	for ind in range(number_of_atoms):
		atoms.append(Atom(width*np.random.rand(),height*np.random.rand(),10*np.random.randn(),10*np.random.randn()))

def show_atoms(show):
	for atom in atoms:
		if show:
			atom.show()
		atom.collision_with_wall()
		atom.move()

grain = Grain(width/2, height/2, 0.1*np.random.randn(), 0.1*np.random.randn())

def show_grain(trail):
	grain.show()
	for atom in atoms:
		grain.collision_with_atom(atom)
	grain.collision_with_wall()
	grain.move()
	trail.insert(0, grain.center)
	if len(trail) == trail_length:
		trail.pop()
	pg.draw.lines(screen, green, False, trail)

def initialize():
	make_atoms()
	running = True
	show = True
	trail = [(width//2, height//2)]
	while running:
		for event in pg.event.get():
			if event.type == pg.QUIT:
				running = False
			if event.type == pg.KEYDOWN:
				if event.key == pg.K_SPACE:
					show = False if show else True
		screen.fill(black)
		show_atoms(show)
		show_grain(trail)
		pg.display.update()

initialize()
