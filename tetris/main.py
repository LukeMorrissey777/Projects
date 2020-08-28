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

SCREEN_WIDTH = 250
SCREEN_HEIGHT = 800

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

        


pygame.init()
screen = pygame.display.set_mode([SCREEN_WIDTH,SCREEN_HEIGHT])
bottom = pygame.sprite.Group()
piece = Piece()
running = True
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