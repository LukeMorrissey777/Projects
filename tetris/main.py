import pygame
from pieces import *
import time
import random 

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_SPACE,
    KEYDOWN,
    QUIT,
)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
clock = pygame.time.Clock()
blue = (0,0,100)
green = (0,100,0)

bright_blue = (0,0,255)
bright_green = (0,150,0)

PIECES = [LINE_P,S_P,Z_P,L_P,J_P,SQ_P,T_P]
PIECE_COLORS = [(125, 60, 152),(176, 58, 46),(31, 97, 141),(241, 196, 15),(211, 84, 0),(23, 165, 137),(165, 23, 154)]

turn = 0


class Block(pygame.sprite.Sprite):
    def __init__(self,piece_num,x,y):
        super(Block, self).__init__()
        self.surf = pygame.Surface((25,25))
        self.surf.fill(PIECE_COLORS[piece_num])
        self.piece_num = piece_num
        self.rect = self.surf.get_rect()
        self.rect.left = x
        self.rect.top = y
        self.prev = [x,y]
    def update(self, pressed_keys):
        self.prev = [self.rect.left,self.rect.top]
        if turn % 10 == 0:
            self.rect.move_ip(0, 25)
        if pressed_keys[K_LEFT] and turn%3==0:
            self.rect.move_ip(-25, 0)
        if pressed_keys[K_RIGHT] and turn%3==0:
            self.rect.move_ip(25, 0)
        if pressed_keys[K_DOWN] and turn % 10 == 1:
            self.rect.move_ip(0,25)
        if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            return -2
        if self.rect.bottom > SCREEN_HEIGHT:
            return -1
    def goPrev(self):
        self.rect.left = self.prev[0]
        self.rect.top = self.prev[1]
    def stayInWidth(self):
        self.rect.left = self.prev[0]
        

class Piece():
    def __init__(self):
        self.piece_num = random.randint(0,6)
        self.piece = pygame.sprite.Group()
        self.turnRotate = -10
        for i in range(4):
            for j in range(4):
                if PIECES[self.piece_num][i][j] == 1:
                    block = Block(self.piece_num,100+25*i,25*j)
                    self.piece.add(block)
    def draw(self):
        for block in self.piece:
            screen.blit(block.surf, block.rect)
    def update(self,key_pressed):
        if key_pressed[K_SPACE]:
            self.rotate()
        x = []
        for block in self.piece:
            x.append(block.update(key_pressed))
        for i in x:
            if i == -1:
                for block in self.piece:
                    block.goPrev()
                    bottom.add(block)
                return -1
            if i == -2:
                for block in self.piece:
                    block.stayInWidth()
                break
    def collide(self):
        for block in self.piece:
            block.goPrev()
            bottom.add(block)
    def rotate(self):
        origin = [-1,-1]
        if self.turnRotate < turn-10:
            self.turnRotate= turn
            for block in self.piece:
                if origin == [-1,-1]:
                    origin = [block.rect.left,block.rect.top]
                else:
                    diff = [block.rect.left-origin[0],block.rect.top-origin[1]]
                    block.rect.left = origin[0] - diff[1]
                    block.rect.top = origin[1] + diff[0]


def checkRows():
    rowNum = {}
    for block in bottom:
        try:
            rowNum[block.rect.top]+=1
        except:
            rowNum[block.rect.top] = 1
    to_be_deleted = []
    for x in rowNum:
        if rowNum[x] >= 10:
            to_be_deleted.append(x)
    to_be_deleted.sort()
    if to_be_deleted != []:
        for block in bottom:
            killed = False
            for x in to_be_deleted:
                if block.rect.top == x:
                    block.kill()
                    killed = True
            for i in range(len(to_be_deleted)):
                if not killed and block.rect.top < to_be_deleted[i]:
                    block.rect.top += 25*(len(to_be_deleted)-i)
                    break

