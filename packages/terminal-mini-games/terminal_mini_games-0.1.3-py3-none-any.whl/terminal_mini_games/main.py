from terminal_mini_games.games.game_2048 import play_2048
from colorama import Fore, Style, init

init(autoreset=True)

def print_main_menu():
    print(f"{Fore.CYAN}Welcome to the Game Center!{Style.RESET_ALL}")
    print("1. 2048")
    print("2. [Other Game - Not Implemented]")
    print("3. [Another Game - Not Implemented]")
    print("4. Exit")

def main():
    while True:
        print_main_menu()
        choice = input("Enter your choice (1-4): ")
        if choice == '1':
            play_2048()
        elif choice in ['2', '3']:
            print(f"{Fore.YELLOW}This game is not implemented yet.{Style.RESET_ALL}")
        elif choice == '4':
            print(f"{Fore.GREEN}Thank you for playing! Goodbye!{Style.RESET_ALL}")
            break
        else:
            print(f"{Fore.RED}Invalid choice. Please enter a number between 1 and 4.{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
