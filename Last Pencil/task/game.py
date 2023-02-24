from string import digits
from random import randint


def character_validation(text: str):
    list1 = list(text)
    validator = True
    for element in list1:
        if element not in digits:
            validator = False
            break

    return validator


def bot_answer(pencils_left: int):
    if pencils_left in range(5, n_pencils + 1, 4):
        return randint(1, 3)
    elif pencils_left in range(4, n_pencils + 1, 4):
        return 3
    elif pencils_left in range(3, n_pencils + 1, 4):
        return 2
    elif pencils_left in range(2, n_pencils + 1, 4) or pencils_left == 1:
        return 1


n_pencils = input("How many pencils would you like to use:")

while True:

    if character_validation(n_pencils):
        if n_pencils == "0":
            n_pencils = input("The number of pencils should be positive")
        else:
            n_pencils = int(n_pencils)
            break
    else:
        n_pencils = input("The number of pencils should be numeric")

first_player = input("Who will be the first (John, Jack):")

while True:
    if first_player == "John":
        player_list = ("John", "Jack")
        break
    elif first_player == "Jack":
        player_list = ("Jack", "John")
        break
    else:
        first_player = input("Choose between 'John' and 'Jack'")

print("|" * n_pencils)

while n_pencils > 0:
    for player in player_list:
        print(player + "'s turn:")

        if player == "John":
            taken = input()
        else:
            taken = str(bot_answer(n_pencils))
            print(taken)

        while True:
            if not character_validation(taken) or taken not in ("1", "2", "3"):
                taken = input("Possible values: '1', '2' or '3'")
                continue

            if n_pencils < int(taken):
                taken = input("Too many pencils were taken")
                continue

            break

        n_pencils -= int(taken)

        if n_pencils > 0:
            print("|" * n_pencils)
        else:
            last_player = player
            break

if last_player == "John":
    print("Jack won!")
else:
    print("John won!")
