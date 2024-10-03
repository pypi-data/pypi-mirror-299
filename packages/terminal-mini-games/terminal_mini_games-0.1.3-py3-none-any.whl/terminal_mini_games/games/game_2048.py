import random
import os
from colorama import Fore, Back, Style, init
from terminal_mini_games.utils.high_score import load_high_scores, save_high_score

init(autoreset=True)

def initialize_board():
    board = [[0] * 4 for _ in range(4)]
    add_new_tile(board)
    add_new_tile(board)
    return board

def add_new_tile(board):
    empty_cells = [(i, j) for i in range(4) for j in range(4) if board[i][j] == 0]
    if empty_cells:
        i, j = random.choice(empty_cells)
        board[i][j] = 2 if random.random() < 0.9 else 4

def print_board(board, score, high_score):
    os.system('clear' if os.name == 'posix' else 'cls')
    print_logo()
    print(f"{Fore.CYAN}Score: {score}{Style.RESET_ALL} | {Fore.YELLOW}High Score: {high_score}{Style.RESET_ALL}\n")
    print("┌───────┬───────┬───────┬───────┐")
    for i, row in enumerate(board):
        print("│" + "│".join(format_tile(num) for num in row) + "│")
        if i < 3:  # Print separator line for all but the last row
            print("├───────┼───────┼───────┼───────┤")
    print("└───────┴───────┴───────┴───────┘")
    print()

def format_tile(num):
    if num == 0:
        return "       "
    colors = {
        2: Fore.CYAN,
        4: Fore.GREEN,
        8: Fore.YELLOW,
        16: Fore.MAGENTA,
        32: Fore.RED,
        64: Fore.BLUE,
        128: Fore.CYAN + Style.BRIGHT,
        256: Fore.GREEN + Style.BRIGHT,
        512: Fore.YELLOW + Style.BRIGHT,
        1024: Fore.MAGENTA + Style.BRIGHT,
        2048: Fore.RED + Style.BRIGHT,
    }
    color = colors.get(num, Fore.WHITE + Style.BRIGHT)
    return f"{color}{str(num).center(7)}{Style.RESET_ALL}"

def print_logo():
    logo = f"""
{Fore.YELLOW}
 222222222222222         000000000            444444444       888888888     
2:::::::::::::::22     00:::::::::00         4::::::::4     88:::::::::88   
2::::::222222:::::2  00:::::::::::::00      4:::::::::4   88:::::::::::::88 
2222222     2:::::2 0:::::::000:::::::0    4::::44::::4  8::::::88888::::::8
            2:::::2 0::::::0   0::::::0   4::::4 4::::4  8:::::8     8:::::8
            2:::::2 0:::::0     0:::::0  4::::4  4::::4  8:::::8     8:::::8
         2222::::2  0:::::0     0:::::0 4::::4   4::::4   8:::::88888:::::8 
    22222::::::22   0:::::0 000 0:::::04::::444444::::444  8:::::::::::::8  
  22::::::::222     0:::::0 000 0:::::04::::::::::::::::4 8:::::88888:::::8 
 2:::::22222        0:::::0     0:::::04444444444:::::4448:::::8     8:::::8
2:::::2             0:::::0     0:::::0          4::::4  8:::::8     8:::::8
2:::::2             0::::::0   0::::::0          4::::4  8:::::8     8:::::8
2:::::2       2222220:::::::000:::::::0          4::::4  8::::::88888::::::8
2::::::2222222:::::2 00:::::::::::::00         44::::::44 88:::::::::::::88 
2::::::::::::::::::2   00:::::::::00           4::::::::4   88:::::::::88   
22222222222222222222     000000000             4444444444     888888888     
{Fore.CYAN}Welcome to 2048!{Style.RESET_ALL}
"""
    print(logo)

def merge_left(row):
    new_row = [num for num in row if num != 0]
    score = 0
    for i in range(len(new_row) - 1):
        if new_row[i] == new_row[i + 1]:
            new_row[i] *= 2
            score += new_row[i]
            new_row[i + 1] = 0
    new_row = [num for num in new_row if num != 0]
    return new_row + [0] * (4 - len(new_row)), score

def move_left(board):
    score = 0
    for i in range(4):
        board[i], row_score = merge_left(board[i])
        score += row_score
    return score

def move_right(board):
    score = 0
    for i in range(4):
        board[i] = board[i][::-1]
        board[i], row_score = merge_left(board[i])
        board[i] = board[i][::-1]
        score += row_score
    return score

def move_up(board):
    score = 0
    for j in range(4):
        col = [board[i][j] for i in range(4)]
        col, col_score = merge_left(col)
        for i in range(4):
            board[i][j] = col[i]
        score += col_score
    return score

def move_down(board):
    score = 0
    for j in range(4):
        col = [board[i][j] for i in range(4)][::-1]
        col, col_score = merge_left(col)
        col = col[::-1]
        for i in range(4):
            board[i][j] = col[i]
        score += col_score
    return score

def is_game_over(board):
    for i in range(4):
        for j in range(4):
            if board[i][j] == 0:
                return False
            if i < 3 and board[i][j] == board[i + 1][j]:
                return False
            if j < 3 and board[i][j] == board[i][j + 1]:
                return False
    return True

def print_instructions():
    print(f"{Fore.CYAN}How to play:{Style.RESET_ALL}")
    print("Use W/A/S/D keys to move the tiles.")
    print("W: Up, A: Left, S: Down, D: Right")
    print("U: Undo last move")
    print("Tiles with the same number merge into one when they touch.")
    print("Add them up to reach 2048!")
    print("\nPress any key to start...")
    input()

def get_difficulty():
    while True:
        difficulty = input("Choose difficulty (easy/medium/hard): ").lower()
        if difficulty in ['easy', 'medium', 'hard']:
            return difficulty
        print("Invalid input. Please choose easy, medium, or hard.")

def play_2048():
    print_instructions()
    difficulty = get_difficulty()
    board = initialize_board()
    score = 0
    high_scores = load_high_scores()
    high_score = high_scores.get("2048", 0)
    previous_board = None
    previous_score = 0

    while True:
        print_board(board, score, high_score)
        move = input("Enter move (W/A/S/D or U to undo): ").strip().lower()
        if move in ['w', 'a', 's', 'd']:
            previous_board = [row[:] for row in board]
            previous_score = score
            if move == 'w':
                score += move_up(board)
            elif move == 'a':
                score += move_left(board)
            elif move == 's':
                score += move_down(board)
            elif move == 'd':
                score += move_right(board)
            add_new_tile(board)
            if score > high_score:
                high_score = score
                save_high_score("2048", high_score)
            if is_game_over(board):
                print_board(board, score, high_score)
                print(f"{Fore.RED}Game Over!{Style.RESET_ALL}")
                print(f"Final Score: {score}")
                break
        elif move == 'u' and previous_board:
            board = [row[:] for row in previous_board]
            score = previous_score
            print(f"{Fore.GREEN}Move undone!{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}Invalid move! Please enter W, A, S, D, or U.{Style.RESET_ALL}")