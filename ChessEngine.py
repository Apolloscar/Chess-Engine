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

    # not work for casteling el passant and pawn promotion
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove

        if move.pieceMoved == "wK":
            self.whiteKingLocation = (move.endRow, move.endCol)
        if move.pieceMoved == "bK":
            self.blackKingLocation = (move.endRow, move.endCol)
    
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
    
    def getValidMoves(self):
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
                    validSquares[(checkRow, checkCol)]
                else:
                    for i in range(1,8):
                        validSquare = (kingRow + check[2]*i, kingCol + check[3]*i)
                        validSquares.append(validSquare)
                        if validSquare[0] == checkRow and validSquare[1] == checkCol:
                            break
                for i in range(len(moves) - 1, -1,-1):
                    if moves[i].pieceMoved[1] != 'K':
                        if not (moves[i].endRow, moves[i].endCol) in validSquares:
                            moves.remove(moves.remove(moves[i]))
            else:
                self.getKingMoves(kingRow,kingCol,moves)

        else:
            moves = self.getAllPossibleMoves() 
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
                piecePinned == True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
        
        if self.whiteToMove:
            if self.board[r-1][c] == "--":
                if not piecePinned or pinDirection == (-1,0):
                    moves.append(Move((r,c), (r-1,c), self.board))
                    if r == 6 and self.board[r-2][c] == "--":
                        moves.append(Move((r,c), (r-2,c), self.board))

            if c-1 >= 0 and  self.board[r-1][c-1][0] == "b" and (not piecePinned or pinDirection(-1,-1)):

                moves.append(Move((r,c), (r-1,c-1), self.board))
            if c+1 < len(self.board[r]) and  self.board[r-1][c+1][0] == "b" and (not piecePinned or pinDirection(-1,1)):
                moves.append(Move((r,c), (r-1,c+1), self.board))

        else:
            if self.board[r+1][c] == "--":
                if not piecePinned or pinDirection == (1,0):
                    if not piecePinned or pinDirection == (1,0):
                        moves.append(Move((r,c), (r+1,c), self.board))
                        if r == 1 and self.board[r+2][c] == "--":
                            moves.append(Move((r,c), (r+2,c), self.board))

            if c-1 >= 0 and  self.board[r+1][c-1][0] == "w" and (not piecePinned or pinDirection == (1,-1)):
                moves.append(Move((r,c), (r+1,c-1), self.board))
            if c+1 < len(self.board[r]) and  self.board[r+1][c+1][0] == "w" and (not piecePinned or pinDirection == (1,1)):
                moves.append(Move((r,c), (r+1,c+1), self.board))

    def getRookMoves(self, r, c, moves):
        current = r + 1
        while current < len(self.board) and self.board[current][c] == "--":
            moves.append(Move((r,c), (current,c), self.board))
            current += 1
        if current < len(self.board) and (self.whiteToMove == (self.board[current][c][0] == 'b')):
            moves.append(Move((r,c), (current,c), self.board))
        
        current = r -1
        while current >= 0 and self.board[current][c] == "--":
            moves.append(Move((r,c), (current,c), self.board))
            current -= 1
        if current >= 0 and (self.whiteToMove == (self.board[current][c][0] == 'b')):
            moves.append(Move((r,c), (current,c), self.board))
        
        current = c + 1
        while current < len(self.board) and self.board[r][current] == "--":
            moves.append(Move((r,c), (r,current), self.board))
            current += 1
        if current < len(self.board) and (self.whiteToMove == (self.board[r][current][0] == 'b')):
            moves.append(Move((r,c), (r,current), self.board))
        
        current = c -1
        while current >= 0 and self.board[r][current] == "--":
            moves.append(Move((r,c), (r,current), self.board))
            current -= 1
        if current >= 0 and (self.whiteToMove == (self.board[r][current][0] == 'b')):
            moves.append(Move((r,c), (r,current), self.board))

    def getKnightMoves(self, r, c, moves):
        knightMoves = ((2,1), (2,-1), (-2,1), (-2,-1), (1,2), (1,-2), (-1,2), (-1,-2))

        for rm,cm in knightMoves:
            rd = r+rm
            cd = c + cm
            if 0<= rd < len(self.board) and 0<= cd < len(self.board) and (self.board[rd][cd] == "--" or (self.whiteToMove == (self.board[rd][cd][0] == 'b'))):
                moves.append(Move((r,c), (rd,cd), self.board))
        
    def getBishopMoves(self, r, c, moves):
        bishopMoves = ((1,1), (1,-1), (-1,1), (-1,-1))

        for rm, cm in bishopMoves:
            rd = r+rm
            cd = c + cm
            while 0<= rd < len(self.board) and 0<= cd < len(self.board) and self.board[rd][cd] == "--":
                moves.append(Move((r,c), (rd,cd), self.board))
                rd += rm
                cd +=  cm
            if 0<= rd < len(self.board) and 0<= cd < len(self.board) and (self.whiteToMove == (self.board[rd][cd][0] == 'b')):
                moves.append(Move((r,c), (rd,cd), self.board))

    def getQueenMoves(self, r, c, moves):
        self.moveFunctions['B'](r,c,moves)
        self.moveFunctions['R'](r,c,moves)
    def getKingMoves(self, r, c, moves):
        kingMoves = ((1,1), (1,-1), (-1,1), (-1,-1), (1,0), (-1,0), (0, 1), (0,-1))
        for rm,cm in kingMoves:
            rd = r+rm
            cd = c + cm
            if 0<= rd < len(self.board) and 0<= cd < len(self.board) and (self.board[rd][cd] == "--" or (self.whiteToMove == (self.board[rd][cd][0] == 'b'))):
                moves.append(Move((r,c), (rd,cd), self.board))
    

        





class Move():
    ranksToRows = {"1":7, "2":6, "3":5, "4":4, "5": 3, "6": 2, "7": 1, "8":0}
    rowsToRanks = { v: k for k,v in ranksToRows.items()}

    filesToCols = {"a":0, "b":1, "c":2, "d": 3, "e":4, "f":5, "g": 6,"h":7}
    colsToFiles = { v: k for k,v in filesToCols.items()}

    def __init__(self, startSq,endSq, board) -> None:
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow*1000 + self.startCol*100 +self.endRow*10 +self.endCol

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getChessNotation(self):
        return self.getRankFile(self.startRow,self.startCol) + self.getRankFile(self.endRow,self.endCol)

    def getRankFile(self, row, col):
        return self.colsToFiles[col] + self.rowsToRanks[row]