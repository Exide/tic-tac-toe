import os

class Console:

    data = list()
    data.append('')
    data.append('Tic-Tac-Toe')
    data.append('by Ryan Zander (c) May 2012')
    data.append('')
    data.append('As a challenge to myself I made this while drinking')
    data.append('and playing Settlers of Catan at a birthday beach party.')
    data.append('')
    data.append('Your turn!')

    def addLine(self, s):
        self.data.append(s)
        self.data.pop(0)

    def getLine(self, n):
        return self.data[n-1]

def isNumber(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def indexToLetter(n):
    # convert an index into a letter value
    if   n == 0: return 'a'
    elif n == 1: return 'b'
    elif n == 2: return 'c'

def letterToIndex(s):
    # convert a letter value into an index
    if   s.lower() == 'a': return 0
    elif s.lower() == 'b': return 1
    elif s.lower() == 'c': return 2

def aiSelectSquare(b):
    # AI just picks the first (row major) square available
    for i, row in enumerate(b):
        for j, column in enumerate(row):
            if column == ' ':
                return (i, j)

def chooseSquare(board, player, (row, column)):
    square = indexToLetter(row).upper() + str(column+1)
    # try and choose the square
    if board[row][column] == ' ':
        board[row][column] = player
        console.addLine('%s takes %s' % (player, square))
        return True
    else:
        console.addLine('The square at %s is taken by %s.' % (square, board[row][column]))
        return False

def emptyBoard():
    return [[' ', ' ', ' '] for i in range(0, 3)]

def compareBoards(board, possibility, player=None):
    for i, row in enumerate(board):
        for j, column in enumerate(row):
            if possibility[i][j]:
                if player:
                    if board[i][j] != player:
                        return False
                else:
                    if board[i][j] == ' ':
                        return False
    return True

def isGameOver(board):
    possible_wins = list()
    # horizontally
    possible_wins.append(((1,1,1),(0,0,0),(0,0,0)))
    possible_wins.append(((0,0,0),(1,1,1),(0,0,0)))
    possible_wins.append(((0,0,0),(0,0,0),(1,1,1)))
    # vertically
    possible_wins.append(((1,0,0),(1,0,0),(1,0,0)))
    possible_wins.append(((0,1,0),(0,1,0),(0,1,0)))
    possible_wins.append(((0,0,1),(0,0,1),(0,0,1)))
    # diagonally
    possible_wins.append(((1,0,0),(0,1,0),(0,0,1)))
    possible_wins.append(((0,0,1),(0,1,0),(1,0,0)))
    # full board
    tie = ((1,1,1),(1,1,1),(1,1,1))

    for possibility in possible_wins:
        if   compareBoards(board, possibility, 'X'): return 'X'
        elif compareBoards(board, possibility, 'O'): return 'O'

    if compareBoards(board, tie):
        return True

    return False

# -----------------------------------------------------------------------------

board = emptyBoard()
console = Console()
gameRunning = True
gameOver = False
yourTurn = True

while gameRunning:

    # clear the screen
    os.system('cls' if os.name=='nt' else 'clear')

    print
    print '      1   2   3     %s' % console.getLine(1)
    print '    +---+---+---+   %s' % console.getLine(2)
    print '  A | %s | %s | %s |   %s' % (board[0][0], board[0][1], board[0][2], console.getLine(3))
    print '    +---+---+---+   %s' % console.getLine(4)
    print '  B | %s | %s | %s |   %s' % (board[1][0], board[1][1], board[1][2], console.getLine(5))
    print '    +---+---+---+   %s' % console.getLine(6)
    print '  C | %s | %s | %s |   %s' % (board[2][0], board[2][1], board[2][2], console.getLine(7))
    print '    +---+---+---+   > %s' % console.getLine(8)
    print
    print '  Options: (q)uit, (r)estart, or enter a square (e.g. b2)'

    if yourTurn:
        # gather the user's input
        answer = raw_input('  > ')

        # validate the input
        if len(answer) < 1 and gameOver:
            # nothing received but the game is over
            console.addLine('The game is over. Reset the game to play again.')
            continue

        if len(answer) < 1 and not gameOver:
            # nothing received
            console.addLine('Select an option.')
            continue

        elif len(answer) == 1:
            # possible menu option
            command = str(answer).lower()
            if command == 'q':
                gameRunning = False
                continue
            elif command == 'r':
                board = emptyBoard()
                if not gameOver:
                    console.addLine('You flip over the table!')
                else:
                    console.addLine('Game board was reset.')
                    gameOver = False
                console.addLine('Your turn!')
                continue
            else:
                console.addLine('There is no "%s" option.' % command)
                continue

        elif len(answer) == 2 and gameOver:
            # square selection but the game is over
            console.addLine('The game is over. Reset the game to play again.')
            continue

        elif len(answer) == 2 and not gameOver:
            # possible square selection

            # extract the row and the column
            if   isNumber(answer[0]): column, row = list(answer)
            elif isNumber(answer[1]): row, column = list(answer)
            else:
                console.addLine('Not sure where the "%s" square is.' % answer)
                continue

            # validate the row
            row = str(row).lower()
            if row not in ['a', 'b', 'c']:
                console.addLine('There is no "%s" row. Try again.' % row)
                continue

            # validate the column
            column = int(column)
            if column not in [1, 2, 3]:
                console.addLine('There is no "%d" column. Try again.' % column)
                continue

            # select the square
            coordinates = (letterToIndex(row), column-1)
            if not chooseSquare(board, 'X', coordinates):
                continue

        elif len(answer) > 2:
            # definitely invalid
            console.addLine('That does not resemble a known command.')
            continue

    else:
        if not gameOver:
            selection = aiSelectSquare(board)
            if selection:
                if not chooseSquare(board, 'O', selection):
                    continue

    # game over?
    winner = isGameOver(board)
    #console.addLine('[Winner:%s]' % str(winner))
    if winner and not gameOver:
        gameOver = True
        if winner == 'X':
            console.addLine('%s wins! Congratulations!' % winner)
        elif winner == 'O':
            console.addLine('%s wins. Better luck next time.' % winner)
        else:
            console.addLine('Nobody wins! Surprise!')

    if not gameOver:
        # next person's turn!
        if yourTurn:
            console.addLine('Computer\'s turn.')
            yourTurn = False
        else:
            console.addLine('Your turn!')
            yourTurn = True
    else:
        yourTurn = True
