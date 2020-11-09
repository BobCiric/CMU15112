#################################################
# hw7.py: Tetris!
#
# Your name: Jinghang Li
# Your andrew id: jinghanl
#
# Your partner's name: Zuhieb Abdi
# Your partner's andrew id: zabdi
#################################################

import cs112_f20_week7_linter
import math, copy, random
from cmu_112_graphics import *

#################################################
# Helper functions
#################################################

def almostEqual(d1, d2, epsilon=10**-7):
    # note: use math.isclose() outside 15-112 with Python version 3.5 or later
    return (abs(d2 - d1) < epsilon)

import decimal
def roundHalfUp(d):
    # Round to nearest with ties going away from zero.
    rounding = decimal.ROUND_HALF_UP
    # See other rounding options here:
    # https://docs.python.org/3/library/decimal.html#rounding-modes
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

#################################################
# Functions for you to write
#################################################

def gameDimensions():
    row = 15
    col = 10
    cellSize = 20
    margin = 25
    return (row, col, cellSize, margin)

def appStarted(app):
    app.score = 0
    app.timerDelay = 500
    app.board = []
    app.rows, app.cols, app.cellSize, app.margin = gameDimensions()
    for row in range(app.rows):
        app.board += [['blue'] * app.cols]
     # Seven "standard" pieces (tetrominoes)
    iPiece = [[  True,  True,  True,  True ]]

    jPiece = [
        [  True, False, False ],
        [  True,  True,  True ]
    ]

    lPiece = [
        [ False, False,  True ],
        [  True,  True,  True ]
    ]

    oPiece = [
        [  True,  True ],
        [  True,  True ]
    ]

    sPiece = [
        [ False,  True,  True ],
        [  True,  True, False ]
    ]

    tPiece = [
        [ False,  True, False ],
        [  True,  True,  True ]
    ]

    zPiece = [
        [  True,  True, False ],
        [ False,  True,  True ]
    ]
    app.tetrisPieceColors = ["red", "yellow", "magenta", 
                        "pink", "cyan", "green", "orange"]
    app.tetrisPieces = [iPiece, jPiece, lPiece, oPiece, sPiece, tPiece, zPiece]
    app.fallingPiece = newFallingPiece(app)
    app.move = True
    app.isGameOver = False
def getFallingPosition(app, piece):
    numFallingPieceCols = len(piece[0])
    y = 0
    x = app.cols//2 - numFallingPieceCols//2
    return x, y

def newFallingPiece(app):
    randomIndex = random.randint(0, len(app.tetrisPieces) - 1)
    app.fallingPiece = app.tetrisPieces[randomIndex]
    app.tetris = app.tetrisPieces[randomIndex]
    app.fallingColor = app.tetrisPieceColors[randomIndex]
    app.x, app.y = getFallingPosition(app, app.fallingPiece)

def drawFallingPiece(app, canvas):
    for i in range(len(app.tetris)):
        for j in range(len(app.tetris[0])):
            if app.tetris[i][j]:
                drawCell(app, canvas, i+app.y, j+app.x, app.fallingColor)

def moveFallingPiece(app, drow, dcol):
    app.x = app.x + dcol
    app.y = app.y + drow
    # if ((app.y >= app.cols-1) or (app.board[app.y][app.x] != 'blue')):
    #     return False

    if fallingPieceIsLegal(app) == False:
        app.x = app.x - dcol
        app.y = app.y - drow
        return False
    return True
        
def rotateFallingPiece(app):
    oldPiece = app.tetris
    oldPieceRow = len(app.tetris)
    oldPieceCol = len(app.tetris[0])
    newPieceRow = oldPieceCol
    newPieceCol = oldPieceRow
    newTetris = []
    for row in range(newPieceRow):
        newTetris += [[None] * newPieceCol]
#Rotation here
    for i in range(len(app.tetris)):
        for j in range(len(app.tetris[0])):
            newTetris[newPieceRow-1-j][i] = app.tetris[i][j]
    app.tetris = newTetris
    oldRow = app.y
    oldCol = app.x 
    
    oldCenterRow = app.y + len(oldPiece)//2 
    oldCenterCol = app.x + len(oldPiece[0])//2 
    newCenterRow = app.y + len(app.tetris)//2
    newCenterCol = app.x + len(app.tetris[0])//2

    newRow = app.y + len(oldPiece)//2 - len(app.tetris)//2 
    newCol = app.x + len(oldPiece[0])//2 - len(app.tetris[0])//2
    app.y = newRow
    app.x = newCol

    if fallingPieceIsLegal(app) == False:
        app.tetris = oldPiece
        app.y = oldRow
        app.x = oldCol

