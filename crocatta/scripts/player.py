#!/usr/bin/env python
import rospy
import random
from geometry_msgs.msg  import Point
from std_msgs.msg import String
import time

Croc = [[0 for i in range(5)]for j in range(5)]
Pit = [[0 for i in range(5)]for j in range(5)]
Visited = [[0 for i in range(5)]for j in range(5)]
Safe = [[0 for i in range(5)]for j in range(5)]

class location:
    x = -1
    y = -1

allDirections = [[0,1],[0,-1],[1,0],[-1,0]]
curr = location()

gameover = False

playerPub = rospy.Publisher('Player',Point,queue_size=10)

previous = Point(-1,-1,-1)
p = Point(-1,-1,-1) 

def Print(A):
    for i in range(0,5):
        x = ''
        for j in range(0,5):
            x+=str(A[j][i])
        print(A)

def play(data):
    time.sleep(0.5)
    print('I heard ' + str(data.x) + ' ' + str(data.y) + ' ' + str(data.z))
    #extracts the data from the game
    curr.x = int(data.x)
    curr.y = int(data.y)
    status = int(data.z)


    #sees if computer won
    if(status == 6):
        print('I won!')
        gameover = True
        return
    #sees if the game is over
    if(status==5):
        print('Oops I lost')
        gameover = True
        return

    #updates status at current location
    Visited[curr.x][curr.y] = 1
    Safe[curr.x][curr.y] = 1
    Croc[curr.x][curr.y] = -100
    Pit[curr.x][curr.y] = -100

    #checks which directions next to the players location are valid
    validDirections = []
    for i in allDirections:
        if((curr.x+i[0])>=0 and (curr.x+i[0])<=4 and(curr.y+i[1])>=0 and (curr.y+i[1])<=4):
            validDirections.append(i)

    #updates status map if nothing is next to us
    if(status==1):
        for i in validDirections:
            Croc[curr.x+i[0]][curr.y+i[1]] = -100
            Pit[curr.x+i[0]][curr.y+i[1]] = -100
            Safe[curr.x+i[0]][curr.y+i[1]] = 1
    #updates status map if Pit is next to us
    elif(status==2):
        for i in validDirections:
            if(Visited[curr.x+i[0]][curr.y+i[1]]==0):
                Croc[curr.x+i[0]][curr.y+i[1]] = -100
                Pit[curr.x+i[0]][curr.y+i[1]] += 1
    #updates status map if Croc is next to us
    elif(status==3):
         for i in validDirections:
            if(Visited[curr.x+i[0]][curr.y+i[1]]==0):
                Croc[curr.x+i[0]][curr.y+i[1]] += 1
                Pit[curr.x+i[0]][curr.y+i[1]] = -100
    #updates status map if Both are next to us
    elif(status==4):
        for i in validDirections:
            if(Visited[curr.x+i[0]][curr.y+i[1]]==0):
                Croc[curr.x+i[0]][curr.y+i[1]] += 1
                Pit[curr.x+i[0]][curr.y+i[1]] += 1
    


    # print('Croc:')
    # print(Croc)
    # print('Pit:')
    # print(Pit)s
    # print('Visited:')
    # print(Visited)
    # print('Safe:')
    # print(Safe)


    #decides if we want to move or shoot
    move = True
    #if we know there is no monster next to us we are going to move
    m = []
    for i in validDirections:
        if(Croc[curr.x+i[0]][curr.y+i[1]]>0):
            move = False
            m.append(i)
    if(not move):
        max = m[0]
        biggerMax = False
        for i in m:
            if not Croc[curr.x+i[0]][curr.y+i[1]] == Croc[curr.x+max[0]][curr.y+max[1]]:
                biggerMax = True
        if len(m)==1:
            biggerMax = True
        if(not biggerMax):
            move = True
        else:
            for i in m:
                if Croc[curr.x+i[0]][curr.y+i[1]] > Croc[curr.x+max[0]][curr.y+max[1]]:
                    max = i
            #shoot in max direction
            shoot = Point(max[0],max[1],1)
            rospy.loginfo(shoot)
            playerPub.publish(shoot)

        
    if(move):
        moveDirections = []
        if not Safe == Visited:
            for i in validDirections:
                if Safe[curr.x+i[0]][curr.y+i[1]] == 1:
                    moveDirections.append(i)
            anyNew = False
            newPlaces = []
            for i in moveDirections:
                if Visited[curr.x+i[0]][curr.y+i[1]]==0:
                    anyNew = True
                    newPlaces.append(i)
            if(anyNew):
                moveDirections = newPlaces
            if(moveDirections == []):
                moveDirections = validDirections
        else:
            moveDirections = validDirections
        x = random.randrange(0,len(moveDirections))
        #move in x direction
        moveD = Point(moveDirections[x][0],moveDirections[x][1],2)
        rospy.loginfo(moveD)
        playerPub.publish(moveD)
    # print('Croc:')
    # for i in Croc:
    #     row = ''
    #     for j in i:
    #         row += str(j)
    #     print(row)
    # print('Pit:')
    # for i in Pit:
    #     row = ''  
    #     for j in i:
    #         row += str(j)
    #     print(row)
    # print('Visited:')
    # for i in Visited:
    #     row = ''
    #     for j in i:
    #         row += str(j)
    #     print(row)
    # print('Safe:')
    # for i in Safe:
    #     row = ''
    #     for j in i:
    #         row += str(j)
    #     print(row)
    


                

rospy.init_node('listener', anonymous=True)
rate = rospy.Rate(1)
    

while(not rospy.is_shutdown() and not gameover):
    rospy.Subscriber("Game",Point,play)
    rospy.spin()
    rate.sleep()