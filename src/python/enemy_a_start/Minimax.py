POSITIVE_INFINITY = 1000000000
NEGATIVE_INFINITY = -100000000

def minimax(depth, current_game_state, final_game_state, turn):
    """
    Receives a current game state, a final game state, and returns the next enemy movement.
    """
    
    if depth == 0:
        return current_game_state.get_score(current_game_state), current_game_state

    if turn == 0: # Enemy
        
        min_eval = POSITIVE_INFINITY
        children = current_game_state.room.enemy.get_successors(current_game_state)
        best_state = None
        
        for child in children:
            eval, _ = minimax(depth - 1, child, final_game_state, 1)  
            if eval < min_eval:
                min_eval = eval
                best_state = child
                
        return min_eval, best_state

    else: #Player
        max_eval=NEGATIVE_INFINITY
        children = current_game_state.get_succesors_for_score_computation()
        best_state=None
        for child in children:
            eval, _ = minimax(depth - 1, child, final_game_state, 0)
            if eval>max_eval:
                max_eval=eval
                best_state =child

        return max_eval, best_state


