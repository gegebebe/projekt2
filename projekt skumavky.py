from random import *
from time import time
import pygame

pygame.init()

screen = pygame.display.set_mode((700, 500))


# pamatove struktury
class Node:
    def __init__(self, data, next):
        self.data: pygame.Color = data
        self.next = next

class Magazine:
    def __init__(self):
        self.start: Node = None
        self.len = 0

    def pop(self, limit = 6):
        amount = 0
        if self.start:
            curr = self.start
            first_color = curr.data
            while curr.data == first_color and amount < limit:
                amount += 1
                self.start = curr.next
                curr = self.start
                if curr == None:
                    break
            self.len -= amount
            return amount, first_color
        else:
            return 0, None
        
    def add(self, amount, data: pygame.Color):
        for i in range(min(amount, 6-self.len)):
            self.start = Node(data, self.start)
            self.len += 1



# HRA

class Game:
    def __init__(self):
        self.skumavky: list[Magazine] = []
        self.turn = 0
        self.ozn = 1000

    def nakresli(self):
        pygame.draw.rect(screen, (250, 250, 250), [42 + self.ozn*70, 97, 56, 306])
        for i in range(len(self.skumavky)):
            pygame.draw.rect(screen, (200, 200, 200), [45 + i*70, 100, 50, 300])
            skum = self.skumavky[i]
            curr = skum.start
            for j in range(skum.len):
                pygame.draw.ellipse(screen, curr.data, [45 + i*70, 100 + (6-skum.len)*50 + j*50, 50, 50])
                curr = curr.next
    
    def oznac(self, poz):
        if (poz[0] - 45)%70 <= 50 and 100 <= poz[1] <= 400:
            new: int = (poz[0] - 45)//70
            if 0 <= new < len(self.skumavky):
                if self.ozn <= len(self.skumavky):
                    if self.ozn != new:
                        self.skumavky[new].add(*self.skumavky[self.ozn].pop(limit = 6-self.skumavky[new].len))
                        self.ozn = 1000
                    else:
                        self.ozn = 1000
                else:
                    self.ozn = new
            else:
                self.ozn = 1000


# Button

class Button:
    def __init__(self, pozx, pozy, sizex, sizey, image: pygame.Surface, color, func):
        self.rectangle = pygame.Rect(pozx, pozy, sizex, sizey)
        self.image = image
        self.color = color
        self.pressed = False
        self.func = func

    def nakresli(self, screen):
        pygame.draw.rect(screen, self.color, self.rectangle)
        if self.image:
            screen.blit(self.image, (self.rectangle.centerx - self.image.get_width()//2,
                                     self.rectangle.centery - self.image.get_height()//2))
            
    def check_click(self):
        mouse_poz = pygame.mouse.get_pos()
        if self.rectangle.collidepoint(mouse_poz):
            if pygame.mouse.get_pressed()[0]:
                if self.pressed == False:
                    self.func()
                self.pressed = True
            else:
                if self.pressed == True:
                    self.pressed = False



# Hlavne Veci


def new_game():
    global game
    game = Game()
    for i in range(skumavky):
        game.skumavky.append(Magazine())

    lopty = []
    farby = [cervena, zelena, modra, cierna, fialova, cyan, zlta]
    for f in range(n_farby):
        farb = choice(farby)
        farby.remove(farb)
        for g in range(gulicky):
            lopty.append(farb)
    shuffle(lopty)
    for i in lopty:
        choice(list(filter(lambda x: x.len < 6, game.skumavky))).add(1, i)

def more_skumaviek():
    global skumavky
    if skumavky < 9:
        skumavky += 1

def less_skumaviek():
    global skumavky
    if skumavky > 3 and n_farby*gulicky < skumavky*5 - 5:
        skumavky -= 1

def more_guliciek():
    global gulicky
    if gulicky < 6 and n_farby*gulicky < skumavky*5 - 5:
        gulicky += 1

def less_guliciek():
    global gulicky
    if gulicky > 2:
        gulicky -= 1

def more_farby():
    global n_farby
    if n_farby < 7 and n_farby*gulicky < skumavky*5 - 5:
        n_farby += 1

def less_farby():
    global n_farby
    if n_farby > 2:
        n_farby -= 1


skumavky = 4
gulicky = 5
n_farby = 3

font = pygame.font.Font(None, 50)
font_m = pygame.font.Font(None, 20)
sipka_left = pygame.image.load("sipka nalavo.png")
sipka_right = pygame.image.load("sipka napravo.png")
new_game_img = pygame.image.load("new game.png")

buttons: list[Button] = []
new_game_button = Button(10, 10, 100, 50, new_game_img, (150, 150, 50), new_game)
less_skumavky_button = Button(150, 10, 50, 50, sipka_left, (80, 80, 220), less_skumaviek)
more_skumavky_button = Button(250, 10, 50, 50, sipka_right, (80, 80, 220), more_skumaviek)
less_gulicky_button = Button(350, 10, 50, 50, sipka_left, (80, 80, 220), less_guliciek)
more_gulicky_button = Button(450, 10, 50, 50, sipka_right, (80, 80, 220), more_guliciek)
less_farby_button = Button(350, 440, 50, 50, sipka_left, (80, 80, 220), less_farby)
more_farby_button = Button(450, 440, 50, 50, sipka_right, (80, 80, 220), more_farby)
buttons.append(new_game_button)
buttons.append(less_skumavky_button)
buttons.append(more_skumavky_button)
buttons.append(less_gulicky_button)
buttons.append(more_gulicky_button)
buttons.append(less_farby_button)
buttons.append(more_farby_button)


cervena = pygame.Color(200, 0, 0)
zelena = pygame.Color(0, 200, 0)
modra = pygame.Color(0, 0, 200)
cierna = pygame.Color(10, 10, 10)
fialova = pygame.Color(139, 72, 181)
cyan = pygame.Color(0, 181, 162)
zlta = pygame.Color(181, 175, 0)
farby = [cervena, zelena, modra, cierna, fialova, cyan, zlta]


new_game()

running = True
cas_od_klik = 0

while running:
    screen.fill((100, 100, 100))
    game.nakresli()
    for butt in buttons:
        butt.nakresli(screen)
        butt.check_click()

    screen.blit(font.render(str(skumavky), False, (255, 255, 255)), (215, 20))
    screen.blit(font_m.render("skumavky", False, (255, 255, 255)), (195, 65))
    screen.blit(font.render(str(gulicky), False, (255, 255, 255)), (415, 20))
    screen.blit(font_m.render("gulicky", False, (255, 255, 255)), (403, 65))
    screen.blit(font.render(str(n_farby), False, (255, 255, 255)), (415, 450))
    screen.blit(font_m.render("farby", False, (255, 255, 255)), (407, 425))


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if pygame.mouse.get_pressed()[0] and time() > cas_od_klik + 0.1:
            poz = pygame.mouse.get_pos()
            game.oznac(poz)
            cas_od_klik = time()
        



    pygame.display.update()

pygame.quit()