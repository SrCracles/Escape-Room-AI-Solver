import os
from pyswip import Prolog
from pathlib import Path
import time

class EscapeRoomGame:
    def __init__(self):
        self.prolog = self.initialize_prolog()
        self.current_state = {
            'x': 0,
            'y': 0,
            'room': 1,
            'has_key': False,
            'has_item': False
        }
        self.room_config = {
            1: {'door': (2, 2), 'puzzle': (3, 3), 'item': (4, 4)},
            2: {'door': (3, 3), 'puzzle': (1, 1), 'item': (4, 4)},
            3: {'door': (4, 0), 'puzzle': (2, 2), 'item': (0, 4)}
        }
        self.puzzles_solved = {1: False, 2: False, 3: False}

    def initialize_prolog(self):
        prolog = Prolog()
        script_dir = Path(__file__).parent.parent  # Sube un nivel para llegar a /proyecto
        
        # Ruta a la carpeta prolog
        prolog_dir = script_dir / "prolog"
        
        # Cargar ambos archivos Prolog
        for file in ["escape_solver.pl", "clp_hints.pl"]:
            try:
                prolog_file_path = prolog_dir / file
                absolute_path = prolog_file_path.resolve()
                # Convertir la ruta a formato string con barras adecuadas
                prolog_path_str = str(absolute_path).replace('\\', '/')
                # Consultar el archivo Prolog
                list(prolog.query(f"consult('{prolog_path_str}')"))
                print(f"{file} cargado correctamente")
            except Exception as e:
                print(f"Error al cargar {file}: {e}")
                exit()
        return prolog

    def display_status(self):
        print("\n" + "="*40)
        print(f"Current position: ({self.current_state['x']}, {self.current_state['y']})")
        print(f"Current room: {self.current_state['room']}")
        print(f"Has key: {'Yes' if self.current_state['has_key'] else 'No'}")
        print(f"Has item: {'Yes' if self.current_state['has_item'] else 'No'}")
        print("="*40 + "\n")

    def display_map(self):
        print("\nCurrent room map:")
        room = self.current_state['room']
        config = self.room_config[room]
        for y in range(5):
            for x in range(5):
                if (x, y) == (self.current_state['x'], self.current_state['y']):
                    print("P", end=" ")  # Player
                elif (x, y) == config['door']:
                    print("D", end=" ")  # Door
                elif (x, y) == config['puzzle']:
                    print("?", end=" ")  # Puzzle
                elif (x, y) == config['item']:
                    print("I", end=" ")  # Item
                else:
                    print(".", end=" ")  # Empty space
            print()

    def move_player(self, direction):
        x, y = self.current_state['x'], self.current_state['y']
        new_x, new_y = x, y
        
        if direction == 'up' and y > 0:
            new_y -= 1
        elif direction == 'down' and y < 4:
            new_y += 1
        elif direction == 'left' and x > 0:
            new_x -= 1
        elif direction == 'right' and x < 4:
            new_x += 1
        else:
            print("Invalid move or out of bounds!")
            return False
        
        self.current_state['x'], self.current_state['y'] = new_x, new_y
        print(f"You moved {direction} to position ({new_x}, {new_y})")
        return True

    def get_item(self):
        room = self.current_state['room']
        item_pos = self.room_config[room]['item']
        
        if (self.current_state['x'], self.current_state['y']) == item_pos:
            if not self.current_state['has_item']:
                self.current_state['has_item'] = True
                print("You got the item needed to solve the puzzle!")
            else:
                print("You already have this item.")
        else:
            print("There's no item here.")

    def solve_puzzle(self):
        room = self.current_state['room']
        puzzle_pos = self.room_config[room]['puzzle']
        
        if (self.current_state['x'], self.current_state['y']) == puzzle_pos:
            if self.current_state['has_item'] and not self.current_state['has_key']:
                self.current_state['has_key'] = True
                self.current_state['has_item'] = False
                print("You solved the puzzle and got the key!")
            elif self.current_state['has_key']:
                print("You've already solved this puzzle.")
            else:
                print("You need the special item to solve this puzzle.")
        else:
            print("There's no puzzle here.")

    def solve_advanced_puzzle(self):
        room = self.current_state['room']
        puzzle_pos = self.room_config[room]['puzzle']
        
        if (self.current_state['x'], self.current_state['y']) == puzzle_pos:
            if not self.puzzles_solved[room]:
                print(f"\n=== Advanced Puzzle in Room {room} ===")
                try:
                    solutions = list(self.prolog.query(
                        f"get_puzzle_info({room}, Hint, ExpectedCode)"
                    ))
                    
                    if solutions:
                        hint = solutions[0]['Hint']
                        expected_code = solutions[0]['ExpectedCode']
                        print(f"Hint: {hint}")
                        
                        answer = input("Enter the code you discovered (or 'skip'): ").strip()
                        if answer.lower() != 'skip':
                            if answer == expected_code:
                                print("Correct! The lock opens and you get a key.")
                                self.puzzles_solved[room] = True
                                self.current_state['has_key'] = True
                            else:
                                print(f"Incorrect. The expected code was {expected_code}")
                    else:
                        print("The puzzle seems too complex right now.")
                except Exception as e:
                    print(f"Error solving puzzle: {str(e)}")
            else:
                print("You already solved this advanced puzzle.")
        else:
            print("There's no puzzle here.")

    def next_room(self):
        room = self.current_state['room']
        door_pos = self.room_config[room]['door']
        
        if (self.current_state['x'], self.current_state['y']) == door_pos:
            if self.current_state['has_key']:
                if room < 3:
                    self.current_state['room'] += 1
                    self.current_state['x'], self.current_state['y'] = 0, 0
                    self.current_state['has_key'] = False
                    print(f"You entered room {self.current_state['room']}!")
                    if self.current_state['room'] == 3:
                        print("You're in the final room! Find the exit to escape.")
                else:
                    print("Congratulations! You escaped the room.")
                    return True
            else:
                print("You need a key to go through this door.")
        else:
            print("You're not at the exit door.")
        return False

    def get_hint(self):
        room = self.current_state['room']
        x, y = self.current_state['x'], self.current_state['y']
        
        door_x, door_y = self.room_config[room]['door']
        query = f"best_next_move({x}, {y}, {room}, {door_x}, {door_y}, NextMove)"
        
        try:
            solutions = list(self.prolog.query(query))
            if solutions:
                next_move = solutions[0]['NextMove']
                print(f"\nHint: The next best move is: {next_move}")
            else:
                print("\nCouldn't get a hint right now.")
        except Exception as e:
            print(f"\nError getting hint: {e}")

    def show_solution(self):
        try:
            print("\nCalculating complete solution...")
            start_time = time.perf_counter()  # Usamos perf_counter para mayor precisión
            
            # Ejecuta la consulta a Prolog
            solutions = list(self.prolog.query("full_solution(Path)"))
            
            end_time = time.perf_counter()
            elapsed_time = (end_time - start_time) * 1000  # Convertimos a milisegundos
            
            if solutions:
                path = solutions[0]["Path"]
                print(f"\nComplete solution (calculated in {elapsed_time:.2f} ms):")  # Mostramos en ms
                for step in path:
                    print(f"- {step}")
            else:
                print(f"\nNo complete solution found (searched for {elapsed_time:.2f} ms).")
        except Exception as e:
            print(f"\nError calculating solution: {e}")

    def main_menu(self):
        print("Welcome to the Escape Room with Advanced Puzzles!")
        print("Instructions:")
        print("- Use commands to move and interact")
        print("- Find items and solve both simple and advanced puzzles")
        print("- Get keys to progress through 3 rooms\n")

        while True:
            self.display_status()
            self.display_map()
            
            print("\nAvailable options:")
            print("1. Move (up/down/left/right)")
            print("2. Get item")
            print("3. Solve simple puzzle (needs item)")
            print("4. Solve advanced puzzle (logic challenge)")
            print("5. Go to next room")
            print("6. Get movement hint")
            print("7. Show complete solution")
            print("8. Exit game")
            
            choice = input("\nWhat do you want to do? ").lower()
            
            if choice in ['up', 'down', 'left', 'right']:
                self.move_player(choice)
            elif choice in ['get item', '2']:
                self.get_item()
            elif choice in ['solve simple puzzle', '3']:
                self.solve_puzzle()
            elif choice in ['solve advanced puzzle', '4']:
                self.solve_advanced_puzzle()
            elif choice in ['next room', '5']:
                if self.next_room():
                    break
            elif choice in ['get hint', '6']:
                self.get_hint()
            elif choice in ['solution', '7']:
                self.show_solution()
            elif choice in ['exit', '8']:
                print("Goodbye!")
                break
            else:
                print("Invalid option. Try again.")
            
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    game = EscapeRoomGame()
    game.main_menu()