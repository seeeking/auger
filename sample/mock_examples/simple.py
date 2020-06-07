from random import randint, choice


def dice():
    strs = ['lucky', 'super lucky']
    return f'Dice shows {randint(1, 6)} and you are {choice(strs)}'


def coin(rand):
    return rand(1, 2)

