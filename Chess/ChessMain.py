"""
Este es nuestro archivo principal. Será responsable de manejar la entrada del usuario y mostrar el objeto gameState actual.
"""

import pygame as p # Importa la biblioteca pygame
from Chess import ChessEngine # Importa el módulo ChessEngine desde el paquete Chess

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
    loadImages() # Carga las imágenes de las piezas
    running = True
    sqSelected = () # Vble para saber el cuadrado seleccionado, inicialmente no hay ninguna (tuple)
    playerClicks = [] # Constancia de los clicks del jugador para mover las piezas (2 tuples)
    while running:
        for e in p.event.get():
            # Si el usuario cierra la ventana, detiene el bucle principal
            if e.type == p.QUIT :
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos() # Localizacion en ejes x e y del raton
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                # Si el jugador pulsa 2 veces la misma casilla, se deselecciona la casilla
                if sqSelected == (col, row):
                    sqSelected = ()
                    playerClicks = []
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected)
                # Si el jugador ha hecho click dos veces hacemos que se mueva la pieza
                if len(playerClicks) == 2:
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    print(move.getChessNotation())
                    gs.makeMove(move)
                    # Reseteamos los clicks del jugador y lo seleccionado
                    sqSelected = ()
                    playerClicks = []

        drawGameState(screen, gs) # Dibuja el estado actual del juego en la pantalla
        clock.tick(MAX_FPS) # Controla la velocidad de actualización de la pantalla
        p.display.flip() # Actualiza la pantalla

'''
Responsable de todos los gráficos dentro del estado actual del juego.
'''
def drawGameState(screen, gs):
    drawBoard(screen) # Esto dibuja los cuadrados en el tablero
    drawPieces(screen, gs.board) # Esto dibuja las piezas encima de los cuadrados del tablero

'''
Dibujar los cuadrados en el tablero. OJO: El cuadrado de arriba a la izquierda del tablero siempre es blanco
'''
def drawBoard(screen):
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


if __name__ == "__main__":
    main() # Ejecuta la función main si este archivo es el programa principal




