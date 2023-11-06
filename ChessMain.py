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
    pieces = ["bR", "bN", "bB", "bQ", "bK", "wR", "wN", "wB", "wQ", "wK", "wp", "bp"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/"+ piece + ".png"), (SQ_SIZE, SQ_SIZE))

def main():
    screen = p.display.set_mode((WIDTH,HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()

    validMoves = gs.getValidMoves()
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
                    for i in range(len(validMoves)):
                        if move == validMoves[i]:
                            newPiece = 'Q'
                            if move.isPromotion:
                                newPiece = drawPromotion(screen,gs)
                                if newPiece == "-":
                                    running = False
                                    break
    
                            gs.makeMove(validMoves[i], promotion=newPiece)
                            moveMade = True
                            sqSelected = ()
                            playerClicks = []
                    if not moveMade:
                        playerClicks = [sqSelected]
            elif q.type == p.KEYDOWN:
                if q.key == p.K_z:
                    gs.undoMove()
                    moveMade = True
        if moveMade:
            validMoves = gs.getValidMoves()
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

def drawPromotion(screen,gs) -> str:
    while True:
        p.draw.rect(screen,(255,31,31), p.Rect(int(SQ_SIZE*1.5),int(2.5*SQ_SIZE), 5*SQ_SIZE,2*SQ_SIZE))
        ally = ["wR", "wN", "wB", "wQ"] if gs.whiteToMove else ["bR", "bN", "bB", "bQ"]

        for i in range(len(ally)):
            screen.blit(IMAGES[ally[i]],p.Rect((2+i)*SQ_SIZE,3*SQ_SIZE,SQ_SIZE,SQ_SIZE))
        

        
        p.display.flip()
        
        for q in p.event.get():
            if q.type == p.QUIT:
                return "-"
            elif q.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE

                if (row,col) == (3,2):
                    return 'R'
                elif (row,col) == (3,3):
                    return 'N'
                elif (row,col) == (3,4):
                    return 'B'
                elif (row,col) == (3,5):
                    return 'Q'

        
    

if __name__ == "__main__":
    main()