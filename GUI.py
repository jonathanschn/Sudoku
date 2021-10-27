import pygame
import copy
from random import shuffle
from solving import legal_position, find_empty

PAPER = (243, 238, 203)
PURPLE = (127, 0, 255)
GREEN = (202, 231, 193)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


# Generating a 9*9 Sudoku board as 2-dim array
# A valid Sudoku has only 1 solution
# Generating a new Sudoku requires creating a valid solution, then gradually removing
# numbers while insuring there is only single solution
class BoardGenerator:

    def __init__(self, board=None):
        self.board = [[0 for i in range(9)] for j in range(9)]
        self.solution_count = 0
        self.generate_board()

    def generate_board(self):
        self.generate_solution(self.board)
        self.remove_nums()
        return

    # Generate a complete Sudoku
    def generate_solution(self, board):
        number_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        for i in range(0, 81):
            row = i // 9
            col = i % 9
            if board[row][col] == 0:
                shuffle(number_list)
                for number in number_list:
                    if legal_position(board, number, (row, col)):
                        board[row][col] = number
                        if not find_empty(board):
                            return True
                        else:
                            if self.generate_solution(board):
                                return True
                break
        board[row][col] = 0
        return False

    # Helper function for remove_nums
    # Create stack with non empty squares, randomized
    def get_non_empty_squares(self, board):
        non_empty_squares = []  # stack
        for row in range(len(board)):
            for col in range(len(board)):
                if board[row][col] != 0:
                    non_empty_squares.append((row, col))
        shuffle(non_empty_squares)
        return non_empty_squares

    def remove_nums(self):
        non_empty_squares = self.get_non_empty_squares(self.board)
        non_empty_squares_count = len(non_empty_squares)
        # 'rounds' parameter allows several failures before returning a board. More than 3 may take a while..
        rounds = 2
        while rounds > 0 and non_empty_squares_count >= 17:  # The hardest Sudoku has minimum of 17 non-empty squares
            row, col = non_empty_squares.pop()
            non_empty_squares_count -= 1
            # backup the value of removed square
            removed_square = self.board[row][col]
            self.board[row][col] = 0
            # make a copy of the grid and try to solve it
            board_copy = copy.deepcopy(self.board)
            self.solution_count = 0
            self.solutions_amount_gen(board_copy)
            # if there is more than one solution, restore the removed cell
            if self.solution_count != 1:
                self.board[row][col] = removed_square
                non_empty_squares_count += 1
                rounds -= 1
        return

    # Helper function for remove_nums
    # Counts amount of solutions for an unfilled board
    def solutions_amount_gen(self, current_board):
        for i in range(0, 81):
            row = i // 9
            col = i % 9
            if current_board[row][col] == 0:
                for number in range(1, 10):
                    if legal_position(current_board, number, (row, col)):
                        current_board[row][col] = number
                        if not find_empty(current_board):
                            self.solution_count += 1
                            break
                        else:
                            if self.solutions_amount_gen(current_board):
                                return True
                break
        current_board[row][col] = 0
        return False


class Grid:

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
        elif pos[1] > self.height + 60:
            return 1000, 1000
        else:
            return None

    def select(self, row, col):
        # Reset all other
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].selectedCube = False
        self.cubes[row][col].selectedCube = True
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
        # Draw Grid Lines
        gap = self.width / 9
        for i in range(self.rows + 1):
            if i % 3 == 0 and i != 0:
                thick = 4
            else:
                thick = 1
            pygame.draw.line(self.win, BLACK, (0, i * gap), (self.width, i * gap), thick)
            pygame.draw.line(self.win, BLACK, (i * gap, 0), (i * gap, self.height), thick)

        # Draw Cubes
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


class Cube:
    rows = 9
    cols = 9

    def __init__(self, value, row, col, width, height):
        self.value = value
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selectedCube = False

    def cube_draw(self, win):
        fnt = pygame.font.SysFont("comicsans", 40)

        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        if not (self.value == 0):
            text = fnt.render(str(self.value), 1, BLACK)
            win.blit(text, (x + (gap / 2 - text.get_width() / 2), y + (gap / 2 - text.get_height() / 2)))

        if self.selectedCube:
            pygame.draw.rect(win, PURPLE, (x, y, gap, gap), 3)

    def draw_change(self, win, g=True):
        fnt = pygame.font.SysFont("comicsans", 40)

        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        pygame.draw.rect(win, GREEN, (x, y, gap, gap), 0)

        text = fnt.render(str(self.value), True, BLACK)
        win.blit(text, (x + (gap / 2 - text.get_width() / 2), y + (gap / 2 - text.get_height() / 2)))
        if g:
            pygame.draw.rect(win, BLACK, (x, y, gap, gap), 1)
        else:
            pygame.draw.rect(win, RED, (x, y, gap, gap), 3)

    def set(self, val):
        self.value = val


class Button:

    def __init__(self, pos_x, pos_y, width, height, win):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.width = width
        self.height = height
        self.selected = False

    def button_draw(self, win):
        x = self.pos_x
        y = self.pos_y
        width = self.width
        height = self.height
        fnt = pygame.font.SysFont("comicsans", 40)
        pygame.draw.rect(win, BLACK, (x, y, width, height), 4)
        text = fnt.render("GENERATE NEW SUDOKU", True, BLACK)
        win.blit(text, (x + (width / 5), y + (height / 3)))


def redraw_window(win, grid, strikes, button):
    win.fill(PAPER)
    fnt = pygame.font.SysFont("comicsans", 40)

    # Draw Strikes
    text = fnt.render("X " * strikes, 1, RED)
    win.blit(text, (20, 560))
    # Draw grid and board
    grid.draw()
    button.button_draw(win)


def main():
    win = pygame.display.set_mode((540, 700))
    pygame.display.set_caption("Sudoku by JS")
    pygame.font.init()
    grid = Grid(9, 9, 540, 540, win, BoardGenerator().board)
    gen_button = Button(0, 600, 540, 100, win)
    key = None
    run = True

    strikes = 0
    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
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
                    grid.solve_gui()

                if event.key == pygame.K_RETURN:
                    i, j = grid.selected
                    if grid.place(key):
                        print("Success")
                    else:
                        print("Wrong")
                        strikes += 1
                        key = None

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked = grid.click(pos)
                if clicked:
                    if clicked[0] == 1000:
                        grid.change_board(win)
                        key = None
                    else:
                        grid.select(clicked[0], clicked[1])
                        key = None

        redraw_window(win, grid, strikes, gen_button)
        pygame.display.update()


main()
pygame.quit()
