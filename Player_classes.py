from abc import abstractmethod
from random import choices


class Player:

    def __init__(self, board, hp, att):
        self.board = board
        self.x = self.board.l // 2
        self.y = self.board.h // 2
        self.px = self.x  # previous x
        self.py = self.y  # previous y
        self.hp = hp
        self.att = att
        self.sp = False  # were superpower used?

    def move_up(self):
        if self.y - 1 >= 0:
            self.px = self.x
            self.py = self.y
            self.y -= 1
        else:
            print("End of the table - choose another move")

    def move_down(self):
        if self.y + 1 < self.board.h:
            self.px = self.x
            self.py = self.y
            self.y += 1
        else:
            print("End of the table - choose another move")

    def move_right(self):
        if self.x + 1 < self.board.l:
            self.px = self.x
            self.py = self.y
            self.x += 1
        else:
            print("End of the table - choose another move")

    def move_left(self):
        if self.x - 1 >= 0:
            self.px = self.x
            self.py = self.y
            self.x -= 1
        else:
            print("End of the table - choose another move")

    def attack(self, enemy):
        b = choices([True, False], [5, 1], k=1)
        if b == [True]:
            enemy.hp -= self.att
            if enemy.hp > 0:
                a = enemy.hp
            else:
                a = 0
            return f"You hurt {enemy.name}. {a} hp points left"
        else:
            return f"Missed! {enemy.name} didn't get hurt"

    @abstractmethod
    def superpower(self):
        pass


class Rat(Player):
    max_hp = 150

    def __init__(self, board):
        super().__init__(board, 150, 10)

    def __str__(self):
        return '\U0001f400'

    def superpower(self):
        if not self.sp:
            print('You activated a sewer teleport')
            xy = input('Enter two coordinates x and y with space between them: ')
            xy = xy.split()
            while len(xy) != 2:
                xy = input('Choose correct coordinates: ')
                xy = xy.split()
            x = int(xy[0])
            y = int(xy[1])
            self.px = self.x
            self.x = x
            self.py = self.y
            self.y = y
            self.board.move_player(self)
            self.sp = True
        else:
            print('Oh, you already used your superpower...')


class Cat(Player):
    max_hp = 100

    def __init__(self, board):
        super().__init__(board, 100, 25)

    def __str__(self):
        return '\U0001f408'

    def superpower(self):
        if not self.sp:
            print('You activated a cat eye')
            for i in range(self.board.h):
                for j in range(self.board.l):
                    if self.board.table[i][j] == 'x':
                        if (j, i) not in self.board.enemies.keys():
                            self.board.table[i][j] = '?'
                    else:
                        if (j, i) in self.board.enemies.keys():
                            self.board.table[i][j] = 'x'
            print(self.board)
            print("Current enemies locations are now marked with 'x'")
            self.sp = True
        else:
            print('Oh, you already used your superpower...')


class Dog(Player):
    max_hp = 70

    def __init__(self, board):
        super().__init__(board, 70, 50)

    def __str__(self):
        return '\U0001f415'

    def superpower(self):
        if not self.sp:
            print('You activated a super-sniff')
            r = input("What do you want to find? Choose 1 for panacea or 2 for weapons: ")
            while r not in ['1', '2']:
                r = input("1 or 2 please: ")
            if r == '1':
                n = self.board.meds.keys()
            else:
                n = self.board.weapons.keys()
            for i in range(self.board.h):
                for j in range(self.board.l):
                    if (j, i) in n:
                        self.board.table[i][j] = 'O'
            print(self.board)
            print("Locations are now marked with 'O'")
            self.sp = True
        else:
            print('Oh, you already used your superpower...')
