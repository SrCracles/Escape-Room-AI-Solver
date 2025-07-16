import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from src.python.enemy_a_start.Door import Door
from src.python.enemy_a_start.Puzzle import Puzzle
from src.python.enemy_a_start.general.State import State
from src.python.enemy_a_start.Game_State import GameState

from src.python.enemy_a_start.general.A_Start import a_start
from src.python.enemy_a_start.Room import Room

from src.python.enemy_a_start.Enemy import Enemy
from src.python.enemy_a_start.Minimax import minimax






def test_minimax():
    puzzle_3 = Puzzle(pos=(13, 3))
    door_3 = Door(pos=(13, 0))
    enemy_3 = Enemy(pos=(4, 3))
    room_3 = Room(number=1, width=14, height=5, puzzle=puzzle_3, door=door_3, enemy=enemy_3)
    
    initial_player_pos = (0, 1)
    final_player_pos = (5, 2)
    
    initial_state_3 = GameState(player_pos=initial_player_pos, room=room_3, has_item_puzzle=True, has_won=True)
    final_state_3 = GameState(player_pos=final_player_pos, room=room_3, has_item_puzzle=True, has_won=False)
    
    successors = enemy_3.get_successors(initial_state_3)
    score,_=minimax(depth=4,current_game_state=initial_state_3,final_game_state= final_state_3,turn=0)
    expected=22.799999999999997
    
    assert score==22.799999999999997

    
        

def test_get_successors():
    puzzle_3 = Puzzle(pos=(13, 3))
    door_3 = Door(pos=(13, 0))
    enemy_3 = Enemy(pos=(4, 3))
    room_3 = Room(number=1, width=14, height=5, puzzle=puzzle_3, door=door_3, enemy=enemy_3)
    
    initial_player_pos = (0, 1)
    final_player_pos = (5, 2)
    
    initial_state_3 = GameState(player_pos=initial_player_pos, room=room_3, has_item_puzzle=True, has_won=True)
    final_state_3 = GameState(player_pos=final_player_pos, room=room_3, has_item_puzzle=True, has_won=False)
    
    successors = enemy_3.get_successors(initial_state_3)
    
    assert len(successors) == 4




        

def test_enemy_walk_left():
    puzzle_3 = Puzzle(pos=(13, 3))
    door_3 = Door(pos=(13, 0))
    enemy_3 = Enemy(pos=(4, 3))
    room_3 = Room(number=1, width=14, height=4, puzzle=puzzle_3, door=door_3, enemy=enemy_3)
    initial_player_pos = (0, 1)
    final_player_pos = (5, 2)
    initial_state_3 = GameState(player_pos=initial_player_pos, room=room_3, has_item_puzzle=True, has_won=True)
    final_state_3 = GameState(player_pos=final_player_pos, room=room_3, has_item_puzzle=True, has_won=False)
    next_enemy_state = enemy_3.walk_left(initial_state_3)
    assert next_enemy_state is not None  
    assert next_enemy_state.room.enemy.pos == (3, 3)  


def test_enemy_walk_right():
    puzzle_3 = Puzzle(pos=(13, 3))
    door_3 = Door(pos=(13, 0))
    enemy_3 = Enemy(pos=(4, 3))
    room_3 = Room(number=1, width=14, height=4, puzzle=puzzle_3, door=door_3, enemy=enemy_3)
    
    initial_player_pos = (0, 1)
    final_player_pos = (5, 2)
    
    initial_state_3 = GameState(player_pos=initial_player_pos, room=room_3, has_item_puzzle=True, has_won=True)
    final_state_3 = GameState(player_pos=final_player_pos, room=room_3, has_item_puzzle=True, has_won=False)
    
    next_enemy_state = enemy_3.walk_right(initial_state_3)
    
    assert next_enemy_state is not None  
    assert next_enemy_state.room.enemy.pos == (5, 3)


def test_enemy_walk_up():
    puzzle_3 = Puzzle(pos=(13, 3))
    door_3 = Door(pos=(13, 0))
    enemy_3 = Enemy(pos=(4, 3))
    room_3 = Room(number=1, width=14, height=5, puzzle=puzzle_3, door=door_3, enemy=enemy_3)
    
    initial_player_pos = (0, 1)
    final_player_pos = (5, 2)
    
    initial_state_3 = GameState(player_pos=initial_player_pos, room=room_3, has_item_puzzle=True, has_won=True)
    final_state_3 = GameState(player_pos=final_player_pos, room=room_3, has_item_puzzle=True, has_won=False)
    
    next_enemy_state = enemy_3.walk_up(initial_state_3)
    
    assert next_enemy_state is not None  
    assert next_enemy_state.room.enemy.pos == (4, 4)


def test_enemy_walk_down():
    puzzle_3 = Puzzle(pos=(13, 3))
    door_3 = Door(pos=(13, 0))
    enemy_3 = Enemy(pos=(1, 1))
    room_3 = Room(number=1, width=14, height=4, puzzle=puzzle_3, door=door_3, enemy=enemy_3)
    
    initial_player_pos = (2, 2)
    final_player_pos = (5, 2)
    
    initial_state_3 = GameState(player_pos=initial_player_pos, room=room_3, has_item_puzzle=True, has_won=True)
    final_state_3 = GameState(player_pos=final_player_pos, room=room_3, has_item_puzzle=True, has_won=False)
    
    next_enemy_state = enemy_3.walk_down(initial_state_3)
    
    assert next_enemy_state is not None  
    assert next_enemy_state.room.enemy.pos == (1, 0)



