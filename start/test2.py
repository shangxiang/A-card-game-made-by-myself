import pygame
from pygame.locals import *
from sys import exit


board = "resource1\\board.jpg"
blank1 = "resource1\\blank1.png"
blank2 = "resource1\\blank2.png"
mask = "resource1\mask.png"
numbers = "resource1\\numbers.png"
pygame.init()

SCREENSIZE = (800, 450)
screen = pygame.display.set_mode(SCREENSIZE, 0, 32)
pygame.display.set_caption("my_fgo")

bd = pygame.image.load(board).convert()
bd = pygame.transform.scale(bd,(800,450))
bk1 = pygame.image.load(blank1).convert()
bk1 = pygame.image.load(blank1).convert()
bk2 = pygame.image.load(blank2).convert()
mk = pygame.image.load(mask).convert_alpha()
num = pygame.image.load(numbers).convert_alpha()
nums = []
for i in range(11):
    nums.append(num.subsurface((i*18,0),(18,35)))

pygame.event.set_allowed([MOUSEBUTTONDOWN, MOUSEBUTTONUP,KEYDOWN])

#font = pygame.font.SysFont("arial", 20)
#font_height = font.get_linesize()


class component():
    def __init__(self, surface ,x_pos, y_pos, x_len=0, y_len=0, color = (0,0,225), image=None,
                 string=None, isbutton = True, font = "arial", font_size=20):
        self.surface = surface
        self.x_len = x_len
        self.y_len = y_len
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.color = color
        self.image = image
        self.string = string
        self.isbutton = isbutton
        self.font = pygame.font.SysFont(font,font_size)
        self.font_height = self.font.get_linesize()

    def draw(self):
        if self.image is None:
            pygame.draw.rect(self.surface,self.color,Rect(self.x_pos,self.y_pos,self.x_len,self.y_len))
            pygame.draw.rect(self.surface,(248,248,255), Rect(self.x_pos,self.y_pos,self.x_len,self.y_len),2)
            self.surface.blit(self.font.render(self.string, True, (0, 0, 0)),
                              (self.x_pos+5,(self.y_len-self.font_height)/2+self.y_pos))
        else:
            image = pygame.image.load(self.image).convert()
            self.surface.blit(image, (self.x_pos, self.y_pos))

    def draw1(self,color):
        pygame.draw.rect(self.surface,color,Rect(self.x_pos,self.y_pos,self.x_len,self.y_len))
        pygame.draw.rect(self.surface,(248,248,255),Rect(self.x_pos,self.y_pos,self.x_len,self.y_len),2)
        self.surface.blit(self.font.render(self.string, True, (0, 0, 0)),
                          (self.x_pos+5,(self.y_len-self.font_height)/2+self.y_pos))

    def mouseon(self):
        if self.isbutton is False:
            return
        (x,y) = pygame.mouse.get_pos()
        #1print(x,y)
        if (x>self.x_pos) and (x<self.x_pos+self.x_len) and (y>self.y_pos) and (y<self.y_pos+self.y_len):
            #print("in area")
            if self.image is None:
                self.draw1(color = (0.9*self.color[0],0.9*self.color[1],0.9*self.color[2]))
            else:
                image = pygame.image.load(self.image).convert_alpha()
                image.blit(mk,dest=(0,0))
                self.surface.blit(image,dest=(self.x_pos,self.y_pos))
            return True
        else:
            self.draw()
            return False

    def drawafterclick(self):
        if self.isbutton is False:
            return
        (l,m,r) = pygame.mouse.get_pressed()
        if self.mouseon() and l == 1:
            pygame.draw.rect(self.surface, (0.6*self.color[0],0.6*self.color[1],0.6*self.color[2]),
                             Rect(self.x_pos, self.y_pos, self.x_len, self.y_len))
            pygame.draw.rect(self.surface, (0,0,0), Rect(self.x_pos, self.y_pos, self.x_len, self.y_len), 2)
            self.surface.blit(self.font.render(self.string, True, (0, 0, 0)),
                              (self.x_pos + 5, (self.y_len - self.font_height) / 2 + self.y_pos))


class interface():
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.component = dict()
        self.interface = pygame.Surface((self.x,self.y))

    def addbutton(self,x_pos, y_pos, x_len=0, y_len=0, name="bt", color = (0,0,225), image = None, string = None):
        bt = component(self.interface ,x_pos, y_pos, x_len, y_len, color, image, string)
        bt.draw()
        self.component[name]=bt

    def addsurface(self,x_pos,y_pos,x_len,y_len,name):
        subsurface = interface(x_len,y_len)
        self.interface.blit(subsurface,x_pos,y_pos)
        self.component[name]=subsurface

    def addfont(self,x_pos,y_pos,string, font = "arial", font_size = 20):
        font = pygame.font.SysFont(font,font_size)
        self.interface.blit(font.render(string, True, (0,0,0)),x_pos,y_pos)

    def addothers(self,x_pos, y_pos, x_len, y_len, name, color = (0,0,225), image = None, string = None):
        nonbt = component(self.interface ,x_pos, y_pos, x_len, y_len, color, image, string, isbutton= False)
        nonbt.draw()
        self.component[name] = nonbt


login_image = "resource1\login.png"
login_button = "resource1\login_button.png"
login_bg = pygame.image.load(login_image).convert()
login_interface = interface(SCREENSIZE[0],SCREENSIZE[1])
login_interface.interface.blit(bd,dest=(0,0))
login_interface.interface.blit(login_bg,dest=(175,75))
login_interface.addbutton(350,300,name="login_bt",image=login_button,x_len=97,y_len=47)

