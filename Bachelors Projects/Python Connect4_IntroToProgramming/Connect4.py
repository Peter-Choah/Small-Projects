import random
boardWidth = 7
boardHeight = 5
userInput = 0
botInput = 0
gameMode = 0
gameStart = 0
track = []
userToken = ''
botToken = ''
user2Token = ''
userTurn = False
botTurn = False
user2Turn = False
userWin = False
botWin = False
user2Win = False
replay = 0
versusBot = 0
versusHuman = 0
empty_data = ''
#SafetyNet if no save file
print(" If this crashes, type 'wipe' and restart the game")
print(" If not, enter anything")
crash = input(' ')
if crash == 'wipe':
    for x in range(20):
        empty_data += 'empty 100 '
    fwrite = open('Highscores.txt', 'w+')
    fwrite.write(empty_data)
    fwrite.close()
    quit()

    
#Functions
def tracker(boardWidth, boardHeight):
    track1 = []
    track_temp = []
    for x in range(boardWidth):
        for y in range(boardHeight):
            track_temp.append([y,0])
        track1.append(track_temp)
        track_temp = []
    return track1
        
def gameBoard(boardWidth, boardHeight):
    
    print("\t\t+-",end='',sep='')
    for x in range(boardWidth):
        if x < 9:
            print("+--", x+1, "--", sep="", end="")
        else:
            print("+--", x+1, "-", sep="", end="")
    print("+-+")

        
    for row in range(boardHeight*4+1):
        if row != 0:
            print("\t\t",end='',sep='')
        if row % 4 == 0 and row != 0:
            print("+-",end='',sep='')
        elif row == 0:
            print('', end='', sep='')
        else:
            print("|+",end='',sep='')
        for column in range(boardWidth):
            if row % 4 == 0 and row != 0:
                print('+-----', sep='', end='')
            elif row % 4 == 2 and track[column][int((row + 3) / 4) - 1] == [int((row + 3) /4) - 1, 1]:
                print("|  X  ", sep='', end='')
            elif row % 4 == 2 and track[column][int((row + 3) / 4) - 1] == [int((row + 3) /4) - 1, 2]:
                print("|  O  ", sep='', end='')
            elif row % 4 == 2 and track[column][int((row + 3) / 4) - 1] == [int((row + 3) /4) - 1, 3]:
                print("|  B  ", sep='', end='')
            elif row == 0:
                print('', end='', sep='')
            else:
                print("|     ", sep='' , end='')
        if row % 4 == 0 and row != 0:
            print("+-+")
        elif row == 0:
            print('', end='', sep='')
        else:
            print("|+|")

def token_check1(gameMode, track, boardWidth, boardHeight, Token):
    win = False
    if gameMode == 1:
        for x in range(boardWidth - 2 - int(gameMode)):
            for y in range(boardHeight - 2 - int(gameMode)):
                if track[x][y] == [y, Token] and track[x+1][y+1] == [y+1, Token] and track[x+2][y+2] == [y+2, Token] and track[x+3][y+3] == [y+3, Token]:
                    win = True
        for x in range(boardWidth - 2 - int(gameMode)):
            for y in range(boardHeight - 1, boardHeight - 5 +(int(gameMode)), -1):
                if track[x][y] == [y, Token] and track[x+1][y-1] == [y-1, Token] and track[x+2][y-2] == [y-2, Token] and track[x+3][y-3] == [y-3, Token]:
                    win = True
        for x in range(boardWidth - 2 - int(gameMode)):
            for y in range(boardHeight):
                if track[x][y] == [y, Token] and track[x+1][y] == [y, Token] and track[x+2][y] == [y, Token] and track[x+3][y] == [y, Token]:
                    win = True
        for x in range(boardWidth):
            for y in range(boardHeight - 2 - int(gameMode)):
                if track[x][y] == [y,Token] and track[x][y+1] == [y+1, Token] and track[x][y+2] == [y+2, Token] and track[x][y+3] == [y+3, Token]:
                    win = True
    if win == True:
        return win

