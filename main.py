import pygame

from game.main_menu import MainMenu

WIDTH = 1080
HEIGHT = WIDTH * (9 / 16)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME)

MainMenu(screen)
