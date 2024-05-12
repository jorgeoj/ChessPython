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
        # Diccionario para la funcion getAllPossibleMoves
        self.moveFunctions = {'p' : self.getPawnMoves, 'R' : self.getRookMoves, 'N' : self.getKnightMoves,
                              'B' : self.getBishopMoves, 'Q' : self.getQueenMoves, 'K' : self.getKingMoves}

        # Variable para saber a quien le toca jugar (True si le toca a las blancas, False si le toca a las negras)
        self.whiteToMove = True
        # Lista para mantener un registro de los movimientos realizados durante la partida
        self.moveLog = []
        # Vamos a guardar la posicion de los reyes para no permitir hacer movimientos que los pongan en jaque
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        # El rey no tiene movimientos validos y está en jaque
        self.checkmate = False
        # El rey no tiene movimientos validos pero no está en jaque
        self.stalemate = False
        self.enpassantPossible = () # Coordeandas para la casilla donde en passant es posible
        self.enPassantPossibleLog = [self.enpassantPossible]

        self.currentCastlingRight = CastleRights(True, True, True, True)
        self.castleRightsLog = [CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks,
                                             self.currentCastlingRight.wqs, self.currentCastlingRight.bqs)]

    """
    Coge un movimiento como parametro y lo ejecuta (No funciona para enrocar, en-passant y promoción)
    """
    def makeMove(self, move):
        # Actualiza el tablero con el movimiento realizado
        self.board[move.startRow][move.startCol] = "--" # La casilla de origen se convierte en vacía
        self.board[move.endRow][move.endCol] = move.pieceMoved # La pieza se mueve a la casilla de destino
        self.moveLog.append(move) # Registra el movimiento por si queremos deshacerlo luego
        self.whiteToMove = not self.whiteToMove # Cambiar el turno de jugador
        # Actualizamos la posicion del rey si se ha movido
        if move.pieceMoved == 'wK':
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == 'bK':
            self.blackKingLocation = (move.endRow, move.endCol)

        # Promocion de peones
        if move.isPawnPromotion:
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + 'Q' # Coge el color de la pieza y lo convierte en reina directamente

        # Enpassant
        if move.isEnpassantMove:
            self.board[move.startRow][move.endCol] = '--' # Capturar el peon

        # Actualizar variable enPassantPossible
        if move.pieceMoved[1] == 'p' and abs(move.startRow - move.endRow) == 2: # Solo avances de 2 casillas de peones
            self.enpassantPossible = ((move.startRow + move.endRow)//2, move.startCol)
        else:
            self.enpassantPossible = ()
        # Enroque
        if move.isCastleMove:
            if move.endCol - move.startCol == 2: # Enroque por lado del rey
                self.board[move.endRow][move.endCol-1] = self.board[move.endRow][move.endCol+1] # Mueve la torre
                self.board[move.endRow][move.endCol+1] = '--' # Borra la torre antigua
            else: # Enroque por lado de la reina
                self.board[move.endRow][move.endCol+1] = self.board[move.endRow][move.endCol-2]
                self.board[move.endRow][move.endCol-2] = '--'

        self.enPassantPossibleLog.append(self.enpassantPossible)

        # Actualizar posibilidad de enrocar (cuando es movimiento de rey o torre)
        self.updateCastleRights(move)
        self.castleRightsLog.append(CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks,
                                             self.currentCastlingRight.wqs, self.currentCastlingRight.bqs))

    """
    Deshacer el ultimo movimiento hecho
    """
    def undoMove(self):
        if len(self.moveLog) != 0: # Asegurarse que hay un movimiento para deshacer
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove # Cambiar turno
            # Actualizar la posicion del rey si fue la ultima pieza movida a la posicion anterior
            if move.pieceMoved == 'wK':
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == 'bK':
                self.blackKingLocation = (move.startRow, move.startCol)
            # Deshacer el en passant
            if move.isEnpassantMove:
                self.board[move.endRow][move.endCol] = '--' # Dejamos donde se quedo el peon vacio
                self.board[move.startRow][move.endCol] = move.pieceCaptured

            self.enPassantPossibleLog.pop()
            self.enpassantPossible = self.enPassantPossibleLog[-1]

            # Deshacer derecho a enrocar
            self.castleRightsLog.pop() # librarse de los nuevos derechos del movimiento que estamos deshaciendo
            newRights = self.castleRightsLog[-1]
            self.currentCastlingRight = CastleRights(newRights.wks, newRights.bks, newRights.wqs, newRights.bqs)

            # Deshacer el enroque
            if move.isCastleMove:
                if move.endCol - move.startCol == 2:  # Lado del rey
                    self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol - 1]
                    self.board[move.endRow][move.endCol - 1] = '--'
                else:  # Lado de la reina
                    self.board[move.endRow][move.endCol - 2] = self.board[move.endRow][move.endCol + 1]
                    self.board[move.endRow][move.endCol + 1] = '--'

            # Para asegurarse que al ir atrás no se quede el estado
            self.checkmate = False
            self.stalemate = False

    """
    Actualizar los derechos de poder enrocar
    """
    def updateCastleRights(self, move):
        if move.pieceMoved == 'wK':
            self.currentCastlingRight.wks = False
            self.currentCastlingRight.wqs = False
        elif move.pieceMoved == 'bK':
            self.currentCastlingRight.bks = False
            self.currentCastlingRight.bqs = False
        elif move.pieceMoved == 'wR':
            if move.startRow == 7:
                if move.startCol == 0: # Torre izquierda
                    self.currentCastlingRight.wqs = False
                elif move.startCol == 7: # Torre derecha
                    self.currentCastlingRight.wks = False
        elif move.pieceMoved == 'bR':
            if move.startRow == 0:
                if move.startCol == 0: # Torre izquierda
                    self.currentCastlingRight.bqs = False
                elif move.startCol == 7: # Torre derecha
                    self.currentCastlingRight.bks = False

        # Si se ha capturado una torre
        if move.pieceCaptured == 'wR':
            if move.endRow == 7:
                if move.endCol == 0:
                    self.currentCastlingRight.wqs = False
                elif move.endCol == 7:
                    self.currentCastlingRight.wks = False
        elif move.pieceCaptured == 'bR':
            if move.endRow == 0:
                if move.endCol == 0:
                    self.currentCastlingRight.bqs = False
                elif move.endCol == 7:
                    self.currentCastlingRight.bks = False

    """
    Todos los movimientos considerando jaque
    """
    def getValidMoves(self):
        tempEnpassantPossible = self.enpassantPossible
        tempCastleRights = CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks,
                                        self.currentCastlingRight.wqs, self.currentCastlingRight.bqs)
        # Generamos todos los movimientos posibles, para cada movimiento hacemos el movimiento, luego generamos todos
        # los movimientos del oponente y para cada uno de esos movimientos, miraremos si atacan al rey, si lo hacen
        # no será un movimiento valido
        moves = self.getAllPossibleMoves()
        if self.whiteToMove:
            self.getCastleMoves(self.whiteKingLocation[0], self.whiteKingLocation[1], moves)
        else:
            self.getCastleMoves(self.blackKingLocation[0], self.blackKingLocation[1], moves)

        for i in range(len(moves)-1, -1, -1): # Recorrer la lista del reves para que al borrar no de problemas
            self.makeMove(moves[i])
            self.whiteToMove = not self.whiteToMove
            if self.inCheck():
                moves.remove(moves[i]) # Quitamos el movimiento no valido
            self.whiteToMove = not self.whiteToMove
            self.undoMove()
        if len(moves) == 0: # Esto significa que es jaque o estancamiento (rey ahogado)
            if self.inCheck():
                self.checkmate = True
            else:
                self.stalemate = True
        else:
            self.checkmate = False
            self.stalemate = False

        self.enpassantPossible = tempEnpassantPossible
        self.currentCastlingRight = tempCastleRights
        return moves

    """
    Determina si el jugador está en jaque
    """
    def inCheck(self):
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])

    """
    Determinar si el enemigo puede atacar a la casilla r, c (row, column)
    """
    def squareUnderAttack(self, r, c):
        self.whiteToMove = not self.whiteToMove # Cambiamos al turno del oponente
        oppMoves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove  # Volvemos a cambiar el turno
        for move in oppMoves:
            # Si se cumple la casilla está siendo atacada
            if move.endRow == r and move.endCol == c:
                return True
        return False

    """
    Todos los movimientos sin considerar jaques
    """
    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)): # Numero de filas
            for c in range(len(self.board[r])): # Numero de columnas en la fila dada
                turn = self.board[r][c][0]
                if(turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    # Segun la pieza que sea seleccionada llamaremos a la funcion de los movimientos de la pieza
                    self.moveFunctions[piece](r, c, moves)
        return moves

    """
    Obtener todos los movimientos del peon en la fila y columna y añadir los movimientos a la lista "moves"
    """
    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove: # Movimiento de los peones blancos
            # El peon avanza una casilla
            if self.board[r-1][c] == "--":
                moves.append(Move((r,c), (r-1, c), self.board))
                # Para el movimiento de 2 casillas (si esta en la fila 6 es su posicion inicial)
                if r == 6 and self.board[r-2][c] == "--":
                    moves.append(Move((r,c), (r-2, c), self.board))
            # Controlar que no se salga del tablero al capturar a la izquierda
            if c-1 >= 0:
                if self.board[r-1][c-1][0] == 'b':
                    moves.append(Move((r, c), (r-1, c-1), self.board))
                elif (r-1, c-1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r - 1, c - 1), self.board, isEnpassantMove=True))
            # Para capturar a la derecha
            if c+1 <= 7:
                if self.board[r-1][c+1][0] == 'b': # indicamos que la pieza es de color contrario
                    moves.append(Move((r, c), (r-1, c+1), self.board))
                elif (r-1, c+1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r - 1, c + 1), self.board, isEnpassantMove=True))
        # Movimiento de los peones negros
        else:
            # El peon avanza una casilla
            if self.board[r+1][c] == "--":
                moves.append(Move((r,c), (r+1, c), self.board))
                # Para el movimiento de 2 casillas (si esta en la fila 1 es su posicion inicial)
                if r == 1 and self.board[r + 2][c] == "--":
                    moves.append(Move((r, c), (r+2, c), self.board))
            # Capturar piezas
            if c-1 >= 0: # capturar a la izquierda
                if self.board[r+1][c-1][0] == 'w':
                    moves.append(Move((r, c), (r+1, c-1), self.board))
                elif (r+1, c-1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r + 1, c - 1), self.board, isEnpassantMove=True))
            if c+1 <= 7: # capturar a la derecha
                if self.board[r+1][c+1][0] == 'w':
                    moves.append(Move((r, c), (r+1, c+1), self.board))
                elif (r+1, c+1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r + 1, c + 1), self.board, isEnpassantMove=True))


    """
    Obtener todos los movimientos de la torre en la fila y columna y añadir los movimientos a la lista "moves"
    """
    def getRookMoves(self, r, c, moves):
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1)) # direcciones: arriba, izquierda, abajo y derecha
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--": # Si la posicion final es un espacio vacio valido
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor: # Si acaba en una pieza enemiga
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else: # Movimiento invalido pieza mismo color
                        break
                else: # Se ha salido del tablero
                    break

    """
    Obtener todos los movimientos del caballo en la fila y columna y añadir los movimientos a la lista "moves"
    """

    def getKnightMoves(self, r, c, moves):
        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)) # Movimiento en L
        allyColor = "w" if self.whiteToMove else "b"
        for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor: # No una pieza aliada (vacia o enemigo)
                    moves.append(Move((r, c), (endRow, endCol), self.board))

    """
    Obtener todos los movimientos del alfil en la fila y columna y añadir los movimientos a la lista "moves"
    """

    def getBishopMoves(self, r, c, moves):
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1)) # Las 4 diagonales
        enemyColor = "b" if self.whiteToMove else "w" # Si el turno es de blancas el enemigo son las negras y viceversa
        for d in directions:
            for i in range(1, 8): # El alfil se puede mover 7 casillas (REVISAR POR SI ACASO)
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8: # Comprobamos que está dentro del tablero
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--": # Si la casilla final es un espacio vacio valido
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor: # Si la casilla final es una pieza del color contrario
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else: # Movimiento no valido por pieza del mismo color
                        break
                else: # Fuera del tablero
                    break

    """
    Obtener todos los movimientos de la reina en la fila y columna y añadir los movimientos a la lista "moves"
    """

    def getQueenMoves(self, r, c, moves):
        # Los movimientos de la reina son los de un alfil y una torre juntos
        self.getRookMoves(r, c, moves)
        self.getBishopMoves(r, c, moves)

    """
    Obtener todos los movimientos del rey en la fila y columna y añadir los movimientos a la lista "moves"
    """

    def getKingMoves(self, r, c, moves):
        kingMoves = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        colorAlly = "w" if self.whiteToMove else "b"
        for i in range(8):
            endRow = r + kingMoves[i][0]
            endCol = c + kingMoves[i][1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                # Si la pieza no es del mismo color (vacio o pieza enemiga)
                if endPiece[0] != colorAlly:
                    moves.append(Move((r, c), (endRow, endCol), self.board))

    """
    Generar todos los movimientos validos de enrocar para el rey y añadirlos a la lista de movimientos
    """
    def getCastleMoves(self, r, c, moves):
        if self.squareUnderAttack(r, c):
            return # No se puede enrocar si se esta en jaque
        if (self.whiteToMove and self.currentCastlingRight.wks) or (not self.whiteToMove and self.currentCastlingRight.bks):
            self.getKingsideCastleMoves(r, c, moves)
        if (self.whiteToMove and self.currentCastlingRight.wqs) or (not self.whiteToMove and self.currentCastlingRight.bqs):
            self.getQueensideCastleMoves(r, c, moves)


    def getKingsideCastleMoves(self, r, c, moves):
        if self.board[r][c+1] == '--' and self.board[r][c+2] == '--':
            if not self.squareUnderAttack(r, c+1) and not self.squareUnderAttack(r, c+2):
                moves.append(Move((r,c), (r, c+2), self.board, isCastleMove=True))

    def getQueensideCastleMoves(self, r, c, moves):
        if self.board[r][c-1] == '--' and self.board[r][c-2] == '--' and self.board[r][c-3] == '--':
            if not self.squareUnderAttack(r, c - 1) and not self.squareUnderAttack(r, c - 2):
                moves.append(Move((r, c), (r, c - 2), self.board, isCastleMove=True))

class CastleRights():
    #wks: white king side, bks: black king side, wqs: white queen side, bks: black queen side,
    def __init__(self, wks, bks, wqs, bqs):
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs


class Move():
    # Mapea claves a valores Clave : Valor
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                   "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3,
                   "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board, isEnpassantMove = False, isCastleMove = False):
        # Inicializa los atributos del movimiento
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol] # Pieza movida
        self.pieceCaptured = board[self.endRow][self.endCol] # Pieza capturada
        # Para la promocion del peon (en su metodo hay que repetir esto muchas veces)
        self.isPawnPromotion = (self.pieceMoved == 'wp' and self.endRow == 0) or (self.pieceMoved == 'bp' and self.endRow == 7)
        # Enrocar
        self.isCastleMove = isCastleMove
        # Para el en passant
        self.isEnpassantMove = isEnpassantMove
        if self.isEnpassantMove:
            self.pieceCaptured = 'wp' if self.pieceMoved == 'bp' else 'bp'

        self.isCapture = self.pieceCaptured != '--'

        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol
        # print(self.moveID)

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

    # Override de la funcion str()
    def __str__(self):
        # Movimiento enroque
        if self.isCastleMove:
            # "O-O"  Enroque por lado de rey
            # "O-O-O" Enroque por lado de reina
            return "O-O" if self.endCol == 6 else "O-O-O"

        endSquare = self.getRankFile(self.endRow, self.endCol)
        # Movimientos de peones
        if self.pieceMoved[1] == 'p':
            if self.isCapture:
                return self.colsToFiles[self.startCol] + "x" + endSquare
            else:
                return endSquare

            #TODO: Promocion, dos piezas del mismo tipo a una casilla, jaque, y # para mate

        moveString = self.pieceMoved[1]
        if self.isCapture:
            moveString += 'x'
        return moveString + endSquare
