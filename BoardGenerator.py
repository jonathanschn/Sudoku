import copy
from random import shuffle
from solving import legal_position, find_empty
from Config import *
# Generating a 9*9 Sudoku board as 2-dim array
# A valid Sudoku has only 1 solution
# Generating a new Sudoku requires creating a valid solution, then gradually removing
# numbers, while ensuring there is only one single solution


class BoardGenerator:

    def __init__(self, board=None):
        self.board = [[0 for i in range(9)] for j in range(9)]
        self.solution_count = 0
        self.generate_board()

    def generate_board(self):
        self.generate_solution(self.board)
        self.remove_nums()
        return

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

    def get_non_empty_squares(self, board):
        non_empty_squares = []
        for row in range(len(board)):
            for col in range(len(board)):
                if board[row][col] != 0:
                    non_empty_squares.append((row, col))
        shuffle(non_empty_squares)
        return non_empty_squares

    def remove_nums(self):
        non_empty_squares = self.get_non_empty_squares(self.board)
        non_empty_squares_count = len(non_empty_squares)
        failures = 0
        while failures < MAX_FAILURES and non_empty_squares_count >= MIN_HINTS:
            row, col = non_empty_squares.pop()
            non_empty_squares_count -= 1
            removed_square = self.board[row][col]
            self.board[row][col] = 0

            board_copy = copy.deepcopy(self.board)
            self.solution_count = 0
            self.solutions_amount_gen(board_copy)

            # if there is more than one solution, restore the removed cell
            if self.solution_count != 1:
                self.board[row][col] = removed_square
                non_empty_squares_count += 1
                failures += 1
        return

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
