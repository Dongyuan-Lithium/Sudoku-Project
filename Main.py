import pygame, sys
from pygame import MOUSEBUTTONDOWN

from Cell_Class import *
from FinalProjectExample.tictactoe import is_valid
from sudoku_generator import SudokuGenerator
from sudoku_generator import *



BG_COLOR = (255, 255, 245)
green = (0, 255, 0)
blue = (0, 0, 128)
LINE_COLOR = (0, 0, 0)
#Initializing the screen/colors
sudoku_image = pygame.image.load("SUDOKU.jpg")
game_over_image = pygame.image.load("game_over.jpg")

pygame.init()
font = pygame.font.Font('freesansbold.ttf', 32)
text = font.render('Welcome to Sudoku!', True, green, blue)
text_2 = font.render('Select Game Mode', True, green, blue)
text_3 = font.render('Easy', True, green, blue)
text_4 = font.render('Medium', True, green, blue)
text_5 = font.render('Hard', True, green, blue)
text_6 = font.render('Reset', True, green, blue)
text_7 = font.render('Restart', True, green, blue)
text_8 = font.render('Exit',True, green, blue)
text_9 = font.render('Game over :(', True, green, blue)
text_10 = font.render('1', True, green, blue)
text_11 = font.render('2', True, green, blue)
text_12 = font.render('3', True, green, blue)
text_13 = font.render('4', True, green, blue)
text_14 = font.render('5', True, green, blue)
text_15 = font.render('6', True, green, blue)
text_16 = font.render('7', True, green, blue)
text_17 = font.render('8', True, green, blue)
text_18 = font.render('9', True, green, blue)
textRect = text.get_rect()
text2rect = text_2.get_rect()
text3rect = text_3.get_rect()
text4rect = text_4.get_rect()
text5rect = text_5.get_rect()
text6rect = text_6.get_rect()
text7rect = text_7.get_rect()
text8rect = text_8.get_rect()
text9rect = text_9.get_rect()
text10rect = text_10.get_rect()
text11rect = text_11.get_rect()
text12rect = text_12.get_rect()
text13rect = text_13.get_rect()
text14rect = text_14.get_rect()
text15rect = text_15.get_rect()
text16rect = text_16.get_rect()
text17rect = text_17.get_rect()
text18rect = text_18.get_rect()
textRect.center = (500 // 2, 200 // 2)
text2rect.center = (500//2, 500//2)
text3rect.center = (250 //2, 700//2)
text4rect.center = (500//2, 700//2)
text5rect.center = (750//2, 700//2)
screen = pygame.display.set_mode((500,500))
screen.fill(BG_COLOR)
screen.blit(sudoku_image,sudoku_image.get_rect(center = (500,500)))
screen.blit(text, textRect)
screen.blit(text_2,text2rect)
screen.blit(text_3, text3rect)
screen.blit(text_4,text4rect)
screen.blit(text_5,text5rect)
pygame.display.flip()

def starting_screen():
    screen.fill(BG_COLOR)
    screen.blit(sudoku_image, sudoku_image.get_rect(center=(500, 500)))
    screen.blit(text, textRect)
    screen.blit(text_2, text2rect)
    screen.blit(text_3, text3rect)
    screen.blit(text_4, text4rect)
    screen.blit(text_5, text5rect)
    pygame.display.flip()

def draw_game_over():
    screen.fill(BG_COLOR)
    screen.blit(game_over_image,game_over_image.get_rect(center = (250,250)))
    text9rect.center = (250,250)
    screen.blit(text_9,text9rect)
    text7rect.center = (250,350)
    screen.blit(text_7,text7rect)
    if text7rect.collidepoint(event.pos):
        starting_screen()





def generate_numbers_fixed(sudoku, num_to_fill=20):
    """
    Fill random cells on the Sudoku board with numbers and display them instantly.

    Parameters:
    sudoku (SudokuGenerator): The Sudoku generator instance.
    num_to_fill (int): The number of random cells to fill.
    """
    # Adjust cell size to match the grid size
    cell_width = 500 // 9  # 500 pixels wide, 9 columns
    cell_height = 390 // 9  # 450 pixels tall, 9 rows
    filled_positions = set()
    max_attempts_per_cell = 100  # Limit attempts to prevent infinite loops

    # Randomly select unique cells to fill
    while len(filled_positions) < num_to_fill:
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        if (row, col) not in filled_positions:
            attempts = 0
            num = random.randint(1, 9)
            while not sudoku.is_valid(row, col, num) and attempts < max_attempts_per_cell:
                num = random.randint(1, 9)
                attempts += 1

            if attempts < max_attempts_per_cell and sudoku.is_valid(row,col,num):
                sudoku.board[row][col] = num  # Place the number
                filled_positions.add((row, col))
            else:
                print(f"Skipping cell ({row}, {col}) after {attempts} attempts.")

    # Render all filled cells in a single pass
    screen.fill(BG_COLOR)  # Clear the screen
    draw_grid()  # Draw the grid lines

    for row, col in filled_positions:
        num = sudoku.board[row][col]
        # Adjust the position for the grid's layout
        text = font.render(str(num), True, LINE_COLOR)
        text_rect = text.get_rect(
            center=(col * cell_width + cell_width // 2, row * cell_height + cell_height // 2)
        )
        screen.blit(text, text_rect)

    # Update the screen once all numbers are rendered
    pygame.display.update()

def draw_grid():
    # Adjusted for 450 pixels height (50px space left at the bottom for buttons)
    grid_height = 390  # height of the grid (leaving 50px for buttons)
    grid_width = 500   # width of the grid

    # Draw horizontal lines
    for i in range(1, grid_height // 130 + 1):  # Adjusted number of lines to fit
        pygame.draw.line(
            screen,
            LINE_COLOR,
            (0, i * 130),
            (grid_width, i * 130),
            5
        )


    # Draw vertical lines
    for i in range(1, grid_width // 166 + 1):  # Adjusted number of vertical lines to fit
        pygame.draw.line(
            screen,
            LINE_COLOR,
            (i * 166, 0),
            (i * 166, grid_height),
            5
        )

    # Draw additional horizontal lines (43px space)
    for i in range(1, grid_height // 43 + 1):  # Adjusted number of lines
        pygame.draw.line(
            screen,
            LINE_COLOR,
            (0, i * 43),
            (grid_width, i * 43),
            1
        )

    # Draw additional vertical lines (55px space)
    for i in range(1, grid_width // 55 + 1):  # Adjusted number of lines
        pygame.draw.line(
            screen,
            LINE_COLOR,
            (i * 55, 0),
            (i * 55, grid_height),
            1
        )

def generate_current_grid(board):
    print(board)



pygame.display.set_caption("Sudoku")
chip_font = pygame.font.Font(None, 400)
game_over_font = pygame.font.Font(None, 40)
game_over = False

sudoku = None
sudoku_2 = None
sudoku_3 = None
x, y = None, None
passed_test = None
testing = True

while True:
    #event loop, or to keep the game continiously going
    row = None
    col = None
    game = 0
    for event in pygame.event.get():
        #Iterating through all the events that could possible happen
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            if event.button == 1:
                x, y = event.pos
                if text3rect.collidepoint(event.pos) and testing is True:
                    sudoku = SudokuGenerator(500, 30)
                    screen.fill(BG_COLOR)
                    draw_grid()
                    generate_numbers_fixed(sudoku, 51)
                    pygame.display.update()
                    text6rect.center = (75,450)
                    screen.blit(text_6,text6rect)
                    text7rect.center = (250,450)
                    screen.blit(text_7,text7rect)
                    text8rect.center = (400,450)
                    screen.blit(text_8,text8rect)
                    testing = False
                    sudoku.print_board()
                    continue


                elif text4rect.collidepoint(event.pos) and testing is True:
                    sudoku_2 = SudokuGenerator(500, 40)
                    screen.fill(BG_COLOR)
                    draw_grid()
                    generate_numbers_fixed(sudoku_2, 41)
                    pygame.display.flip()
                    text6rect.center = (75, 450)
                    screen.blit(text_6, text6rect)
                    text7rect.center = (250, 450)
                    screen.blit(text_7, text7rect)
                    text8rect.center = (400, 450)
                    screen.blit(text_8, text8rect)
                    testing = False
                    continue




                elif text5rect.collidepoint(event.pos) and testing is True:
                    sudoku_3 =SudokuGenerator(500, 50)
                    screen.fill(BG_COLOR)
                    draw_grid()
                    generate_numbers_fixed(sudoku_3, 31)
                    pygame.display.flip()
                    text6rect.center = (75, 450)
                    screen.blit(text_6, text6rect)
                    text7rect.center = (250, 450)
                    screen.blit(text_7, text7rect)
                    text8rect.center = (400, 450)
                    screen.blit(text_8, text8rect)
                    testing = False
                    continue

                if text6rect.collidepoint(event.pos) and sudoku is not None:
                    screen.fill(BG_COLOR)
                    draw_grid()
                    pygame.display.update()

                if text7rect.collidepoint(event.pos):
                    starting_screen()


                if text8rect.collidepoint(event.pos):
                    draw_game_over()

        if event.type == pygame.KEYDOWN:
            cell_width = 500 / 9
            cell_length = 390 / 9
            row = int(x // cell_width)
            col = int(y // cell_length)
            if sudoku is not None:
                if event.key == pygame.K_1:
                    num = 1
                    text10rect.center = (x,y)
                    screen.blit(text_10,text10rect)
                    if sudoku.valid_in_row(row,num):
                        print('yes!')
                        print(row,col)

                if event.key == pygame.K_2:
                    num = 2
                    text11rect.center = (x,y)
                    screen.blit(text_11,text11rect)

                if event.key == pygame.K_3:
                    num = 3
                    text12rect.center = (x,y)
                    screen.blit(text_12,text12rect)

                if event.key == pygame.K_4:
                    num = 4
                    text13rect.center = (x,y)
                    screen.blit(text_13,text13rect)

                if event.key == pygame.K_5:
                    num = 5
                    text14rect.center = (x,y)
                    screen.blit(text_14,text14rect)

                if event.key == pygame.K_6:
                    num = 6
                    text15rect.center = (x,y)
                    screen.blit(text_15, text15rect)

                if event.key == pygame.K_7:
                    num = 7
                    text16rect.center = (x,y)
                    screen.blit(text_16,text16rect)

                if event.key == pygame.K_8:
                    num = 8
                    text17rect.center = (x,y)
                    screen.blit(text_17,text17rect)

                if event.key == pygame.K_9:
                    num = 9
                    text18rect.center = (x,y)
                    screen.blit(text_18, text18rect)

            elif sudoku_2 is not None:
                if event.key == pygame.K_1:
                    num = 1
                    text10rect.center = (x, y)
                    screen.blit(text_10, text10rect)

                if event.key == pygame.K_2:
                    num = 2
                    text11rect.center = (x, y)
                    screen.blit(text_11, text11rect)

                if event.key == pygame.K_3:
                    num = 3
                    text12rect.center = (x, y)
                    screen.blit(text_12, text12rect)

                if event.key == pygame.K_4:
                    num = 4
                    text13rect.center = (x, y)
                    screen.blit(text_13, text13rect)

                if event.key == pygame.K_5:
                    num = 5
                    text14rect.center = (x, y)
                    screen.blit(text_14, text14rect)

                if event.key == pygame.K_6:
                    num = 6
                    text15rect.center = (x, y)
                    screen.blit(text_15, text15rect)

                if event.key == pygame.K_7:
                    num = 7
                    text16rect.center = (x, y)
                    screen.blit(text_16, text16rect)

                if event.key == pygame.K_8:
                    num = 8
                    text17rect.center = (x, y)
                    screen.blit(text_17, text17rect)

                if event.key == pygame.K_9:
                    num = 9
                    text18rect.center = (x, y)
                    screen.blit(text_18, text18rect)

            if sudoku_3 is not None:
                if event.key == pygame.K_1:
                    num = 1
                    text10rect.center = (x, y)
                    screen.blit(text_10, text10rect)

                if event.key == pygame.K_2:
                    num = 2
                    text11rect.center = (x, y)
                    screen.blit(text_11, text11rect)

                if event.key == pygame.K_3:
                    num = 3
                    text12rect.center = (x, y)
                    screen.blit(text_12, text12rect)

                if event.key == pygame.K_4:
                    num = 4
                    text13rect.center = (x, y)
                    screen.blit(text_13, text13rect)

                if event.key == pygame.K_5:
                    num = 5
                    text14rect.center = (x, y)
                    screen.blit(text_14, text14rect)

                if event.key == pygame.K_6:
                    num = 6
                    text15rect.center = (x, y)
                    screen.blit(text_15, text15rect)

                if event.key == pygame.K_7:
                    num = 7
                    text16rect.center = (x, y)
                    screen.blit(text_16, text16rect)

                if event.key == pygame.K_8:
                    num = 8
                    text17rect.center = (x, y)
                    screen.blit(text_17, text17rect)

                if event.key == pygame.K_9:
                    num = 9
                    text18rect.center = (x, y)
                    screen.blit(text_18, text18rect)

    pygame.display.update()