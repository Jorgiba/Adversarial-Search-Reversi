from game import (
    TwoPlayerGameState,
)
from heuristic import (
    simple_evaluation_function,
)
from tournament import (
    StudentHeuristic,
)

# das valor a un estado completo que te mandan, no a una casilla en la que colocar ficha


def func_glob(n: int, state: TwoPlayerGameState) -> float:
    return n + simple_evaluation_function(state)


class Solution2(StudentHeuristic):
    def get_name(self) -> str:
        return "BuenaG"

    def evaluation_function(self, state: TwoPlayerGameState) -> float:
        c1 = 0
        c2 = 0

        # Comprobamos si el juego ya ha terminado
        if state.end_of_game:
            if state.is_player_max(state.player1):
                return 1000
            return -1000

        # Mapeados para early game, mid game y late game (tablero 8x8)
        early_game_map = [
            [20, -3, 11, 8, 8, 11, -3, 20],
            [-3, -7, -4, 1, 1, -4, -7, -3],
            [11, -4, 2, 2, 2, 2, -4, 11],
            [8, 1, 2, 0, 0, 2, 1, 8],
            [8, 1, 2, 0, 0, 2, 1, 8],
            [11, -4, 2, 2, 2, 2, -4, 11],
            [-3, -7, -4, 1, 1, -4, -7, -3],
            [20, -3, 11, 8, 8, 11, -3, 20],
        ]

        mid_game_map = [
            [25, -5, 15, 10, 10, 15, -5, 25],
            [-5, -10, -6, 1, 1, -6, -10, -5],
            [15, -6, 4, 4, 4, 4, -6, 15],
            [10, 1, 4, 0, 0, 4, 1, 10],
            [10, 1, 4, 0, 0, 4, 1, 10],
            [15, -6, 4, 4, 4, 4, -6, 15],
            [-5, -10, -6, 1, 1, -6, -10, -5],
            [25, -5, 15, 10, 10, 15, -5, 25],
        ]

        late_game_map = [
            [100, -15, 25, 20, 20, 25, -15, 100],
            [-15, -25, -15, 2, 2, -15, -25, -15],
            [25, -15, 10, 5, 5, 10, -15, 25],
            [20, 2, 5, 0, 0, 5, 2, 20],
            [20, 2, 5, 0, 0, 5, 2, 20],
            [25, -15, 10, 5, 5, 10, -15, 25],
            [-15, -25, -15, 2, 2, -15, -25, -15],
            [100, -15, 25, 20, 20, 25, -15, 100],
        ]

        # Determinamos la fase del juego basándonos en el número de fichas
        num_fichas = sum(1 for pos in state.board if state.board[pos] is not None)
        total_fichas = state.game.height * state.game.width
        if (
            num_fichas <= total_fichas * 0.25
        ):  # Early game: menos del 25% del tablero ocupado
            board_map = early_game_map
        elif num_fichas <= total_fichas * 0.75:  # Mid game: entre el 25% y el 75%
            board_map = mid_game_map
        else:  # Late game: más del 75% del tablero ocupado
            board_map = late_game_map

        # Calculamos los puntos basados en el mapeado del tablero para cada fase
        p1 = 0  # Puntos para el jugador 1
        p2 = 0  # Puntos para el jugador 2

        for i in range(8):
            for j in range(8):
                pos = (i + 1, j + 1)
                if state.board.get(pos) == state.player1.label:
                    p1 += board_map[i][j]
                elif state.board.get(pos) == state.player2.label:
                    p2 += board_map[i][j]

        # Aplicamos los ajustes adicionales (movimientos, esquinas, puntuación)
        mov1 = len(state.game._get_valid_moves(state.board, state.player1.label))
        mov2 = len(state.game._get_valid_moves(state.board, state.player2.label))
        p1_score = state.scores[0]
        p2_score = state.scores[1]

        # Si soy jugador 2, intercambiamos las puntuaciones y movimientos
        if not state.is_player_max(state.player1):
            p1, p2 = p2, p1
            mov1, mov2 = mov2, mov1
            p1_score, p2_score = p2_score, p1_score

        # Resultado final ponderado
        result = 0
        if (c1 + c2) != 0:
            result += (70 / 100) * ((c1 - c2) / (c1 + c2) * 100)
        if (mov1 + mov2) != 0:
            result += (15 / 100) * ((mov1 - mov2) / (mov1 + mov2) * 100)
        if (p1_score + p2_score) != 0:
            result += (15 / 100) * ((p1_score - p2_score) / (p1_score + p2_score) * 100)

        # Añadimos el resultado basado en el valor de cada casilla del mapeado
        result += p1 - p2

        return result


class Solution11(StudentHeuristic):
  def get_name(self) -> str:
    return "1pa1SinCamiseta"
  def evaluation_function(self, state: TwoPlayerGameState) -> float:
    esqj = [0, 0, 7, 7]
    esqi = [0, 7, 0, 7] #esq inf d, inf i, sup d, sup i
    c1=0
    c2=0
    #comprobamos si el juego ya ha terminado
    if state.end_of_game:
            if state.is_player_max(state.player1):
                return 1000
            return -1000
          
    for i in esqi:
      for j in esqj:
          pos = state.board.get((i+1, j+1), '_',)
          if(pos == state.player1.label): #si en esa esquina esta el jugador 1
            c1 = c1+1 #sumamos 1 a las esquinas de jugador 1
          elif (pos == state.player2.label): #si en esa esquina esta el jugador 2
            c2 = c2+1 #sumamos 1 a las esquinas de jugador 2
          #si no hay nadie en esa esquina aprovechamos para coger los corners closeness
    mov1 = len(state.game._get_valid_moves(state.board,state.player1.label))
    mov2 = len(state.game._get_valid_moves(state.board,state.player2.label))
    p1 = state.scores[0]
    p2 = state.scores[1]
    if state.is_player_max(state.player1)==False:
      c1, c2 = c2, c1
      mov1, mov2 = mov2, mov1
      p1, p2 = p2, p1
    result=0
    if(c1+c2!=0):
      result=result + (70/100) * ((c1-c2)/(c1+c2)*100)
    if(mov1+mov2!=0):
      result=result + (15/100) *((mov1-mov2)/(mov1+mov2)*100)
    if(p1+p2!=0):
      result+=result + (15/100) *((p1-p2)/(p1+p2)*100) 

    return result

