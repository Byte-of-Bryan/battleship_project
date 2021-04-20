"""
Program written by Bryan Morandi - 2021

This is a small project that uses a multidimentional list to create asimple battleship
game against an AI. The skills that I practiced in writing this program are: 
OOP, exception handling, and modularity.

The goal of the game is to sink the enemy battleship that is hidden, by
guessing row and column coordinates each turn. But be carful because the 
enemy also guesses coordinates and can sink your ship if you don't sink theirs first!

The sea is made up of a grid consisting of "O"'s these are currently empty slots
that either have the enemy ship that is hidden from the player, or can be attacked
either by the player or enemy. Once the player chooses coordinates for their ship,
their ship is represented by "#" this is then shown in the sea. When it is time for
the player to attack, "X" represents missed shots at the enemy. When it is time for the
enemy to attack, "*" represents missed shots at the player. 

There is logic in place to prevent the player from attacking their own ship, choosing 
an already entered coordinate either by the player or enemy, entering an invalid number 
or writing text. There is also logic that prevents the AI from choosing an invalid/already 
entered coordinate. If the player sinks the enemy ship first, they win and the program
tells the user how many tries it took for them to win. If the enemy wins then the program 
tells you how many tries it took the AI to beat you.

Once you either win or lose the program asks you if you would like to play again, where 1 = yes
and 2 = no. If you choose yes, a new game will start, if you choose no, it will thank you for 
playing and then close the program.

I added the ability for the player to choose how large the sea is, e.g. how large
the board is. The program will ask for a number (2 - 10) and whatever the player enters
a board will populate (if the player chooses 3 a 3x3 grid will be made). I think of this
as a difficult selection, where 3 is an easy/fast game and where 10 is a hard/potentially long game.
I limited the choice range from 2 to 10, just so the user couldn't enter a rediculously large number.
I also formatted any text to display the correct coordinate range to reflect the current size of the sea.

I added acception handling anytime the program asks for any user input so the program won't crash, it 
will reprompt the user to enter the correct data. This also doesn't effect any of the try counts at the
end of the program, only valid coodinate submissions are counted as tries.

Enjoy playing!
"""

from random import randint


# function to take in user input and create the playing board
def make_sea():
    sea = []
    valid_size = False
    while valid_size == False:
        try:
            sea_size = int(
                input("\nHow large would you like the sea? (2 - 10): "))
            if (sea_size < 2):
                print("Sea too small, enter a size greater than 1")
            elif (sea_size > 10):
                print("Sea too large, enter a size smaller than than 10")
            else:
                for _ in range(sea_size):
                    sea.append(["O"] * sea_size)
                valid_size = True
        except ValueError:
            print("Not an integer, please try again")
    return sea


# function for player to enter in where they would like their ship to be placed in the populated board.
def player_ship_location(sea):
    valid_ship_row = False
    valid_ship_col = False
    print(("-------Enter ship coordinates-------\nPlease enter a number from 1 - {}").format(len(sea)))
    while valid_ship_row == False:
        try:
            player_ship_row = int(
                input("Enter row where you want your ship: "))
            if (player_ship_row not in range(1, len(sea) + 1)):
                print(
                    "Not valid row coordinates, please enter a number between 1 - {}".format(len(sea) + 1))
            else:
                valid_ship_row = True
        except ValueError:
            print("Not an integer, please try again")
    while valid_ship_col == False:
        try:
            player_ship_col = int(
                input("Enter column where you want your ship: "))
            print(" ")
            if (player_ship_col not in range(1, len(sea) + 1)):
                print(
                    "Not valid column coordinates, please enter a number between 1 - {}".format(len(sea) + 1))
            else:
                sea[player_ship_row - 1][player_ship_col - 1] = "#"
                valid_ship_col = True
        except ValueError:
            print("Not an integer, please try again")

    return sea


# function used by enemy_turn & find_enemy_ship that finds a random row
def random_row(sea):
    return randint(0, len(sea) - 1)


# function used by enemy_turn and find_enemy_ship that finds a random column
def random_col(sea):
    return randint(0, len(sea[0]) - 1)


# function that finds a random spot on the board and makes it the enemy ship location, this is hidden from the player
def find_enemy_ship(sea):
    valid_enemy_ship_location = False
    while(valid_enemy_ship_location == False):
        enemy_ship_row = random_row(sea)
        enemy_ship_col = random_col(sea)
        # prevents AI from choosing your ships coordinates
        if (sea[enemy_ship_row][enemy_ship_col] != "#"):
            valid_enemy_ship_location = True
    return enemy_ship_row, enemy_ship_col


# function to print the board
def print_sea(sea):
    for row in sea:
        print(("   ").join(row))
    print(" ")