def fallingPieceIsLegal(app):
    for i in range(len(app.tetris)):
        for j in range(len(app.tetris[0])):
            if ((app.x < 0) or (app.x > app.cols- len(app.tetris[0])) or 
                (app.y > (app.rows - len(app.tetris))) or 
                (app.y < 0) or
                (app.board[i+app.y][j+app.x] != 'blue') and app.tetris[i][j]):
                return False

def placeFallingPiece(app):
    for i in range(len(app.tetris)):
        for j in range(len(app.tetris[0])):
            if app.tetris[i][j]:
                app.board[i+app.y][j+app.x] = app.fallingColor
    removeFullRows(app)

def removeFullRows(app):
    biBoard = []
    blueRow = ['blue'] * app.cols
    for row in range(app.rows):
        biBoard += [ [0] * app.cols]
    for i in range(len(app.board)):
        for j in range(len(app.board[0])):
            if app.board[i][j] != 'blue':
                biBoard[i][j] = 1
    fullRowNum = 0
    fullRowIndex = []
    for i in range(len(biBoard)):
        if sum(biBoard[i]) == app.cols:
            fullRowNum += 1 
            fullRowIndex.append(i)
            app.board.pop(i)
            app.board.insert(0, blueRow)
            app.score += 1

def timerFired(app):
    if app.isGameOver == False:
        if moveFallingPiece(app, 1, 0) == False:
            placeFallingPiece(app)
            newFallingPiece(app)
            if fallingPieceIsLegal(app) == False:
                app.isGameOver = True

def hardDrop(app):
    app.y = app.rows
    while fallingPieceIsLegal(app) == False:
        app.y = app.y - 1

def keyPressed(app, event):
    if app.isGameOver == False:
        if event.key == 'Down':
            moveFallingPiece(app, 1, 0)
        elif event.key == 'Left':
            moveFallingPiece(app, 0, -1)
        elif event.key == 'Right':
            moveFallingPiece(app, 0, 1)
        elif event.key == 'Up':
            rotateFallingPiece(app)
        elif event.key == 'Space':
            hardDrop(app)
    elif event.key =='r':
        if app.isGameOver:
            appStarted(app)

# cited from https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html
def getCellBounds(app, row, col):
    # aka "modelToView"
    # returns (x0, y0, x1, y1) corners/bounding box of given cell in grid
    x0 = app.margin + col * app.cellSize
    x1 = app.margin + (col+1) * app.cellSize
    y0 = app.margin + row * app.cellSize
    y1 = app.margin + (row+1) * app.cellSize
    return (x0, y0, x1, y1)

def drawBoard(app, canvas):
    for i in range(app.rows):
        for j in range(app.cols):
            drawCell(app, canvas, i, j, app.board[i][j])
            
def drawCanvas(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill = 'Orange')

def drawCell(app, canvas, row, col, color):
    (x0, y0, x1, y1) = getCellBounds(app, row, col)
    canvas.create_rectangle(x0, y0, x1, y1, fill = color,# app.board[row][col],
                                            width = 3)
def drawScore(app, canvas):
    canvas.create_text(app.width//2, app.margin-10, 
    text = f'Score = {app.score}', font = 'Arial 15 bold')
def drawGameOver(app,canvas):
    canvas.create_rectangle(0+app.margin,app.height/5,
    app.width-app.margin,app.height/5+50,
    fill = 'black')
    canvas.create_text(app.width//2, app.height/5 + 25, 
    text = 'Game Over', fill ='yellow', font = 'Arial 30')

def redrawAll(app, canvas):
    drawCanvas(app, canvas)
    drawBoard(app, canvas)
    drawFallingPiece(app, canvas)
    drawScore(app, canvas)
    if app.isGameOver:
        drawGameOver(app,canvas)

def playTetris():
    rows, cols, cellSize, margin = gameDimensions()
    width = cols * cellSize + 2 * margin
    height = rows * cellSize + 2 * margin
    runApp(width=width, height=height)
    #redrawAll(app, canvas)
    

#################################################
# main
#################################################

def main():
    cs112_f20_week7_linter.lint()
    playTetris()

if __name__ == '__main__':
    main()

