from game import (
    TwoPlayerGameState,
)
from heuristic import (
    simple_evaluation_function,
)
from tournament import (
    StudentHeuristic,
)



def func_glob(n: int, state: TwoPlayerGameState) -> float:
    return n + simple_evaluation_function(state)



class Solution11(StudentHeuristic):
  def get_name(self) -> str:
    return "1pa1SinCamiseta"
  def evaluation_function(self, state: TwoPlayerGameState) -> float:
    esqj = [0, 0, 7, 7]
    esqi = [0, 7, 0, 7]
    c1=0
    c2=0
    if state.end_of_game:
            if state.is_player_max(state.player1):
                return 1000
            return -1000
          
    for i in esqi:
      for j in esqj:
          pos = state.board.get((i+1, j+1), '_',)
          if(pos == state.player1.label):
            c1 = c1+1
          elif (pos == state.player2.label):
            c2 = c2+1
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

class CombinedHeuristic(StudentHeuristic):
    def get_name(self) -> str:
        return "CombinedRarilla1pa1"

    def evaluation_function(self, state: TwoPlayerGameState) -> float:
        j1_score = 0
        j2_score = 0
        height = state.game.height
        width = state.game.width
        centre_y = height // 2
        centre_x = width // 2

        corner_value = 100
        critical_position_value = -50

        corners = [(1, 1), (1, width), (height, 1), (height, width)]
        critical_positions = [
            (1, 2), (2, 1), (2, 2), (height, 2), (height - 1, 1), (height - 1, 2),
            (height, width - 1), (height - 1, width), (height - 1, width - 1),
            (width, 2), (width - 1, 1), (width - 1, 2)
        ]

        for c in state.board:
            x, y = c
            if (x, y) in critical_positions:
                if state.board[c] is state.player1.label:
                    j1_score += critical_position_value
                elif state.board[c] is state.player2.label:
                    j2_score += critical_position_value
                continue

            if (x, y) in corners:
                if state.board[c] is state.player1.label:
                    j1_score += corner_value
                elif state.board[c] is state.player2.label:
                    j2_score += corner_value
                continue
            
            distancia_centro = abs(x - centre_x) + abs(y - centre_y)
            if 1 < x < width and 1 < y < height:
                distancia_centro -= 2  

            if state.board[c] is state.player1.label:
                j1_score += distancia_centro
            elif state.board[c] is state.player2.label:
                j2_score += distancia_centro

        esqj = [0, 0, 7, 7]
        esqi = [0, 7, 0, 7]
        c1 = 0
        c2 = 0
        for i in esqi:
            for j in esqj:
                pos = state.board.get((i+1, j+1), '_')
                if pos == state.player1.label:
                    c1 += 1
                elif pos == state.player2.label:
                    c2 += 1
        
        mov_j1 = len(state.game._get_valid_moves(state.board,state.player1.label))
        mov_j2 = len(state.game._get_valid_moves(state.board,state.player2.label))

        p1 = state.scores[0]
        p2 = state.scores[1]

        if not state.is_player_max(state.player1):
            c1, c2 = c2, c1
            mov_j1, mov_j2 = mov_j2, mov_j1
            p1, p2 = p2, p1

        result = 0
        if c1 + c2 != 0:
            result += (70 / 100) * ((c1 - c2) / (c1 + c2) * 100)
        if mov_j1 + mov_j2 != 0:
            result += (15 / 100) * ((mov_j1 - mov_j2) / (mov_j1 + mov_j2) * 100)
        if p1 + p2 != 0:
            result += (15 / 100) * ((p1 - p2) / (p1 + p2) * 100)

        j1_score += 7 * mov_j1
        j2_score += 7 * mov_j2

        if state.is_player_max(state.player1):
            return j1_score - j2_score + result
        else:
            return j2_score - j1_score + result

class Solution2(StudentHeuristic):
    def get_name(self) -> str:
        return "BuenaG"

    def evaluation_function(self, state: TwoPlayerGameState) -> float:
        if state.end_of_game:
            if state.is_player_max(state.player1):
                return 1000
            return -1000

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

        num_fichas = sum(1 for pos in state.board if state.board[pos] is not None)
        total_fichas = state.game.height * state.game.width
        if num_fichas <= total_fichas * 0.25:
            board_map = early_game_map
        elif num_fichas <= total_fichas * 0.75:
            board_map = mid_game_map
        else:
            board_map = late_game_map

        p1 = 0
        p2 = 0 

        for i in range(8):
            for j in range(8):
                pos = (i + 1, j + 1)
                if state.board.get(pos) == state.player1.label:
                    p1 += board_map[i][j]
                elif state.board.get(pos) == state.player2.label:
                    p2 += board_map[i][j]

        mov1 = len(state.game._get_valid_moves(state.board, state.player1.label))
        mov2 = len(state.game._get_valid_moves(state.board, state.player2.label))
        p1_score = state.scores[0]
        p2_score = state.scores[1]

        if not state.is_player_max(state.player1):
            p1, p2 = p2, p1
            mov1, mov2 = mov2, mov1
            p1_score, p2_score = p2_score, p1_score

        result = 0
        if (p1 + p2) != 0:
            result += (70 / 100) * ((p1 - p2) / (p1 + p2) * 100)
        if (mov1 + mov2) != 0:
            result += (15 / 100) * ((mov1 - mov2) / (mov1 + mov2) * 100)
        if (p1_score + p2_score) != 0:
            result += (15 / 100) * ((p1_score - p2_score) / (p1_score + p2_score) * 100)


        return result
