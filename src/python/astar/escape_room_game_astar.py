import time
from . import astar_solver

def is_valid_coordinate(x, y, grid_size):
    return 0 <= x < grid_size and 0 <= y < grid_size

def get_coordinate_input(prompt, grid_size, occupied_positions):
    while True:
        try:
            coord_str = input(f"{prompt} (format: x,y): ")
            x_str, y_str = coord_str.split(',')
            x, y = int(x_str.strip()), int(y_str.strip())

            if not is_valid_coordinate(x, y, grid_size):
                print(f"Error: Position ({x},{y}) is outside the grid (0-{grid_size-1}).")
                continue

            if (x, y) in occupied_positions:
                print(f"Error: Position ({x},{y}) is already occupied. Choose a different location.")
                continue

            return (x, y)
        except ValueError:
            print("Invalid format. Please enter coordinates as x,y (e.g., 2,3).")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


def get_user_input_room(room_name):
    occupied_positions = set()

    while True:
        try:
            grid_size = int(input(f"Enter grid size for room {room_name} (minimum 2x2): "))
            if grid_size < 2:
                print("Grid size must be at least 2.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter an integer.")

    print(f"--- Defining positions for Room {room_name} (Grid: {grid_size}x{grid_size}) ---")

    player_start = get_coordinate_input("Enter player start position", grid_size, occupied_positions)
    occupied_positions.add(player_start)

    door_pos = get_coordinate_input("Enter door position", grid_size, occupied_positions)
    occupied_positions.add(door_pos)

    item_pos = get_coordinate_input("Enter item position", grid_size, occupied_positions)
    occupied_positions.add(item_pos)

    puzzle_pos = get_coordinate_input("Enter puzzle position", grid_size, occupied_positions)
    occupied_positions.add(puzzle_pos)

    while True:
        try:
            max_turns = int(input(f"Enter maximum turns for room {room_name}: "))
            if max_turns <= 0:
                print("Maximum turns must be a positive integer.")
                continue

            print("Checking if room is solvable with the given turns...")
            # Pass max_turns as max_turns_for_this_room
            solver_check = astar_solver.EscapeRoomSolver(grid_size, player_start, door_pos, item_pos, puzzle_pos, max_turns, False, False)
            path, turns_needed = solver_check.solve_astar()

            if path:
                print(f"Room configuration valid. Optimal solution requires {turns_needed} turns (within {max_turns}).")
                return grid_size, player_start, door_pos, item_pos, puzzle_pos, max_turns
            else:
                print(f"Room cannot be optimally solved within {max_turns} turns from the start. Try a higher value.")
        except ValueError:
            print("Invalid input. Please enter an integer.")
        except Exception as e:
            print(f"An error occurred during solvability check: {e}")


def draw_grid(grid_size, player_pos, door_pos, item_pos, puzzle_pos, has_item, solved_puzzle):
    grid = [['.' for _ in range(grid_size)] for _ in range(grid_size)]

    grid[door_pos[1]][door_pos[0]] = 'D'

    if not has_item and not solved_puzzle:
        if player_pos != item_pos:
            grid[item_pos[1]][item_pos[0]] = 'I'
    if not solved_puzzle:
        if player_pos != puzzle_pos:
            grid[puzzle_pos[1]][puzzle_pos[0]] = '?'

    if player_pos:
        grid[player_pos[1]][player_pos[0]] = 'P'

    print("-" * (grid_size * 2 + 1))
    for row in grid:
        print(f"|{' '.join(row)}|")
    print("-" * (grid_size * 2 + 1))


def get_next_move_hint(solver):
    # Pass the correct parameter name to the solver
    path, turns_needed = solver.solve_astar()

    if path and turns_needed != float('inf') and len(path) > 0:
         if len(path) == 1 and path[0] == "use_door":
              return "use_door (You should be able to exit!)"
         elif len(path) > 0:
              return path[0]
    else:
        if solver.start_state.x == solver.door_pos[0] and solver.start_state.y == solver.door_pos[1] and solver.start_state.has_key:
             return "You are at the door with the key! Use the door."
        return "No solution found from the current state within remaining turns."


