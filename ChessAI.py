import random
pieceScore = {"K": 0, "Q": 9, "R": 5, "N": 3, "B":3, "p":1}
CHECKMATE = 1000
STALEMATE = 0

def findRandomMove(validMoves):
    return validMoves[random.randint(0,len(validMoves) - 1)]

def findBestMove(gs, validMoves):
    turnMultiplier = 1 if gs.whiteToMove else -1

    maxScore = -CHECKMATE
    for playerMove in validMoves:
        gs.makeMove(playerMove)

        if gs.checkmate:
            score = CHECKMATE
        elif gs.stalemate:
            score = STALEMATE
        else:
            score = scoreMaterial(gs.board)*turnMultiplier
        if score >  maxScore:
            maxScore= score
            bestMove = playerMove
        gs.undoMove()
        print(score)
    return bestMove


def scoreMaterial(board):
    score = 0
    for row in board:
        for square in row:
            if square[0] == 'w':
                score += pieceScore[square[1]]
            elif square[0] == 'b':
                score -= pieceScore[square[1]]
    return score