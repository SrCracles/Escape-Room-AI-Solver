import pytest
from src.python.astar.astar_solver import EscapeRoomSolver, State

@pytest.fixture
def simple_solver_config():
    return {
        "grid_size": 5,
        "player_start": (0, 0),
        "door_pos": (4, 4),
        "item_pos": (1, 1), 
        "puzzle_pos": (1, 2), 
        "max_turns_for_this_room": 20
    }

@pytest.fixture
def full_game_solver_config():
    # Configuración que requiere coger item y resolver puzzle
    return {
        "grid_size": 5,
        "player_start": (0, 0),
        "door_pos": (4, 4),
        "item_pos": (2, 2),
        "puzzle_pos": (1, 3),
        "max_turns_for_this_room": 20
    }

@pytest.fixture
def solver_simple(simple_solver_config):
    return EscapeRoomSolver(**simple_solver_config)

@pytest.fixture
def solver_full(full_game_solver_config):
    return EscapeRoomSolver(**full_game_solver_config)





# --- Tests ---

def test_initialization(solver_simple):
    assert solver_simple.grid_size == 5
    assert solver_simple.start_pos == (0, 0)
    assert solver_simple.door_pos == (4, 4)
    assert solver_simple.item_pos == (1, 1)
    assert solver_simple.puzzle_pos == (1, 2)
    assert solver_simple.max_turns == 20
    assert solver_simple.start_state == State(0, 0, False, False, False)

def test_initialization_invalid_start():
     with pytest.raises(ValueError, match="Invalid player start position"):
        EscapeRoomSolver(3, (-1, 0), (1,1), (0,1), (1,0), 10)
     with pytest.raises(ValueError, match="Invalid player start position"):
        EscapeRoomSolver(3, (3, 0), (1,1), (0,1), (1,0), 10)

@pytest.mark.parametrize("x, y, expected", [
    (0, 0, True), (4, 4, True), (2, 3, True), # Inside
    (-1, 0, False), (0, -1, False),           # Negative coords
    (5, 0, False), (0, 5, False),             # Outside bounds
    (5, 5, False)
])
def test_is_valid_pos(solver_simple, x, y, expected):
    assert solver_simple.is_valid_pos(x, y) == expected

@pytest.mark.parametrize("pos1, pos2, expected", [
    ((0, 0), (4, 4), 8),
    ((1, 1), (1, 1), 0),
    ((0, 0), (0, 3), 3),
    ((2, 1), (4, 0), 3),
])
def test_manhattan_distance(solver_simple, pos1, pos2, expected):
    assert solver_simple.manhattan_distance(pos1, pos2) == expected

def test_heuristic_no_item_no_key(solver_full):
    state = State(0, 0, False, False, False)
    # Expected: dist(0,0->2,2) + dist(2,2->1,3) + dist(1,3->4,4) = 4 + 2 + 4 = 10
    assert solver_full.heuristic(state) == 10

def test_heuristic_has_item(solver_full):
    state = State(2, 2, False, True, False)
    # Expected: dist(2,2->1,3) + dist(1,3->4,4) = 2 + 4 = 6
    assert solver_full.heuristic(state) == 6

def test_heuristic_has_key(solver_full):
    state = State(1, 3, True, False, True) # has_key=True when puzzle solved
    # Expected: dist(1,3->4,4) = 4
    assert solver_full.heuristic(state) == 4

def test_get_neighbors_walk(solver_simple):
    state = State(0, 0, False, False, False)
    neighbors = solver_simple.get_neighbors(state)
    actions = {n[0] for n in neighbors}
    assert 'walk(down)' in actions
    assert 'walk(right)' in actions
    assert len(actions) == 2

def test_get_neighbors_at_item(solver_full):
    state = State(2, 2, False, False, False)
    neighbors = solver_full.get_neighbors(state)
    actions = {n[0] for n in neighbors}
    assert 'get_item' in actions
    assert 'walk(up)' in actions

