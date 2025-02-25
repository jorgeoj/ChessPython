"""
Este es nuestro archivo principal. Será responsable de manejar la entrada del usuario y mostrar el objeto gameState actual.
"""

import pygame as p # Importa la biblioteca pygame
from Chess import ChessEngine, SmartMoveFinder # Importa el módulo ChessEngine desde el paquete Chess

import easygui

BOARD_WIDTH = BOARD_HEIGHT = 512 # Define el ancho y alto de la ventana del juego
MOVE_LOG_PANEL_WIDTH = 450
MOVE_LOG_PANEL_HEIGHT = BOARD_HEIGHT
DIMENSION = 8 # Define las dimensiones del tablero de ajedrez (8x8)
SQ_SIZE = BOARD_HEIGHT // DIMENSION # Calcula el tamaño de cada cuadrado del tablero
MAX_FPS = 15 # Establece el máximo de fps para animaciones más adelante
IMAGES = {} # Diccionario global para almacenar las imágenes de las piezas del ajedrez

'''
El main de nuestro código. Se encargará de la entrada del usuario y de actualizar los gráficos.
'''
def main():
    p.init() # Inicializa Pygame
    screen = p.display.set_mode((BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH, BOARD_HEIGHT)) # Crea la ventana del juego
    clock = p.time.Clock() # Objeto para controlar el tiempo del juego
    screen.fill(p.Color("white"))
    moveLogFont = p.font.SysFont("Arial", 16, False, False)  # Nombre fuente, tamaño, negrita, italica
    gs = ChessEngine.GameState() # Crea un objeto GameState para representar el estado del juego
    validMoves = gs.getValidMoves() # Generamos los movimientos validos y los guardamos en una lista
    moveMade = False # Variable flag para cuando un movimiento es hecho
    animate = False # Flag para cuando haya que animar un movimiento
    loadPiecesImages() # Carga las imágenes de las piezas
    running = True
    sqSelected = () # Vble para saber el cuadrado seleccionado, inicialmente no hay ninguna (tuple)
    playerClicks = [] # Constancia de los clicks del jugador para mover las piezas (2 tuples)
    gameOver = False
    selectPlayer()

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
                    # Si el jugador pulsa 2 veces la misma casilla, se deselecciona la casilla o si se hizo clic en el log
                    if sqSelected == (row, col) or col >= 8:
                        sqSelected = ()
                        playerClicks = [] # Limpiar clicks de jugador
                    else:
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected)
                    # Si el jugador ha hecho click dos veces hacemos que se mueva la pieza
                    if len(playerClicks) == 2:
                        move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
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
                if undoMoveEnabled:
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
                    selectPlayer()

        # Movimientos IA
        if not gameOver and not humanTurn:
            AIMove = SmartMoveFinder.findBestMove(gs, validMoves)
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

        drawGameState(screen, gs, validMoves, sqSelected, moveLogFont) # Dibuja el estado actual del juego en la pantalla

        if gs.checkmate or gs.stalemate:
            gameOver = True
            drawEndGameText(screen, 'Ahogamiento (R para reiniciar)' if gs.stalemate else
            'Negras ganan por mate (R para reiniciar)' if gs.whiteToMove else 'Blancas ganan por mate (R para reiniciar)')

        clock.tick(MAX_FPS) # Controla la velocidad de actualización de la pantalla
        p.display.flip() # Actualiza la pantalla

'''
Inicializa un diccionario global de imágenes. Esto se llamará exactamente una vez en el main.
'''
def loadPiecesImages():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for piece in pieces:
        # Carga las imágenes de las piezas y las escala al tamaño del cuadrado del tablero
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))

'''
Responsable de los valores de decidir como se jugará
'''
def selectPlayer():
    global playerOne, playerTwo, undoMoveEnabled

    # Mensaje y título principal
    msg = "¿Quieres jugar contra la máquina o con alguien?"
    title = "Selección de Jugadores"
    choices = ["Contra la máquina", "Con alguien"]
    # Elección del tipo de jugador
    choice = easygui.buttonbox(msg = msg, title = title, choices = choices)

    # Condiciones según la elección
    if choice == "Contra la máquina":
        msg = "¿Qué color quieres jugar?"
        title = "Selección de Color"
        choices = ["Blancas", "Negras"]
        choiceAI = easygui.buttonbox(msg = msg, title = title, choices = choices)
        # Asignar valores según el color elegido
        if choiceAI == "Blancas":
            playerOne = True
            playerTwo = False
        elif choiceAI == "Negras":
            playerOne = False
            playerTwo = True

        undoMoveEnabled = False # Variable para permitir deshacer movimiento o no
    elif choice == "Con alguien":
        playerOne = True
        playerTwo = True
        undoMoveEnabled = True

