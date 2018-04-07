#!/usr/bin/python2.6
# -*- coding: utf-8 -*-


import pygame
import time
from pygame.locals import *
from sys import exit


pygame.init()

board = "resource1\\board.jpg"
blank1 = "resource1\\blank1.png"
blank2 = "resource1\\blank2.png"
mask = "resource1\mask.png"
numbers = "resource1\\numbers.png"


SCREENSIZE = (800, 450)
screen = pygame.display.set_mode(SCREENSIZE, 0, 32)
pygame.display.set_caption("my_card_game")

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

default_font = pygame.font.SysFont("arial", 32)
font_height = default_font.get_linesize()
chinese_font = pygame.font.SysFont("simhei",20)
chinese_font_32 = pygame.font.SysFont("simhei",32)

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
            self.surface.blit(self.image, (self.x_pos, self.y_pos))

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
                image1 = self.image.convert_alpha()
                image1.blit(mk,dest=(0,0))
                self.surface.blit(image1,dest=(self.x_pos,self.y_pos))
            return True
        else:
            self.draw()
            return False

    def isclick(self):
        if self.isbutton is False:
            return False
        (l,m,r) = pygame.mouse.get_pressed()
        if self.mouseon():
            if l == 1:
                if self.image is None:
                    pygame.draw.rect(self.surface, (0.6 * self.color[0], 0.6 * self.color[1], 0.6 * self.color[2]),
                                     Rect(self.x_pos, self.y_pos, self.x_len, self.y_len))
                pygame.draw.rect(self.surface, (0, 0, 0), Rect(self.x_pos+2, self.y_pos+2, self.x_len-4, self.y_len-4), 4)
                return True
            else:
                return False
        else:
            return False

                #self.surface.blit(self.font.render(self.string, True, (0, 0, 0)),
                 #                 (self.x_pos + 5, (self.y_len - self.font_height) / 2 + self.y_pos))


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


class player():
    def __init__(self, account=0, key=0, money=0, level=0, file=None):
        self.account = account
        self.key = key
        self.money = money
        self.level = level
        self.cards = []
        self.file = file
        self.size = 0
        #file.write("%s\t%s\t%d\t%d\n"%(self.account,self.key,self.money,self.level))

    def readfile(self):
        if self.file is None:
            return
        else:
            line = self.file.readline()
            words = line.split('\n')
            words = words[0].split('\t')
            self.account = words[0]
            self.key = words[1]
            self.money = int(words[2])
            self.level = int(words[3])
            line = self.file.readline()
            while line != '':
                words = line.split('\n')
                words = words[0].split('\t')
                card = character(words[1],int(words[2]),int(words[3]),int(words[4]),words[5],
                                 int(words[6]),words[7],self.account,int(words[0]))
                self.cards.append(card)
                line = self.file.readline()
            self.size = len(self.cards)

    def getcard(self,name):
        self.size += 1
        for i in all_cards:
            if i.name == name:
                break
        new_card = character(i.name,i.attack,i.life,1,player=self.account,number=self.size-1)
        self.cards.append(new_card)
        self.save()

    def deletecard(self,number):
        for i in range(len(self.cards)):
            if self.cards[i].number == number:
                del self.cards[i]
                break
        self.size = len(self.cards)
        self.save()

    def save(self):
        self.file.close()
        new_file = open("user\%s.txt"%self.account,'w+')
        new_file.write("%s\t%s\t%d\t%d\n" % (self.account, self.key, self.money, self.level))
        for i in range(len(self.cards)):
            new_file.write("%d\t%s\t%d\t%d\t%d\t%s,%s,%s,%s\t%d\t%s\n"%(i,self.cards[i].name,self.cards[i].attack,
                                                               self.cards[i].life,self.cards[i].level,
                                                               self.cards[i].skill[0],self.cards[i].skill[1],
                                                               self.cards[i].skill[2],self.cards[i].skill[3],
                                                               self.cards[i].lucky,self.cards[i].image))
        self.file = new_file


