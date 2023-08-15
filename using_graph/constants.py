import pygame
from classes import *
###################################### CONSTANTS ############################################
SCREEN_SIZE = WIDTH, HEIGHT = 500,500
MIN = lambda a, b: a if b > a else b
RADIUS = MIN(WIDTH, HEIGHT)/2
CENT = CX, CY = WIDTH/2, HEIGHT/2
VCENT = V2(*CENT)
WHITE   = (255, 255, 255)
BLACK   = (  0,   0,   0)
RED     = (255,   0,   0)
GREEN   = (  0, 255,   0)
BLUE    = (  0,   0, 255)
