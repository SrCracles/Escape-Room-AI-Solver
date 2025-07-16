import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from src.python.enemy_a_start.general.State import State
from src.python.enemy_a_start.Game_State import GameState
from src.python.enemy_a_start.Game_Constants import GameConstants

from src.python.enemy_a_start.general.A_Start import a_start
from src.python.enemy_a_start.Room import Room
gameConstants = GameConstants()
import time

def test_lvl_1():
    initial_state = gameConstants.lvl_1_get_initial_state()
    final_state = gameConstants.lvl_1_get_final_state()
    
    start = time.time()
    path = a_start(initial_state, final_state)
    end = time.time()
    dif = end - start
    ans = get_actions(path)
    expected = "Walk rightWalk rightWalk rightWalk rightWalk rightWalk rightWalk rightWalk rightUse door"
    
    assert ans == expected
    assert dif > 0

def test_lvl_2():
    initial_state = gameConstants.lvl_2_get_initial_state()
    final_state = gameConstants.lvl_2_get_final_state()
    
    start = time.time()
    path = a_start(initial_state, final_state)
    end = time.time()
    dif = end - start
    ans = get_actions(path)
    expected = "Walk rightWalk rightWalk rightWalk rightWalk rightWalk rightWalk rightWalk rightWalk rightWalk rightWalk rightWalk rightWalk rightWalk rightSolve puzzleUse door"
    
    assert ans == expected
    assert dif > 0

   

def test_lvl_3():
    
    initial_state = gameConstants.lvl_3_get_initial_state()
    final_state = gameConstants.lvl_3_get_final_state()
    
    start = time.time()
    path = a_start(initial_state, final_state)
    end = time.time()
    dif=end-start
    ans=get_actions(path)
    expected="Walk rightWalk rightWalk rightWalk rightWalk rightWalk rightWalk rightWalk rightWalk rightWalk rightWalk upWalk rightWalk rightSolve puzzleWalk LeftWalk LeftWalk LeftWalk LeftWalk LeftWalk LeftWalk LeftWalk downUse door"
    assert ans==expected
    assert dif>0
def get_actions(path):
    ans=""
    for step in path:
        if step.action:
            ans+=step.action
    return ans
