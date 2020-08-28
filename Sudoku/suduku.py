import random
from copy import deepcopy



board = [
[8,4,0,0,7,0,2,3,0],
[0,0,0,0,0,0,9,0,0],
[0,0,7,0,0,0,8,0,0],
[0,0,9,0,0,4,7,1,0],
[0,0,0,0,5,0,0,0,3],
[7,0,0,0,6,3,0,0,0],
[5,0,3,0,0,0,0,0,0],
[0,1,0,0,0,5,0,0,4],
[0,8,0,0,2,0,0,0,0]
]

def printBoard(x):
    for i in x:
        print(i)


def solver(b):
    guess = deepcopy(b)
    #initializes the numbers in the rows, columns and each box
    rows = [[0 for i in range(0,9)]for j in range(0,9)]
    cols = [[0 for i in range(0,9)]for j in range(0,9)]
    boxs = [[0 for i in range(0,9)]for j in range(0,9)]
    #this stores possible numbers for each individual box
    poss = [[[0 for i in range(9)]for j in range(9)]for k in range(9)]
    solved = False
    move = True
    #loops until it is solved
    while (not solved):
        #loops through puzzle and updates all the information
        for row in range(0,9):
            for col in range(0,9):
                if guess[row][col]!=0:
                    rows[row][guess[row][col]-1] = 1
                    cols[col][guess[row][col]-1] = 1
                    box = int(row/3)*3 + int(col/3)
                    boxs[box][guess[row][col]-1] = 1
                    poss[row][col][guess[row][col]-1]=1
        #loops through rows to update what numbers are already in each row
        for i in range(9):
            already = []
            for j in range(9):
                if rows[i][j]!=0:
                    already.append(j)
            for j in already:
                for k in range(9):
                    if poss[i][k][j]==0:
                        poss[i][k][j]=-1
        #loops through columns and updates what numbers are in each column
        for i in range(9):
            already = []
            for j in range(9):
                if cols[i][j]!=0:
                    already.append(j)
            for j in already:
                for k in range(9):
                    if poss[k][i][j]==0:
                        poss[k][i][j]=-1
        #loops through all boxes to see what numbers are in each box
        for i in range(9):
            already = []
            for j in range(9):
                if boxs[i][j]!=0:
                    already.append(j)
            for j in already:
                for x in range(9):
                    for y in range(9):
                        if int(x/3)*3+int(y/3)==i:
                            if poss[x][y][j]==0:
                                poss[x][y][j]=-1
        #checks to see if there is a violation
        numUnsolved = 0
        for i in range(9):
            for j in range(9):
                if guess[i][j]==0:  
                    numUnsolved+=1
                    count = 0 
                    for k in range(9):
                        if poss[i][j][k] < 0:
                            count +=1
                    if count == 9:
                        # printBoard(guess)
                        # print(str(i)+','+str(j))
                        return False
        #checks to see if puzzle is solved
        if numUnsolved==0:
            return guess

        move = False
        #checks to see if an individual box has only one number that can go in it
        for i in range(9):
            for j in range(9):
                count = 0
                value = 0
                for k in range(9):
                    if poss[i][j][k]==0:
                        count+=1
                        value = k+1
                    elif poss[i][j][k]>0:
                        count+=2
                if count ==1:
                    guess[i][j] = value
                    # print('Only 1 num')
                    # print(str(i)+','+str(j)+':'+str(value))
                    move = True
                    break
            if move:
                break
        if move:
            continue
        #checks to see if an individual box is the only in a row that can have a specific number
        for i in range(9):
            count = [0 for j in range(9)]
            value = [-1 for j in range(9)]
            for j in range(9):
                if guess[i][j]>0:
                    count[guess[i][j]-1]+=2
                elif guess[i][j]==0:
                    for k in range(9):
                        if poss[i][j][k] == 0:
                            count[k]+=1
                            value[k]=j
            for j in range(9):
                if count[j]==1:
                    guess[i][value[j]]=j+1
                    # print('Row')
                    # print(str(i)+','+str(value[j])+':'+str(j+1))
                    move = True
                    break
            if move:
                break
        if move:
            continue
                    
        #checks to see if an individual box is the only in a column that can have a specific number
        for i in range(9):
            count = [0 for j in range(9)]
            value = [-1 for j in range(9)]
            for j in range(9):
                if guess[j][i]>0:
                    count[guess[j][i]-1]+=2
                elif guess[j][i]==0:
                    for k in range(9):
                        if poss[j][i][k] == 0:
                            count[k]+=1
                            value[k]=j
            for j in range(9):
                if count[j]==1:
                    guess[value[j]][i]=j+1
                    # print('Col')
                    # print(str(value[j])+','+str(i)+':'+str(j+1))
                    move = True
                    break
            if move:
                break
        if move:
            continue

        for i in range(9):
            count = [0 for j in range(9)]
            value = [[-1,-1] for j in range(9)]
            for j in range(9):
                for k in range(9):
                    if int(j/3)*3+int(k/3)==i:
                        if guess[j][k]>0:
                            count[guess[j][k]-1]+=2
                        else:
                            for l in range(9):
                                if poss[j][k][l]==0:
                                    count[l]+=1
                                    value[l] = [j,k]
            for j in range(9):
                if count[j]==1:
                    guess[value[j][0]][value[j][1]]=j+1
                    # print('Box')
                    # print(str(value[j][0])+','+str(value[j][1])+':'+str(j+1))
                    move = True
                    break
            if move:
                break
        if move:
            continue

        #randomly "guess" a number and see if it leads to a contradiction
        numOps = 2
        while (not move) and numOps < 9:
            for i in range(9):
                for j in range(9):
                    if guess[i][j]==0:
                        count = 0
                        options = []
                        for k in range(9):
                            if poss[i][j][k]==0:
                                count+=1
                                options.append(k+1)
                        if count == numOps:
                            for k in options:
                                guess[i][j] = k
                                # print('Guess----------------------------------------')
                                # print(numOps)
                                # print(str(i)+','+str(j)+':'+str(k))
                                result = solver(guess)
                                if not result:
                                    # print('Guess was wrong+++++++++++++++++++++++++++++++++++')
                                    # print(str(i)+','+str(j)+':'+str(k))
                                    guess[i][j]=0
                                else:
                                    return result
                            # print('Wrong')
                            return False
            numOps+=1
    return guess


    
solution = solver(board)
for i in solution:
    print(i)