import pygame
import sys
import copy
import random
from sudoku_generator import SudokuGenerator, generate_sudoku

# Screen and Color Constants
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 550
GRID_SIZE = 450
CELL_SIZE = GRID_SIZE // 9
BG_COLOR = (255, 255, 245)
LINE_COLOR = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GRAY = (128, 128, 128)

class Cell:
    def __init__(self, value, row, col, screen):
        self.value = value
        self.sketched_value = None
        self.row = row
        self.col = col
        self.screen = screen
        self.is_original = value != 0
        self.is_selected = False

    def draw(self, x_offset=25):
        # Draw cell background
        cell_rect = pygame.Rect(
            x_offset + self.col * CELL_SIZE,
            self.row * CELL_SIZE,
            CELL_SIZE,
            CELL_SIZE
        )
        
        # Highlight selected cell
        if self.is_selected:
            pygame.draw.rect(self.screen, (255, 220, 220), cell_rect)
            pygame.draw.rect(self.screen, RED, cell_rect, 3)
        
        font = pygame.font.Font(None, 36)
        small_font = pygame.font.Font(None, 24)
        
        # Draw cell value
        if self.value != 0:
            # Original cells in black, user-entered in blue
            color = LINE_COLOR if self.is_original else BLUE
            text = font.render(str(self.value), True, color)
            text_rect = text.get_rect(
                center=(x_offset + self.col * CELL_SIZE + CELL_SIZE // 2, 
                        self.row * CELL_SIZE + CELL_SIZE // 2)
            )
            self.screen.blit(text, text_rect)
        elif self.sketched_value:
            # Smaller font for sketched value
            text = small_font.render(str(self.sketched_value), True, GRAY)
            text_rect = text.get_rect(
                topleft=(x_offset + self.col * CELL_SIZE + 5,
                        self.row * CELL_SIZE + 5)
            )
            self.screen.blit(text, text_rect)

class Board:
    def __init__(self, width, height, screen, difficulty):
        self.width = width
        self.height = height
        self.screen = screen
        self.difficulty = difficulty
        self.selected_cell = None
        self.cells = [[None for _ in range(9)] for _ in range(9)]
        self.original_board = None
        
        # Generate Sudoku board based on difficulty
        if difficulty == 'easy':
            removed_cells = 30
        elif difficulty == 'medium':
            removed_cells = 40
        else:  # hard
            removed_cells = 50
        
        # Keep generating until we get a valid board
        while True:
            board = generate_sudoku(9, removed_cells)
            if self.is_solvable(board):
                break
        
        self.original_board = copy.deepcopy(board)
        self.solution = self.solve_board(copy.deepcopy(board))
        
        # Create Cell objects
        for row in range(9):
            for col in range(9):
                self.cells[row][col] = Cell(board[row][col], row, col, screen)

    def move_selected(self, direction):
        if not self.selected_cell:
            # If no cell is selected, select top-left cell
            self.select(0, 0)
            return

        current_row = self.selected_cell.row
        current_col = self.selected_cell.col
        
        if direction == 'up':
            new_row = (current_row - 1) % 9
            self.select(new_row, current_col)
        elif direction == 'down':
            new_row = (current_row + 1) % 9
            self.select(new_row, current_col)
        elif direction == 'left':
            new_col = (current_col - 1) % 9
            self.select(current_row, new_col)
        elif direction == 'right':
            new_col = (current_col + 1) % 9
            self.select(current_row, new_col)

    def is_solvable(self, board):
        return self.solve_board(copy.deepcopy(board)) is not None

    def solve_board(self, board):
        empty = self.find_empty_in_board(board)
        if not empty:
            return board
            
        row, col = empty
        
        for num in range(1, 10):
            if self.is_valid_in_board(board, row, col, num):
                board[row][col] = num
                
                if self.solve_board(board):
                    return board
                    
                board[row][col] = 0
                
        return None

    def find_empty_in_board(self, board):
        for row in range(9):
            for col in range(9):
                if board[row][col] == 0:
                    return (row, col)
        return None

    def is_valid_in_board(self, board, row, col, num):
        # Check row
        for x in range(9):
            if board[row][x] == num:
                return False
                
        # Check column
        for x in range(9):
            if board[x][col] == num:
                return False
                
        # Check box
        box_x = (col // 3) * 3
        box_y = (row // 3) * 3
        for i in range(3):
            for j in range(3):
                if board[box_y + i][box_x + j] == num:
                    return False
                    
        return True

    def draw(self):
        # Draw background
        pygame.draw.rect(self.screen, BG_COLOR, 
                        (25, 0, GRID_SIZE, GRID_SIZE))
        
        # Draw cells
        for row in self.cells:
            for cell in row:
                cell.draw()

        # Draw grid
        for i in range(10):
            line_width = 4 if i % 3 == 0 else 1
            # Horizontal lines
            pygame.draw.line(self.screen, LINE_COLOR, 
                (25, i * CELL_SIZE), 
                (25 + GRID_SIZE, i * CELL_SIZE), line_width)
            # Vertical lines
            pygame.draw.line(self.screen, LINE_COLOR, 
                (25 + i * CELL_SIZE, 0), 
                (25 + i * CELL_SIZE, GRID_SIZE), line_width)

    def select(self, row, col):
        # Deselect previous cell
        if self.selected_cell:
            self.selected_cell.is_selected = False
        
        # Select new cell
        self.selected_cell = self.cells[row][col]
        self.selected_cell.is_selected = True

    def click(self, x, y):
        # Adjust grid
        adjusted_x = x - 25
        if 0 <= adjusted_x < GRID_SIZE and 0 <= y < GRID_SIZE:
            col = adjusted_x // CELL_SIZE
            row = y // CELL_SIZE
            return row, col
        return None

    def reset_to_original(self):
        for row in range(9):
            for col in range(9):
                self.cells[row][col].value = self.original_board[row][col]
                self.cells[row][col].sketched_value = None
                self.cells[row][col].is_selected = False
        self.selected_cell = None

    def clear(self):
        if self.selected_cell and not self.selected_cell.is_original:
            self.selected_cell.value = 0
            self.selected_cell.sketched_value = None

    def sketch(self, value):
        if self.selected_cell and not self.selected_cell.is_original:
            self.selected_cell.sketched_value = value

    def place_number(self, value):
        if self.selected_cell and not self.selected_cell.is_original:
            self.selected_cell.value = value
            self.selected_cell.sketched_value = None
            return True
        return False

    def is_full(self):
        for row in self.cells:
            for cell in row:
                if cell.value == 0:
                    return False
        return True

    def check_board(self):
        # Create board
        current_board = [[self.cells[row][col].value 
                         for col in range(9)] 
                         for row in range(9)]
        
        # Check for valid numbers 1-9
        for i in range(9):
            row_nums = set()
            col_nums = set()
            box_nums = set()
            
            for j in range(9):
                # Check rows
                if current_board[i][j] not in row_nums:
                    row_nums.add(current_board[i][j])
                else:
                    return False
                    
                # Check columns
                if current_board[j][i] not in col_nums:
                    col_nums.add(current_board[j][i])
                else:
                    return False
                    
                # Check 3x3 boxes
                box_row = (i // 3) * 3 + j // 3
                box_col = (i % 3) * 3 + j % 3
                if current_board[box_row][box_col] not in box_nums:
                    box_nums.add(current_board[box_row][box_col])
                else:
                    return False
                
        return True

def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Sudoku")
    
    # Load background image
    try:
        bg_image = pygame.image.load("SUDOKU.jpg")
        bg_image = pygame.transform.scale(bg_image, (WINDOW_WIDTH, WINDOW_HEIGHT))
        bg_image_game_over = pygame.image.load("game_over.jpg")
        bg_image_game_over = pygame.transform.scale(bg_image_game_over, (WINDOW_WIDTH, WINDOW_HEIGHT))
    except:
        bg_image = None
    
    # Game states
    STARTING_SCREEN = 0
    GAME_SCREEN = 1
    GAME_OVER_SCREEN = 2
    GAME_WON_SCREEN = 3
    
    current_screen = STARTING_SCREEN
    current_board = None
    difficulty = None

    # Buttons
    easy_button = pygame.Rect(100, 300, 100, 50)
    medium_button = pygame.Rect(200, 300, 100, 50)
    hard_button = pygame.Rect(300, 300, 100, 50)
    reset_button = pygame.Rect(50, 500, 100, 40)
    restart_button = pygame.Rect(200, 500, 100, 40)
    exit_button = pygame.Rect(350, 500, 100, 40)

    font = pygame.font.Font(None, 36)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if current_screen == STARTING_SCREEN:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if easy_button.collidepoint(event.pos):
                        difficulty = 'easy'
                        current_board = Board(GRID_SIZE, GRID_SIZE, screen, difficulty)
                        current_screen = GAME_SCREEN
                    elif medium_button.collidepoint(event.pos):
                        difficulty = 'medium'
                        current_board = Board(GRID_SIZE, GRID_SIZE, screen, difficulty)
                        current_screen = GAME_SCREEN
                    elif hard_button.collidepoint(event.pos):
                        difficulty = 'hard'
                        current_board = Board(GRID_SIZE, GRID_SIZE, screen, difficulty)
                        current_screen = GAME_SCREEN

            elif current_screen == GAME_SCREEN:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Check game buttons
                    if reset_button.collidepoint(event.pos):
                        current_board.reset_to_original()
                    elif restart_button.collidepoint(event.pos):
                        current_screen = STARTING_SCREEN
                    elif exit_button.collidepoint(event.pos):
                        running = False

                    # Check cell selection
                    click_pos = current_board.click(event.pos[0], event.pos[1])
                    if click_pos:
                        current_board.select(click_pos[0], click_pos[1])

                if event.type == pygame.KEYDOWN:
                    # Number and game actions
                    if current_board.selected_cell:
                        if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, 
                                       pygame.K_4, pygame.K_5, pygame.K_6, 
                                       pygame.K_7, pygame.K_8, pygame.K_9]:
                            num = int(event.unicode)
                            current_board.sketch(num)
                        
                        elif event.key == pygame.K_RETURN:
                            if current_board.selected_cell.sketched_value:
                                current_board.place_number(
                                    current_board.selected_cell.sketched_value)
                                if current_board.is_full():
                                    if current_board.check_board():
                                        current_screen = GAME_WON_SCREEN
                                    else:
                                        current_screen = GAME_OVER_SCREEN
                        
                        elif event.key == pygame.K_BACKSPACE:
                            current_board.clear()
                    
                    # Arrow key navigation
                    if event.key == pygame.K_UP:
                        current_board.move_selected('up')
                    elif event.key == pygame.K_DOWN:
                        current_board.move_selected('down')
                    elif event.key == pygame.K_LEFT:
                        current_board.move_selected('left')
                    elif event.key == pygame.K_RIGHT:
                        current_board.move_selected('right')

            elif current_screen in [GAME_OVER_SCREEN, GAME_WON_SCREEN]:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if restart_button.collidepoint(event.pos):
                        current_screen = STARTING_SCREEN

        screen.fill(BG_COLOR)

        if current_screen == STARTING_SCREEN:
            # Draw background image
            if bg_image:
                screen.blit(bg_image, (0, 0))
            
            difficulty_text = font.render("Select Difficulty", True, BLUE)
            screen.blit(difficulty_text, (150, 200))

            # Draw difficulty buttons
            pygame.draw.rect(screen, GREEN, easy_button)
            pygame.draw.rect(screen, GREEN, medium_button)
            pygame.draw.rect(screen, GREEN, hard_button)
            
            easy_text = font.render("Easy", True, LINE_COLOR)
            medium_text = font.render("Medium", True, LINE_COLOR)
            hard_text = font.render("Hard", True, LINE_COLOR)
            
            screen.blit(easy_text, (easy_button.x + 20, easy_button.y + 10))
            screen.blit(medium_text, (medium_button.x + 10, medium_button.y + 10))
            screen.blit(hard_text, (hard_button.x + 20, hard_button.y + 10))

        elif current_screen == GAME_SCREEN:
            current_board.draw()

            # Draw game buttons
            pygame.draw.rect(screen, GREEN, reset_button)
            pygame.draw.rect(screen, GREEN, restart_button)
            pygame.draw.rect(screen, GREEN, exit_button)

            reset_text = font.render("Reset", True, LINE_COLOR)
            restart_text = font.render("Restart", True, LINE_COLOR)
            exit_text = font.render("Exit", True, LINE_COLOR)

            screen.blit(reset_text, (reset_button.x + 10, reset_button.y + 10))
            screen.blit(restart_text, (restart_button.x + 10, restart_button.y + 10))
            screen.blit(exit_text, (exit_button.x + 20, exit_button.y + 10))

        elif current_screen == GAME_WON_SCREEN:
            if bg_image:
                screen.blit(bg_image, (0, 0))
            game_won_text = font.render("Game Won!", True, GREEN)
            screen.blit(game_won_text, (180, 200))
            
            # Draw restart button
            pygame.draw.rect(screen, GREEN, restart_button)
            restart_text = font.render("Restart", True, LINE_COLOR)
            screen.blit(restart_text, (restart_button.x + 10, restart_button.y + 10))

        elif current_screen == GAME_OVER_SCREEN:
            if bg_image_game_over:
                screen.blit(bg_image_game_over, (0, 0))
            game_over_text = font.render("Game Over :(", True, RED)
            screen.blit(game_over_text, (180, 200))
            
            # Draw restart button
            pygame.draw.rect(screen, GREEN, restart_button)
            restart_text = font.render("Restart", True, LINE_COLOR)
            screen.blit(restart_text, (restart_button.x + 10, restart_button.y + 10))

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()