def test_get_neighbors_at_item_with_item(solver_full):
    state = State(2, 2, False, True, False)
    neighbors = solver_full.get_neighbors(state)
    actions = {n[0] for n in neighbors}
    assert 'get_item' not in actions
    assert 'walk(up)' in actions

def test_get_neighbors_at_puzzle_no_item(solver_full):
    state = State(1, 3, False, False, False)
    neighbors = solver_full.get_neighbors(state)
    actions = {n[0] for n in neighbors}
    assert 'solve_puzzle' not in actions
    assert 'walk(up)' in actions

def test_get_neighbors_at_puzzle_with_item(solver_full):
    state = State(1, 3, False, True, False)
    neighbors = solver_full.get_neighbors(state)
    actions = {n[0] for n in neighbors}
    assert 'solve_puzzle' in actions
    assert 'walk(up)' in actions

def test_get_neighbors_at_puzzle_solved(solver_full):
    state = State(1, 3, True, False, True)
    neighbors = solver_full.get_neighbors(state)
    actions = {n[0] for n in neighbors}
    assert 'solve_puzzle' not in actions
    assert 'get_item' not in actions # Item doesn't respawn
    assert 'walk(up)' in actions

# --- A* Solve Tests ---

def test_solve_astar_simple_direct_path():
    # 3x3 grid, start(0,0), door(2,2), item(0,1), puzzle(1,0)
    solver = EscapeRoomSolver(3, (0,0), (2,2), (0,1), (1,0), 10) # Max 10 turns
    path, turns = solver.solve_astar()
    # Expected path requires item and puzzle: 9 turns total
    assert path is not None
    assert turns == 9 # CORREGIDO: Expected turns

def test_solve_astar_full_game(solver_full):
    # Start(0,0) -> Item(2,2) -> Puzzle(1,3) -> Door(4,4)
    path, turns = solver_full.solve_astar()
    assert path is not None
    # Expected: 4 moves + get_item(1) + 2 moves + solve(1) + 4 moves + use_door(1) = 13
    assert turns == 13
    assert path[-1] == 'use_door'
    assert 'get_item' in path
    assert 'solve_puzzle' in path

def test_solve_astar_insufficient_turns(solver_full):
    # Use the existing fixture config, but create a solver with fewer turns
    config = solver_full.__dict__ # Get attributes from the fixture object
    solver_low_turns = EscapeRoomSolver(
        grid_size=config['grid_size'],
        player_start=config['start_pos'],
        door_pos=config['door_pos'],
        item_pos=config['item_pos'],
        puzzle_pos=config['puzzle_pos'],
        max_turns_for_this_room=10,
        has_item=False,
        solved_puzzle=False
    )
    path, turns = solver_low_turns.solve_astar()
    assert path is None
    assert turns == float('inf')

def test_solve_astar_start_with_item():
    config = { "grid_size": 5, "player_start": (0, 0), "door_pos": (4, 4),
               "item_pos": (2, 2), "puzzle_pos": (1, 3),
               "max_turns_for_this_room": 20 }
    solver = EscapeRoomSolver(**config, has_item=True)
    path, turns = solver.solve_astar()
    # Path: Start(0,0) -> Puzzle(1,3) -> Door(4,4)
    # Turns: 4 moves + solve(1) + 4 moves + use_door(1) = 10
    assert path is not None
    assert turns == 10
    assert 'get_item' not in path
    assert 'solve_puzzle' in path
    assert path[-1] == 'use_door'

def test_solve_astar_start_with_key():
    config = { "grid_size": 5, "player_start": (0, 0), "door_pos": (4, 4),
               "item_pos": (2, 2), "puzzle_pos": (1, 3),
               "max_turns_for_this_room": 20 }
    # Start with key (puzzle already solved)
    solver = EscapeRoomSolver(**config, has_item=True, solved_puzzle=True)
    path, turns = solver.solve_astar()
     # Path: Start(0,0) -> Door(4,4)
    # Turns: 8 moves + use_door(1) = 9
    assert path is not None
    assert turns == 9
    assert 'get_item' not in path
    assert 'solve_puzzle' not in path
    assert path[-1] == 'use_door'