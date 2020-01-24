import random
import time

mode = 0
player1 = ''
player2 = ''


# draw the game board
def drawBoard(board):
    print(" {} | {} | {} ".format(board[7], board[8], board[9]))
    print("-----------")
    print(" {} | {} | {} ".format(board[4], board[5], board[6]))
    print("-----------")
    print(" {} | {} | {} ".format(board[1], board[2], board[3]))


# check game is won or not
def checkWin(board):
    if (board[1] == board[2] == board[3] != ' ' or  # row
            board[4] == board[6] == board[5] != ' ' or
            board[7] == board[8] == board[9] != ' ' or
            board[1] == board[4] == board[7] != ' ' or  # column
            board[2] == board[5] == board[8] != ' ' or
            board[3] == board[6] == board[9] != ' ' or  # diagonal
            board[1] == board[5] == board[9] != ' ' or
            board[3] == board[5] == board[7] != ' '):
        return 'win'

    # game draw condition if board is full
    elif board.count(' ') == 1:
        return 'draw'

    # run game
    else:
        return 'running'


# game play in single player or two player
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


# get players name
def getPlayers():
    global player1, player2
    if mode == 1:
        player1 = input('Enter your name ').capitalize()
        player2 = 'Computer'
    else:
        player1 = input('Player 1, enter your name ').capitalize()
        player2 = input('Player 2, enter your name ').capitalize()


# get player letters and who goes first in the game
def getLetter():
    player = random.choice([1, 2])
    letter = ''
    if player == 1:
        print(player1 + ", you will go first.")
    else:
        print(player2 + ", you will go first.")
        if mode == 1:
            letter = random.choice(['X', 'O'])
            print(player2 + " selected letter " + letter)

    while letter not in ['X', 'O']:
        print("Do you want to be X or O? ")
        letter = input().upper()

    if player == 1:
        if letter == 'X':
            return [player1, 'X', 'O']
        else:
            return [player1, 'O', 'X']
    else:
        if letter == 'X':
            return [player2, 'O', 'X']
        else:
            return [player2, 'X', 'O']


# check move position is free in board
def checkMove(board, move):
    return board[move] == ' '


# get player move position
def playerMove(board, move):
    while True:
        try:
            while move not in range(1, 10):
                move = int(input("Enter position in between 1-9 where you want to mark : "))
                if move < 9:
                    if not checkMove(board, move):
                        print("Position {} already occupied, choose other free position.".format(move))
                        continue
        except ValueError:
            print("Enter only position in between 1-9")
            continue
        else:
            break
    return move


# get ai move in single player
def aiMove(board, player1letter, player2letter):
    turn = 11 - board.count(' ')

    # create possible moves list
    possible_moves = []
    for i in range(1, 10):
        if checkMove(board, i):
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
    for let in [player2letter, player1letter]:
        for i in possible_moves:
            temp_board = board.copy()
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
        pm = board.index(player1letter)

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

        if board[1] == player2letter:
            if 9 in possible_moves:
                return 9
        elif board[3] == player2letter:
            if 7 in possible_moves:
                return 7
        elif board[7] == player2letter:
            if 3 in possible_moves:
                return 3
        elif board[9] == player2letter:
            if 1 in possible_moves:
                return 1

    if turn == 4:
        # take center position if available
        # else take any middle edges position

        if 5 in possible_moves:
            return 5
        elif board[5] == player2letter:
            return random.choice(edges)

    # Take any one corner if available
    if len(corners) > 0:
        return random.choice(corners)

    # Take any one edge if available
    if len(edges) > 0:
        return random.choice(edges)


# mark the player chosen position
def makeMove(board, letter, move):
    if checkMove(board, move):
        board[move] = letter


# get who is winner in the game
def getWinner(board, game, player):
    if game == 'draw':
        drawBoard(board)
        print("Draw game")
    elif game == 'win':
        drawBoard(board)
        if player == player2:
            print("Congratulations, " + player1 + " won the game")
        elif player == player1:
            print("Congratulations, " + player2 + " won the game")


# get input for play again
def playAgain():
    pa = ''
    while pa not in ['yes', 'no']:
        pa = input("Are you play game again? (yes/no) ")

    if pa == 'yes':
        runGame()
    elif pa == 'no':
        time.sleep(4)
        exit()


# main function of the game
def runGame():
    player, player1letter, player2letter = getLetter()
    board = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
    while checkWin(board) == 'running':
        move = 0
        if player == player1:
            drawBoard(board)
            print(player1 + ', your turn - ' + player1letter)
            move = playerMove(board, move)
            letter = player1letter

            if checkMove(board, move):
                player = player2
                makeMove(board, letter, move)

        elif player == player2:
            drawBoard(board)
            print(player2 + ', your turn - ' + player2letter)

            if mode == 1:
                move = aiMove(board, player1letter, player2letter)
                print("Computer placed {} in position {}.".format(player2letter, move))
            else:
                move = playerMove(board, move)
            letter = player2letter

            if checkMove(board, move):
                player = player1
                makeMove(board, letter, move)

            makeMove(board, letter, move)
        checkWin(board)

    getWinner(board, checkWin(board), player)
    
    if checkWin(board) != 'running':
        playAgain()


def main():
    print("Welcome to Tic Tac Toe game")
    playMode()
    getPlayers()
    runGame()


if __name__ == "__main__":
    main()
