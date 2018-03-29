import pygame
from pygame.locals import *
from sys import exit

background_image1 = "login.png"
background_image2 = "screen2.png"

pygame.init()

SCREENSIZE = (800,450)
screen = pygame.display.set_mode(SCREENSIZE,0,32)
pygame.display.set_caption("my_fgo")
background1 = pygame.image.load(background_image1).convert()
background2 = pygame.image.load(background_image2).convert()

print(type(background1))
pygame.event.set_allowed([MOUSEBUTTONDOWN,MOUSEBUTTONUP])

font = pygame.font.SysFont("arial",32)
font_height = font.get_linesize()

class button():
    def __init__(self,x_pos,y_pos,x_len,y_len,image=None,string = None):
        self.buttonsurface = pygame.surface((x_len,y_len))
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.x_len = x_len
        self.y_len = y_len
        self.image = image
        self.beforeclick = (0,0,225)
        self.afterclick = (0,0,153)


state = 0
pygame.draw.rect(screen, (0, 0, 225), Rect((20, 60), (120, 40)))
screen.blit(font.render("BUTTEN", True, (0, 0, 0)), (25, 65))

while True:
    if state==0:
        screen.blit(background1, (0, 0))
        screen.blit(font.render("click BUTTON to start", True, (0, 0, 0)), (20, 20))
        while True:
            pygame.display.update()
            event = pygame.event.wait()
            if event.type == QUIT:
                exit()
            if event.type == MOUSEBUTTONDOWN:
                print("mouse down")
                (x,y) = pygame.mouse.get_pos()
                print("%d %d"%(x,y))
                if (x < 140) and (x > 20) and (y>60) and (y<100):
                    print("in area")
                    pygame.draw.rect(screen, (0, 0, 153), Rect((20, 60), (120, 40)))
                    pygame.draw.rect(screen, (0, 0, 0), Rect((20, 60), (120, 40)),2)
                    screen.blit(font.render("BUTTEN", True, (0, 0, 0)), (25, 65))
                    pygame.display.update()
            elif event.type == MOUSEBUTTONUP:
                print("mouse up")
                (x, y) = pygame.mouse.get_pos()
                if x < 140 and x > 20 and y > 60 and y < 100:
                    state = 1
                    pygame.draw.rect(screen, (0, 0, 225), Rect((20, 60), (120, 40)))
                    screen.blit(font.render("BUTTEN", True, (0, 0, 0)), (25, 65))
                    break
            else:
                pygame.draw.rect(screen, (0, 0, 225), Rect((20, 60), (120, 40)))
                screen.blit(font.render("BUTTEN", True, (0, 0, 0)), (25, 65))
    if state == 1:
        screen.blit(background2,(0,0))
        screen.blit(font.render("click to exit", True, (0, 0, 0)), (20, 20))
        pygame.display.update()
        while True:
            event = pygame.event.wait()
            if event.type == MOUSEBUTTONDOWN:
                exit()
