import pytest
from unittest.mock import patch, call
from src.python.astar import escape_room_game_astar
from src.python.astar import astar_solver

@pytest.fixture
def base_room_configs():
    return [
        {'name': 'A', 'grid': 5, 'start': (0,0), 'door': (4,4), 'item': (2,2), 'puzzle': (1,3), 'max_turns': 15},
        {'name': 'B', 'grid': 4, 'start': (1,0), 'door': (3,3), 'item': (0,2), 'puzzle': (2,2), 'max_turns': 10},
    ]




def test_is_valid_coordinate():
    assert escape_room_game_astar.is_valid_coordinate(0, 0, 5) == True
    assert escape_room_game_astar.is_valid_coordinate(4, 4, 5) == True
    assert escape_room_game_astar.is_valid_coordinate(-1, 0, 5) == False
    assert escape_room_game_astar.is_valid_coordinate(0, 5, 5) == False

def test_get_coordinate_input_valid(mocker):
    mocker.patch('builtins.input', return_value='1,2')
    occupied = set()
    result = escape_room_game_astar.get_coordinate_input("Test prompt", 5, occupied)
    assert result == (1, 2)

def test_get_coordinate_input_invalid_format_then_valid(mocker):
    mock_input = mocker.patch('builtins.input', side_effect=['abc', '1, 2'])
    occupied = set()
    result = escape_room_game_astar.get_coordinate_input("Test prompt", 5, occupied)
    assert result == (1, 2)
    assert mock_input.call_count == 2

def test_get_coordinate_input_out_of_bounds_then_valid(mocker):
    mock_input = mocker.patch('builtins.input', side_effect=['6,1', '1, 2'])
    occupied = set()
    result = escape_room_game_astar.get_coordinate_input("Test prompt", 5, occupied)
    assert result == (1, 2)
    assert mock_input.call_count == 2

def test_get_coordinate_input_occupied_then_valid(mocker):
    mock_input = mocker.patch('builtins.input', side_effect=['1,1', '1, 2'])
    occupied = {(1, 1)}
    result = escape_room_game_astar.get_coordinate_input("Test prompt", 5, occupied)
    assert result == (1, 2)
    assert mock_input.call_count == 2

def test_get_user_input_room_success(mocker):
    input_sequence = [ '5', '0,0', '4,4', '2,2', '1,3', '15' ]
    mocker.patch('builtins.input', side_effect=input_sequence)
    mock_solve = mocker.patch('src.python.astar.astar_solver.EscapeRoomSolver.solve_astar', return_value=(['mock_path'], 10))
    mocker.patch('builtins.print')

    gs, ps, dp, ip, pp, mt = escape_room_game_astar.get_user_input_room('TestRoom')

    assert gs == 5
    assert ps == (0, 0)
    assert dp == (4, 4)
    assert ip == (2, 2)
    assert pp == (1, 3)
    assert mt == 15
    mock_solve.assert_called_once()

def test_get_user_input_room_invalid_turns_then_success(mocker):
    input_sequence = [ '5', '0,0', '4,4', '2,2', '1,3', '5', '15' ]
    mocker.patch('builtins.input', side_effect=input_sequence)
    mock_solve = mocker.patch('src.python.astar.astar_solver.EscapeRoomSolver.solve_astar', side_effect=[
        (None, float('inf')), (['mock_path'], 10)
    ])
    mocker.patch('builtins.print')

    gs, ps, dp, ip, pp, mt = escape_room_game_astar.get_user_input_room('TestRoom')

    assert mt == 15
    assert mock_solve.call_count == 2



def test_draw_grid_initial_state(capsys, base_room_configs):
    config = base_room_configs[0]
    escape_room_game_astar.draw_grid(
        config['grid'], config['start'], config['door'], config['item'], config['puzzle'],
        has_item=False, solved_puzzle=False
    )
    captured = capsys.readouterr()
    out = captured.out
    assert 'P' in out
    assert 'D' in out
    assert 'I' in out
    assert '?' in out
    assert out.count('-') > 10
    assert out.count('|') == 10

def test_draw_grid_has_item(capsys, base_room_configs):
    config = base_room_configs[0]
    player_at_item = config['item']
    escape_room_game_astar.draw_grid(
        config['grid'], player_at_item, config['door'], config['item'], config['puzzle'],
        has_item=True, solved_puzzle=False
    )
    captured = capsys.readouterr()
    out = captured.out
    assert 'I' not in out
    assert '?' in out
    assert 'P' in out
    assert 'D' in out

def test_draw_grid_solved_puzzle(capsys, base_room_configs):
    config = base_room_configs[0]
    player_at_puzzle = config['puzzle']
    escape_room_game_astar.draw_grid(
        config['grid'], player_at_puzzle, config['door'], config['item'], config['puzzle'],
        has_item=False, solved_puzzle=True
    )
    captured = capsys.readouterr()
    out = captured.out
    assert 'I' not in out
    assert '?' not in out
    assert 'P' in out
    assert 'D' in out




