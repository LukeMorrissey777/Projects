#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Point
import time

import random


#classes for the pit, player and crocatta
class Pit:
    x = -1
    y = -1

class Player:
    x = -1
    y = -1
    arrows = 2

class Crocatta:
    x = -1
    y = -1

#function to check if 2 things are in the same place
def inSamePlace(A,B):
    if(A.x == B.x and A.y == B.y):
        return True
    return False



#function to check if player is next to pit or crocatta
def nextTo(P,C,P1,P2,P3):
    NTPit = False
    NTCro = False
    for i in [[-1,0],[1,0],[0,1],[0,-1]]:
        temp = Player()
        temp.x = P.x + i[0]
        temp.y = P.y + i[1]
        if(inSamePlace(temp,C)):
            NTCro = True
        if(inSamePlace(temp,P1) or inSamePlace(temp,P2) or inSamePlace(temp,P3)):
            NTPit = True
    if(NTCro and NTPit):
        print('I hear panting and feel a breeze')
        return 4
    elif(NTCro):
        print('I hear panting')
        return 3
    elif(NTPit):
        print('I feel a breeze')
        return 2
    else:
        print('Silence')
        return 1

#this prints the map, showing the player as '@' and all other spaces as 'X'
def printMap(P,C,P1,P2,P3):
    print('')
    for i in range(0,5):
        x = ''
        for j in range(0,5):
            if(j==P.x and i==P.y):
                x = x + '@'
            elif(j==C.x and i==C.y):
                x = x + 'C'
            elif(j==P1.x and i==P1.y):
                x = x + 'P'
            elif(j==P2.x and i==P2.y):
                x = x + 'P'
            elif(j==P3.x and i==P3.y):
                x = x + 'P'
            else:
                x = x + 'X'
        print(x)
    print('')

#checks if game is over
def isOver(P,C,P1,P2,P3):
    x = [C,P1,P2,P3]
    for i in x:
        if(inSamePlace(P,i)):
            if(i==C):
                print('You ran into the Crocatta, the game is super over')
                message = Point(0,0,5)
                rospy.loginfo(message)
                pubGame.publish(message)
            else:
                print('You fell into the pit, the game is over')
                message = Point(0,0,5)
                rospy.loginfo(message)
                pubGame.publish(message)
            return True
    return False



def fightOrFlight(choice):
    time.sleep(0.5)
    print('I heard ' + str(choice.x) + ' ' + str(choice.y) + ' ' + str(choice.z))
    #user wants to move
    direction = [int(choice.x),int(choice.y)]
    if(int(choice.z) == 2):
        if(direction==[0,-1]):
            me.y += -1
        if(direction==[0,1]):
            me.y += 1
        if(direction == [1,0]):
            me.x += 1
        if(direction == [-1,0]):
            me.x += -1
        gameover = isOver(me,l4,pit1,pit2,pit3)
        if(gameover):
            return

    #user wants to shoot an arrow
    else:
        me.arrows += -1
        temp = Player()
        if(direction==[0,-1]):
            temp.x = me.x
            temp.y = me.y-1
        if(direction==[0,1]):
            temp.x = me.x
            temp.y = me.y+1
        if(direction == [1,0]):
            temp.x = me.x+1
            temp.y = me.y
        if(direction == [-1,0]):
            temp.x = me.x-1
            temp.y = me.y
        if(inSamePlace(temp,l4)):
            gameover = True
            print('You shot the Crocotta! YOU WIN!')
            message = Point(0,0,6)
            rospy.loginfo(message)
            pubGame.publish(message)
            return
        else:
            if(me.arrows == 0):
                print('You ran out of arrows. YOU LOSE!')
                gameover = True
                message = Point(0,0,5)
                rospy.loginfo(message)
                pubGame.publish(message)
                return
            else:
                print('You missed! The Crocatta has moved!')
                l4.x = random.randrange(0,5)
                l4.y = random.randrange(0,5)
                while(inSamePlace(l4,me) or inSamePlace(l4,pit1) or inSamePlace(l4,pit2 or inSamePlace(l4,pit3))):
                    l4.x = random.randrange(0,5)
                    l4.y = random.randrange(0,5)
    #checks to see if something is next to us
    printMap(me,l4,pit1,pit2,pit3)
    safe = nextTo(me,l4,pit1,pit2,pit3)

    #publish a point with current position in x,y and what the player hears in the z
    currentPlace = Point(me.x,me.y,safe)
    rospy.loginfo(currentPlace)
    pubGame.publish(currentPlace)


#creates the pits and makes their locations randomly also checks to make sure they
#are not at the same spot
pit1 = Pit()
pit2 = Pit()
pit3 = Pit()

pit1.x = random.randrange(0,5)
pit1.y = random.randrange(0,5)

pit2.x = random.randrange(0,5)
pit2.y = random.randrange(0,5)

pit3.x = random.randrange(0,5)
pit3.y = random.randrange(0,5)

while(inSamePlace(pit2,pit3)):
    pit2.x = random.randrange(0,5)
    pit2.y = random.randrange(0,5)

while(inSamePlace(pit3,pit1) or inSamePlace(pit3,pit2)):
    pit3.x = random.randrange(0,5)
    pit3.y = random.randrange(0,5)



#spawns the crocatta, puts it at a random location not in a pit
l4 = Crocatta()
l4.x = random.randrange(0,5)
l4.y = random.randrange(0,5)

while(inSamePlace(l4,pit1) or inSamePlace(l4,pit2) or inSamePlace(l4,pit3)):
    l4.x = random.randrange(0,5)
    l4.y = random.randrange(0,5)


#spawns the player in a random location not in a pit or in a square with a crocatta
me = Player()
me.x = random.randrange(0,5)
me.y = random.randrange(0,5)

while(inSamePlace(me,l4) or inSamePlace(me,pit1) or inSamePlace(me,pit2) or inSamePlace(me,pit3)):
    me.x = random.randrange(0,5)
    me.y = random.randrange(0,5)


gameover = False

pubGame = rospy.Publisher('Game',Point,queue_size=10)
rospy.init_node('talker',anonymous=True)
rate = rospy.Rate(1)


#checks to see if something is next to us
printMap(me,l4,pit1,pit2,pit3)
choice = nextTo(me,l4,pit1,pit2,pit3)

#publish a point with current position in x,y and what the player hears in the z
currentPlace = Point(me.x,me.y,choice)
rospy.loginfo(currentPlace)
pubGame.publish(currentPlace)

while(not gameover and not rospy.is_shutdown()):
    rospy.Subscriber("Player",Point,fightOrFlight)
    rospy.spin()
    rate.sleep()






    
    



