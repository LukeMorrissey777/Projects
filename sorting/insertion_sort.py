import pygame
import random
import time

from pygame.locals import *


scl = 5

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
running = True
pygame.init()
screen = pygame.display.set_mode([SCREEN_WIDTH,SCREEN_HEIGHT])


def draw(A,i):
    screen.fill((255,255,255))
    for k in range(len(A)):
        if k == i:
            pygame.draw.rect(screen,(0,255,0),(k*scl,SCREEN_HEIGHT-A[k],scl,A[k]))
        else:
            pygame.draw.rect(screen,(0,0,0),(k*scl,SCREEN_HEIGHT-A[k],scl,A[k]))
    pygame.display.flip()

def insertionSort(A):
    for i in range(1,len(A)):
        s = A[i]
        j = 1
        while A[i-j] > s and j <= i:
            A[i-j+1],A[i-j] = A[i-j],A[i-j+1]
            j += 1
            draw(A,i-j+1)
            time.sleep(0.01)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
        A[i-j+1] = s
    draw(A,-1)
    return A

x = [random.randint(0,SCREEN_HEIGHT) for i in range(SCREEN_WIDTH/scl)]
# print(insertionSort(x))





running = insertionSort(x)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