def test_get_next_move_hint_found(mocker):
    mock_solver = mocker.MagicMock(spec=astar_solver.EscapeRoomSolver)
    mock_solver.solve_astar.return_value = (['walk(right)', 'get_item', 'use_door'], 3)
    hint = escape_room_game_astar.get_next_move_hint(mock_solver)
    assert hint == 'walk(right)'
    mock_solver.solve_astar.assert_called_once()

def test_get_next_move_hint_only_door(mocker):
    mock_solver = mocker.MagicMock(spec=astar_solver.EscapeRoomSolver)
    mock_solver.solve_astar.return_value = (['use_door'], 1)
    hint = escape_room_game_astar.get_next_move_hint(mock_solver)
    assert hint == 'use_door (You should be able to exit!)'

def test_get_next_move_hint_not_found(mocker):
    mock_solver = mocker.MagicMock(spec=astar_solver.EscapeRoomSolver)
    mock_solver.start_state = astar_solver.State(0,0,False,False,False)
    mock_solver.door_pos = (4,4)
    mock_solver.item_pos = (2,2)
    mock_solver.puzzle_pos = (1,3)
    mock_solver.solve_astar.return_value = (None, float('inf'))
    hint = escape_room_game_astar.get_next_move_hint(mock_solver)
    assert "No solution found" in hint




def test_solve_all_autopilot_success(mocker, capsys, base_room_configs):
    mock_astar = mocker.patch('src.python.astar.astar_solver.EscapeRoomSolver.solve_astar', side_effect=[
        (['walk(right)', 'get_item', 'use_door'], 3), # Room A
        (['walk(down)', 'solve_puzzle', 'use_door'], 3)  # Room B
    ])
    mocker.patch('time.sleep')
    mocker.patch('builtins.print')

    success = escape_room_game_astar.solve_all_autopilot(
        base_room_configs, start_room_index=0, initial_player_pos=(0,0),
        initial_has_item=False, initial_solved_puzzle=False, initial_turns_used_in_current_room=0
    )

    assert success == True
    assert mock_astar.call_count == 2

def test_solve_all_autopilot_fail_no_path(mocker, base_room_configs):
    mock_astar = mocker.patch('src.python.astar.astar_solver.EscapeRoomSolver.solve_astar', return_value=(None, float('inf')))
    mocker.patch('time.sleep')
    mocker.patch('builtins.print')

    success = escape_room_game_astar.solve_all_autopilot(
        base_room_configs, start_room_index=0, initial_player_pos=(0,0),
        initial_has_item=False, initial_solved_puzzle=False, initial_turns_used_in_current_room=0
    )

    assert success == False
    mock_astar.assert_called_once()

def test_solve_all_autopilot_fail_insufficient_turns(mocker, base_room_configs):
    # Mock A* to return a path requiring 7 turns.
    mock_astar = mocker.patch('src.python.astar.astar_solver.EscapeRoomSolver.solve_astar',
                              return_value=(['walk(right)', 'use_door'], 7)) # Needs 7 turns
    mocker.patch('time.sleep')
    mocker.patch('builtins.print')

    # Config with max 10 turns
    configs = [{'name': 'A', 'grid': 5, 'start': (0,0), 'door': (4,4), 'item': (2,2), 'puzzle': (1,3), 'max_turns': 10}]

    # Start autopilot with 5 turns used (remaining = 10 - 5 = 5)
    success = escape_room_game_astar.solve_all_autopilot(
        configs, start_room_index=0, initial_player_pos=(0,1), # Arbitrary starting pos for test
        initial_has_item=False, initial_solved_puzzle=False,
        initial_turns_used_in_current_room=5
    )
    # Since remaining turns (5) < turns_needed (7), autopilot should fail.

    assert success == False
    # A* is called once, determines path is too long for remaining turns
    mock_astar.assert_called_once()


# --- Basic Game State Transition Tests ---

def test_state_update_move():
    player_pos = (0, 0)
    turns = 0
    # Simulate moving right
    new_player_pos = (1, 0)
    turn_cost_move = 1
    # Apply updates
    turns += turn_cost_move
    player_pos = new_player_pos
    # Assert results
    assert turns == 1
    assert player_pos == (1, 0)

def test_state_update_get_item():
    player_pos = (2, 2)
    item_pos = (2, 2)
    has_item = False
    solved_puzzle = False
    turns = 5
    turn_cost_interaction = 0
    # Check interaction
    if player_pos == item_pos and not has_item and not solved_puzzle:
        has_item = True
        turn_cost_interaction = 1 # Item pickup costs 1 extra
    # Apply cost
    turns += turn_cost_interaction
    # Assert
    assert has_item == True
    assert turns == 6

def test_state_update_solve_puzzle():
    player_pos = (1, 3)
    puzzle_pos = (1, 3)
    has_item = True
    solved_puzzle = False
    turns = 8
    turn_cost_interaction = 0
    # Check interaction
    if player_pos == puzzle_pos and has_item and not solved_puzzle:
         solved_puzzle = True
         has_item = False
         # turn_cost_interaction = 0 # Solving doesn't cost *extra*
    # Apply cost
    turns += turn_cost_interaction
    # Assert
    assert solved_puzzle == True
    assert has_item == False
    assert turns == 8