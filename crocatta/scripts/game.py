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
    if(NTCro):
        print('I hear panting')
    if(NTPit):
        print('I feel a breeze')
    if(not NTPit and not NTCro):
        print('Silence')
    return

#this prints the map, showing the player as '@' and all other spaces as 'X'
def printMap(P):
    print('')
    for i in range(0,5):
        x = ''
        for j in range(0,5):
            if(j==P.x and i==P.y):
                x = x + '@'
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
            else:
                print('You fell into the pit, the game is over')
            return True
    return False


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

while(inSamePlace(pit2,pit1)):
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

while(not gameover):
    #checks to see if something is next to us
    printMap(me)
    nextTo(me,l4,pit1,pit2,pit3)

    #asks the user 
    choice = input('Would you like to move(1) or shoot an arrow(2)? ')
    while(not(choice == '1') and not(choice == '2')):
        choice = input('Invalid choice. Enter 1 to move or 2 to shoot ')

    #user wants to move
    if(choice == '1'):
        direction = input('Would you like to move up(w), down(s), left(a) or right(d)? ')
        while(not(direction == 'w') and not(direction == 's') and not(direction == 'd') and not(direction == 'a')):
            direction = input('Invalid direction please choose again ')
        if(direction=='w'):
            if(me.y==0):
                print('Oops you bumped into the wall')
            else:
                me.y += -1
        if(direction=='s'):
            if(me.y==4):
                print('Oops you bumped into the wall')
            else:
                me.y += 1
        if(direction == 'd'):
            if(me.x ==4):
                print('Oops you bumped into the wall')
            else:
                me.x += 1
        if(direction == 'a'):
            if(me.x == 0):
                print('Oops you bumped into the wall')
            else:
                me.x += -1
        gameover = isOver(me,l4,pit1,pit2,pit3)

    #user wants to shoot an arrow
    else:
        me.arrows += -1
        direction = input('Would you like to shoot up(w), down(s), left(a) or right(d)? ')
        while(not(direction == 'w') and not(direction == 's') and not(direction == 'd') and not(direction == 'a')):
            direction = input('Invalid direction please choose again ')
        temp = Player()
        if(direction=='w'):
            if(me.y==0):
                print('Oops you shot the wall')
            else:
                temp.x = me.x
                temp.y = me.y-1
        if(direction=='s'):
            if(me.y==4):
                print('Oops you shot the wall')
            else:
                temp.x = me.x
                temp.y = me.y+1
        if(direction == 'd'):
            if(me.x ==4):
                print('Oops you shot the wall')
            else:
                temp.x = me.x+1
                temp.y = me.y
        if(direction == 'a'):
            if(me.x == 0):
                print('Oops you shot the wall')
            else:
                temp.x = me.x-1
                temp.y = me.y
        if(inSamePlace(temp,l4)):
            gameover = True
            print('You shot the Crocotta! YOU WIN!')
        else:
            if(me.arrows == 0):
                print('You ran out of arrows. YOU LOSE!')
                gameover = True
            else:
                print('You missed! The Crocatta has moved!')
                l4.x = random.randrange(0,5)
                l4.y = random.randrange(0,5)
                while(inSamePlace(l4,me) or inSamePlace(l4,pit1) or inSamePlace(l4,pit2 or inSamePlace(l4,pit3))):
                    l4.x = random.randrange(0,5)
                    l4.y = random.randrange(0,5)



    
    