def token_check2(gameMode, track, boardWidth, boardHeight, Token):
    win = False
    if gameMode == 2:
        for x in range(boardWidth - 2 - int(gameMode)):
            for y in range(boardHeight - 2 - int(gameMode)):
                if track[x][y] == [y, Token] and track[x+1][y+1] == [y+1, Token] and track[x+2][y+2] == [y+2, Token] and track[x+3][y+3] == [y+3, Token] and track[x+4][y+4] == [y+4, Token]:
                    win = True
        for x in range(boardWidth - 2 - int(gameMode)):
            for y in range(boardHeight - 1, boardHeight - 5 +(int(gameMode)), -1):
                if track[x][y] == [y, Token] and track[x+1][y-1] == [y-1, Token] and track[x+2][y-2] == [y-2, Token] and track[x+3][y-3] == [y-3, Token] and track[x+4][y-4] == [y-4, Token]:
                    win = True
        for x in range(boardWidth - 2 - int(gameMode)):
            for y in range(boardHeight ):
                if track[x][y] == [y, Token] and track[x+1][y] == [y, Token] and track[x+2][y] == [y, Token] and track[x+3][y] == [y, Token] and track[x+4][y] == [y, Token]:
                    win = True
        for x in range(boardWidth):
            for y in range(boardHeight - 2 - int(gameMode)):
                if track[x][y] == [y,Token] and track[x][y+1] == [y+1, Token] and track[x][y+2] == [y+2, Token] and track[x][y+3] == [y+3, Token] and track[x][y+4] == [y+4, Token]:
                    win = True
    if win == True:
        return win

def draw(boardWidth, boardHeight):
    no_win = False
    for x in range(boardWidth):
        if track[x][0] != [0, 0]:
            no_win = True
        else:
            no_win = False
            break
    return no_win
#Start
while gameStart == 0:

    gameMode = 0
    track = tracker(boardWidth, boardHeight)
    
#reading file
    f = open('Highscores.txt', 'r')
    data = f.readlines()
    f.close()
    empty_data = ''
    wipe = 0

    playerNames = []
    counter = 0
    moves = []
    scores = data[0].split(' ')
    dataChange = False
    blank = False
    record = ''
    temp_name = ''
    not_win = False
#emptydata
    if data == []:
        for x in range(20):
            empty_data += 'empty 100 '
        fwrite = open('Highscores.txt', 'w')
        fwrite.write(empty_data)
        fwrite.close()

#Highscore reading
    for n in range(0,40,2):
        playerNames.append(scores[n])

    for s in range(1,41,2):
        moves.append(scores[s])
#StartPage
    userInput = 0
    gameBoard(boardWidth, boardHeight)
    print("\t/////////////"*5)
    print("\t\\\\CONNECT 4\\\\\t\\\\CONNECT 5\\\\\t\\\\ SPECIAL \\\\\t\\\\ SCORES \\\\\t\\\\  QUIT   \\\\")
    print("\t/////////////"*5)
    print("\t     1\t\t     2\t\t     3\t\t     4\t\t     5")
    print(" Type '1' for CONNECT 4, '2' for CONNECT 5, '3' for SPECIAL, '4' for scoreboard or '5' to quit.")
    while gameStart == 0 and gameMode != 4:
        gameMode = int(input(' '))
        if gameMode == 1:
            boardWidth = 7
            gameStart = 1
        elif gameMode == 2:
            boardWidth = 9
            gameStart = 1
#Battle Royale
        elif gameMode == 3:
            boardWidth = 10
            gameStart = 1
            versusBot = 1
            versusHuman = 1
            print(" BATTLE ROYALE MODE \n Connect 4 to win!")
            print(" Player 1 = X, Player 2 = O, Bot = B")
            print(" If Draw, the bot tokens will be removed and the tokens will fall")
            userToken = 1
            user2Token = 2
            botToken = 3
            a = 0
            b = 0
            c = 0
            while a == b or a == c or b == c:
                a = random.randrange(10)
                b = random.randrange(10)
                c = random.randrange(10)
            if a < b and b < c:
                print(" Player 1 goes first, Player 2 goes second, Bot goes last")
            elif a < c and c < b:
                print(" Player 1 goes first, Bot goes second, Player 2 goes last")
            elif b < a and a < c:
                print(" Player 2 goes first, Player 1 goes second, Bot goes last")
            elif b < c and c < a:
                print(" Player 2 goes first, Bot goes second, Player 1 goes last")
            elif c < b and b < a:
                print(" Bot goes first, Player 2 goes second, Player 1 goes last")
            elif c < a and a < b:
                print(" Bot goes first, Player 1 goes second, Player 2 goes last")
