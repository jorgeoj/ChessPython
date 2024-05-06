"""
Este es nuestro archivo principal. Será responsable de manejar la entrada del usuario y mostrar el objeto gameState actual.
"""

import pygame as p # Importa la biblioteca pygame
from Chess import ChessEngine, SmartMoveFinder # Importa el módulo ChessEngine desde el paquete Chess

WIDTH = HEIGHT = 512 # Define el ancho y alto de la ventana del juego
DIMENSION = 8 # Define las dimensiones del tablero de ajedrez (8x8)
SQ_SIZE = HEIGHT // DIMENSION # Calcula el tamaño de cada cuadrado del tablero
MAX_FPS = 15 # Establece el máximo de fps para animaciones más adelante
IMAGES = {} # Diccionario global para almacenar las imágenes de las piezas del ajedrez

'''
Inicializa un diccionario global de imágenes. Esto se llamará exactamente una vez en el main.
'''
def loadImages():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for piece in pieces:
        # Carga las imágenes de las piezas y las escala al tamaño del cuadrado del tablero
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))
    # OJO:Podemos acceder a imagenes también poniendo: IMAGES['wp'] (wp como ejemplo de cada pieza)

'''
El main de nuestro código. Se encargará de la entrada del usuario y de actualizar los gráficos.
'''
def main():
    p.init() # Inicializa Pygame
    screen = p.display.set_mode((WIDTH, HEIGHT)) # Crea la ventana del juego
    clock = p.time.Clock() # Objeto para controlar el tiempo del juego
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState() # Crea un objeto GameState para representar el estado del juego
    validMoves = gs.getValidMoves() # Generamos los movimientos validos y los guardamos en una lista
    moveMade = False # Variable flag para cuando un movimiento es hecho
    animate = False # Flag para cuando haya que animar un movimiento
    loadImages() # Carga las imágenes de las piezas
    running = True
    sqSelected = () # Vble para saber el cuadrado seleccionado, inicialmente no hay ninguna (tuple)
    playerClicks = [] # Constancia de los clicks del jugador para mover las piezas (2 tuples)
    gameOver = False

    playerOne = True # Si el jugador juega blancas será verdadero si lo hace la IA será falso
    playerTwo = False # Lo mismo de arriba pero con las negras

    while running:
        humanTurn = (gs.whiteToMove and playerOne) or (not gs.whiteToMove and playerTwo)
        for e in p.event.get():
            # Si el usuario cierra la ventana, detiene el bucle principal
            if e.type == p.QUIT:
                running = False
            # Al pulsar el raton
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver and humanTurn:
                    location = p.mouse.get_pos() # Localizacion en ejes x e y del raton
                    col = location[0]//SQ_SIZE
                    row = location[1]//SQ_SIZE
                    # Si el jugador pulsa 2 veces la misma casilla, se deselecciona la casilla
                    if sqSelected == (col, row):
                        sqSelected = ()
                        playerClicks = [] # Limpiar clicks de jugador
                    else:
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected)
                    # Si el jugador ha hecho click dos veces hacemos que se mueva la pieza
                    if len(playerClicks) == 2:
                        move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                        print(move.getChessNotation())
                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                gs.makeMove(validMoves[i])
                                moveMade = True
                                animate = True
                                # Reseteamos los clicks del jugador y lo seleccionado
                                sqSelected = ()
                                playerClicks = []
                        if not moveMade:
                            # Si nos equivocamos de pieza al hacer click y le damos a la que queremos mover en el segundo
                            # se guarda el click para que haga el movimiento la segunda pieza clicada
                            playerClicks = [sqSelected]
            # Al pulsar una tecla
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: # Deshacer movimiento con tecla "z" (se puede cambiar)
                    gs.undoMove()
                    moveMade = True
                    animate = False
                    gameOver = False
                if e.key == p.K_r: # Resetear el tablero cuando se pulsa la letra "r"
                    gs = ChessEngine.GameState()
                    validMoves = gs.getValidMoves()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = False
                    animate = False
                    gameOver = False

        # Movimientos IA
        if not gameOver and not humanTurn:
            AIMove = SmartMoveFinder.findBestMoveMinMax(gs, validMoves)
            if AIMove is None:
                AIMove = SmartMoveFinder.findRandomMove(validMoves)
            gs.makeMove(AIMove)
            moveMade = True
            animate = True

        if moveMade:
            if animate:
                animateMove(gs.moveLog[-1], screen, gs.board, clock)
            validMoves = gs.getValidMoves()
            moveMade = False
            animate = False

        drawGameState(screen, gs, validMoves, sqSelected) # Dibuja el estado actual del juego en la pantalla

        if gs.checkmate:
            gameOver = True
            if gs.whiteToMove:
                drawText(screen, 'Black wins by checkmate (R to restart)')
            else:
                drawText(screen, 'White wins by checkmate (R to restart)')
        elif gs.stalemate:
            gameOver = True
            drawText(screen, 'Stalemate (R for restart)')

        clock.tick(MAX_FPS) # Controla la velocidad de actualización de la pantalla
        p.display.flip() # Actualiza la pantalla

