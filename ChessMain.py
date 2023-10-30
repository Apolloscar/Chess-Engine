## Handle user input and display current Game state

import pygame as p
import ChessEngine

p.init()
WIDTH, HEIGHT = 512, 512
DIMENSION = 8
SQ_SIZE = HEIGHT//DIMENSION
MAX_FPS = 15
IMAGES = {}

def loadImages():
    pieces = ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR", "wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR", "wp", "bp"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/"+ piece + ".png"), (SQ_SIZE, SQ_SIZE))

def main():
    screen = p.display.set_mode((WIDTH,HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()

    validMoves = gs.getValidMoves
    moveMade = False

    loadImages()
    running = True
    sqSelected = ()
    playerClicks = []
    while running:
        for q in p.event.get():
            if q.type == p.QUIT:
                running = False
            elif q.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                if sqSelected == (row,col): 
                    sqSelected = ()
                    playerClicks = []
                else:
                    sqSelected = (row,col)
                    playerClicks.append(sqSelected)
                if len(playerClicks) == 2:
                    move = ChessEngine.Move(playerClicks[0],playerClicks[1], gs.board)
                    if move in validMoves:
                        gs.makeMove(move)
                        moveMade = True
                    sqSelected = ()
                    playerClicks = []
            elif q.type == p.KEYDOWN:
                if q.key == p.K_z:
                    gs.undoMove()
                    moveMade = True
        if moveMade:
            validMoves = gs.getValidMoves
            moveMade = False
        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()
        

def drawGameState(screen, gs):
    drawBoard(screen)
    drawPieces(screen,gs.board)

def drawBoard(screen):
    # light color, dark color
    colors = [(235,236,208), (119,149,86)]
    for i in range(DIMENSION):
        for j in range(DIMENSION):
            color = colors[((i+j) %2)]
            p.draw.rect(screen,color, p.Rect(int(j*SQ_SIZE),int(i*SQ_SIZE), SQ_SIZE,SQ_SIZE))


def drawPieces(screen, board):
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            piece = board[row][col]
            if piece != "--":
                screen.blit(IMAGES[piece],p.Rect(col*SQ_SIZE,row*SQ_SIZE,SQ_SIZE,SQ_SIZE))
if __name__ == "__main__":
    main()