state = 0
count = 0
account = []
key = []
while True:
    if state == 0:
        screen.blit(login_interface.interface, (0, 0))
        login_interface.component["login_bt"].mouseon()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_0:
                    login_interface.interface.blit(nums[0], dest=(330+count * 18, 145))
                    account.append(0)
                    count = count + 1
                if event.key == K_1:
                    login_interface.interface.blit(nums[1], dest=(330+count * 18, 145))
                    count = count + 1
                    account.append(1)
                if event.key == K_2:
                    login_interface.interface.blit(nums[2], dest=(330+count * 18, 145))
                    count = count + 1
                    account.append(2)
                if event.key == K_3:
                    login_interface.interface.blit(nums[3], dest=(330+count * 18, 145))
                    count = count + 1
                    account.append(3)
                if event.key == K_4:
                    login_interface.interface.blit(nums[4], dest=(330+count * 18, 145))
                    count = count + 1
                    account.append(4)
                if event.key == K_5:
                    login_interface.interface.blit(nums[5], dest=(330+count * 18, 145))
                    count = count + 1
                    account.append(5)
                if event.key == K_6:
                    login_interface.interface.blit(nums[6], dest=(330+count * 18, 145))
                    count = count + 1
                    account.append(6)
                if event.key == K_7:
                    login_interface.interface.blit(nums[7], dest=(330+count * 18, 145))
                    count = count + 1
                    account.append(7)
                if event.key == K_8:
                    login_interface.interface.blit(nums[8], dest=(330+count * 18, 145))
                    count = count + 1
                    account.append(8)
                if event.key == K_9:
                    login_interface.interface.blit(nums[9], dest=(330+count * 18, 145))
                    count = count + 1
                    account.append(9)
                if event.key == K_BACKSPACE:
                    count = count - 1
                    account = account[0:count]
                    login_interface.interface.blit(bk1, dest=(330 + count * 18, 142))
                if event.key == K_TAB:
                    state =1
                    count =0
            if event.type == QUIT:
                exit()
    if state == 1:
        screen.blit(login_interface.interface, (0, 0))
        login_interface.component["login_bt"].mouseon()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_0:
                    login_interface.interface.blit(nums[10], dest=(330+count * 18, 185))
                    key.append(0)
                    count = count + 1
                if event.key == K_1:
                    login_interface.interface.blit(nums[10], dest=(330+count * 18, 185))
                    count = count + 1
                    key.append(1)
                if event.key == K_2:
                    login_interface.interface.blit(nums[10], dest=(330+count * 18, 185))
                    count = count + 1
                    key.append(2)
                if event.key == K_3:
                    login_interface.interface.blit(nums[10], dest=(330+count * 18, 185))
                    count = count + 1
                    key.append(3)
                if event.key == K_4:
                    login_interface.interface.blit(nums[10], dest=(330+count * 18, 185))
                    count = count + 1
                    key.append(4)
                if event.key == K_5:
                    login_interface.interface.blit(nums[10], dest=(330+count * 18, 185))
                    count = count + 1
                    key.append(5)
                if event.key == K_6:
                    login_interface.interface.blit(nums[10], dest=(330+count * 18, 185))
                    count = count + 1
                    key.append(6)
                if event.key == K_7:
                    login_interface.interface.blit(nums[10], dest=(330+count * 18, 185))
                    count = count + 1
                    key.append(7)
                if event.key == K_8:
                    login_interface.interface.blit(nums[10], dest=(330+count * 18, 185))
                    count = count + 1
                    key.append(8)
                if event.key == K_9:
                    login_interface.interface.blit(nums[10], dest=(330+count * 18, 185))
                    count = count + 1
                    key.append(9)
                if event.key == K_BACKSPACE:
                    count = count - 1
                    key = key[0:count]
                    login_interface.interface.blit(bk2, dest=(330 + count * 18, 182))
                if event.key == K_RETURN:
                    state = 2
                    count = 0
            if event.type == QUIT:
                exit()








'''
state = 0
pygame.draw.rect(screen, (0, 0, 225), Rect((20, 60), (120, 40)))
screen.blit(font.render("BUTTEN", True, (0, 0, 0)), (25, 65))

while True:
    if state == 0:
        screen.blit(background1, (0, 0))
        screen.blit(font.render("click BUTTON to start", True, (0, 0, 0)), (20, 20))
        while True:
            pygame.display.update()
            event = pygame.event.wait()
            if event.type == QUIT:
                exit()
            if event.type == MOUSEBUTTONDOWN:
                print("mouse down")
                (x, y) = pygame.mouse.get_pos()
                print("%d %d" % (x, y))
                if (x < 140) and (x > 20) and (y > 60) and (y < 100):
                    print("in area")
                    pygame.draw.rect(screen, (0, 0, 153), Rect((20, 60), (120, 40)))
                    pygame.draw.rect(screen, (0, 0, 0), Rect((20, 60), (120, 40)), 2)
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
        screen.blit(background2, (0, 0))
        screen.blit(font.render("click to exit", True, (0, 0, 0)), (20, 20))
        pygame.display.update()
        while True:
            event = pygame.event.wait()
            if event.type == MOUSEBUTTONDOWN:
                exit()
'''