'''
Responsable de todos los gráficos dentro del estado actual del juego.
'''
def drawGameState(screen, gs, validMoves, sqSelected, moveLogFont):
    drawBoard(screen) # Esto dibuja los cuadrados en el tablero
    highlightSquares(screen, gs, validMoves, sqSelected)
    drawPieces(screen, gs.board) # Esto dibuja las piezas encima de los cuadrados del tablero
    drawMoveLog(screen, gs, moveLogFont)

'''
Dibujar los cuadrados en el tablero. OJO: El cuadrado de arriba a la izquierda del tablero siempre es blanco
'''
def drawBoard(screen):
    global colors
    # colors = [p.Color("white"), p.Color("gray")] Colores del tablero (blanco y gris) para posible cambio color tablero
    colors = [p.Color("#dfc07f"), p.Color("#7a4f37")] # Colores del tablero (marron y clarito)

    # El primer for recorre filas, el segundo recorre columnas. Dibuja cada casilla del tablero
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c) % 2)] # Alterna los colores de los cuadrados para simular un tablero de ajedrez
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

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
Dibujar las piezas en el tablero usando el GameState.board actual
'''
def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c] # Obtiene la pieza en la posición (r, c) del tablero
            if piece != "--": # Nos aseguramos que no sea un cuadrado vacio, para dibujar la pieza
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

'''
Dibujar el log de los movimientos
'''
def drawMoveLog(screen, gs, font):
    moveLogRect = p.Rect(BOARD_WIDTH, 0, MOVE_LOG_PANEL_WIDTH, MOVE_LOG_PANEL_HEIGHT)
    p.draw.rect(screen, p.Color("black"), moveLogRect)
    moveLog = gs.moveLog
    moveTexts = []
    for i in range(0, len(moveLog), 2):
        moveString = str(i//2 + 1) + ". " + str(moveLog[i]) + " "
        if i + 1 < len(moveLog): # Para asegurarse que las negras también han movido
            moveString += str(moveLog[i+1])
        moveTexts.append(moveString)

    movesPerRow = 5
    padding = 5
    lineSpacing = 2
    textY = padding

    for i in range(0, len(moveTexts), movesPerRow):
        text = ""
        for j in range(movesPerRow):
            if i + j < len(moveTexts):
                text += moveTexts[i+j]+ "  "
        textObject = font.render(text, True, p.Color('green')) # Color de las letras de log (probar white tambien)
        textLocation = moveLogRect.move(padding, textY)
        screen.blit(textObject, textLocation)
        textY += textObject.get_height() + lineSpacing

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
        r, c = (move.startRow + dR * frame/frameCount, move.startCol + dC * frame/frameCount)
        drawBoard(screen)
        drawPieces(screen, board)
        # Borrar la pieza movida de su casilla final
        color = colors[(move.endRow + move.endCol) % 2]
        endSquare = p.Rect(move.endCol * SQ_SIZE, move.endRow * SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen, color, endSquare)
        # Dibujar la pieza capturada en el rectangulo
        if move.pieceCaptured != '--':
            if move.isEnpassantMove:
                enPassantRow = move.endRow + 1 if move.pieceCaptured[0] == 'b' else move.endRow - 1
                endSquare = p.Rect(move.endCol * SQ_SIZE, enPassantRow * SQ_SIZE, SQ_SIZE, SQ_SIZE)
            screen.blit(IMAGES[move.pieceCaptured], endSquare)
        # Dibujar la pieza moviendose
        screen.blit(IMAGES[move.pieceMoved], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        clock.tick(60)

def drawEndGameText(screen, text):
    font = p.font.SysFont("Arial", 30, True, False) # Nombre fuente, tamaño, negrita, italica
    textObject = font.render(text, 0, p.Color('Black'))
    textLocation = p.Rect(0, 0, BOARD_WIDTH, BOARD_HEIGHT).move(BOARD_WIDTH / 2 - textObject.get_width() / 2,
                                                                BOARD_HEIGHT / 2 - textObject.get_height() / 2)
    screen.blit(textObject, textLocation)
    textObject = font.render(text, 0, p.Color('Yellow'))
    screen.blit(textObject, textLocation.move(2, 2))

# Ejecuta la función main si este archivo es el programa principal
if __name__ == "__main__":
    main()