#ScoreBoard                
        elif gameMode == 4:
            replay = 2
            print("\n\n")
            print(' ','{0:^23}{1:10}{2:^23}'.format('CONNECT 4','','CONNECT 5'))
            print(' ','{0:^4}{1:^15}{2:^6}{3:8}{4:^4}{5:^15}{6:^6}'.format('No.','Player Names','Moves','','No.','Player Names', 'Moves'))
            for count in range(len(playerNames)-10):
                print(' ','{0:^4}{1:^15}{2:^6}{3:8}{4:^4}{5:^15}{6:^6}'.format(count+1, playerNames[count], moves[count],'', count+1, playerNames[count+10], moves[count+10]))
            print("\n\n")
            print("\t///////////////////"*2)
            print("\t\\\\ BACK TO MENU? \\\\\t\\\\   WIPE DATA   \\\\")
            print("\t///////////////////"*2)
            print("\t\t1\t\t\t2")
            print("\n\n")
            print(" Type '1' to go back to menu or '2' to WIPE the scoreboard")
            while userInput != 1 and userInput != 2:
                userInput = int(input(' '))
                if userInput == 1:
                    gameStart = 0
                elif userInput == 2:
                    wipe = 1
                    gameStart = 0
                    if wipe == 1:
                        for x in range(20):
                            empty_data += 'empty 100 '
                        fwrite = open('Highscores.txt', 'w')
                        fwrite.write(empty_data)
                        fwrite.close()
                    wipe = 0
                else:
                    print(" Please input '1' or '2'")
        elif gameMode == 5:
            quit()
        else:
            print(" Please type in '1', '2', '3', or '4' only.")
#versus?
    userInput = 0
    while userInput != 1 and userInput !=2 and gameMode != 3 and gameMode != 4:
        print(" Type '1' for vs AI or '2' for versus human.")
        userInput = int(input(' '))
    if userInput == 1:
        versusBot = 1
        gameStart = 1
    elif userInput == 2:
        versusHuman = 1
        gameStart = 1
        
#Choosing tokens
    userInput = 0
    while userInput != 1 and userInput != 2 and gameMode != 3 and gameMode != 4:
        print(" Type '1' for X or type '2' for O")
        userInput = int(input(" "))
    if versusBot == 1:
        if userInput == 1:
            userToken = 1
            botToken = 2
            print(" Player = X, Bot = O")
        elif userInput == 2:
            userToken = 2
            botToken = 1
            print(" Player = O, Bot = O")
    elif versusHuman == 1:
        if userInput == 1:
            userToken = 1
            user2Token = 2
            print(" Player 1 = X, Player 2 = O")
        elif userInput == 2:
            userToken = 2
            user2Token = 1
            print(" Player 1 = O, Player 2 = X")
    else:
        gameStart = 0
#who first?
    userInput = 0
    while userInput != 1 and userInput != 2 and userInput != 3 and gameMode != 3 and gameMode != 4:
        print(" Who starts first?")
        if versusBot == 1:
            userInput = int(input(" 1 - Yourself\n 2 - Bot\n 3 - Random\n  "))
            if userInput == 1:
                userTurn = True
            elif userInput == 2:
                botTurn = True
            elif userInput == 3:
                r_num = random.randint(1, 2)
                if r_num == 1:
                    userTurn = True
                    print(" You go first!")
                elif r_num == 2:
                    botTurn = True
                    print(" Bot goes first!")
        elif versusHuman == 1:
            userInput = int(input(" 1 - Player 1\n 2 - Player 2\n 3 - Random\n "))
            if userInput == 1:
                userTurn = True
            elif userInput == 2:
                user2Turn = True
            elif userInput == 3:
                r_num = random.randint(1, 2)
                if r_num == 1:
                    userTurn = True
                    print(" Player 1 goes first!")
                elif r_num == 2:
                    user2Turn = True
                    print(" Player 2 goes first!")




