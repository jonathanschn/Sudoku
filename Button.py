import pygame
from Config import *


class Button:

    def __init__(self, pos_x, pos_y, width, height, win, mouse_hover):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.width = width
        self.height = height
        self.selected = False
        self.mouse_hover = False
        self.rect = pygame.Rect(self.pos_x, self.pos_y, width, height)

    def button_draw(self, win):
        width = self.width
        height = self.height
        fnt = pygame.font.SysFont("comicsans", 40)
        color = BLACK
        if self.mouse_hover:
            color = PURPLE
        pygame.draw.rect(win, color, self.rect, 4)
        text = fnt.render("GENERATE NEW SUDOKU", True, color)
        win.blit(text, (self.pos_x + (width / 5), self.pos_y + (height / 3)))


class Button2:
    def __init__(self, text, pos, font, bg="black"):
        self.x, self.y = pos
        self.font = pygame.font.SysFont("Arial", 40)

