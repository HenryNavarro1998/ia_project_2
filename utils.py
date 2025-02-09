"""
Módulo de utilidades para el juego de damas. Contiene funciones para:
- Inicializar el tablero
- Manipular movimientos
- Verificar estado del juego
- Generar movimientos válidos
"""

BOARD_SIZE = 4  # Tamaño del tablero (4x4)

def init_board():
    """
    Inicializa el tablero de juego con la configuración inicial.
    
    Returns:
        list: Matriz 4x4 con las piezas en sus posiciones iniciales:
              - 'o' (jugador inferior) en (0,1) y (0,3)
              - 'x' (jugador superior) en (3,0) y (3,2)
              - None en las demás posiciones
    """
    board = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    # Configuración inicial de las piezas
    board[0][1] = "o"  # Pieza normal del jugador 'o' (abajo)
    board[0][3] = "o"
    board[3][0] = "x"  # Pieza normal del jugador 'x' (arriba)
    board[3][2] = "x"
    return board

def print_board(board):
    """
    Imprime el tablero en consola con formato legible.
    
    Args:
        board (list): Matriz 4x4 que representa el estado actual del juego
    """
    print("\n#################################################\n")
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            # Representación visual: '-' para casillas vacías
            print(board[i][j] if board[i][j] else "-", end="\t")
        print("\n")
    print("\n#################################################\n")

def handle_move(board, move):
    """
    Ejecuta un movimiento válido en el tablero y retorna el nuevo estado.
    
    Args:
        board (list): Estado actual del tablero
        move (tuple): Tupla con posiciones ((fila_origen, columna_origen), (fila_destino, columna_destino))
    
    Returns:
        list: Nuevo estado del tablero después del movimiento
    """
    new_board = [row.copy() for row in board]  # Copia profunda del tablero
    
    from_pos, to_pos = move
    from_x, from_y = from_pos
    to_x, to_y = to_pos

    # Validación de movimiento (no implementada completamente)
    if move not in generate_moves(board, board[from_x][from_y].lower()):
        return board  # Devuelve el tablero original si el movimiento es inválido

    # Ejecutar movimiento
    new_board[to_x][to_y] = new_board[from_x][from_y]
    new_board[from_x][from_y] = None

    # Manejar capturas (movimientos de 2 casillas)
    if abs(from_x - to_x) == 2:
        mid_x = (from_x + to_x) // 2
        mid_y = (from_y + to_y) // 2
        new_board[mid_x][mid_y] = None  # Eliminar pieza capturadas

    # Coronación de reyes (Nota: Condición podría necesitar ajustes)
    if new_board[to_x][to_y] in ["o", "x"]:  # Solo para piezas normales
        # 'o' se corona en la última fila (3), 'x' en la primera (0)
        if (new_board[to_x][to_y] == "o" and to_x == 3) or \
           (new_board[to_x][to_y] == "x" and to_x == 0):
            new_board[to_x][to_y] = new_board[to_x][to_y].upper()  # Convertir a mayúscula para reyes

    return new_board

def is_game_over(board):
    """
    Determina si el juego ha terminado y verifica al ganador.
    
    Args:
        board (list): Estado actual del tablero
    
    Returns:
        tuple: (juego_terminado (bool), ganador (str/o None))
    """
    red_count = sum(row.count("o") + row.count("O") for row in board)  # Conteo de piezas rojas
    blue_count = sum(row.count("x") + row.count("X") for row in board)  # Conteo de piezas azules
    winner = None

    # Condiciones de victoria
    if red_count == 0 or not generate_moves(board, "o"):
        winner = "x"  # Jugador azul gana
    elif blue_count == 0 or not generate_moves(board, "x"):
        winner = "o"  # Jugador rojo gana

    # Juego termina si algún jugador pierde todas sus piezas o no tiene movimientos
    game_over = (
        red_count == 0
        or blue_count == 0
        or not generate_moves(board, "x")
        or not generate_moves(board, "o")
    )
    
    return (game_over, winner)

def generate_moves(board, player):
    """
    Genera todos los movimientos válidos para un jugador en el estado actual.
    
    Args:
        board (list): Estado actual del tablero
        player (str): 'o' o 'x' indicando el jugador actual
    
    Returns:
        list: Lista de movimientos válidos en formato ((from_x, from_y), (to_x, to_y))
    """
    MOVES = [(-1, -1), (-1, 1), (1, -1), (1, 1)]  # Direcciones posibles
    valid_moves = []

    def in_bounds(x, y):
        """Verifica si las coordenadas están dentro del tablero"""
        return 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE

    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            piece = board[i][j]
            if piece and piece.lower() == player:
                # Determinar direcciones permitidas según tipo de pieza
                directions = MOVES
                if piece.islower():  # Piezas normales
                    directions = [(1, -1), (1, 1)] if player == "o" else [(-1, -1), (-1, 1)]

                for dx, dy in directions:
                    # Movimiento simple
                    to_x, to_y = i + dx, j + dy
                    if in_bounds(to_x, to_y) and not board[to_x][to_y]:
                        valid_moves.append(((i, j), (to_x, to_y)))

                    # Movimiento de captura
                    capture_x, capture_y = i + 2*dx, j + 2*dy
                    mid_x, mid_y = i + dx, j + dy
                    if (in_bounds(capture_x, capture_y) and 
                        not board[capture_x][capture_y] and 
                        board[mid_x][mid_y] and 
                        board[mid_x][mid_y].lower() != player):
                        valid_moves.append(((i, j), (capture_x, capture_y)))

    return valid_moves