#Tracker
    if gameMode != 4:
        
        track = tracker(boardWidth, boardHeight)
        gameBoard(boardWidth, boardHeight)
        print('\n\n\n')

#game switch
    while gameStart == 1 and gameMode !=3 and gameMode != 4:
        userInput = 0

#User1_tokens
        gameStart = 0
        if userTurn:
            while gameStart == 0:
                replay = 0
                if versusBot == 1:
                    print(" Total moves: ", counter)
                userInput = int(input(' Player 1 insert column:  '))
                if (userInput - 1) in range(boardWidth):
                    y = boardHeight - 1
                    gameStart = 1
                    while track[userInput - 1][y] != [y,0] and gameStart == 1:
                        if y > 0:
                             y -= 1
                        else:
                            print("\t\tColumn is full!!!")
                            gameStart = 0
                    track[userInput - 1][y] = [y,userToken]
                else:
                    print(" Insert into a valid column")
            gameBoard(boardWidth, boardHeight)
            print('\n\n\n')
            gameStart = 1
            if versusBot == 1 :
                counter += 1
                botTurn = True
                userTurn = False
            elif versusHuman == 1:
                user2Turn = True
                userTurn = False
#User1_Check
        if gameMode == 1:
            userWin = token_check1(gameMode, track, boardWidth, boardHeight, userToken)
            not_win = draw(boardWidth, boardHeight)
            if userWin:
                print('\n\n\n')
                print("\t\t   PLAYER 1 WIN!!!")
                gameStart = 2
                botTurn = False
                user2Turn = False
                if counter != 0:
                    n = 1
                    while n != 0 and n < 11:
                        if counter < int(moves[n-1]):
                            for m in range(9 - n):
                                moves[9-m] = moves[9-1-m]
                                playerNames[9-m] = playerNames[9-1-m]
                            blank = True
                            while blank:
                                temp_name = input("WOW!, you've reached the leaderboards, type your name please\n")
                                if ' ' in temp_name:
                                    blank = True
                                    print("No space(s) in your name please")
                                else:
                                    blank = False
                            playerNames[n-1] = temp_name
                            moves[n-1] = str(counter)
                            dataChange = True
                            n = 0
                        else:
                            n += 1
            elif not_win:
                print('\n\n\n')
                print("\t\t   DRAW!!!")
                gameStart = 2
                botTurn = False
                user2Turn = False
            
            
        elif gameMode == 2:
            userWin = token_check2(gameMode, track, boardWidth, boardHeight, userToken)
            not_win = draw(boardWidth, boardHeight)
            if userWin:
                print('\n\n\n')
                print("\t\t PLAYER 1 WIN!!!")
                gameStart = 2
                botTurn = False
                user2Turn = False
                if counter != 0:
                    n = 11
                    while n != 0 and n < 21:
                        if counter < int(moves[n-1]):
                            for m in range(19 - n):
                                moves[19-m] = moves[19-1-m]
                                playerNames[19-m] = playerNames[19-1-m]
                            blank = True
                            while blank:
                                temp_name = input("WOW!, you've reached the leaderboards, type your name please\n")
                                if ' ' in temp_name:
                                    blank = True
                                    print("No space(s) in your name please")
                                else:
                                    blank = False
                            playerNames[n-1] = temp_name
                            moves[n-1] = str(counter)
                            dataChange = True
                            n = 0
                        else:
                            n += 1
            elif not_win:
                print('\n\n\n')
                print("\t\t   DRAW!!!")
                gameStart = 2
                botTurn = False
                user2Turn = False
