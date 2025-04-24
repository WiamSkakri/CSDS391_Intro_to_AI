# Imports
import random
import sys
import heapq
import math
import pandas as pd
from tabulate import tabulate
import os
 
class EightPuzzle:
    # This method is to initialize the puzzle to the default solved state
    def __init__(self):
        self.state = [0, 1, 2, 3, 4, 5, 6, 7, 8 ]
        self.rng = random.Random()
    
    # This method set the state of the 8-puzzle to a new passed state
    def set_state(self, new_state):
        if len(new_state) != 9:
            print("Error! Invalid input state. Too few or too many arguments")
            return False
        self.state = new_state
        return True
    
    
    
    # This method is used to print the code in a 3x3 matrix
    def print_state(self):
        for i in range(0, 9, 3):
            print(' | '.join(map(str, self.state[i:i+3])))
            if i < 6:  # Add a line after every row except the last
             print('-' * 9)

    # Helper Method to find the index of the empty tile
    def find_blank(self):
        #Find the index of the blank tile (0)
        return self.state.index(0)
    
    # This command moves the tiles if it is a valid move
    def move(self, direction):
        #Move the blank tile in the specified direction
        blank_index = self.find_blank()
        moves = {
            'up': lambda i: i - 3 if i >= 3 else None,
            'down': lambda i: i + 3 if i < 6 else None,
            'left': lambda i: i - 1 if i % 3 > 0 else None,
            'right': lambda i: i + 1 if i % 3 < 2 else None
        }

        if direction not in moves:
            print("Error: Invalid move")
            return False

        new_index = moves[direction](blank_index)
        if new_index is None:
            print("Error: Invalid move")
            return False

        # Swap blank with adjacent tile
        self.state[blank_index], self.state[new_index] = self.state[new_index], self.state[blank_index]
        return True

    # This helper method sets the seed
    def set_seed(self, seed):
        #Set the random number generator seed
        self.rng.seed(seed)
    
    # Scramble the puzzle state with n random moves. Retry invalid moves silently.
    def scramble_state(self, n):
        
        self.state = [0, 1, 2, 3, 4, 5, 6, 7, 8]  # Reset to goal state
        possible_moves = ['up', 'down', 'left', 'right']
        
        for _ in range(n):
            valid_move = False
            for _ in range(10):  # Retry up to 10 times for a valid move
                move = self.rng.choice(possible_moves)
                if self.move(move):
                    valid_move = True
                    break
            if not valid_move:
                continue  # Skip errors during scrambling

    # This method solves the puzzle using Breath First Search Algorithm
    def solve_bfs(self, max_nodes=1000):
        from collections import deque
        
        goal_state = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        
        if self.state == goal_state:
            print("Nodes created during search: 1")
            print("Solution length: 0")
            print("Move sequence:")
            return True
        
        # Use set for faster lookup
        visited = set()
        nodes_created = 0
        
        # Store state, path, and moves
        queue = deque([(self.state.copy(), [])])
        
        # Moves in specified order
        moves = ['left', 'right', 'up', 'down']
        
        while queue and nodes_created < max_nodes:
            current_state, move_sequence = queue.popleft()
            
            # Efficient state representation for visited check
            state_key = tuple(current_state)
            
            if state_key in visited:
                continue
            
            visited.add(state_key)
            nodes_created += 1
            
            if current_state == goal_state:
                print(f"Nodes created during search: {nodes_created}")
                print(f"Solution length: {len(move_sequence)}")
                print("Move sequence:")
                for move in move_sequence:
                    print(move)
                return move_sequence, nodes_created
            
            # Generate successor states more efficiently
            blank_index = current_state.index(0)
            
            for move in moves:
                new_blank_index = {
                    'up': blank_index - 3 if blank_index >= 3 else None,
                    'down': blank_index + 3 if blank_index < 6 else None,
                    'left': blank_index - 1 if blank_index % 3 > 0 else None,
                    'right': blank_index + 1 if blank_index % 3 < 2 else None
                }[move]
                
                if new_blank_index is not None:
                    new_state = current_state.copy()
                    new_state[blank_index], new_state[new_blank_index] = new_state[new_blank_index], new_state[blank_index]
                    
                    new_state_key = tuple(new_state)
                    if new_state_key not in visited:
                        queue.append((new_state, move_sequence + [move]))
        
        print(f"Error: maxnodes limit ({max_nodes}) reached")
        return False
    
    # This method solves the puzzle using Depth First Search Algorithm
    def solve_dfs(self, max_nodes=1000, depth_limit=31):
        from collections import deque

        goal_state = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        if self.state == goal_state:
            print("Nodes created during search: 1")
            print("Solution length: 0")
            print("Move sequence:")
            return True

        # Use a set for O(1) lookup time for visited states
        visited = set()
        nodes_created = 0
        
        # Stack stores (state, path, depth)
        stack = [(tuple(self.state), [], 0)]

        # Move order: left, right, up, down (as required)
        moves = ['left', 'right', 'up', 'down']

        while stack and nodes_created < max_nodes:
            state_tuple, move_sequence, depth = stack.pop()

            # Skip visited states & avoid exceeding depth limit
            if state_tuple in visited or depth > depth_limit:
                continue

            visited.add(state_tuple)
            nodes_created += 1

            if list(state_tuple) == goal_state:
                print(f"Nodes created during search: {nodes_created}")
                print(f"Solution length: {len(move_sequence)}")
                print("Move sequence:")
                for move in move_sequence:
                    print(f"move {move}")
                return move_sequence, nodes_created

            # Generate successor states efficiently
            blank_index = state_tuple.index(0)

            for move in moves:
                new_blank_index = {
                    'up': blank_index - 3 if blank_index >= 3 else None,
                    'down': blank_index + 3 if blank_index < 6 else None,
                    'left': blank_index - 1 if blank_index % 3 > 0 else None,
                    'right': blank_index + 1 if blank_index % 3 < 2 else None
                }[move]

                if new_blank_index is not None:
                    new_state = list(state_tuple)
                    new_state[blank_index], new_state[new_blank_index] = new_state[new_blank_index], new_state[blank_index]

                    new_state_tuple = tuple(new_state)
                    if new_state_tuple not in visited:
                        stack.append((new_state_tuple, move_sequence + [move], depth + 1))

        print(f"Error: maxnodes limit ({max_nodes}) reached or depth limit exceeded")
        return False
    
    # This method uses the A* search to solve the puzzle
    def solve_astar(self, heuristic="h1", max_nodes=1000):
        goal_state = [0, 1, 2, 3, 4, 5, 6, 7, 8]

        def h(state):
            """Calculate the heuristic value based on the chosen heuristic."""
            if heuristic == "h1":  # Number of misplaced tiles
                return sum(1 for i, tile in enumerate(state) if tile != 0 and tile != goal_state[i])
            elif heuristic == "h2":  # Sum of Manhattan distances
                return sum(abs((tile // 3) - (i // 3)) + abs((tile % 3) - (i % 3)) for i, tile in enumerate(state) if tile != 0)
            else:
                raise ValueError(f"Invalid heuristic: {heuristic}")

        if self.state == goal_state:
            print("Nodes created during search: 1")
            print("Solution length: 0")
            print("Move sequence:")
            return move_sequence, nodes_created

        moves = ['left', 'right', 'up', 'down']
        visited = set()
        nodes_created = 0

        # Priority queue stores (priority, g, state, move_sequence)
        pq = []
        initial_priority = h(self.state)
        heapq.heappush(pq, (initial_priority, 0, self.state.copy(), []))

        while pq and nodes_created < max_nodes:
            priority, g, current_state, move_sequence = heapq.heappop(pq)

            state_key = tuple(current_state)
            if state_key in visited:
                continue

            visited.add(state_key)
            nodes_created += 1

            if current_state == goal_state:
                print(f"Nodes created during search: {nodes_created}")
                print(f"Solution length: {len(move_sequence)}")
                print("Move sequence:")
                for move in move_sequence:
                    print(f"move {move}")
                return move_sequence, nodes_created

            blank_index = current_state.index(0)

            for move in moves:
                new_blank_index = {
                    'up': blank_index - 3 if blank_index >= 3 else None,
                    'down': blank_index + 3 if blank_index < 6 else None,
                    'left': blank_index - 1 if blank_index % 3 > 0 else None,
                    'right': blank_index + 1 if blank_index % 3 < 2 else None
                }[move]

                if new_blank_index is not None:
                    new_state = current_state.copy()
                    new_state[blank_index], new_state[new_blank_index] = new_state[new_blank_index], new_state[blank_index]

                    new_state_key = tuple(new_state)
                    if new_state_key not in visited:
                        new_g = g + 1
                        new_priority = new_g + h(new_state)
                        heapq.heappush(pq, (new_priority, new_g, new_state, move_sequence + [move]))

        print(f"Error: maxnodes limit ({max_nodes}) reached")
        return False
    
    # This method calculates the Effective Branching Factor using an iterative approach using binary search method (considered Newton's method before)
    def effective_branching_factor(self, N, d, tolerance=1e-6):
    
        if d == 0:
            return 0  # No branching if depth is zero

        low, high = 1, N  # b* is at least 1 and at most N
        
        while high - low > tolerance:
            mid = (low + high) / 2
            try:
                # Compute sum of geometric series (bounded to avoid overflow)
                computed_N = sum(mid ** i for i in range(d + 1))
                if computed_N < N + 1:
                    low = mid
                else:
                    high = mid
            except OverflowError:
                high = mid  # If overflow occurs, reduce the upper bound

        return round(mid, 6)  # Return rounded result for readability
    
    # This method creates a table to compare the effective branching factor of BFS, DFS, and A-star search with both h1 and h2
    def compare_search_algorithms(self, bfs_maxnodes, dfs_depth_limit, dfs_maxnodes, astar_h1_maxnodes, astar_h2_maxnodes):
        
        search_algorithms = {
            "BFS": lambda: self.solve_bfs(max_nodes=bfs_maxnodes),
            "DFS": lambda: self.solve_dfs(max_nodes=dfs_maxnodes, depth_limit=dfs_depth_limit),
            "A*(h1)": lambda: self.solve_astar(heuristic='h1', max_nodes=astar_h1_maxnodes),
            "A*(h2)": lambda: self.solve_astar(heuristic='h2', max_nodes=astar_h2_maxnodes)
        }
        
        results = []
        for name, algorithm in search_algorithms.items():
            result = algorithm()  # Run search algorithm
        
            if not result:
                move_sequence, nodes_created = [], 0  # Default values for failed searches
            else:
                move_sequence, nodes_created = result  # Extract move sequence and nodes generated
            d = len(move_sequence) if move_sequence else 0
            b_star = self.effective_branching_factor(nodes_created, d)
            results.append((name, nodes_created, d, b_star, move_sequence))
        
        return results
    

    # Displaying
    def display_comparison_table(self, results):
        # Initialize data structures
        move_lengths = {"BFS": [], "DFS": [], "A*(h1)": [], "A*(h2)": []}
        nodes_created = {"BFS": [], "DFS": [], "A*(h1)": [], "A*(h2)": []}
        b_star_values = {"BFS": [], "DFS": [], "A*(h1)": [], "A*(h2)": []}

        # Populate data
        for result in results:
            algo, nodes, move_sequence_length, b_star, _ = result  # move_sequence_length = len(move_sequence)
            move_lengths[algo].append(move_sequence_length)
            nodes_created[algo].append(nodes)
            b_star_values[algo].append(b_star)

        # Create table as a list of rows
        table = [
            ["d"] + [move_lengths[algo] for algo in ["BFS", "DFS", "A*(h1)", "A*(h2)"]],
            ["Nodes Created"] + [nodes_created[algo] for algo in ["BFS", "DFS", "A*(h1)", "A*(h2)"]],
            ["b*"] + [b_star_values[algo] for algo in ["BFS", "DFS", "A*(h1)", "A*(h2)"]],
        ]

        # Convert to DataFrame for formatting
        df = pd.DataFrame(table, columns=["Metric", "BFS", "DFS", "A*(h1)", "A*(h2)"])

        # Display the formatted table
        print(tabulate(df, headers="keys", tablefmt="grid", showindex=False))
        
       

        

    # Adding cmd functionality to the code
    # This method parses a command string and executes the corresponding method
    # The string representing the command: (e.g., "setState 1 2 3 4 5 6 7 8 0")
    def cmd(self, command_string):
        # Parse and execute a command
        # Ignore empty lines and comments
        if not command_string or command_string.startswith('#'):
            if command_string:
                print(command_string)
            return True

        # Split command and arguments
        parts = command_string.split()

        try:
            if parts[0] == 'setState':
                # Expect 9 arguments after 'setState'
                if len(parts) != 10:
                    print("Error: invalid puzzle state")
                    return False
                state = [int(x) for x in parts[1:]]
                return self.set_state(state)
            
            elif parts[0] == 'printState':
                self.print_state()
                return True
            
            elif parts[0] == 'move':
                if len(parts) != 2:
                    print("Error: Invalid move")
                    return False
                return self.move(parts[1])
            
            elif parts[0] == 'scrambleState':
                if len(parts) != 2:
                    print("Error: invalid command")
                    return False
                self.scramble_state(int(parts[1]))
                return True
            
            elif parts[0] == 'setSeed':
                if len(parts) != 2:
                    print("Error: invalid command")
                    return False
                self.set_seed(int(parts[1]))
                return True
            
            elif parts[0] == 'solve':
                if len(parts) > 1:
                    if parts[1] == 'BFS':
                        max_nodes = 1000
                        if len(parts) > 2 and parts[2].startswith('maxnodes='):
                            max_nodes = int(parts[2].split('=')[1])
                        return self.solve_bfs(max_nodes)

                    elif parts[1] == 'DFS':
                        max_nodes = 1000
                        depth_limit = 31

                        for param in parts[2:]:
                            if param.startswith('maxnodes='):
                                max_nodes = int(param.split('=')[1])
                            elif param.startswith('depthlimit='):
                                depth_limit = int(param.split('=')[1])

                        return self.solve_dfs(max_nodes, depth_limit)

                    elif parts[1] == 'A*':
                        heuristic = "h1"
                        max_nodes = 1000

                        for param in parts[2:]:
                            if param.startswith('heuristic='):
                                heuristic = param.split('=')[1]
                            elif param.startswith('maxnodes='):
                                max_nodes = int(param.split('=')[1])

                        return self.solve_astar(heuristic, max_nodes)
                    
            
            elif parts[0] == 'effectiveBranchingFactor':
                if len(parts) != 3:
                    print("Error: invalid command. Usage: effectiveBranchingFactor <nodes_generated> <solution_depth>")
                    return False
    
                nodes_generated = int(parts[1])
                solution_depth = int(parts[2])
                b_star = self.effective_branching_factor(nodes_generated, solution_depth)
                print(f"Effective Branching Factor: {b_star}")
                return True
            

            elif parts[0] == 'compareSearch':
                bfs_maxnodes = 10000
                dfs_depth_limit = 20000
                dfs_maxnodes = 10000000000
                astar_h1_maxnodes = 10000
                astar_h2_maxnodes = 10000
                
                for param in parts[1:]:
                    if param.startswith('bfs_maxnodes='):
                        bfs_maxnodes = int(param.split('=')[1])
                    elif param.startswith('dfs_depth_limit='):
                        dfs_depth_limit = int(param.split('=')[1])
                    elif param.startswith('dfs_maxnodes='):
                        dfs_maxnodes = int(param.split('=')[1])
                    elif param.startswith('astar_h1_maxnodes='):
                        astar_h1_maxnodes = int(param.split('=')[1])
                    elif param.startswith('astar_h2_maxnodes='):
                        astar_h2_maxnodes = int(param.split('=')[1])
                
                results = self.compare_search_algorithms(
                    bfs_maxnodes=bfs_maxnodes,
                    dfs_depth_limit=dfs_depth_limit,
                    dfs_maxnodes=dfs_maxnodes,
                    astar_h1_maxnodes=astar_h1_maxnodes,
                    astar_h2_maxnodes=astar_h2_maxnodes
                )
                
                self.display_comparison_table(results)
                return True
            elif parts[0] == 'clear':
                # Clear the terminal screen
                os.system('cls' if os.name == 'nt' else 'clear')
                return True
        

            
            else:
                print(f"Error: invalid command: {command_string}")
                return False
            
        
        except ValueError:
            print(f"Error: invalid command: {command_string}")
            return False
        
    # This method reads commands from files
    def cmd_file(self, filename):
       
        try:
            with open(filename, 'r') as file:
                for line in file:
                    line = line.strip()  # Remove leading/trailing whitespace
                    print(line)  # Always print the command or comment
                    
                    # Handle empty lines and comments
                    if not line or line.startswith('#'):
                        continue
                    
                    # Attempt to execute the command
                    success = self.cmd(line)
                    
                    # Print error message if command execution failed
                    if not success:
                        print(f"Error: Command failed: {line}")
        except FileNotFoundError:
            print(f"Error: File {filename} not found")


# # Main method
# # Only when the code is executed directly and not imported to another module
def main():
    
    # Create puzzle instance
    puzzle = EightPuzzle()

    # If no arguments provided, start interactive mode
    if len(sys.argv) == 1:
        print("Interactive mode. Enter commands (type 'quit' to exit):")
        while True:
            command = input("> ")
            if command.lower() == 'quit':
                break
            puzzle.cmd(command)
    # If a file is provided as an argument
    elif len(sys.argv) == 2:
        puzzle.cmd_file(sys.argv[1])
    
    else:
        print("Usage: python EightPuzzle.py [command_file]")

# # Ensure the main method is called only when the script is run directly
if __name__ == "__main__":
   main()  
    


    
