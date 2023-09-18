import pygame

from game.main_menu import MainMenu

WIDTH = 1920
HEIGHT = 1080

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN | pygame.NOFRAME)

MainMenu(screen)
