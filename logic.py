import random

def find_empty(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return (i, j)
    return None

def is_valid(board, n, p):
    for r in range(len(board[0])):
        if board[p[0]][r] == n and p[1] != r:
            return False
    
    for c in range(len(board)):
        if board[c][p[1]] == n and p[0] != c:
            return False

    box_x = p[0] // 3
    box_y = p[1] // 3

    for c in range(box_x*3, box_x*3 + 3):
        for r in range(box_y*3, box_y*3 + 3):
            if board[c][r] == n and (c, r) != p:
                return False
    
    return True

def solve(board):
    empty = find_empty(board)
    if not empty:
        return True
    else:
        r, c = empty

    for i in range(1, 10):
        if is_valid(board, i, (r, c)):
            board[r][c] = i

            if solve(board):
                return True
            
            board[r][c] = 0

    return False

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
            
            if count > 1:
                return count
    return count

def generate_puzzle(attempts=40):
    board = [[0 for _ in range(9)] for _ in range(9)]
    

    first_row = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    random.shuffle(first_row)
    for i in range(9):
        board[0][i] = first_row[i]
        

    solve(board)
    
    solved_board = [row[:] for row in board]

    positions = [(r, c) for r in range(9) for c in range(9)]
    random.shuffle(positions)
    
    holes_dug = 0
    for r, c in positions:
        if holes_dug >= attempts:
            break
        
        backup = board[r][c]
        board[r][c] = 0
        
        if count_solutions(board) == 1:
            holes_dug += 1
        else:
            board[r][c] = backup

    return board, solved_board