def drawTetris():
    largeText = pygame.font.Font('freesansbold.ttf',115)
    T_TextSurf, T_TextRect = text_objects("T", largeText,PIECE_COLORS[0])
    T_TextRect.center = ((SCREEN_WIDTH/2)-125,(SCREEN_HEIGHT/4))
    screen.blit(T_TextSurf, T_TextRect)
 
    e_TextSurf, e_TextRect = text_objects("e", largeText,PIECE_COLORS[1])
    e_TextRect.center = ((SCREEN_WIDTH/2)-66,(SCREEN_HEIGHT/4))
    screen.blit(e_TextSurf, e_TextRect)

    t_TextSurf, t_TextRect = text_objects("t", largeText,PIECE_COLORS[2])
    t_TextRect.center = ((SCREEN_WIDTH/2)-15,(SCREEN_HEIGHT/4))
    screen.blit(t_TextSurf, t_TextRect)

    r_TextSurf, r_TextRect = text_objects("r", largeText,PIECE_COLORS[3])
    r_TextRect.center = ((SCREEN_WIDTH/2)+35,(SCREEN_HEIGHT/4))
    screen.blit(r_TextSurf, r_TextRect)

    i_TextSurf, i_TextRect = text_objects("i", largeText,PIECE_COLORS[4])
    i_TextRect.center = ((SCREEN_WIDTH/2)+75,(SCREEN_HEIGHT/4))
    screen.blit(i_TextSurf, i_TextRect)

    s_TextSurf, s_TextRect = text_objects("s", largeText,PIECE_COLORS[5])
    s_TextRect.center = ((SCREEN_WIDTH/2)+130,(SCREEN_HEIGHT/4))
    screen.blit(s_TextSurf, s_TextRect)


def game_intro():

    intro = True

    while intro:
        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        screen.fill((0,0,0))
        drawTetris()

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if 150+100 > mouse[0] > 150 and 450+50 > mouse[1] > 450:
            pygame.draw.rect(screen, bright_green,(150,450,100,50))
            if click[0] == 1:
                intro = False

        else:
            pygame.draw.rect(screen, green,(150,450,100,50))
        
        if 550+100 > mouse[0] > 550 and 450+50 > mouse[1] > 450:
            pygame.draw.rect(screen, bright_blue,(550,450,100,50))
            if click[0] == 1:
                instruct()
        else:
            pygame.draw.rect(screen, blue,(550,450,100,50))

        smallText = pygame.font.Font("freesansbold.ttf",20)
        textSurf, textRect = text_objects("Start", smallText,(255,255,255))
        textRect.center = ( (150+(100/2)), (450+(50/2)) )
        screen.blit(textSurf, textRect)

        textSurf, textRect = text_objects("Rules", smallText,(255,255,255))
        textRect.center = ( (550+(100/2)), (450+(50/2)) )
        screen.blit(textSurf, textRect)

        pygame.display.update()
        clock.tick(15)

def instruct():
    instruct = True
    while instruct:
        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        screen.fill((0,0,0))
        drawTetris()

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        medium_text = pygame.font.Font("freesansbold.ttf",50)
        textSurf, textRect = text_objects("How to play:", medium_text,(255,255,255))
        textRect.center = ( (SCREEN_WIDTH/2), (400) )
        screen.blit(textSurf, textRect)
        textSurf, textRect = text_objects("Press space to rotate", medium_text,(255,255,255))
        textRect.center = ( (SCREEN_WIDTH/2), (400)+50 )
        screen.blit(textSurf, textRect)
        textSurf, textRect = text_objects("Use arrow keys to move block", medium_text,(255,255,255))
        textRect.center = ( (SCREEN_WIDTH/2), (400)+100 )
        screen.blit(textSurf, textRect)


        if SCREEN_WIDTH/2+50 > mouse[0] > SCREEN_WIDTH/2-50 and 600+50 > mouse[1] > 600:
            pygame.draw.rect(screen, bright_blue,(SCREEN_WIDTH/2-50,600,100,50))
            if click[0] == 1:
                return
        else:
            pygame.draw.rect(screen, blue,(SCREEN_WIDTH/2-50,600,100,50))

        smallText = pygame.font.Font("freesansbold.ttf",20)
        textSurf, textRect = text_objects("Back", smallText,(255,255,255))
        textRect.center = ( (SCREEN_WIDTH/2), (600+(50/2)) )
        screen.blit(textSurf, textRect)

        pygame.display.update()
        clock.tick(15)



def text_objects(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

pygame.init()
screen = pygame.display.set_mode([SCREEN_WIDTH,SCREEN_HEIGHT])
bottom = pygame.sprite.Group()
piece = Piece()
running = True
game_intro()
while running:
    time.sleep(.02)
    turn +=1
    checkRows()
    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    # Fill the screen with black
    screen.fill((0,0,0))

    # Draw the player on the screen
    piece.draw()

    # Get all the keys currently pressed
    pressed_keys = pygame.key.get_pressed()

    for entity in bottom:
        screen.blit(entity.surf, entity.rect)
    
    if(piece.update(pressed_keys) == -1):
        piece = Piece()
    for block in piece.piece:
        if pygame.sprite.spritecollideany(block,bottom):
            piece.collide()
            piece = Piece()
            break
    
    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()