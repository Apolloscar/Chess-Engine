# Store information about current stae of game. Also dtermine valid moves of cuurent state and move log

class GameState():
    def __init__(self) -> None:
        
        # board is 8X8 with two characacters: 'b' or 'w' for color and K,Q,R,B,N,p for piec and "--" for blank
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp","bp","bp","bp","bp","bp","bp"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["wp", "wp","wp","wp","wp","wp","wp","wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        self.moveFunctions = {'p': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getKnightMoves, 'B': self.getBishopMoves, 'Q': self.getQueenMoves, 'K': self.getKingMoves}
        self.whiteToMove = True
        self.moveLog = []
        self.whiteKingLocation = (7,4)
        self.blackKingLocation = (0,4)

        self.inCheck = False
        self.pins = []
        self.checks = []

        self.checkmate = False
        self.stalemate = False

        self.enpassantPossible = ()

        self.currentCastlingRight = CastleRights(True, True, True, True)

        self.castleRightsLog = [CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks, self.currentCastlingRight.wqs, self.currentCastlingRight.bqs)]

    # not work for casteling el passant and pawn promotion
    def makeMove(self, move, promotion = 'Q'):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove

        if move.pieceMoved == "wK":
            self.whiteKingLocation = (move.endRow, move.endCol)
        if move.pieceMoved == "bK":
            self.blackKingLocation = (move.endRow, move.endCol)

        if move.isPromotion:
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + promotion

        if move.isEmpassantMove:
            self.board[move.startRow][move.endCol] = "--"
        
        if move.pieceMoved[1] == 'p' and abs(move.startRow - move.endRow) == 2:
            self.enpassantPossible = ((move.startRow +move.endRow)//2, move.startCol)
        else:
            self.enpassantPossible = ()

        #update castling rights - when king or rook moves for the first time
        if move.isCastleMove:
            if move.endCol - move.startCol == 2:
                self.board[move.endRow][move.endCol -1] = self.board[move.endRow][move.endCol +1]
                self.board[move.endRow][move.endCol +1] = "--"
            else:
                self.board[move.endRow][move.endCol +1] = self.board[move.endRow][move.endCol -2]
                self.board[move.endRow][move.endCol -2] = "--"

        self.updateCastleRights(move)
        self.castleRightsLog.append(CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks, self.currentCastlingRight.wqs, self.currentCastlingRight.bqs))
    
    def undoMove(self):
        if len(self.moveLog) == 0:
            return
        move = self.moveLog.pop()
        self.board[move.startRow][move.startCol] = move.pieceMoved
        self.board[move.endRow][move.endCol] = move.pieceCaptured
        self.whiteToMove = not self.whiteToMove

        if move.pieceMoved == "wK":
            self.whiteKingLocation = (move.startRow, move.startCol)
        if move.pieceMoved == "bK":
            self.blackKingLocation = (move.startRow, move.startCol)
        
        if move.isEmpassantMove:
            
            self.board[move.endRow][move.endCol] = "--"
            
            self.board[move.startRow][move.endCol] = move.pieceCaptured
            self.enpassantPossible = (move.endRow, move.endCol)
        if move.pieceMoved[1] == 'p' and abs(move.startRow - move.endRow) == 2:
            self.enpassantPossible = ()

        #undo castling rights
        self.castleRightsLog.pop()
        self.currentCastlingRight = self.castleRightsLog[-1]

        if move.isCastleMove:
            if move.endCol - move.startCol == 2:
                self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol - 1]
                self.board[move.endRow][move.endCol - 1] = "--"
            else:
                self.board[move.endRow][move.endCol - 2] = self.board[move.endRow][move.endCol +1]
                self.board[move.endRow][move.endCol + 1] = "--"
        self.stalemate = False
        self.checkmate = False
    #update castle rights
    def updateCastleRights(self, move):
        if move.pieceMoved == "wK":
            self.currentCastlingRight.wks = False
            self.currentCastlingRight.wqs = False
        elif move.pieceMoved == "bK":
            self.currentCastlingRight.bks = False
            self.currentCastlingRight.bqs = False
        elif move.pieceMoved == "wR":
            if move.startRow == 7:
                if move.startCol == 0:
                    self.currentCastlingRight.wqs = False
                elif move.startCol == 7:
                    self.currentCastlingRight.wks = False
        elif move.pieceMoved == "bR":
            if move.startRow == 0:
                if move.startCol == 0:
                    self.currentCastlingRight.bqs = False
                elif move.startCol == 7:
                    self.currentCastlingRight.bks = False


    
    def getValidMoves(self):
        tempEnpassantPossible = self.enpassantPossible
        tempCastlingPossible = CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks, self.currentCastlingRight.wqs, self.currentCastlingRight.bqs)
        moves = []
        self.inCheck, self.pins, self.checks = self.checkForPinsAndChecks()

        if self.whiteToMove:
            kingRow = self.whiteKingLocation[0]
            kingCol = self.whiteKingLocation[1]
        else:
            kingRow = self.blackKingLocation[0]
            kingCol = self.blackKingLocation[1]

        if self.inCheck:
            if len(self.checks) == 1:
                moves = self.getAllPossibleMoves()

                check = self.checks[0]
                checkRow = check[0]
                checkCol = check[1]

                pieceChecking = self.board[checkRow][checkCol]
                validSquares = []

                if pieceChecking[1] == 'N':
                
                    validSquares.append((checkRow, checkCol))
                else:
                    for i in range(1,8):
                        validSquare = (kingRow + check[2]*i, kingCol + check[3]*i)
                        validSquares.append(validSquare)
                        if validSquare[0] == checkRow and validSquare[1] == checkCol:
                            break
                for i in range(len(moves) - 1, -1,-1):
                    if moves[i].pieceMoved[1] != 'K':
                        if not (moves[i].endRow, moves[i].endCol) in validSquares:
                            moves.remove(moves[i])
            else:
                self.getKingMoves(kingRow,kingCol,moves)

        else:
            moves = self.getAllPossibleMoves() 
        self.enpassantPossible = tempEnpassantPossible
        self.currentCastlingRight = tempCastlingPossible

        if not moves:
            if self.inCheck:
                self.checkmate = True
            else:
                self.stalemate = True
        return moves


    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == "w" and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r,c,moves)
        return moves
    
    def checkForPinsAndChecks(self):
        pins = []
        checks = []
        inCheck = False
        if self.whiteToMove:
            enemy = 'b'
            ally = 'w'
            startRow = self.whiteKingLocation[0]
            startCol = self.whiteKingLocation[1]
        else:
            enemy = 'w'
            ally = 'b'
            startRow = self.blackKingLocation[0]
            startCol = self.blackKingLocation[1]
        directions = ((-1,0), (0,-1), (1,0), (0,1), (-1,-1), (-1,1), (1,-1), (1,1))

        for j in range(len(directions)):
            d = directions[j]
            possiblePin = ()
            for i in range(1,8):
                endRow = startRow + d[0]*i
                endCol = startCol + d[1]*i
                if 0 <= endRow < 8 and 0<=endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] == ally:
                        if possiblePin == ():
                            possiblePin = (endRow,endCol, d[0], d[1])
                        else:
                            break
                    elif endPiece[0] == enemy:
                        type = endPiece[1]

                        if ((0 <= j <= 3 and type == 'R')
                            or (4 <= j <=7 and type == 'B')
                            or (i == 1 and type == 'p' and ((enemy == 'w' and 6<=j<=7) or (enemy == 'b' and 4<=j<=5)))
                            or(type == 'Q') or (i== 1 and type == 'K')):

                            if possiblePin == ():
                                inCheck = True
                                checks.append((endRow,endCol, d[0], d[1]))
                            else:
                                pins.append(possiblePin)
                        
                        break
        knightMoves = ((-2,-1), (-2,1), (-1,-2), (-1,2), (1,-2), (1,2), (2,-1), (2,1))

        for m in knightMoves:
            endRow = startRow + m[0]
            endCol = startCol + m[1]
            if 0 <= endCol < 8 and 0 <= endRow < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] == enemy and  endPiece[1] == 'N':
                    inCheck = True
                    checks.append((endRow,endCol, m[0], m[1]))
        return inCheck, pins, checks


    def getPawnMoves(self, r, c, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins)-1,-1,-1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
        
        if self.whiteToMove:
            if self.board[r-1][c] == "--":
                if not piecePinned or pinDirection == (-1,0):
                    moves.append(Move((r,c), (r-1,c), self.board))
                    if r == 6 and self.board[r-2][c] == "--":
                        moves.append(Move((r,c), (r-2,c), self.board))

            if (not piecePinned or pinDirection ==(-1,-1)):
                if c-1 >= 0 and  self.board[r-1][c-1][0] == "b":
                    moves.append(Move((r,c), (r-1,c-1), self.board))
                elif (r-1, c-1) == self.enpassantPossible:
                    moves.append(Move((r,c), (r-1,c-1), self.board, isEmpassant= True))
                
                if c+1 < len(self.board[r]) and  self.board[r-1][c+1][0] == "b":
                    moves.append(Move((r,c), (r-1,c+1), self.board))
                elif (r-1, c+1) == self.enpassantPossible:
                    moves.append(Move((r,c), (r-1,c+1), self.board, isEmpassant=True))

        else:
            if self.board[r+1][c] == "--":
                if not piecePinned or pinDirection == (1,0):
                    moves.append(Move((r,c), (r+1,c), self.board))
                    if r == 1 and self.board[r+2][c] == "--":
                        moves.append(Move((r,c), (r+2,c), self.board))
                
            if (not piecePinned or pinDirection == (-1,-1)):
                if c-1 >= 0 and  self.board[r+1][c-1][0] == "w" :
                    moves.append(Move((r,c), (r+1,c-1), self.board))
                elif (r+1, c-1) == self.enpassantPossible:
                    moves.append(Move((r,c), (r+1,c-1), self.board, isEmpassant= True))
                
                if c+1 < len(self.board[r]) and  self.board[r+1][c+1][0] == "w":
                    moves.append(Move((r,c), (r+1,c+1), self.board))

                elif (r+1, c+1) == self.enpassantPossible:
                    moves.append(Move((r,c), (r+1,c+1), self.board, isEmpassant= True))

    def getRookMoves(self, r, c, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                if self.board[r][c][1] != 'Q':
                    self.pins.remove(self.pins[i])
                break
        directions = ((-1,0), (0,-1), (1,0), (0,1))
        enemy = 'b' if self.whiteToMove else 'w'
        for d in directions:
            for i in range(1,8):
                endRow = r + d[0]*i
                endCol = c + d[1]*i
                if 0<=endRow < 8 and 0<= endCol < 8:
                    if (not piecePinned or pinDirection == d or pinDirection == (-d[0], -d[1])):
                        endPiece = self.board[endRow][endCol]
                        if endPiece == "--":
                            moves.append(Move((r,c), (endRow,endCol), self.board))
                        elif endPiece[0] == enemy:
                            moves.append(Move((r,c), (endRow,endCol), self.board))
                            break
                        else:
                            break
                else:
                    break   

    def getKnightMoves(self, r, c, moves):
        piecePinned = False
        for i in range(len(self.pins)-1,-1,-1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                self.pins.remove(self.pins[i])
                break

        knightMoves = ((2,1), (2,-1), (-2,1), (-2,-1), (1,2), (1,-2), (-1,2), (-1,-2))
        ally = 'w' if self.whiteToMove else 'b'

        for rm,cm in knightMoves:
            rd = r+rm
            cd = c + cm
            if 0<= rd < len(self.board) and 0<= cd < len(self.board):
                if not piecePinned:
                    endPiece =  self.board[rd][cd]
                    if endPiece[0] != ally:
                        moves.append(Move((r,c), (rd,cd), self.board))
        
    def getBishopMoves(self, r, c, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins)-1,-1,-1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        bishopMoves = ((1,1), (1,-1), (-1,1), (-1,-1))
        enemy = 'b' if self.whiteToMove else 'w'

        for d in bishopMoves:
            for i in range(1,8):
                endRow = r + d[0]*i
                endCol = c + d[1]*i
                if 0<= endRow < 8 and 0 <= endCol < 8:
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0],-d[1]):
                        endPiece = self.board[endRow][endCol]
                        if endPiece == "--":
                            moves.append(Move((r,c),(endRow,endCol), self.board))
                        elif endPiece[0] == enemy:
                            moves.append(Move((r,c),(endRow,endCol), self.board))
                            break
                        else:
                            break
                else:
                    break

    def getQueenMoves(self, r, c, moves):
        self.moveFunctions['B'](r,c,moves)
        self.moveFunctions['R'](r,c,moves)
    def getKingMoves(self, r, c, moves):
        rowMoves = (-1,-1,-1,0,0,1,1,1)
        colMoves = (-1,0,1,-1,1,-1,0,1)
        ally = 'w' if self.whiteToMove else 'b'
        checkDirection = set()
        for checks in self.checks:
            checkDirection.add((checks[2],checks[3]))
        for i in range(8):
            endRow = r + rowMoves[i]
            endCol = c + colMoves[i]

            if 0<= endCol < 8 and 0 <= endRow < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != ally:
                    if ally == 'w':
                        self.whiteKingLocation = (endRow,endCol)
                    else:
                        self.blackKingLocation = (endRow,endCol)
                        
                        
                        
                    inCheck, pins, checks = self.checkForPinsAndChecks()
                    if not inCheck and (-(endRow - r), -(endCol - c)) not in checkDirection:
                        moves.append(Move((r,c), (endRow,endCol), self.board))
                    if ally == 'w':
                        self.whiteKingLocation = (r,c)
                    else:
                        self.blackKingLocation = (r,c)
                        
                        
        self.getCastleMoves(r,c,moves,ally)
    
    def getCastleMoves(self, r,c,moves, ally):
        if self.inCheck:
            return
        
        if (self.whiteToMove and self.currentCastlingRight.wks) or (not self.whiteToMove and self.currentCastlingRight.bks):
            self.getKingsideCastleMoves(r,c,moves,ally)

        if (self.whiteToMove and self.currentCastlingRight.wqs) or (not self.whiteToMove and self.currentCastlingRight.bqs):
            self.getQueensideCastleMoves(r,c,moves,ally)
            
    def getKingsideCastleMoves(self, r,c,moves,ally):
        if self.board[r][c+1] == "--" and self.board[r][c+2] == "--":
            if self.checkSquareForCastling(r,c+1,ally) and self.checkSquareForCastling(r,c+2,ally):
                moves.append(Move((r,c), (r,c+2), self.board, isCastle = True))

    def getQueensideCastleMoves(self, r,c,moves,ally):
        if self.board[r][c-1] == "--" and self.board[r][c-2] == "--"  and self.board[r][c-3] == "--":
            if self.checkSquareForCastling(r,c-1,ally) and self.checkSquareForCastling(r,c-2,ally):
                moves.append(Move((r,c), (r,c-2), self.board, isCastle = True))

    def checkSquareForCastling(self,r,c,ally) -> bool:
        

        if ally == 'w':
            if r-1 >=0 and c -1 >=0 and self.board[r-1][c-1] == "bp":
                return False
            if r-1 >=0 and c +1 <8 and self.board[r-1][c+1] == "bp":
                return False
        if ally == 'b':
            if r+1 < 8 and c -1 >=0 and self.board[r+1][c-1] == "wp":
                return False
            if r+1 < 8 and c +1 <8 and self.board[r+1][c+1] == "wp":
                return False
            
        
        
        attackDirections = ((1,1), (1,-1), (-1,1), (-1,-1), (1,0), (-1,0), (0,1), (0,-1))
        for directions in attackDirections:
            for i in range(1,8):
                endRow = r + directions[0]*i
                endCol = c + directions[1]*i
                
                if 0<= endRow < 8 and 0<= endCol < 8 and self.board[endRow][endCol] != "--":
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] != ally:
                        if ((i == 1 and endPiece[1] == 'K') or
                            (directions in attackDirections[0:4] and (endPiece[1] == 'B' or endPiece[1] == 'Q')) or
                            (directions in attackDirections[4:8] and (endPiece[1] == 'R' or endPiece[1] == 'Q'))):
                            return False
                    break
        knightMoves = ((-2,-1), (-2,1), (-1,-2), (-1,2), (1,-2), (1,2), (2,-1), (2,1))

        for directions in knightMoves:
            endRow = r + directions[0]
            endCol = c + directions[1]
            if 0<= endRow < 8 and 0<= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != ally and endPiece[1] == 'N':
                    return False
        return True



    
