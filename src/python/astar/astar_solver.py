import heapq
import time
from collections import namedtuple

# Estado local
State = namedtuple('State', ['x', 'y', 'has_key', 'has_item', 'solved_puzzle'])

class EscapeRoomSolver:

    def __init__(self, grid_size, player_start, door_pos, item_pos, puzzle_pos, max_turns_for_this_room, has_item = False, solved_puzzle = False):
        self.grid_size = grid_size

        if not player_start or not (0 <= player_start[0] < grid_size and 0 <= player_start[1] < grid_size):
             raise ValueError(f"Invalid player start position {player_start} for grid size {grid_size}")
        self.start_pos = (player_start[0], player_start[1])
        self.door_pos = (door_pos[0], door_pos[1])
        self.item_pos = (item_pos[0], item_pos[1])
        self.puzzle_pos = (puzzle_pos[0], puzzle_pos[1])
        self.max_turns = max_turns_for_this_room
        self.has_item = has_item
        self.solved_puzzle = solved_puzzle

        
        self.start_state = State(self.start_pos[0], self.start_pos[1], self.solved_puzzle, self.has_item, self.solved_puzzle)
        
        self.goal_state_condition = lambda state: state.x == self.door_pos[0] and state.y == self.door_pos[1] and state.has_key


    def is_valid_pos(self, x, y):
      return 0 <= x < self.grid_size and 0 <= y < self.grid_size

    def manhattan_distance(self, pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    # La heuristica estima el costo restante hasta el objetivo
    def heuristic(self, state):
        current_pos = (state.x, state.y)
        
        if state.has_key:
            return self.manhattan_distance(current_pos, self.door_pos)
        
        elif state.has_item:
            dist_to_puzzle = self.manhattan_distance(current_pos, self.puzzle_pos)
            dist_puzzle_to_door = self.manhattan_distance(self.puzzle_pos, self.door_pos)
            return dist_to_puzzle + dist_puzzle_to_door
        
        else:
            dist_to_item = self.manhattan_distance(current_pos, self.item_pos)
            dist_item_to_puzzle = self.manhattan_distance(self.item_pos, self.puzzle_pos)
            dist_puzzle_to_door = self.manhattan_distance(self.puzzle_pos, self.door_pos)
            return dist_to_item + dist_item_to_puzzle + dist_puzzle_to_door


    def get_neighbors(self, state):
        neighbors = []
        x, y, has_key, has_item, solved_puzzle = state
        action_cost = 1 # Each action takes 1 turn

        for action_name, dx, dy in [('walk(up)', 0, -1), ('walk(down)', 0, 1),
                                   ('walk(left)', -1, 0), ('walk(right)', 1, 0)]:
            nx, ny = x + dx, y + dy
            if self.is_valid_pos(nx, ny):
                # Movement doesn't change item/key status directly in the state definition
                next_state = State(nx, ny, has_key, has_item, solved_puzzle)
                neighbors.append((action_name, next_state, action_cost))

        # Can pick up item if at item location and don't have it
        if (x, y) == self.item_pos and not has_item:
            # The state change reflects *having* the item after this action
            next_state = State(x, y, has_key, True, solved_puzzle)
            neighbors.append(('get_item', next_state, action_cost))

        # Can solve puzzle if at puzzle location, have item, and puzzle not solved
        if (x, y) == self.puzzle_pos and has_item and not solved_puzzle:
             # State change: gain key, lose item, puzzle is solved
             next_state = State(x, y, True, False, True)
             neighbors.append(('solve_puzzle', next_state, action_cost))

        return neighbors


    def reconstruct_path(self, came_from, current_state):
        path = []
        temp_state = current_state
        while temp_state in came_from:
            prev_state, action = came_from[temp_state]
            path.insert(0, action)
            temp_state = prev_state
        # The final action is always using the door
        path.append("use_door")
        return path


    def solve_astar(self):
        start_time = time.time()
        # g_score: cost (turns) from start to a state
        g_score = {self.start_state: 0}
        # f_score: estimated total cost (g_score + heuristic)
        initial_f_score = self.heuristic(self.start_state)
        # Priority queue stores (f_score, state)
        open_set_pq = [(initial_f_score, self.start_state)]
        heapq.heapify(open_set_pq)
        # Keep track of states in the priority queue for quick lookup
        open_set_hash = {self.start_state}
        # came_from: reconstruct path {state: (previous_state, action)}
        came_from = {}

        while open_set_pq:
            # Get state with lowest f_score
            current_f, current_state = heapq.heappop(open_set_pq)
            open_set_hash.remove(current_state)

            current_g = g_score.get(current_state, float('inf'))

            # Check if we reached the goal
            if self.goal_state_condition(current_state):
                # +1 for the final "use_door" action which isn't part of came_from path
                total_turns_in_room = current_g + 1
                if total_turns_in_room <= self.max_turns:
                    path = self.reconstruct_path(came_from, current_state)
                    end_time = time.time()
                    execution_time = end_time - start_time
                    print(f"A* algorithm execution time: {execution_time:.4f} seconds")
                    return path, total_turns_in_room
                else:
                    # Found a path, but it exceeds max turns allowed *for this A* run*
                    continue # Keep searching if other paths might be shorter

            # If current path cost already exceeds max_turns, prune this path
            if current_g + 1 > self.max_turns:
                 continue

            # Explore neighbors
            for action, neighbor_state, action_cost in self.get_neighbors(current_state):
                tentative_g_score = current_g + action_cost

                # If this path to neighbor is worse than a known path, skip
                if tentative_g_score >= g_score.get(neighbor_state, float('inf')):
                    continue

                # Check if this step *would* exceed max_turns
                # Add +1 because goal check needs one more turn ('use_door')
                if tentative_g_score + 1 > self.max_turns and not self.goal_state_condition(neighbor_state):
                    continue


                # This path is the best so far. Record it.
                came_from[neighbor_state] = (current_state, action)
                g_score[neighbor_state] = tentative_g_score
                new_f_score = tentative_g_score + self.heuristic(neighbor_state)

                # If neighbor not in open set, add it
                if neighbor_state not in open_set_hash:
                    heapq.heappush(open_set_pq, (new_f_score, neighbor_state))
                    open_set_hash.add(neighbor_state)

        end_time = time.time()
        execution_time = end_time - start_time
        print(f"A* algorithm execution time: {execution_time:.4f} seconds")
        return None, float('inf')