def solve_all_autopilot(room_configs, start_room_index, initial_player_pos, initial_has_item, initial_solved_puzzle, initial_turns_used_in_current_room):
    print("\n--- AUTOPILOT ENGAGED ---")

    current_player_pos = initial_player_pos
    current_has_item = initial_has_item
    current_solved_puzzle = initial_solved_puzzle

    for i in range(start_room_index, len(room_configs)):
        room_config = room_configs[i]
        room_name = room_config['name']
        grid_size = room_config['grid']

        if i > start_room_index:
            current_player_pos = room_config['start']
            current_has_item = False
            current_solved_puzzle = False

        door_pos = room_config['door']
        item_pos = room_config['item']
        puzzle_pos = room_config['puzzle']
        max_turns_for_room = room_config['max_turns']

        if i == start_room_index:
            turns_already_used = initial_turns_used_in_current_room
        else:
            turns_already_used = 0

        remaining_turns = max_turns_for_room - turns_already_used
        if remaining_turns <= 0:
             print(f"\nCannot continue autopilot. No turns left to start Room {room_name}.")
             return False

        print(f"\n--- Solving Room {room_name} (Max Turns: {max_turns_for_room}, Remaining: {remaining_turns}) ---")
        print(f"Starting State: Pos={current_player_pos}, Item={current_has_item}, Key={current_solved_puzzle}")
        draw_grid(grid_size, current_player_pos, door_pos, item_pos, puzzle_pos, current_has_item, current_solved_puzzle)

        # Pass max_turns correctly
        solver = astar_solver.EscapeRoomSolver(
            grid_size, current_player_pos, door_pos, item_pos, puzzle_pos,
            remaining_turns, # A* limit is the remaining turns
            current_has_item, current_solved_puzzle
        )
        path, turns_needed = solver.solve_astar()

        if path is None or turns_needed == float('inf'):
            print(f"\nAutopilot failed. Cannot find a solution for Room {room_name} (A* returned no path within {remaining_turns} turns).")
            return False
        elif turns_needed > remaining_turns:
             print(f"\nAutopilot failed. Optimal path requires {turns_needed} turns, but only {remaining_turns} remain for Room {room_name}.")
             return False

        print(f"Optimal path found ({turns_needed} actions/turns): {' -> '.join(path)}")
        time.sleep(1)

        simulated_turns_count_in_room = turns_already_used
        for action_index, action in enumerate(path):
            simulated_turns_count_in_room += 1
            print(f"\nStep {action_index + 1}/{len(path)}: Action: {action} (Turn {simulated_turns_count_in_room}/{max_turns_for_room})")

            if action.startswith('walk'):
                if action.endswith('(up)'): current_player_pos = (current_player_pos[0], current_player_pos[1] - 1)
                elif action.endswith('(down)'): current_player_pos = (current_player_pos[0], current_player_pos[1] + 1)
                elif action.endswith('(left)'): current_player_pos = (current_player_pos[0] - 1, current_player_pos[1])
                elif action.endswith('(right)'): current_player_pos = (current_player_pos[0] + 1, current_player_pos[1])
            elif action == 'get_item':
                current_has_item = True
                print("Item acquired!")
            elif action == 'solve_puzzle':
                current_has_item = False
                current_solved_puzzle = True
                print("Puzzle solved! Key acquired.")
            elif action == 'use_door':
                print(f"Using door to exit Room {room_name}...")

            draw_grid(grid_size, current_player_pos, door_pos, item_pos, puzzle_pos, current_has_item, current_solved_puzzle)
            time.sleep(0.8)

        print(f"Room {room_name} cleared by autopilot.")

    print("\n--- AUTOPILOT COMPLETED SUCCESSFULLY ---")
    return True


