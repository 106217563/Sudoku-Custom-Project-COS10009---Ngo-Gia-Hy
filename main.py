import pygame
import sys
from logic import generate_puzzle 

pygame.init()
pygame.mixer.init()

width, height = 540, 600 
SIZE = 540 
LINE_THICK = 4 
LINE_THIN = 1 

WHITE = (255, 255, 255) #Background Color
BLACK = (0, 0, 0) #Grid Color
GRAY = (200, 200, 200) 
BLUE = (50, 111, 168)
RED = (255, 0, 0)
GREEN = (0, 128, 0)

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("SUDOKU") 

FONT = pygame.font.SysFont("consolas", 40)
FONT_2 = pygame.font.SysFont("consolas", 20)
LARGE_FONT = pygame.font.SysFont("arial", 60, bold=True)

HEART_IMG = pygame.image.load("images/heart.png").convert_alpha()
HEART_IMG = pygame.transform.scale(HEART_IMG, (30, 30))

try:
    WRONG_SOUND = pygame.mixer.Sound("sounds/wrong.mp3")
    WRONG_SOUND.set_volume(0.5) 
except:
    WRONG_SOUND = None
    
try:
    GAME_OVER = pygame.mixer.Sound("sounds/gameover.mp3")
    GAME_OVER.set_volume(0.5) 
except:
    GAME_OVER = None

def draw_grid():
    for i in range(10):
        if i % 3 == 0:
            thickness = LINE_THICK #The lines at the edges of each 3x3 box are more thick
        else:
            thickness = LINE_THIN 
            
        pygame.draw.line(screen, BLACK, (0, i * (SIZE // 9)), (SIZE, i * (SIZE // 9)), thickness)

    # Vẽ các cột dọc
    for i in range(10):
        if i % 3 == 0:
            thickness = LINE_THICK #The lines at the edges of each 3x3 box are more thick
        else:
            thickness = LINE_THIN
            
        pygame.draw.line(screen, BLACK, (i * (SIZE // 9), 0), (i * (SIZE // 9), SIZE), thickness)
        
def draw_num(board, original_cells):
    gap = SIZE // 9
    for i in range(9):
        for j in range(9):
            if board[i][j] != 0: #check if the cell is not blank
                color = BLACK if original_cells[i][j] else BLUE #Original puzzle numbers are black, while player inputs are blue
                text = FONT.render(str(board[i][j]), True, color)
                
                #Math formula to center the text in 1 single cell
                x = j * gap + (gap // 2 - text.get_width() // 2)
                y = i * gap + (gap // 2 - text.get_height() // 2)
                screen.blit(text, (x, y))
                
def draw_menu():
    title = LARGE_FONT.render("SUDOKU", True, BLACK)
    opt1 = FONT.render("Press 1: EASY", True, BLUE)
    opt2 = FONT.render("Press 2: MEDIUM", True, BLUE)
    opt3 = FONT.render("Press 3: HARD", True, RED)
            
    screen.blit(title, (width//2 - title.get_width()//2, 100))
    screen.blit(opt1, (width//2 - opt1.get_width()//2, 250))
    screen.blit(opt2, (width//2 - opt2.get_width()//2, 320))
    screen.blit(opt3, (width//2 - opt3.get_width()//2, 390))
    
def draw_end_screen(state):
    s = pygame.Surface((width, height))
    s.set_alpha(180) 
    
    if state == "WIN":
        s.fill(WHITE)
        text1 = LARGE_FONT.render("YOU WIN!", True, GREEN)
        text2_color = BLACK
    else: # GAMEOVER
        s.fill(BLACK)
        text1 = LARGE_FONT.render("GAME OVER", True, RED)
        text2_color = WHITE
        
    screen.blit(s, (0,0))
    
    text2 = FONT_2.render("Press 'R' to Return Menu", True, text2_color)
    text3 = FONT_2.render("Press 'ESC' to Quit", True, text2_color)
                
    screen.blit(text1, (width//2 - text1.get_width()//2, height//2 - 60))
    screen.blit(text2, (width//2 - text2.get_width()//2, height//2 + 10))
    screen.blit(text3, (width//2 - text3.get_width()//2, height//2 + 40))

#Convert the click from Pixels into 2D array coordinates (row, col)
def get_clicked_pos(pos):
    gap = SIZE // 9
    x, y = pos
    
    c = x // gap
    r = y // gap
    
    return r, c

def check_win(board):
    for row in board:
        if 0 in row:
            return False
    return True



# --- Main Loop ---
def main():    
    board = None
    solved_board = None
    
    state = "MENU"
    
    original_cells = None
    
    selected = None
    lives = 5
    running = True
    
    while running:
        screen.fill(WHITE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            #Get position
            if state == "MENU":
                if event.type == pygame.KEYDOWN:
                    attempts = 0
                    # Select Difficulty (Number of holes)
                    if event.key == pygame.K_1: attempts = 30 # Easy
                    elif event.key == pygame.K_2: attempts = 40 # Medium
                    elif event.key == pygame.K_3: attempts = 50 # Hard
                    
                    if attempts > 0:
                        board, solved_board = generate_puzzle(attempts=attempts)
                        original_cells = [[board[i][j] != 0 for j in range(9)] for i in range(9)]
                        
                        selected = None
                        lives = 5
                        state = "PLAYING" # Start the game
            
            # --- PLAYING SCREEN ---
            elif state == "PLAYING":
                # Get mouse position
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if pos[1] < SIZE: # Prevent clicking on the UI area below the board
                        selected = get_clicked_pos(pos)
            
                if event.type == pygame.KEYDOWN and selected:
                    row, col = selected
                    if not original_cells[row][col]:
                        val = None
                        
                        if event.key == pygame.K_1: val = 1
                        if event.key == pygame.K_2: val = 2
                        if event.key == pygame.K_3: val = 3
                        if event.key == pygame.K_4: val = 4
                        if event.key == pygame.K_5: val = 5
                        if event.key == pygame.K_6: val = 6
                        if event.key == pygame.K_7: val = 7
                        if event.key == pygame.K_8: val = 8
                        if event.key == pygame.K_9: val = 9
                    
                        #Check the player input with the final answer (To avoid valid input at the time but not the answer)
                        if val is not None:
                            if solved_board[row][col] == val:
                                board[row][col] = val
                                
                                if check_win(board):
                                    state = "WIN"
                            else:
                                if lives > 1:
                                    if WRONG_SOUND:
                                        WRONG_SOUND.play()
                                lives -= 1
                                
                                if lives <= 0:
                                    state = "GAMEOVER"
                                    GAME_OVER.play()
                
                        if event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
                            board[row][col] = 0
            elif state == "GAMEOVER" or state == "WIN":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        state = "MENU" #Press "R" to restart
                    elif event.key == pygame.K_ESCAPE:
                        running = False #Press Esc to turn off the game

        if state == "MENU":
            draw_menu()

        elif state == "PLAYING":
            draw_grid() 
            draw_num(board, original_cells)
            
            start_x = 20 
            start_y = 550 
            spacing = 10
        
            #Lives logic and draw the heart icons                
            for i in range(lives):
                current_x = start_x + i * (HEART_IMG.get_width() + spacing)
                screen.blit(HEART_IMG, (current_x, start_y))
            
            if selected:
                gap = SIZE // 9
                pygame.draw.rect(screen, RED, (selected[1] * gap, selected[0] * gap, gap, gap), 3)
        
        if state in ["WIN", "GAMEOVER"]:
                draw_end_screen(state)

            
        pygame.display.update()
    
if __name__ == "__main__":
    main()