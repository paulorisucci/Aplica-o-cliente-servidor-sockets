from random import randint


class Criatura:
    def __init__(self, name = 'player', Atk = 5, Def = 5, level=1, Exp = 0):
        self._level = level
        self._atk = Atk
        self._def = Def
        self._exp = Exp
        self._name = name

    @property
    def level(self):
        return self._level
    @level.setter
    def level(self, new_level):
        self._level = new_level

    @property
    def exp(self):
        return self._exp
    @exp.setter
    def exp(self, new_exp):
        self._exp = new_exp

    @property
    def attack(self):
        return self._atk
    @attack.setter
    def attack(self, new_attack):
        self._atk = new_attack

    @property
    def defense(self):
        return self._def
    @defense.setter
    def defense(self, new_defense):
        self._defense = new_defense

    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, new_name):
        self._name = new_name

    def gain_exp(self, exp):
        self._exp += exp
        if self._exp >= ((self._level**2)*100):
            self.level_up()

    def level_up(self):
        bonus_atk = randint(0, 2)
        bonus_def = randint(0, 2)

        self._level += 1
        self._atk += bonus_atk
        self._def += bonus_def


        print(f'''Parabéns, {self._name}! Você avançou para o level {self._level}!
Você ganhou {bonus_atk} de ataque e {bonus_def} de defesa!''')

    def presentation(self):
        return f'Creature: {self._name}\nLevel: {self._level}\nAttack:{self._atk}\nDefense:{self._def}\nLevel:{self._level}\nEXP:{self._exp}'

    def __str__(self):
        return f'''{self._name};{self._atk};{self._def};{self._level};{self._exp}'''


def embate(player, creature, choice):
    if choice == 'ATK':

        if player.attack >= creature.attack:
            winner, looser = player, creature
        else:
            winner, looser = creature, player

    elif choice == 'DEF':

        if player.defense >= creature.defense:
            winner, looser = player, creature
        else:
            winner, looser = creature, player

    else:
        dice = randint(1, 6)
        if dice <= 3:
            winner, looser = creature, player
        else:
            return 'RUN'

    return winner, looser


def convert_str_creature(string):
    # f'''{self._name};{self._atk};{self._def};{self._level};{self._exp}'''
    attributes = string.split(';')
    name = attributes[0]
    attack = int(attributes[1])
    defense = int(attributes[2])
    level = int(attributes[3])
    exp = int(attributes[4])
    return Criatura(name, attack, defense, level, exp)