class character():
    def __init__(self,name,attack,life,level,skill=None,lucky=None,image=None,player = None,number = None):
        self.number = number
        self.image = image
        self.player = player
        self.name = name
        self.attack = attack
        self.life = life
        self.level = level
        if skill is not None:
            self.skill = []
            templete = skill.split(',')
            for i in templete:
                self.skill.append(i)
            self.lucky = lucky
        else:
            for i in all_cards:
                if i.name == self.name:
                    self.skill = i.skill
                    self.lucky = i.lucky
                    self.image = i.image

    def show(self,surface=screen):
        templete = pygame.image.load(self.image).convert_alpha()
        surface.blit(templete,dest=(125,60))
        surface.blit(chinese_font_32.render("%slevel %d"%(self.name,self.level),True,(0,0,0)),dest=(470,70))
        surface.blit(chinese_font_32.render("%d" % self.attack, True, (0, 0, 0)),dest=(470,130))
        surface.blit(chinese_font_32.render("%d"%self.life,True,(0,0,0)),dest=(470,190))
        templete = pygame.image.load(find_skill(self.skill[0])).convert_alpha()
        surface.blit(templete,dest=(470,240))
        templete = pygame.image.load(find_skill(self.skill[1])).convert_alpha()
        surface.blit(templete, dest=(580, 240))
        templete = pygame.image.load(find_skill(self.skill[3])).convert_alpha()
        surface.blit(templete, dest=(580, 300))
        templete = pygame.image.load(find_skill(self.skill[2])).convert_alpha()
        surface.blit(templete, dest=(470, 300))


class tech():
    def __init__(self,name,image):
        self.name = name
        self.image = image


def find_skill(name):
    for i in all_skills:
        if i.name == name:
            return i.image
    else: return False

# the card database
cards_file = open("all_cards.txt",'r')
all_cards = []
a_card = cards_file.readline()
while a_card != '':
    info = a_card.split('\n')
    info = info[0].split('\t')
    #print(info)
    new_card = character(info[0], int(info[1]), int(info[2]), int(info[3]), info[4], int(info[5]),
                         info[6])
    a_card = cards_file.readline()
    all_cards.append(new_card)

skill_file = open("all_skills.txt",'r')
all_skills = []
a_skill = skill_file.readline()
while a_skill != '':
    info = a_skill.split('\n')
    info = info[0].split('\t')
    #print(info)
    new_skill = tech(info[0],info[1])
    all_skills.append(new_skill)
    a_skill = skill_file.readline()

# the login interface
login_image = "resource1\login.png"
login_button = "resource1\login_button.png"
login_bg = pygame.image.load(login_image).convert()
login_bt = pygame.image.load(login_button).convert_alpha()
login_interface = interface(SCREENSIZE[0],SCREENSIZE[1])
login_interface.interface.blit(bd,dest=(0,0))
login_interface.interface.blit(login_bg,dest=(175,75))
login_interface.addbutton(350,300,name="login_bt",image=login_bt,x_len=96,y_len=41)

# state 2 3 88
wrong_key = "resource1\\wrong_key.png"
new_player = "resource1\\new_player.png"
old_player = "resource1\\old_player.png"
o_p = pygame.image.load(old_player).convert_alpha()
n_p = pygame.image.load(new_player).convert_alpha()
w_k = pygame.image.load(wrong_key).convert_alpha()
#welcome_interface = login_interface.interface.blit(mk,dest = (0,0))

# state 4
choose = []
my_card = "resource1\mycard.png"
battle = "resource1\\battle.png"
get_card = "resource1\getcard.png"
team = "resource1\\team.png"
left = "resource1\left.png"
right = "resource1\\right.png"
mc = pygame.image.load(my_card).convert_alpha()
btl = pygame.image.load(battle).convert_alpha()
gc = pygame.image.load(get_card).convert_alpha()
tm = pygame.image.load(team).convert_alpha()
lt = pygame.image.load(left).convert_alpha()
rt = pygame.image.load(right).convert_alpha()
main_interface = interface(SCREENSIZE[0],SCREENSIZE[1])
choose.append(component(main_interface.interface,175,75,450,300,image=mc))
choose.append(component(main_interface.interface,175, 75, 450, 300, image=btl))
choose.append(component(main_interface.interface,175, 75, 450, 300, image=gc))
choose.append(component(main_interface.interface,175, 75, 450, 300, image=tm))

background2 = "resource1\\background2.png"
qianghua = "resource1\\strengthup.png"
gongji = "resource1\\attack.png"
xingyun = "resource1\\lucky.png"
shengming = "resource1\\life.png"
xingming = "resource1\\name.png"
jineng = "resource1\\skill.png"
preview = pygame.image.load("resource1\\preview.png").convert_alpha()
skill = pygame.image.load(jineng).convert_alpha()
qh = pygame.image.load(qianghua).convert_alpha()
attack = pygame.image.load(gongji).convert_alpha()
lucky = pygame.image.load(xingyun).convert_alpha()
life = pygame.image.load(shengming).convert_alpha()
name = pygame.image.load(xingming).convert_alpha()
bg2 = pygame.image.load(background2).convert_alpha()
backspace = pygame.image.load("resource1\\backspace.png").convert_alpha()
card_interface = interface(800,450)