#User2_tokens
        if versusHuman == 1:
            if user2Turn:
                gameStart = 0
                while gameStart == 0:
                    replay = 0
                    userInput = int(input(' Player 2 insert column:  '))
                    if (userInput - 1) in range(boardWidth):
                        y = boardHeight - 1
                        gameStart = 1
                        while track[userInput - 1][y] != [y,0] and gameStart == 1:
                            if y > 0:
                                 y -= 1
                            else:
                                print("\t\tColumn is full!!!")
                                gameStart = 0
                        track[userInput - 1][y] = [y,user2Token]
                        
                    else:
                        print(" Insert into a valid column")
                gameBoard(boardWidth, boardHeight)
                print('\n\n\n')
                gameStart = 1
                userTurn = True
                user2Turn = False
                
#User2_Check
            if gameMode == 1:
                user2Win = token_check1(gameMode, track, boardWidth, boardHeight, user2Token)
                not_win = draw(boardWidth, boardHeight)
                if user2Win:
                    print('\n\n\n')
                    print("\t\t   PLAYER 2 WIN!!!")
                    gameStart = 2
                    userTurn = False
                elif not_win:
                    print('\n\n\n')
                    print("\t\t   DRAW!!!")
                    gameStart = 2
                    userTurn = False
            elif gameMode == 2:
                user2Win = token_check2(gameMode, track, boardWidth, boardHeight, user2Token)
                if user2Win:
                    print('\n\n\n')
                    print("\t\t  PLAYER 2 WIN!!!")
                    gameStart = 2
                    userTurn = False
                elif not_win:
                    print('\n\n\n')
                    print("\t\t   DRAW!!!")
                    gameStart = 2
                    userTurn = False
#Bot_tokens
        if versusBot == 1:
            if botTurn:      
                while gameStart == 0:
                    replay = 0
                    botInput = random.randint(1,boardWidth)
                    y = boardHeight - 1
                    gameStart = 1
                    while track[botInput - 1][y] != [y,0] and gameStart == 1:
                        if y > 0:
                            y -=1
                        else:
                            gameStart = 0
                    if track[botInput - 1][0] == [0, 0]:
                        track[botInput - 1][y] = [y, botToken]
                        print(" Bot inserts column", botInput)
                    else:
                        gameStart = 0
                    userTurn = True
                    botTurn = False

                    gameBoard(boardWidth, boardHeight)
                    print('\n\n\n')
                    
        #Bot_Check
                if gameMode == 1:
                    botWin = token_check1(gameMode, track, boardWidth, boardHeight, botToken)
                    not_win = draw(boardWidth, boardHeight)
                    if botWin:
                        print('\n\n\n')
                        print("\t\t   BOT WINS!!!")
                        gameStart = 2
                        userTurn = False
                    elif not_win:
                        print('\n\n\n')
                        print("\t\t   DRAW!!!")
                        gameStart = 2
                        userTurn = False
 
                    
                elif gameMode == 2:
                    botWin = token_check2(gameMode, track, boardWidth, boardHeight, botToken)
                    not_win = draw(boardWidth, boardHeight)
                    if botWin:
                        print('\n\n\n')
                        print("\t\t   BOT WINS!!!")
                        gameStart = 2
                        userTurn = False
                    elif not_win:
                        print('\n\n\n')
                        print("\t\t   DRAW!!!")
                        gameStart = 2
                        userTurn = False

                
#win_state
        if gameStart == 2:
            gameBoard(boardWidth, boardHeight)
            if versusBot == 1 and versusHuman == 0:
                print(' Total moves: ',counter)
            print(" Do you wish to play again?")
            replay = int(input(" 1 - Yes \n 2 - No \n "))
            if dataChange == True:
                record = ''
                for x in range(20):
                    record += playerNames[x] + ' ' + str(moves[x]) + ' '
#write to file
                myFile = open('Highscores.txt', 'w')
                myFile.write(record)
                myFile.close()
                dataChange = False
