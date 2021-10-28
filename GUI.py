import pygame
from solving import legal_position, find_empty
from BoardGenerator import BoardGenerator
from Button import Button
from Cube import Cube
from Config import *


class Gui:

    def __init__(self, rows, cols, width, height, win, initial_board):
        self.initial_board = initial_board
        self.rows = rows
        self.cols = cols
        self.cubes = [[Cube(self.initial_board[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)]
        self.width = width
        self.height = height
        self.model = None
        self.selected = None
        self.win = win

    def change_board(self, win):
        self.initial_board = BoardGenerator().board
        self.update_cubes()
        for row in range(0, 9):
            for col in range(0, 9):
                self.cubes[row][col].set(self.initial_board[row][col])
                self.cubes[row][col].draw_change(win, False)
        return

    def click(self, pos):
        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width / 9
            x = pos[0] // gap
            y = pos[1] // gap
            return int(y), int(x)
        else:
            return None

    def select(self, row, col):
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].selected_cube = False
        self.cubes[row][col].selected_cube = True
        self.selected = (row, col)

    def update_cubes(self):
        self.model = [[self.cubes[i][j].value for j in range(self.cols)] for i in range(self.rows)]

    def place(self, val):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set(val)
            self.update_cubes()
            if legal_position(self.model, val, (row, col)) and self.solve():
                return True
            else:
                self.cubes[row][col].set(0)
                self.update_cubes()
                return False

    def draw(self):
        gap = self.width / 9
        for i in range(self.rows + 1):
            if i % 3 == 0 and i != 0:
                thick = 4
            else:
                thick = 1
            pygame.draw.line(self.win, BLACK, (0, i * gap), (self.width, i * gap), thick)
            pygame.draw.line(self.win, BLACK, (i * gap, 0), (i * gap, self.height), thick)

        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].cube_draw(self.win)

    def solve(self):
        find = find_empty(self.model)
        if not find:
            return True
        else:
            row, col = find

        for i in range(1, 10):
            if legal_position(self.model, i, (row, col)):
                self.model[row][col] = i

                if self.solve():
                    return True

                self.model[row][col] = 0

        return False

    def solve_gui(self):
        self.update_cubes()
        find = find_empty(self.model)
        if not find:
            return True
        else:
            row, col = find

        for i in range(1, 10):
            if legal_position(self.model, i, (row, col)):
                self.model[row][col] = i
                self.cubes[row][col].set(i)
                self.cubes[row][col].draw_change(self.win, True)
                self.update_cubes()
                pygame.display.update()
                pygame.time.delay(50)

                if self.solve_gui():
                    return True

                self.model[row][col] = 0
                self.cubes[row][col].set(0)
                self.update_cubes()
                self.cubes[row][col].draw_change(self.win, False)
                pygame.display.update()
                pygame.time.delay(100)

        return False


def redraw_window(win, grid, strikes, button):
    win.fill(PAPER)
    fnt = pygame.font.SysFont("comicsans", 40)

    text = fnt.render("X " * strikes, True, RED)
    win.blit(text, (20, 560))
    grid.draw()
    button.button_draw(win)


def main():
    win = pygame.display.set_mode((540, 700))
    pygame.display.set_caption("Sudoku by JS")
    pygame.font.init()
    gui = Gui(9, 9, 540, 540, win, BoardGenerator().board)
    gen_button = Button(0, 600, 540, 100, win, False)
    key = None
    run = True

    strikes = 0
    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            gen_button.mouse_hover = False
            pos = pygame.mouse.get_pos()
            if gen_button.rect.collidepoint(pos):
                gen_button.mouse_hover = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9

                if event.key == pygame.K_SPACE:
                    gui.solve_gui()

                if event.key == pygame.K_RETURN:
                    if not gui.place(key):
                        strikes += 1
                        key = None

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if gen_button.rect.collidepoint(mouse_pos):
                    gui.change_board(win)
                    key = None
                else:
                    clicked = gui.click(pos)
                    if clicked:
                        gui.select(clicked[0], clicked[1])
                        key = None

        redraw_window(win, gui, strikes, gen_button)
        pygame.display.update()


main()
pygame.quit()
