"""
Esta clase es responsable de calcular los mejores movimientos que pueda hacer la IA (Inteligencia artificial) para
jugar en contra del usuario
"""

import random

pieceScore = {"K": 0, "Q": 10, "R": 5, "B": 3, "N": 3, "p": 1}

# Evaluacion de puntuacion para los caballos (mejor que no se vayan a las columnas 1 o 8) y otras piezas
knightPositionScores = [[1, 1, 1, 1, 1, 1, 1, 1],
                        [1, 2, 2, 2, 2, 2, 2, 1],
                        [1000, 2, 3, 3, 3, 3, 2, 1000],
                        [-1, 2, 3, 4, 4, 3, 2, -1],
                        [-1, 2, 3, 4, 4, 3, 2, -1],
                        [-1, 2, 3, 3, 3, 3, 2, -1],
                        [1, 2, 2, 2, 2, 2, 2, 1],
                        [1, 1, 1, 1, 1, 1, 1, 1]]

# Buscamos las diagonales con los alfiles
bishopPositionScores = [[4, 3, 2, 1, 1, 2, 3, 4],
                        [3, 4, 3, 2, 2, 3, 4, 3],
                        [2, 3, 4, 3, 3, 4, 3, 2],
                        [1, 2, 3, 4, 4, 3, 2, 1],
                        [1, 2, 3, 4, 4, 3, 2, 1],
                        [2, 3, 4, 3, 3, 4, 3, 2],
                        [3, 4, 3, 2, 2, 3, 4, 3],
                        [4, 3, 2, 1, 1, 2, 3, 4]]

# Cuanto mas por el centro la reina mejor
queenPositionScores = [[1, 1, 1, 3, 1, 1, 1, 1],
                       [1, 2, 3, 3, 3, 1, 1, 1],
                       [1, 4, 3, 3, 3, 4, 2, 1],
                       [1, 2, 3, 3, 3, 2, 2, 1],
                       [1, 2, 3, 3, 3, 2, 2, 1],
                       [1, 4, 3, 3, 3, 4, 2, 1],
                       [1, 1, 2, 3, 3, 1, 1, 1],
                       [1, 1, 1, 3, 1, 1, 1, 1]]

rookPositionScores = [[6, 2, 4, 4, 4, 4, 2, 6],
                      [1, 4, 4, 4, 4, 4, 4, 1],
                      [1, 1, 2, 3, 3, 2, 1, 1],
                      [1, 2, 3, 4, 4, 3, 2, 1],
                      [1, 2, 3, 4, 4, 3, 2, 1],
                      [1, 1, 2, 3, 3, 2, 1, 1],
                      [1, 4, 4, 4, 4, 4, 4, 1],
                      [6, 2, 4, 4, 4, 4, 2, 6]]

whitePawnPositionScores = [[8, 8, 8, 8, 8, 8, 8, 8],
                           [8, 8, 8, 8, 8, 8, 8, 8],
                           [5, 6, 6, 7, 7, 6, 6, 5],
                           [2, 3, 3, 5, 5, 3, 3, 2],
                           [1, 2, 3, 4, 4, 3, 2, 1],
                           [1, 1, 2, 3, 3, 2, 1, 1],
                           [0, 1, 1, 0, 0, 1, 1, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0]]

blackPawnPositionScores = [[0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 1, 1, 0, 0, 1, 1, 0],
                           [1, 1, 2, 3, 3, 2, 1, 1],
                           [1, 2, 3, 4, 4, 3, 2, 1],
                           [1, 3, 3, 5, 5, 3, 3, 1],
                           [5, 6, 6, 7, 7, 6, 6, 5],
                           [8, 8, 8, 8, 8, 8, 8, 8],
                           [8, 8, 8, 8, 8, 8, 8, 8]]


piecePositionScores = {"N": knightPositionScores, "Q": queenPositionScores, "B": bishopPositionScores, "R": rookPositionScores, "bp": blackPawnPositionScores,
                       "wp": whitePawnPositionScores}

CHECKMATE_POINTS = 1000
STALEMATE_POINTS = 0
MOVEMENT_DEPTH = 2 # Movimientos a futuro a calcular

