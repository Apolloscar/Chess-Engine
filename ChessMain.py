## Handle user input and display current Game state

import pygame as p
import ChessEngine, ChessAI

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

    animate = False
    loadImages()
    running = True
    sqSelected = ()
    playerClicks = []
    gameOver = False
    playerOne = True
    playerTwo = False
    while running:
        humanTurn =(playerOne and gs.whiteToMove) or (playerTwo and not gs.whiteToMove)
        for q in p.event.get():
            if q.type == p.QUIT:
                running = False
            elif q.type == p.MOUSEBUTTONDOWN:
                if not gameOver and humanTurn:
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
                                animate = True
                                sqSelected = ()
                                playerClicks = []
                        if not moveMade:
                            playerClicks = [sqSelected]
            elif q.type == p.KEYDOWN:
                if q.key == p.K_z:
                    gs.undoMove()
                    humanTurn =(playerOne and gs.whiteToMove) or (playerTwo and not gs.whiteToMove)
                    while not humanTurn:
                        gs.undoMove()
                        humanTurn =(playerOne and gs.whiteToMove) or (playerTwo and not gs.whiteToMove)
                    moveMade = True
                    animate = False
                    gameOver = False
                    
                    
                if q.key == p.K_r:
                    gs = ChessEngine.GameState()
                    validMoves = gs.getValidMoves()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = False
                    animate = False
                    gameOver = False
                    humanTurn =(playerOne and gs.whiteToMove) or (playerTwo and not gs.whiteToMove)
        if not gameOver and not humanTurn:
            AIMove = ChessAI.findBestMoveMinMax(gs,validMoves)
            if not AIMove:
                AIMove =  ChessAI.findRandomMove(validMoves)
            gs.makeMove(AIMove)
            moveMade = True
            animate = True
        
                    
        if moveMade:
            if animate:
                animateMove(gs.moveLog[-1], screen,gs.board,clock)
                
            validMoves = gs.getValidMoves()
            moveMade = False
            animate = False
        
        drawGameState(screen, gs, validMoves, sqSelected)
        
        if gs.checkmate:
            gameOver = True
            if gs.whiteToMove:
                drawText(screen, "Black wins")
            else:
                drawText(screen, "White wins")
        elif gs.stalemate:
            gameOver = True
            drawText(screen, "Stalemate")
        clock.tick(MAX_FPS)
        p.display.flip()
        
def highlightSquares(screen, gs, validMoves, sqSelected):
    if sqSelected != ():
        r,c = sqSelected
        if gs.board[r][c][0]  == ('w' if gs.whiteToMove else 'b'):
            s = p.Surface((SQ_SIZE,SQ_SIZE))
            s.set_alpha(100)
            s.fill(p.Color("blue"))
            screen.blit(s,(c*SQ_SIZE, r*SQ_SIZE))
            s.fill(p.Color("yellow"))

            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (SQ_SIZE*move.endCol, SQ_SIZE*move.endRow))

def drawGameState(screen, gs, validMoves, sqSelected):
    drawBoard(screen)
    highlightSquares(screen, gs, validMoves, sqSelected)
    drawPieces(screen,gs.board)

def drawBoard(screen):
    # light color, dark color
    global colors
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

def animateMove(move,screen,board,clock):
    global colors
    #places pieces will move through
    coords = []
    dr = move.endRow - move.startRow
    dc = move.endCol - move.startCol
    framesPerSquare = 10
    frameCount = (abs(dr) + abs(dc)) * framesPerSquare

    for frame in range(frameCount+1):
        r, c = (move.startRow + dr*frame/frameCount, move.startCol + dc*frame/frameCount)
        drawBoard(screen)
        drawPieces(screen,board)

        color  = colors[(move.endRow + move.endCol) %2]
        endSquare = p.Rect(move.endCol*SQ_SIZE, move.endRow*SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen, color, endSquare)
        
        if move.pieceCaptured != "--" and not move.isEmpassantMove:
            
            screen.blit(IMAGES[move.pieceCaptured], endSquare)

        screen.blit(IMAGES[move.pieceMoved], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        clock.tick(60)

def drawText(screen,text):
    font = p.font.SysFont("Helvitca", 32, True, False)
    textObject = font.render(text,0, p.Color("Gray"))
    textLocation = p.Rect(0,0,WIDTH,HEIGHT).move(WIDTH/2 - textObject.get_width()/2, HEIGHT/2 - textObject.get_height()/2)
    screen.blit(textObject, textLocation)
    textObject = font.render(text, 0 , p.Color("Black"))
    screen.blit(textObject, textLocation.move(2,2))

if __name__ == "__main__":
    main()