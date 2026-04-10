import random

#Scan through 81 cells. If the position is blank -> return that position. If not -> return None
def find_empty(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return (i, j)
    return None

#Validation: Check that the number is unique on the row, column, and the corresponding 3x3 subgrid.
def is_valid(board, n, p):
    for r in range(len(board[0])):
        if board[p[0]][r] == n and p[1] != r:
            return False
    
    for c in range(len(board)):
        if board[c][p[1]] == n and p[0] != c:
            return False

    box_x = p[0] // 3
    box_y = p[1] // 3

    for i in range(box_x*3, box_x*3 + 3):
        for j in range(box_y*3, box_y*3 + 3):
            if board[i][j] == n and (i, j) != p:
                return False
    return True

#Solve function. Using the core Recursive Backtracking algorithm to solve the Sudoku board. Return True if a solution is found, else return False if it reaches a dead end.
def solve(board):
    empty = find_empty(board)
    #Base case: No empty cells left, puzzle is solved
    if not empty:
        return True
    else:
        r, c = empty

    #Try to fill the empty cell with number 1-9
    for i in range(1, 10):
        if is_valid(board, i, (r, c)):
            #Tentatively place the number
            board[r][c] = i
            
            #Recursively attempt to solve the rest of the board
            if solve(board):
                return True
            
            #Backtracking: The guess was wrong, reset cell to 0 and try next value
            board[r][c] = 0

    return False

#Count all possible solutions of the puzzle. Ensure that the board given to the player only has exactly 1 solution.
def count_solutions(board):
    empty = find_empty(board)
    if not empty:
        return 1
    
    r, c = empty
    count = 0
    for i in range(1, 10):
        if is_valid(board, i, (r, c)):
            board[r][c] = i
            count += count_solutions(board)
            board[r][c] = 0
            
            #Early Pruning: If more than 1 solution is found, stop searching -> Optimize performance
            if count > 1:
                return count
    return count

def generate_puzzle(attempts=40):
    board = [[0 for _ in range(9)] for _ in range(9)]
    
    #Randomly fill the first row with number 1 to 9
    first_row = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    random.shuffle(first_row)
    for i in range(9):
        board[0][i] = first_row[i]
        
    #Solve the board based on the first random row
    solve(board)
    
    solved_board = [row[:] for row in board] #Instead of using loop to copy the board, use slice notation to create an independent copy, which optimizes execution speed

    #Randomly pick cells to erase to create the board for player
    positions = [(r, c) for r in range(9) for c in range(9)]
    random.shuffle(positions)
    
    
    holes_dug = 0
    for r, c in positions:
        if holes_dug >= attempts:
            break
        
        #Backup the value before removing it
        backup = board[r][c]
        board[r][c] = 0
        
        #If after erasing the cell, the solution is still unique -> +1 holes
        if count_solutions(board) == 1:
            holes_dug += 1
        else: #If after erasing the cell, the board has another solution -> restore that cell with the backup
            board[r][c] = backup

    return board, solved_board