# function for when its time for the player to choose the row attack coordinate
def row_guess(sea):
    valid_row = False
    print(("----Enter Attack Coordinates----\nPlease enter a number from 1 - {}").format(len(sea)))
    while(valid_row == False):
        try:
            guess_row = int(input("Guess Row: "))
            if (guess_row not in range(1, len(sea)+1)):
                print(
                    ("Not a valid row, please enter number from 1 - {} ").format(len(sea)))
            else:
                valid_row = True
        except ValueError:
            print("Not an integer, please try again")
    return guess_row - 1


# function for when its time for the player to choose the column attack coordinate
def col_guess(sea):
    valid_col = False
    while(valid_col == False):
        try:
            guess_col = int(input("Guess Column: "))
            if (guess_col not in range(1, len(sea)+1)):
                print(
                    ("Not a valid row, please enter number from 1 - {}: ").format(len(sea)))
            else:
                valid_col = True
        except ValueError:
            print("Not an integer, please try again")
    return guess_col - 1


# function that has the logic for the AI to choose random valid coordinates
def enemy_turn(sea, enemy_guess_count, enemy_ship_row, enemy_ship_col):
    valid_enemy_attack = False
    while (valid_enemy_attack == False):
        attack_row = random_row(sea)
        attack_col = random_col(sea)
        # enemy hit your ship
        if (sea[attack_row][attack_col] == "#"):
            print("\n---------Enemy sunk your battleship! You lose!---------")
            print("-------The enemy sunk your battleship in {} tries-------\n".format(
                enemy_guess_count))
            valid_enemy_attack = True
            return True
        # prevents AI from choosing already entered coordinate
        elif (sea[attack_row][attack_col] != "O"):
            continue
        # prevents AI from choosing their ships coordinates
        elif (attack_row == enemy_ship_row and attack_col == enemy_ship_col):
            continue
        # prints the enemy attack if missed
        else:
            sea[attack_row][attack_col] = "*"
            print("---ENEMY MOVE---")
            print_sea(sea)
            valid_enemy_attack = True
    return False


# function that uses guess_row and guess_col and takes in user input when it is time for the player to attack
def player_turn(sea, valid_guess_count, enemy_ship_row, enemy_ship_col):
    valid_player_turn = False
    while (valid_player_turn == False):
        guess_row = row_guess(sea)
        guess_col = col_guess(sea)

        # already played coordinates
        if (sea[guess_row][guess_col] == "X" or sea[guess_row][guess_col] == "*"):
            print("Coordinates already entered, Try again")
        # player entered their ship coordinates
        elif (sea[guess_row][guess_col] == "#"):
            print("Don't blow yourself up now... Try again")
        # prints the player attack if missed
        elif (guess_row != enemy_ship_row or guess_col != enemy_ship_col):
            print("\n-------You missed my battleship!------")
            sea[guess_row][guess_col] = "X"
            print("---PLAYER MOVE---")
            print_sea(sea)
            valid_player_turn = True
        # player hit enemy ship
        else:
            print("\n-----You sunk my battleship! You win!-----")
            print(
                "-------It took {} valid tries to win------\n".format(valid_guess_count))
            return True
    return False


# function that asks the user if they would like to play again
def play_again():
    print("Choose an option:\n1 - yes\n2 - no")
    while(True):
        try:
            answer = int(
                input("Play again? "))
            if(answer == 1):
                main()
                return False  # if played again, this stops the recursive call asking to play again
            elif (answer == 2):
                print("Thanks for playing!")
                return False
            else:
                print("Not a valid choice, choose 1 or 2.")
        except ValueError:
            print("Not an integer, please try again")


# function that keeps track of the player and enemy turns and also how many turns the player and enemy took to win/lose
def play_battleship(sea, enemy_ship_row, enemy_ship_col):
    valid_guess_count = 1
    enemy_guess_count = 1
    enemy_sunk = False
    player_sunk = False
    while (enemy_sunk == False and player_sunk == False):
        enemy_sunk = player_turn(
            sea, valid_guess_count, enemy_ship_row, enemy_ship_col)
        valid_guess_count += 1
        if enemy_sunk == True:
            break
        player_sunk = enemy_turn(
            sea, enemy_guess_count, enemy_ship_row, enemy_ship_col)
        enemy_guess_count += 1
        if player_sunk == True:
            break


# uses all the above functions to run the battlechip game.
def main():
    sea = make_sea()
    print_sea(sea)
    sea = player_ship_location(sea)
    print("******Let's Play Battleship!******")
    print("\n# = Player Ship Location\nX = Player Missed Attack\n* = Enemy Missed Attack\n")
    print_sea(sea)
    enemy_ship_row, enemy_ship_col = find_enemy_ship(sea)
    play_battleship(sea, enemy_ship_row, enemy_ship_col)
    play_again()


main()
