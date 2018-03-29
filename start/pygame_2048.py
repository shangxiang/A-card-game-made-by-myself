import pygame
from pygame.locals import *
from sys import exit
from random import randrange, choice

def transpose(field):
    return [list(row) for row in zip(*field)]

def invert(field):
    return [row[::-1] for row in field]

field = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]


def spawn(field):
    #print(field)
    #print('AAA')
    new_element = 4 if randrange(100) > 89 else 2
    while True:
        i = choice([i for i in range(4)])
        j = choice([j for j in range(4)])
        if field[i][j] == 0:
            field[i][j] = new_element
            return field
    ''''(i, j) = choice([(i, j) for i in range(4) for j in range(4) if field[i][j] == 0])
    field[i][j] = new_element
    return field'''

def move_is_possible(field, direction):
    def row_is_left_movable(row):
        def change(i):
            if row[i] == 0 and row[i + 1] != row[i]:
                return True
            if row[i] != 0 and row[i + 1] == row[i]:
                return True
            return False

        return any(change(i) for i in range(len(row) - 1))

    check = {}
    check['left'] = lambda field: any(row_is_left_movable(row) for row in field)
    check['right'] = lambda field: check['left'](invert(field))
    check['up'] = lambda field: check['left'](transpose(field))
    check['down'] = lambda field: check['right'](transpose(field))

    if direction in check:
        return check[direction](field)
    else:
        return False

def move_row_left(row):
    def tighten(row):
        new_row = [i for i in row if i != 0]
        new_row += [0 for i in range(len(row) - len(new_row))]
        return new_row

    def merge(row):
        pair = False
        new_row = []
        for i in range(len(row)):
            if pair:
                new_row.append(2 * row[i])
                #self.score += 2 * row[i]
                pair = False
            else:
                if i + 1 < len(row) and row[i] == row[i + 1]:
                    pair = True
                    new_row.append(0)
                else:
                    new_row.append(row[i])
        assert len(new_row) == len(row)
        return new_row

    return tighten(merge(tighten(row)))

def move_left(field, direction='left'):
    if move_is_possible(field, direction):
        return [move_row_left(row) for row in field]
    else:
        return field

def move_right(field, direction = 'right'):
    return invert(move_left(invert(field),direction))

def move_up(field):
    return transpose(move_left(transpose(field),'up'))

def move_down(field):
    return transpose(move_right(transpose(field),'down'))

background_image = 'beijing.png'

pygame.init()
SCREEN_SIZE = (450,450)
screen = pygame.display.set_mode(SCREEN_SIZE,0,32)

font = pygame.font.SysFont("arial",32)
font_height = font.get_linesize()
pygame.event.set_allowed([KEYDOWN, QUIT])

pygame.display.set_caption("2048")
background = pygame.image.load(background_image).convert()

while True:
    field = spawn(field)
    screen.blit(background,(0,0))
    x = 60-(font_height/2)
    y = 60-(font_height/2)
    print(field)
    for j in range(4):
        screen.blit(font.render(str(field[0][j]), True, (0, 0, 0)), (x, y))
        screen.blit(font.render(str(field[1][j]), True, (0, 0, 0)), (x, y+110))
        screen.blit(font.render(str(field[2][j]), True, (0, 0, 0)), (x, y + 220))
        screen.blit(font.render(str(field[3][j]), True, (0, 0, 0)), (x, y + 330))
        print('b')
        x += 110

    pygame.display.update()
    while True:
        event = pygame.event.wait()
        if event.type == QUIT:
            exit()
        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                field = move_left(field)
            if event.key == K_RIGHT:
                field = move_right(field)
            if event.key == K_UP:
                field = move_up(field)
            if event.key == K_DOWN:
                field = move_down(field)
            print(field)
            break
