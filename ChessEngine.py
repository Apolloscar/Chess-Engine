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
        self.whiteToMove = True
        self.moveLog = []

    # not work for casteling el passant and pawn promotion
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove
    
    def undoMove(self):
        if len(self.moveLog) == 0:
            return
        move = self.moveLog.pop()
        self.board[move.startRow][move.startCol] = move.pieceMoved
        self.board[move.endRow][move.endCol] = move.pieceCaptured
        self.whiteToMove = not self.whiteToMove
    
    def getValidMoves(self):
        pass

    def getAllPossibleMoves(self):
        pass
        





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

    def getChessNotation(self):
        return self.getRankFile(self.startRow,self.startCol) + self.getRankFile(self.endRow,self.endCol)

    def getRankFile(self, row, col):
        return self.colsToFiles[col] + self.rowsToRanks[row]