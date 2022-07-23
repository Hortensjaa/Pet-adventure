from random import choice, choices
from prettytable import PrettyTable, ALL


class Board:

    def __init__(self, l, h):
        if int(l) < 5:
            print('Minimal length is 5')
            l = 5
        if int(h) < 5:
            print('Minimal height is 5')
            h = 5
        self.l = int(l)
        self.h = int(h)
        self.table = [['?' for _ in range(self.l)] for _ in range(self.h)]
        self.meds = {}
        self.weapons = {}
        self.enemies = {}
        for _ in range((self.h * self.l) // 15):
            med = Panacea(self)
            w = Weapon(self)
            self.meds[(med.x, med.y)] = med
            self.weapons[(w.x, w.y)] = w
        for _ in range((self.h * self.l) // 5):
            en = Enemy(self)
            self.enemies[(en.x, en.y)] = en

    def __str__(self):
        t = PrettyTable()
        for i in range(self.h):
            t.add_row(self.table[i])
        t.header = False
        t.hrules = ALL
        return str(t)

    def move_player(self, player, k=' '):
        self.table[player.y][player.x] = player
        self.table[player.py][player.px] = k

    def move_enemies(self):
        update = {}
        for e in self.enemies.values():
            e.move()
            while (e.x, e.y) in update.keys():
                e.move()
            update[(e.x, e.y)] = e
        self.enemies = update


class Item:

    def __init__(self, board):  # coordinates (x,y)
        self.board = board
        self.x = choice(range(board.l))
        self.y = choice(range(board.h))


class Weapon(Item):
    d = {'Golden fang': 30, 'Dewclaw': 10, 'Venom': 15}

    def __init__(self, board):
        super().__init__(board)
        self.name = choice(list(Weapon.d.keys()))
        self.force = Weapon.d[self.name]

    def collect_weapon(self, player):
        print(f"You found {self.name} - weapon, that gives you {self.force} attack force")
        player.att += self.force
        del self.board.weapons[(player.x, player.y)]


class Panacea(Item):

    def __init__(self, board):
        super().__init__(board)
        self.heal = choice(range(10, 50))

    def heal_player(self, player):
        if type(player).max_hp > player.hp + self.heal:
            a = self.heal
            player.hp += a
        else:
            a = type(player).max_hp - player.hp
            player.hp = type(player).max_hp
        print(f"You found panacea - it restored {a} of your health points")
        del self.board.meds[(player.x, player.y)]


class Letter(Item):

    def __init__(self, board, letter):
        super().__init__(board)
        self.letter = letter

    def __str__(self):
        return self.letter


class Key:

    def __init__(self):
        with open('keys.txt', 'r') as f:
            self.key = choice(f.readlines()).strip()
        self.encoded = ['_' for _ in range(len(self.key))]  # already known letters
        self.shots = 3  # chances

    def __str__(self):
        return "".join(self.encoded)

    def decode(self, letter):
        if letter in self.key:
            i = self.key.find(letter)
            while self.encoded[i] != '_':
                i = i + 1 + self.key[i + 1:].find(letter)
            self.encoded[i] = letter
            return f"You found letter {letter}. Now you have: {str(self)}"


class Enemy(Item):
    d = {'Warrior Rat': (150, 20), 'One-eye cat': (100, 15), 'Wounded dog': (30, 50)}

    def __init__(self, board):
        super().__init__(board)
        self.name = choice(list(Enemy.d.keys()))
        self.hp = Enemy.d[self.name][0]
        self.att = Enemy.d[self.name][1]

    def attack(self, player):
        b = choices([True, False], [3, 1], k=1)
        if b == [True]:
            player.hp -= self.att
            if player.hp > 0:
                a = player.hp
            else:
                a = 0
            return f"{self.name} hurt you. You have {a} hp"
        else:
            return f"{self.name} missed - you are lucky!"

    def move(self):
        a = choice([-1, 0, 1])
        while self.x + a >= self.board.l or self.x + a < 0:
            a = choice([-1, 0, 1])
        self.x += a
        b = choice([-1, 0, 1])
        while self.y + b >= self.board.h or self.y + b < 0:
            b = choice([-1, 0, 1])
        self.y += b
