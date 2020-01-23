import random
import time

theBoard = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
mode = 0
player = 1
mark = ''
player1 = ''
player1mark = ''
player2 = ''
player2mark = ''


# Get game play mode single player or two player
def playMode():
    global mode
    while True:
        try:
            while mode not in [1, 2]:
                mode = int(input("Are you play Tic Tac Toe in single player or two player (1 / 2) "))
        except ValueError:
            print("Enter 1 for single player or 2 for two player.")
            continue
        else:
            break


# Function for get players names, who goes first and player mark
def getPlayers():
    global player, player1, player1mark, player2, player2mark

    playMode()
    # get player names
    if mode == 2 and player1 == '':
        player1 = input("Enter player 1 name ").capitalize()
        player2 = input("Enter player 2 name ").capitalize()
    elif mode == 1 and player1 == '':
        player1 = input("Enter player name ").capitalize()
        player2 = 'Computer'

    # who goes first
    player = random.choice([1, 0])  # 1 = player1 and  0 = player2 or computer
    if player == 1:
        print("{} will go first".format(player1))
        player1mark = ''
        while player1mark not in ['X', 'O']:
            player1mark = input("{}, choose your mark X or O ".format(player1)).upper()

        if player1mark == 'X':
            player2mark = 'O'
        else:
            player2mark = 'X'

    elif player == 0:
        print("{} will go first.".format(player2))
        if mode == 2:
            player2mark = input("{}, choose your mark X or O ".format(player2)).upper()
        elif mode == 1:
            player2mark = random.choice(['X', 'O'])

        if player2mark == 'X':
            player1mark = 'O'
        else:
            player1mark = 'X'

        if mode == 1:
            print("Computer selected {} mark and your mark is {}".format(player2mark, player1mark))
            time.sleep(3)


# Print the game board
def printBoard(board):
    print(" {} | {} | {} ".format(board[7], board[8], board[9]))
    print("-----------")
    print(" {} | {} | {} ".format(board[4], board[5], board[6]))
    print("-----------")
    print(" {} | {} | {} ".format(board[1], board[2], board[3]))


# check the position is free or not to mark the position
def checkMove(m):
    return theBoard[m] == ' '


# check game is won or not
def checkWin(board):
    if board[1] == board[2] == board[3] != ' ':
        return 'win'
    elif board[4] == board[6] == board[5] != ' ':
        return 'win'
    elif board[7] == board[8] == board[9] != ' ':
        return 'win'

    # vertical winning condition
    elif board[1] == board[4] == board[7] != ' ':
        return 'win'
    elif board[2] == board[5] == board[8] != ' ':
        return 'win'
    elif board[3] == board[6] == board[9] != ' ':
        return 'win'

    # diagonal winning condition
    elif board[1] == board[5] == board[9] != ' ':
        return 'win'
    elif board[3] == board[5] == board[7] != ' ':
        return 'win'

    # game draw condition if board is full
    elif board.count(' ') == 1:
        return 'draw'

    # run game
    else:
        return 'running'


# Function for get position input from player to mark the position
def playerMove(move):
    while True:
        try:
            while move not in range(1, 10):
                move = int(input("Enter position in between 1-9 where you want to mark {} : ".format(mark)))
                if move < 9:
                    if not checkMove(move):
                        print("Position {} already occupied, choose other free position.".format(move))
                        continue
        except ValueError:
            print("Enter only position in between 1-9")
            continue
        else:
            break
    return move


# Get computer move in single player
def aiMove(move):
    turn = 11 - theBoard.count(' ')

    # create possible moves list
    possible_moves = []
    for i in range(1, 10):
        if checkMove(i):
            possible_moves.append(i)

    # possible corner moves list
    corners = []
    for i in possible_moves:
        if i in [1, 3, 7, 9]:
            corners.append(i)

    # possible middle edges moves list
    edges = []
    for i in possible_moves:
        if i in [2, 4, 6, 8]:
            edges.append(i)

    # check the game win in next move take that place
    for let in [player2mark, player1mark]:
        for i in possible_moves:
            temp_board = theBoard.copy()
            temp_board[i] = let
            if checkWin(temp_board) == "win":
                move = i
                return move

    if turn == 1:
        return random.choice(corners)

    if turn == 2:
        # If player taken any corner ai take center
        # If player taken middle edges, ai take any corner besides to player position
        # else player taken center position take any corner

        # pm : player first marked position in theBoard
        pm = theBoard.index(player1mark)

        if pm in [1, 3, 7, 9]:
            return 5
        elif pm in [2, 4, 6, 8]:
            if pm == 2:
                return random.choice([1, 3])
            elif pm == 4:
                return random.choice([1, 7])
            elif pm == 6:
                return random.choice([3, 9])
            elif pm == 8:
                return random.choice([7, 9])

        return random.choice(corners)

    if turn == 3:
        # take diagonal opposite position to first position

        if theBoard[1] == player2mark:
            if 9 in possible_moves:
                return 9
        elif theBoard[3] == player2mark:
            if 7 in possible_moves:
                return 7
        elif theBoard[7] == player2mark:
            if 3 in possible_moves:
                return 3
        elif theBoard[9] == player2mark:
            if 1 in possible_moves:
                return 1

    if turn == 4:
        # take center position if available
        # else take any middle edges position

        if 5 in possible_moves:
            return 5
        elif theBoard[5] == player2mark:
            return random.choice(edges)

    # Take any one corner if available
    if len(corners) > 0:
        return random.choice(corners)

    # Take any one edge if available
    if len(edges) > 0:
        return random.choice(edges)


# Print the game winner
def getWinner(game):
    time.sleep(1)
    if game == 'draw':
        print("Game Draw")
    elif game == 'win':
        winner = player - 1
        if winner % 2 != 0:
            print('Congratulations, {} won the game'.format(player1))
        elif winner % 2 == 0:
            print('Congratulations, {} won the game'.format(player2))


# Main game function
def runGame():
    global player, mark

    getPlayers()
    while checkWin(theBoard) == "running":
        printBoard(theBoard)
        move = 0
        if player % 2 != 0:
            print("{}'s move - {}".format(player1, player1mark))
            mark = player1mark
            move = playerMove(move)
        elif player % 2 == 0:
            print("{}'s move - {}".format(player2, player2mark))
            mark = player2mark
            if mode == 1:
                move = aiMove(move)
                print("Computer placed {} in position {}.".format(player2mark, move))
                time.sleep(2)
            elif mode == 2:
                move = playerMove(move)

        if checkMove(move):
            theBoard[move] = mark
            player += 1
            checkWin(theBoard)

    printBoard(theBoard)
    getWinner(checkWin(theBoard))


# ask for play again
def playAgain():
    pa = ""
    while pa not in ['yes', 'no']:
        pa = input("Are you play game again? (yes / no) ").lower()
    return pa


def main():
    global theBoard, player, player1mark, player2mark
    runGame()
    while checkWin(theBoard) != 'running':
        pa = playAgain()
        if pa == 'yes':
            theBoard = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
            player = 1
            player1mark = ''
            player2mark = ''
            runGame()
        elif pa == 'no':
            time.sleep(2)
            exit()


if __name__ == '__main__':
    main()
