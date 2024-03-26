"""
Esta clase es responsable de almacenar toda la información sobre el estado actual de una partida de ajedrez. También
será responsable de determinar los movimientos válidos en el estado actual y llevar un registro de los movimientos.
"""
class GameState():
    def __init__(self):
        # Tablero de 8x8 (lista 2D), cada elemento de la lista tiene 2 caracteres.
        # El primer caracter representa el color de la pieza (b para negro y w para blanco), el segundo caracter
        # representa el tipo de pieza (R para torre, N para caballo, B para alfil, Q para reina y K para rey)
        # los caracteres "--" representan  un espacio vacío sin una pieza
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        # Variable para saber a quien le toca jugar (True si le toca a las blancas, False si le toca a las negras)
        self.whiteToMove = True
        # Lista para mantener un registro de los movimientos realizados durante la partida
        self.moveLog = []

    """
    Coge un movimiento como parametro y lo ejecuta (No funciona para enrocar, en-passant y promoción)
    """
    def makeMove(self, move):
        # Actualiza el tablero con el movimiento realizado
        self.board[move.startRow][move.startCol] = "--" # La casilla de origen se convierte en vacía
        self.board[move.endRow][move.endCol] = move.pieceMoved # La pieza se mueve a la casilla de destino
        self.moveLog.append(move) # Registra el movimiento por si queremos deshacerlo luego
        self.whiteToMove = not self.whiteToMove # Cambiar el turno de jugador

    """
    Deshacer el ultimo movimiento hecho
    """
    def undoMove(self):
        if len(self.moveLog) != 0: # Asegurarse que hay un movimiento para deshacer
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not  self.whiteToMove # Cambiar turno

    """
    Todos los movimientos considerando jaque
    """
    def getValidMoves(self):
        return self.getAllPossibleMoves() # Mas adelante se cambiará (ahora no nos preocupamos de los jaques)

    """
    Todos los movimientos sin considerar jaques
    """
    def getAllPossibleMoves(self):
        moves = [Move((6,4),(4,4), self.board)] # Por ahora no hay movs validos esto se cambiara
        for r in range(len(self.board)): # Numero de filas
            for c in range(len(self.board[r])): # Numero de columnas en la fila dada
                turn = self.board[r][c][0]
                if(turn == 'w' and self.whiteToMove) and (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    # Segun la pieza que sea llamaremos a la funcion de los movimientos de la pieza (Aun hay que poner el resto)
                    if piece == 'p':
                        self.getPawnMoves(r, c, moves)
                    elif piece == 'R':
                        self.getRookMoves(r, c, moves)
        return moves

    """
    Obtener todos los movimientos del peon en la fila y columna y añadir los movimientos a la lista "moves"
    """
    def getPawnMoves(self, r, c, moves):
        pass

    """
    Obtener todos los movimientos de la torre en la fila y columna y añadir los movimientos a la lista "moves"
    """
    def getRookMoves(self, r, c, moves):
        pass

class Move():
    # Mapea claves a valores Clave : Valor
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                   "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3,
                   "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board):
        # Inicializa los atributos del movimiento
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol] # Pieza movida
        self.pieceCaptured = board[self.endRow][self.endCol] # Pieza capturada
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol
        print(self.moveID)

    """
    Override metodo equals
    """
    def __eq__(self, other):
        if isinstance(other, Move):
            return  self.moveID == other.moveID
        return False



    def getChessNotation(self):
        # Devuelve la notación de ajedrez del movimiento (por ejemplo, "e2e4" para un movimiento de peón)
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        # Convierte la posición de la fila y columna en notación de ajedrez (por ejemplo, "e4" para la casilla (3,4))
        return self.colsToFiles[c] + self.rowsToRanks[r]