title2 = pygame.image.load("resource1\\levelup.png").convert_alpha()
level = pygame.image.load("resource1\\level.png").convert_alpha()
confirm = pygame.image.load("resource1\\confirm.png").convert_alpha()
#choose = pygame.image.load("resource1\\choose.png").convert_alpha()
levelup_interface = interface(800,450)

counter = 0
x = 0
y = 0
state = 0
count = 0
account = []
key = []
while True:
    if state == 0:
        screen.blit(login_interface.interface, (0, 0))
        login_interface.component["login_bt"].mouseon()
        login_interface.component["login_bt"].isclick()
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
            if event.type == QUIT:
                exit()
        flag = login_interface.component["login_bt"].isclick()
        if flag:
            s = ""
            k = ""
            for i in account:
                s = s + str(i)
            for i in key:
                k = k + str(i)
            try:
                account_file = open("user\%s.txt" % s, 'r+')
            except BaseException:                       #new player
                account_file = open("user\%s.txt" % s, 'w+')
                user = player(s,k,100,1,account_file)
                user.getcard("章鱼哥")
                user.save()
                state = 3
            else:                                       #existed player
                user = player(file=account_file)
                user.readfile()
                user.save()
                if user.key == k:
                    state = 2
                else :
                    state = 88
            count = 0
        pygame.display.update()
    if state == 88:
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            else:
                screen.blit(login_interface.interface, (0, 0))
                screen.blit(mk,(0,0))
                screen.blit(w_k, (175, 75))
                pygame.display.update()
    if state == 2:
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            else:
                screen.blit(login_interface.interface, (0, 0))
                screen.blit(o_p, (280, 245))
                pygame.display.update()
                time.sleep(1)
                state = 4
    if state == 3:
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            else:
                screen.blit(login_interface.interface, (0, 0))
                screen.blit(n_p, (280, 245))
                pygame.display.update()
                time.sleep(1)
                state = 4
    if state == 4:
        clicked = False
        main_interface.interface.blit(bd, dest=(0, 0))
        choose[x].draw()
        choose[x].mouseon()
        clicked = choose[x].isclick()
        main_interface.addbutton(0, 75, 50, 300, name="left", image=lt)
        main_interface.addbutton(750, 75, 50, 300, name="right", image=rt)
        main_interface.component["right"].mouseon()
        next_flag = main_interface.component["right"].isclick()
        main_interface.component["left"].mouseon()
        last_flag = main_interface.component["left"].isclick()
        screen.blit(main_interface.interface,dest=(0,0))
        screen.blit(chinese_font.render("账户：%s"%s,True,(0,0,0)),(10,10))
        screen.blit(chinese_font.render("金钱：%d" %user.money, True, (0, 0, 0)), (10, 30))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            if next_flag:
                if x <3:
                    x = x+1
            if last_flag:
                if x >0:
                    x = x-1
        if clicked:
            state = x+5
    if state == 5:
        card_interface.interface.blit(bg2, dest=(0, 0))
        card_interface.addbutton(300, 10, 200, 50, "title", image=preview)
        card_interface.addbutton(350, 60, 100, 50, "name", image=name)
        card_interface.addbutton(350, 120, 100, 50, "attack", image=attack)
        card_interface.addbutton(350, 180, 100, 50, "life", image=life)
        card_interface.addbutton(350, 240, 100, 50, "skill", image=skill)
        card_interface.addbutton(350, 360, 100, 50, "strengthen", image=qh)
        card_interface.addbutton(470, 360, 100, 50, "back", image=backspace)
        card_interface.addbutton(0, 75, 50, 300, name="left", image=lt)
        card_interface.addbutton(750, 75, 50, 300, name="right", image=rt)
        card_interface.component["strengthen"].mouseon()
        card_interface.component["back"].mouseon()
        card_interface.component["left"].mouseon()
        last_flag = card_interface.component["left"].isclick()
        card_interface.component["right"].mouseon()
        next_flag = card_interface.component["right"].isclick()
        screen.blit(card_interface.interface, dest=(0, 0))
        screen.blit(chinese_font.render("账户：%s" % s, True, (0, 0, 0)), (10, 10))
        screen.blit(chinese_font.render("收藏数：%d" % user.size, True, (0, 0, 0)), (10, 30))
        user.cards[y].show()
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            if last_flag and y>0:
                y = y-1
            if next_flag and y<len(user.cards)-1:
                y = y + 1
            if card_interface.component["back"].isclick():
                state = 4
            if card_interface.component["strengthen"].isclick():
                target = user.cards[y]
                target_image = pygame.image.load(target.image).convert_alpha()
                state = 9
    if state == 9:
        get = False
        levelup_interface.interface.blit(bg2, dest=(0, 0))
        levelup_interface.addbutton(300, 10, 200, 50, "title", image=title2)
        levelup_interface.addbutton(300,60,100,50,"name",image=name)
        levelup_interface.addbutton(410,60,100,50,"level",image=level)
        levelup_interface.addbutton(520,60,100,50,"life",image=life)
        levelup_interface.addbutton(630,60,100,50,"attack",image=attack)
        levelup_interface.addbutton(470, 360, 100, 50, "back", image=backspace)
        levelup_interface.component["back"].mouseon()
        levelup_interface.interface.blit(target_image,dest=(30,60))
        remember = -1
        for items in range(counter,counter+6):
            pos = items % 6
            if items == target.number:
                remember = items
            if items < len(user.cards):
                levelup_interface.interface.blit(chinese_font_32.render("%s"%user.cards[items].name,
                                                                        True,(0,0,0)),dest = (300,120+40*pos))
                levelup_interface.interface.blit(chinese_font_32.render("%d" % user.cards[items].level, True, (0, 0, 0)),
                                                 dest=(450, 120 + 40 * pos))
                levelup_interface.interface.blit(chinese_font_32.render("%d" % user.cards[items].life, True, (0, 0, 0)),
                                                 dest=(540, 120 + 40 * pos))
                levelup_interface.interface.blit(chinese_font_32.render("%d" % user.cards[items].attack, True, (0, 0, 0)),
                                                 dest=(650, 120 + 40 * pos))
                if remember == -1:
                    subsurface = levelup_interface.interface.subsurface(
                        Rect(300, 120 + 40 * pos, 450, 40)).convert_alpha()
                    component1 = component(levelup_interface.interface, 300, 120 + 40 * pos, 450, 40, image=subsurface)
                    # levelup_interface.interface.lock()
                    component1.mouseon()
                    get = component1.isclick()
                    if get:
                        break
            remember = -1
        levelup_interface.addbutton(240, 75, 50, 300, name="left", image=lt)
        last_flag = levelup_interface.component["left"].mouseon()
        last_flag = levelup_interface.component["left"].isclick()
        levelup_interface.addbutton(750, 75, 50, 300, name="right", image=rt)
        next_flag = levelup_interface.component["right"].mouseon()
        next_flag = levelup_interface.component["right"].isclick()
        screen.blit(levelup_interface.interface, dest=(0, 0))
        screen.blit(chinese_font.render("账户：%s" % s, True, (0, 0, 0)), (10, 10))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            if levelup_interface.component["back"].isclick():
                state = 5
            if get:
                state =87
            if next_flag:
                if counter < len(user.cards)-1:
                    counter = counter + 6
            if last_flag:
                if counter > 0:
                    counter = counter - 6
    if state == 87:
        screen.blit(levelup_interface.interface,dest=(0,0))
        screen.blit(mk, dest=(0,0))
        screen.blit(mk, dest=(0, 0))
        screen.blit(mk, dest=(0, 0))
        screen.blit(chinese_font_32.render("此操作将消耗这张%s,确定？"%user.cards[items].name,True,(0,0,0)),dest=(150,200))
        beback = component(screen,470, 360, 100, 50,image=backspace)
        beback.draw()
        beback.mouseon()
        besure = component(screen,350, 360, 100, 50,image=confirm)
        besure.draw()
        besure.mouseon()
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            if besure.isclick():
                target.life += user.cards[items].life*0.01
                target.attack += user.cards[items].attack*0.01
                target.level += 1
                user.save()
                user.deletecard(items)
                screen.blit(chinese_font_32.render("强化成功！请返回查看！",True,(0,0,0)),dest=(150,250))
                pygame.display.update()
                counter =0
                get = False
                state = 9
                time.sleep(1)
            if beback.isclick():
                counter = 0
                get = False
                state = 9
    if state == 6:
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
    if state == 7:
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
    if state == 8:
        for event in pygame.event.get():
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
