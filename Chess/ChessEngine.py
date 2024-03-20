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