import random
import pygame
import sys


def ExitGame():
    pygame.quit()
    sys.exit()


def RandomBrightColor():
    Red = random.randrange(100, 256)
    Green = random.randrange(100, 256)
    Blue = random.randrange(100, 256)

    RGB = (Red, Green, Blue)
    return RGB
