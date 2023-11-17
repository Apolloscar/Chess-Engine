import random
pieceScore = {"K": 0, "Q": 9, "R": 5, "N": 3, "B":3, "p":1}
CHECKMATE = 1000
STALEMATE = 0
DEPTH = 2

def findRandomMove(validMoves):
    return validMoves[random.randint(0,len(validMoves) - 1)]

def findBestMove(gs, validMoves):
    turnMultiplier = 1 if gs.whiteToMove else -1
    bestPlayerMove = None
    opponentMinMaxScore = CHECKMATE
    random.shuffle(validMoves)
    for playerMove in validMoves:
        gs.makeMove(playerMove)
        opponentsMoves = gs.getValidMoves()
        if gs.stalemate:
            opponentsMaxScore = STALEMATE
        elif gs.checkmate:
            opponentsMaxScore = -CHECKMATE
        else:
            opponentsMaxScore = -CHECKMATE
            for opponentsMove in opponentsMoves:
                gs.makeMove(opponentsMove)
                gs.getValidMoves()
                if gs.checkmate:
                    score = CHECKMATE 
                elif gs.stalemate:
                    score = STALEMATE
                else:
                    score = scoreMaterial(gs.board)*-turnMultiplier
                if score >  opponentsMaxScore:
                    opponentsMaxScore= score
                gs.undoMove()
        if opponentMinMaxScore > opponentsMaxScore:
            opponentMinMaxScore = opponentsMaxScore
            bestPlayerMove = playerMove
        gs.undoMove()
    return bestPlayerMove


def findBestMoveMinMax(gs, validMoves):
    global nextMove
    
    nextMove = None
    findMoveMinMax(gs,validMoves, DEPTH, gs.whiteToMove)
    return nextMove

def findMoveMinMax(gs, validMoves, depth, whiteToMove):
    global nextMove
    
    if depth ==  0:
        return scoreBoard(gs)
    
    if whiteToMove:
        maxScore = -CHECKMATE
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score = findMoveMinMax(gs,nextMoves, depth  - 1, False)
            if score > maxScore:
                maxScore = score
                if depth == DEPTH:
                    nextMove  = move
            gs.undoMove()
        
        return maxScore
    else:
        minScore = CHECKMATE
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score = findMoveMinMax(gs,nextMoves, depth  - 1, True)
            if score < minScore:
                minScore = score
                if depth == DEPTH:
                    nextMove  = move
            gs.undoMove()
        
        return minScore
    

def scoreMaterial(board):
    score = 0
    for row in board:
        for square in row:
            if square[0] == 'w':
                score += pieceScore[square[1]]
            elif square[0] == 'b':
                score -= pieceScore[square[1]]
    return score

def scoreBoard(gs):
    if gs.checkmate:
        if gs.whiteToMove:
            return -CHECKMATE
        else:
            return CHECKMATE
    elif gs.stalemate:
        return STALEMATE
    score = 0
    for row in gs.board:
        for square in row:
            if square[0] == 'w':
                score += pieceScore[square[1]]
            elif square[0] == 'b':
                score -= pieceScore[square[1]]
    return score