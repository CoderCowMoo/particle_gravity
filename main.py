import pygame
from pygame.locals import *
import sys
import random
import math

# heavy assist from this tutorial and this documentation
# https://coderslegacy.com/python/python-pygame-tutorial/
# https://www.pygame.org/docs/

pygame.init()

# declarations
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

SCREENX = 500
SCREENY = 500
DISPLAYSURF = pygame.display.set_mode((SCREENX, SCREENY), pygame.RESIZABLE)
DISPLAYSURF.fill(BLACK)
pygame.display.set_caption("Particles with gravity broski brodielicious")

FPS = 60
FPSController = pygame.time.Clock()

GRAVITATIONAL_CONSTANT = 4.0 # took that right out of my ass

FONT = pygame.font.SysFont(None, 20)

def randColour() -> tuple:
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

# this is gonna be a global thing, with a little number in a corner saying how big the object
# you're going to place is.
mass = 4 # by default

# each body has a random colour assigned at birth.
class Body():
    def __init__(self, x, y, mass=mass):
        self.x = x
        self.y = y
        self.vx = 0.0 # initially stationary I suppose (relative to what may I ask?? stfu dumbass, relative to observer)
        self.vy = 0.0
        self.mass = mass # ah. we need a way to select the mass.
        self.colour = randColour()
        self.radius = 0.08824 * self.mass + 9.647

    # how da hell do you do grabity. lmao grabity. I reckon a loop over each object, asking it to update it's velocity.
    # then we need a velocity variable.
    # ok then how do we update velocity? ah thats actually sounding kinda easy. Loop over each object. and based on mass?
    # we need a mass varibale.
    # ok so we loop over each object, for each object we loop over all other objects 
    # and add velocity in the respective directions
    def update_velocity(self, self_index):
        # as discussed.
        # self_index to splice the bodies array. (most efficient?)
        # https://stackoverflow.com/questions/19286657/index-all-except-one-item-in-python
        bodies_except = bodies[:self_index] + bodies[self_index+1:]
        for body in bodies_except:
            # we'll use it's mass to affect how far we move towards it
            # first we consider if it's positively x or negatively x.
            # how do we do that? subtract it's x from ours. So a body
            # on the left hand side. Attracted towards the sun
            # would have a positive result from self.x - sun.x
            # gravity = constant x (mass_1 * mass_2)/distance^2
            # thanks newton goat
            # fuckin idiot this isn't distance. GOod lord
            dx = body.x - self.x
            dy = body.y - self.y
            distance = math.sqrt( dx**2 + dy**2 )
            # this should stop spazzing.
            min_distance = self.radius + body.radius
            if distance < min_distance:
                distance = min_distance
            # i don't know why, but it's pushing in the opposite direction right now.
            # should I just invert it?
            # gemini 3.1 pro says if I do the body - self then it already points the right way. Good.
            force = GRAVITATIONAL_CONSTANT * ( (self.mass * body.mass) / distance**2 )
            # now how do we split up the force? ewww trigonometry
            # https://www.cs.princeton.edu/courses/archive/spr01/cs126/assignments/nbody.html
            # danke princeton :)
            # how do I get the angle between?
            forceX = force * dx/distance
            forceY = force * dy/distance
            # do I add or multiply to the velocity?
            # my gut says ... add
            # apparently have to divide by mass too.
            self.vx += forceX / self.mass**1.5
            self.vy += forceY / self.mass**1.5
            # yay
            
    def update_position(self):
        # how do we change position based on velocity?
        # thanks google ai overview. yes new = old + vel * time_step
        self.x += self.vx
        self.y += self.vy
        
        # if this new position is out of the bounds of screen, we can wrap it around?
        self.x %= SCREENX + 1
        self.y %= SCREENY + 1
    
    def draw(self, surface):
        # how to equate mass to radius?
        # if default mass of 4, I want a dot e.g. let's say 10 pixels wide
        # but if we have a sun in the middle, it should only be like 100.
        # ok so radius = e ^ (mass/200)
        # gonna try linear regression on the above 2 points
        # y = 0.08824 * mass + 9.647
        # gonna calc radius once at birth
        # can I draw in the centre of the screen at all times by translating by SCREENX/2 and SCREENY/2?
        pygame.draw.circle(surface, self.colour, (self.x, self.y), self.radius)

# let's place a sun in the middle 
bodies = [Body(SCREENX/2, SCREENY/2, 500)] # who knows what a sensible number for this is
bodies.append(Body(0, 0, 4))
bodies[1].vy = 1.0
bodies.append(Body(250, 0, 50))
bodies[2].vx = 5.2

# game loop
# where we should just draw each body in a circle and in it's colour?
# we should also update the position based on velocity I suppose.
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == VIDEORESIZE:
            SCREENX, SCREENY = event.w, event.h
            DISPLAYSURF = pygame.display.set_mode((SCREENX, SCREENY), pygame.RESIZABLE)
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                bodies.append(Body(event.pos[0], event.pos[1], mass=mass))
    
    # let's clear the screen first things first
    DISPLAYSURF.fill(BLACK)

    # let's draw the current mass in the top left
    textSurface = FONT.render("Mass = " + str(mass), True, WHITE)
    textRect = textSurface.get_rect()
    textRect.topleft = (5, 5)
    DISPLAYSURF.blit(textSurface, textRect)
    
    # let's update velocities
    for index, body in enumerate(bodies):
        body.update_velocity(index)

    # then we gotta update positions?
    for body in bodies:
        body.update_position()

    # drawing
    for body in bodies:
        body.draw(DISPLAYSURF)

    # let's check if any keys were pressed
    pressed = pygame.key.get_pressed()
    if pressed[K_UP]:
        mass += 10
    if pressed[K_DOWN]:
        if not (mass <= 1):
            mass -= 10
            mass = max(1, mass)


    # updating
    pygame.display.update()
    FPSController.tick(FPS)


# problem, when the bodies get super close to each other, they just spazz out and disappear.