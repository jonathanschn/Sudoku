# Print Sudoku board for testing
def print_board(board):
    for i in range(len(board)):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - - -")

        for j in range(len(board[0])):
            if j % 3 == 0 and j != 0:
                print(" | ", end="")
            if j == len(board) - 1:
                print(str(board[i][j]) + " | ")
            else:
                print(str(board[i][j]) + " ", end="")


def legal_position(board, number, position):
    box_x = position[1] // 3
    box_y = position[0] // 3
    for i in range(len(board[0])):
        if board[position[0]][i] == number and i != position[1]:
            return False

    for i in range(len(board)):
        if board[i][position[1]] == number and i != position[0]:
            return False

    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if board[i][j] == number and (i, j) != position:
                return False

    return True


def find_empty(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                return i, j
    return None


def backtrack(board):
    empty_cell = find_empty(board)
    if not empty_cell:
        return True
    else:
        cell_row, cell_col = empty_cell

    for i in range(1, 10):
        if legal_position(board, i, (cell_row, cell_col)):
            board[cell_row][cell_col] = i

            if backtrack(board):
                return True

            board[cell_row][cell_col] = 0

    return False