'''
Coge un movimiento aleatorio de la lista y lo devuelve
'''
def findRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves)-1)]

'''
Encuentra el mejor movimiento min max sin recursion
'''
def findBestMoveMinMaxNoRecursion(gs, validMoves):
    turnMultiplier = 1 if gs.whiteToMove else -1
    opponentMinMaxScore = CHECKMATE_POINTS
    bestPlayerMove = None
    random.shuffle(validMoves)

    for playerMove in validMoves:
        gs.makeMove(playerMove)
        opponentsMoves = gs.getValidMoves()
        if gs.stalemate:
            opponentMaxScore = STALEMATE_POINTS
        elif gs.checkmate:
            opponentMaxScore = -CHECKMATE_POINTS
        else:
            opponentMaxScore = -CHECKMATE_POINTS
            for opponentsMoves in opponentsMoves:
                gs.makeMove(opponentsMoves)
                gs.getValidMoves()
                if gs.checkmate:
                    score = CHECKMATE_POINTS
                elif gs.stalemate:
                    score = STALEMATE_POINTS
                else:
                    score = -turnMultiplier * scoreMaterial(gs.board)
                if score > opponentMaxScore:
                    opponentMaxScore = score
                gs.undoMove()
        if opponentMaxScore < opponentMinMaxScore:
            opponentMinMaxScore = opponentMaxScore
            bestPlayerMove = playerMove
        gs.undoMove()
    return bestPlayerMove

'''
Función de ayuda para hacer la primera llamada recursiva
'''
def findBestMove(gs, validMoves):
    global nextMove
    nextMove = None
    random.shuffle(validMoves)
    findMoveNegaMaxAlphaBeta(gs, validMoves, MOVEMENT_DEPTH, -CHECKMATE_POINTS, CHECKMATE_POINTS, 1 if gs.whiteToMove else -1)
    return nextMove

def findMoveNegaMaxAlphaBeta(gs, validMoves, depth, alpha, beta, turnMultiplier):
    global nextMove
    if depth == 0:
        return turnMultiplier * scoreBoard(gs)

    # Ordenar movimientos - IMPLEMENTAR MAS ADELANTE
    maxScore = -CHECKMATE_POINTS
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMaxAlphaBeta(gs, nextMoves, depth - 1, -beta, -alpha, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == MOVEMENT_DEPTH:
                nextMove = move
        gs.undoMove()
        # Aqui se elimina de manera selectiva las ramas
        if maxScore > alpha:
            alpha = maxScore
        if alpha >= beta:
            break
    return maxScore

'''
Puntuacion positiva buena para blancas, puntuación negativa buena para negras
'''
def scoreBoard(gs):
    if gs.checkmate:
        if gs.whiteToMove:
            return -CHECKMATE_POINTS # Las negras ganan
        else:
            return CHECKMATE_POINTS # Las blancas ganan
    elif gs.stalemate:
        return STALEMATE_POINTS

    score = 0
    for row in range(len(gs.board)):
        for col in range(len(gs.board[row])):
            square = gs.board[row][col]
            if square != "--":
                piecePositionScore = 0
                # Puntuarlo por posiciones
                if square[1] != "K": # Si no es un rey (ya que no se ha implementado puntuacion por el)
                    if square[1] == "p": # para peones
                        piecePositionScore = piecePositionScores[square][row][col]
                    else: # para el resto de piezas
                        piecePositionScore = piecePositionScores[square[1]][row][col]

                if square[0] == 'w':
                    score += pieceScore[square[1]] + piecePositionScore * .1 # Multiplicarlo por .1 para que siga teniendo en cuenta las otras casillas
                elif square[0] == 'b':
                    score -= pieceScore[square[1]] - piecePositionScore * .1

    return score

'''
Puntuar el tablero segun las piezas
'''
def scoreMaterial(board):
    score = 0
    for row in board:
        for square in row:
            if square[0] == 'w':
                score += pieceScore[square[1]]
            elif square[0] == 'b':
                score -= pieceScore[square[1]]

    return score
