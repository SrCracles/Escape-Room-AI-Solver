import pytest
from unittest.mock import patch, MagicMock, call
from src.python.escape_room import EscapeRoomGame
from pyswip import Prolog

@pytest.fixture
def game_instance():
    """Fixture que proporciona una instancia limpia del juego para cada test"""
    with patch('pyswip.Prolog'):
        game = EscapeRoomGame()
        game.prolog = MagicMock(spec=Prolog)
        return game

@pytest.fixture
def room_configs():
    """Configuraciones base para las salas"""
    return {
        1: {'door': (2, 2), 'puzzle': (3, 3), 'item': (4, 4)},
        2: {'door': (3, 3), 'puzzle': (1, 1), 'item': (4, 4)},
        3: {'door': (4, 0), 'puzzle': (2, 2), 'item': (0, 4)}
    }

def test_initialize_prolog_success():
    """Test para la inicialización exitosa de Prolog"""
    with patch('pyswip.Prolog') as mock_prolog:
        mock_prolog.return_value.query.return_value = True
        game = EscapeRoomGame()
        assert game.prolog is not None

def test_move_player_valid(game_instance):
    """Test para movimientos válidos"""
    directions = ['up', 'down', 'left', 'right']
    expected_positions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    
    for direction, (dx, dy) in zip(directions, expected_positions):
        game_instance.current_state = {'x': 2, 'y': 2, 'room': 1, 'has_key': False, 'has_item': False}
        result = game_instance.move_player(direction)
        assert result is True
        assert game_instance.current_state['x'] == 2 + dx
        assert game_instance.current_state['y'] == 2 + dy

def test_move_player_invalid(game_instance):
    """Test para movimientos inválidos (fuera de límites)"""
    game_instance.current_state = {'x': 0, 'y': 0, 'room': 1, 'has_key': False, 'has_item': False}
    assert game_instance.move_player('left') is False
    assert game_instance.move_player('up') is False

def test_get_item_success(game_instance, room_configs):
    """Test para obtener ítem exitosamente"""
    room = 1
    game_instance.current_state = {'x': 4, 'y': 4, 'room': room, 'has_key': False, 'has_item': False}
    game_instance.get_item()
    assert game_instance.current_state['has_item'] is True

def test_solve_puzzle_requires_item(game_instance, room_configs, capsys):
    room = 1
    game_instance.current_state = {'x': 3, 'y': 3, 'room': room, 'has_key': False, 'has_item': False}
    game_instance.solve_puzzle()
    captured = capsys.readouterr()
    assert "You need the special item" in captured.out

def test_solve_advanced_puzzle_correct_code(game_instance, room_configs):
    """Test para resolver puzzle avanzado con código correcto"""
    room = 1
    game_instance.current_state = {'x': 3, 'y': 3, 'room': room, 'has_key': False, 'has_item': False}
    game_instance.prolog.query.return_value = [{'Hint': 'Color code hint', 'ExpectedCode': '123'}]
    
    with patch('builtins.input', return_value='123'):
        game_instance.solve_advanced_puzzle()
        assert game_instance.current_state['has_key'] is True
        assert game_instance.puzzles_solved[room] is True

def test_next_room_requires_key(game_instance, room_configs, capsys):
    room = 1
    game_instance.current_state = {'x': 2, 'y': 2, 'room': room, 'has_key': False, 'has_item': False}
    game_instance.next_room()
    captured = capsys.readouterr()
    assert "You need a key" in captured.out

def test_get_hint_success(game_instance, room_configs, capsys):
    room = 1
    game_instance.current_state = {'x': 0, 'y': 0, 'room': room, 'has_key': False, 'has_item': False}
    game_instance.prolog.query.return_value = [{'NextMove': 'right'}]

    game_instance.get_hint()
    captured = capsys.readouterr()
    assert "right" in captured.out


def test_show_solution_success(game_instance, capsys):
    mock_solution = [{'Path': ['move(right)', 'get_item']}]
    game_instance.prolog.query.return_value = mock_solution

    game_instance.show_solution()
    captured = capsys.readouterr()
    assert "Complete solution" in captured.out
    assert "move(right)" in captured.out
    
    game_instance.show_solution()
    output = capsys.readouterr().out
    assert "Complete solution" in output
    assert "move(right)" in output

def test_display_map(game_instance, room_configs, capsys):
    room = 1
    game_instance.current_state = {'x': 0, 'y': 0, 'room': room, 'has_key': False, 'has_item': False}

    game_instance.display_map()
    captured = capsys.readouterr()
    assert "Current room map" in captured.out
    assert "P" in captured.out  # Jugador
    assert "D" in captured.out  # Puerta
    assert "I" in captured.out  # Ítem
    assert "?" in captured.out  # Puzzle

'''
def test_main_menu_exit(game_instance):
    """Test para salir del menú principal"""
    with patch('builtins.input', return_value='8'):
        with pytest.raises(SystemExit):
            game_instance.main_menu()
'''

# Pruebas para la integración con Prolog
def test_prolog_queries(game_instance):
    """Test para verificar las consultas a Prolog"""
    room = 1
    x, y = 0, 0
    door_x, door_y = game_instance.room_config[room]['door']
    
    # Test para get_hint
    game_instance.current_state = {'x': x, 'y': y, 'room': room, 'has_key': False, 'has_item': False}
    game_instance.get_hint()
    game_instance.prolog.query.assert_called_with(
        f"best_next_move({x}, {y}, {room}, {door_x}, {door_y}, NextMove)"
    )
    
    # Test para show_solution
    game_instance.show_solution()
    game_instance.prolog.query.assert_called_with("full_solution(Path)")