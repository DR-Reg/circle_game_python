## Human play main file
import pygame
import Agent
from CircleGame import CircleGame

SIZE = 500
RAD = 1 
window = pygame.display.set_mode((SIZE,SIZE))
pygame.init()

rd = Agent.Random(pygame, RAD, SIZE/2)
hum = Agent.Human(pygame, RAD, SIZE/2)

game = CircleGame([rd,hum], RAD)

win = False

while not win:
    win, moves = game.make_move()