#replay
        if replay == 1:
            track = tracker(boardWidth, boardHeight)
            gameStart = 1
            userWin = False
            user2Win = False
            botWin = False
            counter = 0
            not_win = False
            userInput = 0
            while userInput != 1 and userInput != 2 and userInput != 3 and gameMode != 3 and gameMode != 4:
                print(" Who starts first?")
                if versusBot == 1:
                    userInput = int(input(" 1 - Yourself\n 2 - Bot\n 3 - Random\n  "))
                    if userInput == 1:
                        userTurn = True
                    elif userInput == 2:
                        botTurn = True
                    elif userInput == 3:
                        r_num = random.randint(1, 2)
                        if r_num == 1:
                            userTurn = True
                            print(" You go first!")
                        elif r_num == 2:
                            botTurn = True
                            print(" Bot goes first!")
                elif versusHuman == 1:
                    userInput = int(input(" 1 - Player 1\n 2 - Player 2\n 3 - Random\n "))
                    if userInput == 1:
                        userTurn = True
                    elif userInput == 2:
                        user2Turn = True
                    elif userInput == 3:
                        r_num = random.randint(1, 2)
                        if r_num == 1:
                            userTurn = True
                            print(" Player 1 goes first!")
                        elif r_num == 2:
                            user2Turn = True
                            print(" Player 2 goes first!")
            gameBoard(boardWidth,boardHeight)
        elif replay == 2:
            gameStart = 0
            versusHuman = 0
            versusBot = 0
            userWin = False
            user2Win = False
            botWin = False
            
###Battle Royale Mode       
#game switch
    while gameStart == 1 and gameMode == 3 and gameMode != 4:
        userInput = 0
        for counter in range(10):
            if userWin or user2Win or botWin or not_win:
                userTurn = False
                user2Turn = False
                botTurn = False
            else:
                if a == counter:
                    userTurn = True
                    user2Turn = False
                    botTurn = False
                elif b == counter:
                    userTurn = False
                    user2Turn = True
                    botTurn = False
                elif c == counter:
                    userTurn = False
                    user2Turn = False
                    botTurn = True
                else:
                    userTurn = False
                    user2Turn = False
                    botTurn = False
                    gameStart = 1
                
#User1_tokens

            if userTurn:
                gameStart = 0
                while gameStart == 0:
                    replay = 0
                    userInput = int(input(' Player 1 insert column:  '))
                    if (userInput - 1) in range(boardWidth):
                        y = boardHeight - 1
                        gameStart = 1
                        while track[userInput - 1][y] != [y,0] and gameStart == 1:
                            if y > 0:
                                 y -= 1
                            else:
                                print("\t\tColumn is full!!!")
                                gameStart = 0
                        track[userInput - 1][y] = [y,userToken]
                    else:
                        print(" Insert into a valid column")
                gameBoard(boardWidth, boardHeight)
                print('\n\n\n')
                gameStart = 1

#User1_Check
                userWin = token_check1(gameMode - 2, track, boardWidth, boardHeight, userToken)
                not_win = draw(boardWidth, boardHeight)
                if userWin:
                    print('\n\n\n')
                    print("\t\t   PLAYER 1 WIN!!!")
                    gameStart = 2
                elif not_win:
                    gameStart = 2
                    print('\n\n\n')
                    print("\t\t   DRAW!!!")
                    
                    
                    
                
#User2_tokens

            if user2Turn:
                gameStart = 0
                while gameStart == 0:
                    replay = 0
                    userInput = int(input(' Player 2 insert column:  '))
                    if (userInput - 1) in range(boardWidth):
                        y = boardHeight - 1
                        gameStart = 1
                        while track[userInput - 1][y] != [y,0] and gameStart == 1:
                            if y > 0:
                                 y -= 1
                            else:
                                print("\t\tColumn is full!!!")
                                gameStart = 0
                        track[userInput - 1][y] = [y,user2Token]
                        
                    else:
                        print(" Insert into a valid column")
                gameBoard(boardWidth, boardHeight)
                print('\n\n\n')
                gameStart = 1
#User2_Check

                user2Win = token_check1(gameMode - 2, track, boardWidth, boardHeight, user2Token)
                not_win = draw(boardWidth, boardHeight)
                if user2Win:
                    print('\n\n\n')
                    print("\t\t   PLAYER 2 WIN!!!")
                    gameStart = 2
                elif not_win:
                    gameStart = 2
                    print('\n\n\n')
                    print("\t\t   DRAW!!!")
                    