def run_game():
    room_configs = []
    room_names = ['A', 'B', 'C']

    for room_name in room_names:
        print(f"\n--- Room {room_name} Configuration ---")
        grid_size, player_start, door, item, puzzle, max_turns = get_user_input_room(room_name)
        room_configs.append({
            'name': room_name, 'grid': grid_size, 'start': player_start,
            'door': door, 'item': item, 'puzzle': puzzle, 'max_turns': max_turns,
        })

    current_room_index = 0
    player_pos = room_configs[0]['start']
    has_item = False
    solved_puzzle = False
    turns_in_room = 0
    total_turns_overall = 0

    while current_room_index < len(room_configs):
        current_room = room_configs[current_room_index]
        room_name = current_room['name']
        grid_size = current_room['grid']
        door_pos = current_room['door']
        item_pos = current_room['item']
        puzzle_pos = current_room['puzzle']
        max_turns = current_room['max_turns']

        print(f"\n=== Entering Room {room_name} ===")
        print(f"Objective: Get item at {item_pos}, solve puzzle at {puzzle_pos}, exit via door at {door_pos}")
        print(f"Starting at: {player_pos}")
        print(f"Max Turns for this room: {max_turns}")

        while True:
            draw_grid(grid_size, player_pos, door_pos, item_pos, puzzle_pos, has_item, solved_puzzle)
            print(f"Room: {room_name} | Turns Used: {turns_in_room}/{max_turns} | Item: {'Yes' if has_item else 'No'} | Key: {'Yes' if solved_puzzle else 'No'}")
            print("Actions: [up, down, left, right], help, solve_all, quit")

            # Check loss condition *before* input, allowing win on last turn
            if turns_in_room >= max_turns and not (player_pos == door_pos and solved_puzzle):
                 print("\nGame Over: You ran out of turns in this room.")
                 return

            action = input("Enter action: ").lower().strip()

            new_player_pos = player_pos
            moved = False
            turn_cost_move = 0
            turn_cost_interaction = 0 # Reset interaction cost each cycle

            if action in ['up', 'down', 'left', 'right']:
                dx, dy = 0, 0
                if action == 'up': dy = -1
                elif action == 'down': dy = 1
                elif action == 'left': dx = -1
                elif action == 'right': dx = 1

                potential_pos = (player_pos[0] + dx, player_pos[1] + dy)
                if is_valid_coordinate(potential_pos[0], potential_pos[1], grid_size):
                    new_player_pos = potential_pos
                    moved = True
                    turn_cost_move = 1
                else:
                     print("Invalid move: Cannot move outside the grid.")
                     continue

            elif action == 'help':
                print("Calculating hint...")
                remaining_turns_for_hint = max_turns - turns_in_room
                if remaining_turns_for_hint > 0:
                    # Pass max_turns correctly
                    hint_solver = astar_solver.EscapeRoomSolver(
                        grid_size, player_pos, door_pos, item_pos, puzzle_pos,
                        remaining_turns_for_hint, # Limit A* to remaining turns
                        has_item, solved_puzzle
                    )
                    hint = get_next_move_hint(hint_solver)
                    print(f"Hint: The next optimal move might be '{hint}'.")
                else:
                    print("Hint: No turns remaining!")
                continue

            elif action == 'solve_all':
                success = solve_all_autopilot(
                    room_configs, current_room_index, player_pos,
                    has_item, solved_puzzle, turns_in_room
                )
                if success: print("\nGame finished via autopilot.")
                else: print("\nAutopilot could not complete the game from the current state.")
                return

            elif action == 'quit':
                print("Quitting game. Thanks for playing!")
                return
            else:
                print(f"Unknown action: '{action}'. Please use valid actions.")
                continue

            # --- Update State After Action ---
            if turn_cost_move > 0:
                # Apply movement cost first
                turns_in_room += turn_cost_move
                total_turns_overall += turn_cost_move
                player_pos = new_player_pos
                print(f"Moved to {player_pos}. Turn {turns_in_room}/{max_turns}")

                if player_pos == item_pos and not has_item and not solved_puzzle:
                     has_item = True
                     turn_cost_interaction = 1 # Item pickup costs extra turn
                     print(f"Picked up the item! (Costs {turn_cost_interaction} extra turn)")
                elif player_pos == puzzle_pos and has_item and not solved_puzzle:
                     solved_puzzle = True
                     has_item = False
                     turn_cost_interaction = 1
                     print(f"Solved the puzzle! Key acquired. (Costs {turn_cost_interaction} extra turn)")

                # Apply interaction cost if any
                if turn_cost_interaction > 0:
                    turns_in_room += turn_cost_interaction
                    total_turns_overall += turn_cost_interaction
                    print(f"Turn count after interaction: {turns_in_room}/{max_turns}")

                # Check for game over immediately after ALL turn costs for the action are applied
                if turns_in_room > max_turns:
                    draw_grid(grid_size, player_pos, door_pos, item_pos, puzzle_pos, has_item, solved_puzzle)
                    print(f"Room: {room_name} | Turns Used: {turns_in_room}/{max_turns} | Item: {'Yes' if has_item else 'No'} | Key: {'Yes' if solved_puzzle else 'No'}")
                    print("\nGame Over: Ran out of turns after action.")
                    return

                # Check for winning condition AFTER interaction costs
                if player_pos == door_pos and solved_puzzle:
                    door_use_cost = 1
                    print(f"Using the door... (Costs {door_use_cost} extra turn)")
                    turns_in_room += door_use_cost
                    total_turns_overall += door_use_cost
                    print(f"Turn count after using door: {turns_in_room}/{max_turns}")

                    # Check if using the door exceeded turns
                    if turns_in_room > max_turns:
                         draw_grid(grid_size, player_pos, door_pos, item_pos, puzzle_pos, has_item, solved_puzzle)
                         print(f"Room: {room_name} | Turns Used: {turns_in_room}/{max_turns} | Item: {'Yes' if has_item else 'No'} | Key: {'Yes' if solved_puzzle else 'No'}")
                         print("\nGame Over: Ran out of turns using the door.")
                         return

                    # If still within limits, proceed to next room
                    print(f"\n*** Room {room_name} Cleared! ***")
                    print(f"Exiting room. Total turns in room: {turns_in_room}")

                    current_room_index += 1
                    if current_room_index < len(room_configs):
                        player_pos = room_configs[current_room_index]['start']
                        has_item = False
                        solved_puzzle = False
                        turns_in_room = 0
                        break # Break inner loop, continue to next room
                    else:
                        print("\n*** Congratulations! You have escaped all the rooms! ***")
                        print(f"Total turns overall: {total_turns_overall}")
                        return # Game finished