class CastleRights():
    def __init__(self,wks,bks,wqs,bqs) -> None:
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs

class Move():
    ranksToRows = {"1":7, "2":6, "3":5, "4":4, "5": 3, "6": 2, "7": 1, "8":0}
    rowsToRanks = { v: k for k,v in ranksToRows.items()}

    filesToCols = {"a":0, "b":1, "c":2, "d": 3, "e":4, "f":5, "g": 6,"h":7}
    colsToFiles = { v: k for k,v in filesToCols.items()}

    def __init__(self, startSq,endSq, board, isEmpassant = False, isCastle = False) -> None:
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol] 


        self.isPromotion = ((self.pieceMoved == "wp" and self.endRow == 0) or (self.pieceMoved == "bp" and self.endRow == 7))
        self.isEmpassantMove = isEmpassant

        if self.isEmpassantMove:
            self.pieceCaptured = "wp" if self.pieceMoved == "bp" else "bp"

        self.isCastleMove = isCastle
        self.moveID = self.startRow*1000 + self.startCol*100 +self.endRow*10 +self.endCol

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getChessNotation(self):
        return self.getRankFile(self.startRow,self.startCol) + self.getRankFile(self.endRow,self.endCol)

    def getRankFile(self, row, col):
        return self.colsToFiles[col] + self.rowsToRanks[row]