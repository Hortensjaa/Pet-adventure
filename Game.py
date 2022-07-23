from Items_classes import Board, Key, Letter
from Player_classes import Rat, Cat, Dog

if __name__ == '__main__':

    # generating table
    l = input('Choose table length (not less than 5): ')
    h = input('Choose table height (not less than 5): ')
    board = Board(l, h)  # columns, rows

    # generating letters on table
    psswd = Key()
    letters = {}
    for l in psswd.key:  # for every letter in key
        let = Letter(board, l)
        while (let.x, let.y) in letters.keys():
            let = Letter(board, l)
        letters[(let.x, let.y)] = let.letter

    # generating player
    player = input("Choose your fighter - type 'rat', 'cat' or 'dog':\n").lower()
    while player not in ['rat', 'cat', 'dog']:
        player = input("Type 'rat', 'cat' or 'dog'!\n")
    if player == 'rat':
        player = Rat(board)
    elif player == 'cat':
        player = Cat(board)
    elif player == 'dog':
        player = Dog(board)
    print(str(player) + ' <-- look, it is you!')

    board.table[player.y][player.x] = player

    d = {'a': player.move_left, 'd': player.move_right, 'w': player.move_up, 's': player.move_down}
    print('Use "w", "a", "s", "d" to move, "q" to use superpower, "1" to guess the key or "0" to leave')

    while psswd.shots > 0 and player.hp > 0:

        print(f'You have {player.hp} health points and {player.att} attack force\n'
              f'Key: {psswd}. You have {psswd.shots} chances to guess a key (hidden word).')
        print(board)
        r = input().lower()

        if r in d.keys():
            d[r]()

            # meeting an enemy
            if (player.x, player.y) in board.enemies.keys():
                enemy = board.enemies[(player.x, player.y)]
                print(f"You met {enemy.name}, with {enemy.hp} hp - if it hurts you, you will lost {enemy.att} hp")
                print(enemy.attack(player))
                while player.hp > 0 and enemy.hp > 0:  # fighting mode loop
                    r = input('Choose 1 to fight or 0 to retreat: ')
                    while r not in ['0', '1']:
                        r = input('Choose 1 or 0, nothing else will help you!')
                    if r == '0':
                        board.table[enemy.y][enemy.x] = 'x'  # mark if we saw an enemy
                        player.x = player.px
                        player.y = player.py
                        print("Sometimes the best option is to run away...")
                        break
                    else:
                        print(player.attack(enemy))
                        if enemy.hp <= 0:
                            print(f"You killed {enemy.name}")
                            del board.enemies[(enemy.x, enemy.y)]
                            board.move_player(player)
                            break
                        print(enemy.attack(player))
                if player.hp <= 0:
                    print(f"{enemy.name} killed you")
                    continue
                else:
                    board.move_enemies()
                    continue

            # finding panacea
            if (player.x, player.y) in board.meds.keys():
                board.meds[(player.x, player.y)].heal_player(player)

            # finding a weapon
            if (player.x, player.y) in board.weapons.keys():
                board.weapons[(player.x, player.y)].collect_weapon(player)

            # finding a letter
            if (player.x, player.y) in letters.keys():
                print(psswd.decode(letters[(player.x, player.y)]))
                del letters[(player.x, player.y)]

            board.move_player(player)

        elif r == "q":
            player.superpower()

        elif r == '1':
            guess = input("Enter the key: ").upper()
            if guess == psswd.key:
                print("YOU WON!")
                break
            else:
                print("No, it is not the key")
                psswd.shots -= 1

        elif r == '0':  # exit
            a = input("Are you sure, you want to exit? Choose 1 for 'yes' or 0 for 'no': ")
            if a == '0':
                continue
            print("Okay, see you later!")
            break

        else:
            print('Choose: \nA, W, S, D - moves \nQ - superpower \n1 - try to guess a key \n0 - exit:(')
            continue

        board.move_enemies()
        print()
