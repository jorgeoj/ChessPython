import random

pieceScore = {"K": 0, "Q": 10, "R": 5, "B": 3, "N": 3, "p": 1}

# Evaluacion de puntuacion para los caballos (mejor que no se vayan a las columnas 1 o 8) y otras piezas
knightScore = [[1, 1, 1, 1, 1, 1, 1, 1],
               [1, 2, 2, 2, 2, 2, 2, 1],
               [1, 2, 3, 3, 3, 3, 2, 1],
               [1, 2, 3, 4, 4, 3, 2, 1],
               [1, 2, 3, 4, 4, 3, 2, 1],
               [1, 2, 3, 3, 3, 3, 2, 1],
               [1, 2, 2, 2, 2, 2, 2, 1],
               [1, 1, 1, 1, 1, 1, 1, 1]]

# Buscamos las diagonales con los alfiles
bishopScores = [[4, 3, 2, 1, 1, 2, 3, 4],
               [3, 4, 3, 2, 2, 3, 4, 3],
               [2, 3, 4, 3, 3, 4, 3, 2],
               [1, 2, 3, 4, 4, 3, 2, 1],
               [1, 2, 3, 4, 4, 3, 2, 1],
               [2, 3, 4, 3, 3, 4, 3, 2],
               [3, 4, 3, 2, 2, 3, 4, 3],
               [4, 3, 2, 1, 1, 2, 3, 4]]

# Cuanto mas por el centro la reina mejor
queenScores = [[1, 1, 1, 3, 1, 1, 1, 1],
               [1, 2, 3, 3, 3, 1, 1, 1],
               [1, 4, 3, 3, 3, 4, 2, 1],
               [1, 2, 3, 3, 3, 2, 2, 1],
               [1, 2, 3, 3, 3, 2, 2, 1],
               [1, 4, 3, 3, 3, 4, 2, 1],
               [1, 1, 2, 3, 3, 1, 1, 1],
               [1, 1, 1, 3, 1, 1, 1, 1]]

# TODO revisar esta porque se mueve demasiado la torre
rookScores = [[6, 3, 4, 4, 4, 4, 3, 6],
               [1, 4, 4, 4, 4, 4, 4, 1],
               [1, 1, 2, 3, 3, 2, 1, 1],
               [1, 2, 3, 4, 4, 3, 2, 1],
               [1, 2, 3, 4, 4, 3, 2, 1],
               [1, 1, 2, 3, 3, 2, 1, 1],
               [1, 4, 4, 4, 4, 4, 4, 1],
               [6, 3, 4, 4, 4, 4, 3, 6]]

whitePawnScores = [[8, 8, 8, 8, 8, 8, 8, 8],
               [8, 8, 8, 8, 8, 8, 8, 8],
               [5, 6, 6, 7, 7, 6, 6, 5],
               [2, 3, 3, 5, 5, 3, 3, 2],
               [1, 2, 3, 4, 4, 3, 2, 1],
               [1, 1, 2, 3, 3, 2, 1, 1],
               [0, 1, 1, 0, 0, 1, 1, 0],
               [0, 0, 0, 0, 0, 0, 0, 0]]

blackPawnScores = [[0, 0, 0, 0, 0, 0, 0, 0],
               [0, 1, 1, 0, 0, 1, 1, 0],
               [1, 1, 2, 3, 3, 2, 1, 1],
               [1, 2, 3, 4, 4, 3, 2, 1],
               [1, 3, 3, 5, 5, 3, 3, 1],
               [5, 6, 6, 7, 7, 6, 6, 5],
               [8, 8, 8, 8, 8, 8, 8, 8],
               [8, 8, 8, 8, 8, 8, 8, 8]]


piecePositionScores = {"N": knightScore, "Q": queenScores, "B": bishopScores, "R": rookScores, "bp": blackPawnScores,
                       "wp": whitePawnScores}


CHECKMATE = 1000
STALEMATE = 0
DEPTH = 2 # Movimientos a futuro a calcular


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
    opponentMinMaxScore = CHECKMATE
    bestPlayerMove = None
    random.shuffle(validMoves)

    for playerMove in validMoves:
        gs.makeMove(playerMove)
        opponentsMoves = gs.getValidMoves()
        if gs.stalemate:
            opponentMaxScore = STALEMATE
        elif gs.checkmate:
            opponentMaxScore = -CHECKMATE
        else:
            opponentMaxScore = -CHECKMATE
            for opponentsMoves in opponentsMoves:
                gs.makeMove(opponentsMoves)
                gs.getValidMoves()
                if gs.checkmate:
                    score = CHECKMATE
                elif gs.stalemate:
                    score = STALEMATE
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
    global nextMove, counter
    nextMove = None
    random.shuffle(validMoves)
    counter = 0 # Para ver la diferencia de movimientos calculados entre un metodo y otro
    # findMoveMinMax(gs, validMoves, DEPTH, gs.whiteToMove)
    #findMoveNegaMax(gs, validMoves, DEPTH, 1 if gs.whiteToMove else -1)
    findMoveNegaMaxAlphaBeta(gs, validMoves, DEPTH, -CHECKMATE, CHECKMATE, 1 if gs.whiteToMove else -1)
    print(counter)

    return nextMove

'''
def findMoveMinMax(gs, validMoves, depth, whiteToMove):
    global nextMove
    if depth == 0:
        return scoreMaterial(gs.board)

    if whiteToMove:
        maxScore = -CHECKMATE
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score = findMoveMinMax(gs, nextMoves, depth - 1, False)
            if score > maxScore:
                maxScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
        return maxScore

    else:
        minScore = CHECKMATE
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score = findMoveMinMax(gs, nextMoves, depth - 1, True)
            if score < minScore:
                minScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
        return minScore
'''


def findMoveNegaMax(gs, validMoves, depth, turnMultiplier):
    global nextMove, counter
    counter += 1
    if depth == 0:
        return turnMultiplier * scoreBoard(gs)

    maxScore = -CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMax(gs, nextMoves, depth - 1, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        gs.undoMove()
    return maxScore



def findMoveNegaMaxAlphaBeta(gs, validMoves, depth, alpha, beta, turnMultiplier):
    global nextMove, counter
    counter += 1
    if depth == 0:
        return turnMultiplier * scoreBoard(gs)

    # Ordenar movimientos - IMPLEMENTAR MAS ADELANTE
    maxScore = -CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMaxAlphaBeta(gs, nextMoves, depth - 1, -beta, -alpha, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
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
            return -CHECKMATE # Las negras ganan
        else:
            return CHECKMATE # Las blancas ganan
    elif gs.stalemate:
        return STALEMATE

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