'''
Resaltar la casilla seleccionada y los movimientos posibles de la pieza seleccionada
'''
def highlightSquares(screen, gs, validMoves, sqSelected):
    if sqSelected != ():
        r, c = sqSelected
        if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'): # Casilla seleccionada es una pieza que se puede mover
            # Resaltar la casilla seleccionada
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100) # Valor de transparencia (0 transparente, 255 opaco)
            s.fill(p.Color('blue'))
            screen.blit(s, (c*SQ_SIZE, r*SQ_SIZE))
            # Resaltar movimientos de esa casilla
            s.fill(p.Color('yellow'))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (move.endCol*SQ_SIZE, move.endRow*SQ_SIZE))


'''
Responsable de todos los gráficos dentro del estado actual del juego.
'''
def drawGameState(screen, gs, validMoves, sqSelected):
    drawBoard(screen) # Esto dibuja los cuadrados en el tablero
    highlightSquares(screen, gs, validMoves, sqSelected)
    drawPieces(screen, gs.board) # Esto dibuja las piezas encima de los cuadrados del tablero


'''
Dibujar los cuadrados en el tablero. OJO: El cuadrado de arriba a la izquierda del tablero siempre es blanco
'''
def drawBoard(screen):
    global colors
    colors = [p.Color("white"), p.Color("gray")] # Colores del tablero (se pueden cambiar mas adelante)
    # El primer for recorre filas, el segundo recorre columnas. Dibuja cada cuadrado del tablero
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c) % 2)] # Alterna los colores de los cuadrados para simular un tablero de ajedrez
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


'''
Dibujar las piezas en el tablero usando el GameState.board actual
'''
def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c] # Obtiene la pieza en la posición (r, c) del tablero
            if piece != "--": # Nos aseguramos que no sea un cuadrado vacio, para dibujar la pieza
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

'''
Animar los movimientos
'''
def animateMove(move, screen, board, clock):
    global colors
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framesPerSquare = 10 # Frames para mover una casilla
    frameCount = (abs(dR) + abs(dC)) * framesPerSquare
    for frame in range(frameCount + 1):
        r, c = (move.startRow + dR*frame/frameCount, move.startCol + dC*frame/frameCount)
        drawBoard(screen)
        drawPieces(screen, board)
        # Borrar la pieza movida de su casilla final
        color = colors[(move.endRow + move.endCol) % 2]
        endSquare = p.Rect(move.endCol*SQ_SIZE, move.endRow*SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen, color, endSquare)
        # Dibujar la pieza capturada en el rectangulo
        if move.pieceCaptured != '--':
            screen.blit(IMAGES[move.pieceCaptured], endSquare)
        # Dibujar la pieza moviendose
        screen.blit(IMAGES[move.pieceMoved], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        clock.tick(60)

def drawText(screen, text):
    font = p.font.SysFont("Arial", 30, True, False) # Nombre fuente, tamaño, negrita, italica
    textObject = font.render(text, 0, p.Color('Black'))
    textLocation = p.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH/2 -textObject.get_width()/2, HEIGHT/2 - textObject.get_height()/2)
    screen.blit(textObject, textLocation)
    textObject = font.render(text, 0, p.Color('Yellow'))
    screen.blit(textObject, textLocation.move(2, 2))

if __name__ == "__main__":
    main() # Ejecuta la función main si este archivo es el programa principal


# NOTA:Para mate rapido, mover: peon alfil blanco rey 1, peon rey negro 2, peon caballo blanco rey 2 y reina negra por la diagonal