#Bot_tokens
            if versusBot == 1:
                if botTurn:
                    gameStart = 0
                    while gameStart == 0:
                        replay = 0
                        botInput = random.randint(1,boardWidth)
                        y = boardHeight - 1
                        gameStart = 1
                        while track[botInput - 1][y] != [y,0] and gameStart == 1:
                            if y > 0:
                                y -=1
                            else:
                                gameStart = 0
                        if track[botInput - 1][0] == [0, 0]:
                            track[botInput - 1][y] = [y, botToken]
                            print(" Bot inserts column", botInput)
                        else:
                            gameStart = 0
                    gameBoard(boardWidth, boardHeight)
                    print('\n\n\n')
                    
#Bot_Check

                botWin = token_check1(gameMode - 2, track, boardWidth, boardHeight, botToken)
                not_win = draw(boardWidth, boardHeight)
                if botWin:
                    print('\n\n\n')
                    print("\t\t   BOT WINS!!!")
                    gameStart = 2
                elif not_win:
                    gameStart = 2
                    print('\n\n\n')
                    print("\t\t   DRAW!!!")
                
#win_state
        if gameStart == 2:
            
#Drops tokens
            if versusBot == 1 and not_win == True:
                print(" Removing Bot Tokens....")
                for x in range(boardWidth):
                    for y in range (boardHeight):
                        if track[x][y] == [y, 3]:
                            for z in range(y):
                                track[x][y - z][1] = track[x][y - z - 1][1]
                            track[x][0] = [0, 0]
                userTurn = False
                user2Turn = False
                versusBot = 0
                not_win = False
                gameStart = 1
                gameBoard(boardWidth, boardHeight)
                
                userWin = token_check1(gameMode - 2, track, boardWidth, boardHeight, userToken)
                user2Win = token_check1(gameMode - 2, track, boardWidth, boardHeight, user2Token)
                if userWin and user2Win:
                    print('\n\n\n')
                    print("\t\t   DRAW!!!")
                    print(" Do you wish to play again?")
                    replay = int(input(" 1 - Yes \n 2 - No \n "))
                elif userWin:
                    print('\n\n\n')
                    print("\t\t   PLAYER 1 WIN!!!")
                    print(" Do you wish to play again?")
                    replay = int(input(" 1 - Yes \n 2 - No \n "))
                elif user2Win:
                    print('\n\n\n')
                    print("\t\t   PLAYER 2 WIN!!!")
                    print(" Do you wish to play again?")
                    replay = int(input(" 1 - Yes \n 2 - No \n "))


            else:    
                gameBoard(boardWidth, boardHeight)
                print(" Do you wish to play again?")
                replay = int(input(" 1 - Yes \n 2 - No \n "))
                
#replay
        if replay == 1:
            track = tracker(boardWidth, boardHeight)
            gameStart = 1
            versusBot = 1
            userWin = False
            user2Win = False
            botWin = False
            not_win = False
            a = 0
            b = 0
            c = 0
            while a == b or a == c or b == c:
                a = random.randrange(10)
                b = random.randrange(10)
                c = random.randrange(10)
            if a < b and b < c:
                print(" Player 1 goes first, Player 2 goes second, Bot goes last")
            elif a < c and c < b:
                print(" Player 1 goes first, Bot goes second, Player 2 goes last")
            elif b < a and a < c:
                print(" Player 2 goes first, Player 1 goes second, Bot goes last")
            elif b < c and c < a:
                print(" Player 2 goes first, Bot goes second, Player 1 goes last")
            elif c < b and b < a:
                print(" Bot goes first, Player 2 goes second, Player 1 goes last")
            elif c < a and a < b:
                print(" Bot goes first, Player 1 goes second, Player 2 goes last")
        elif replay == 2:
            gameStart = 0
            versusHuman = 0
            versusBot = 0
            userWin = False
            user2Win = False
            botWin = False
            gameMode = 0
                        
            


