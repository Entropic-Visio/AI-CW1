# Name: Rezwan Rahman
# Date-Modified: 19/02/2024
# Student-ID: RAH25529097
# Purpose: An AI Program to Create A Less Wasteful Environment.

from typing import List, Tuple
from tabulate import tabulate
import heapq


class Tile:
    """
    Tiles of the Environment or the Node.
    Stores Information for Each Cell.

    Instead of 0's and 1's our matrix is made out up of tile objects which can store more.

    """

    def __init__(self, x, y) -> None:
        self.state = "clean"
        self.x_pos = x
        self.y_pos = y

    def change_state(self) -> None:
        if self.state == 'clean':
            self.state = 'waste'
        else:
            self.state = 'clean'

    def __repr__(self) -> str:
        return f"{self.x_pos, self.y_pos}\n{self.state}"


class Environment:
    """
    Environment Class
    This is the Environment where the Agent will be Traversing and Cleaning.
    The Agent Class Will be Taking the Environment Class.
    """

    def __init__(self, size) -> None:
        self.size = size
        self.environment = self.create_environment(size)

    def create_environment(self, size) -> List[List[Tile]]:
        """Creates the environment to do the cleaning operation."""
        return [[Tile(x, y) for y in range(size)] for x in range(size)]
    
    def print_environment(self) -> str:
        """Returns a string of the current environment which is foramtted in tabulate."""
        formatted_table = [[str(tile) for tile in row] for row in self.environment]
        return tabulate(formatted_table, tablefmt="grid")
    
    def change_tile_to_waste(self, coord) -> None:
        """Changes tiles from waste to clean or vice versa"""
        self.environment[coord[0]][coord[1]].change_state()

    def check_clean(self) -> bool:
        """Does a linear search to check if all are clean and returns a boolean."""
        for i in range(self.size):
            for j in range(self.size):
                if self.environment[i][j].state == "waste":
                    return False
        return True
    
    def select_waste_tile(self) -> None:
        """Select waste tiles"""

        try:
            print(self.print_environment())
            x = int(input("Enter X Coordinate Value (e.g 0..1..2..n) or -1 to Quit: "))
            y = int(input("Enter Y Coordinate Value (e.g 0..1..2..n) or -1 to Quit: "))
                
            if x == -1 or y == -1:
                return None
            
            if x < self.size and y < self.size:
                self.change_tile_to_waste((x, y))
            else:
                print("Enter Valid Number within the size of the environment, Current Size: {self.size}")
                return self.select_waste_tile()
            
            return self.change_tile_to_waste()

        except:
            print("Please Enter a Valid Integer.")
            return self.select_waste_tile()


            

class Agent:
    """
    Smart Waste Management Robot Class (Agent)

    @params: x - the current x position of the agent
    @params: y - the current y position of the agent

    The agent is using A* algorithm to optimally clean the environment.
    The A* algorithm is exteremly beneficial in this type of environment as we only have 4 directional movement.
    Up, Down, Left and Rightt"""

    def __init__(self, x, y) -> None:
        self.current_x = x
        self.current_y = y

    def manhattan_distance(self, start_tile, goal_tile) -> int:
        """
        Manhattan Distance - returns the absolute value of current tile and goal tile
        Manhatten Distance = | X1 - X2 | + | Y1 - Y2 |
        This gives us a good estimate on how to path our algorithm, and ensure that it has a cost-effective path, where distance travelled is as low as possible.
        """
        return abs(start_tile[0] - goal_tile[0]) + abs(start_tile[1] - goal_tile[1])

    def astar_search(self, start, goal, env) -> List:
        """A* search algorithm to find the optimal path to waste tiles
        """
        frontier = [(0, start)] # frontier is just a priority queue
        came_from = {} # 
        cost_so_far = {}
        came_from[start] = None
        cost_so_far[start] = 0

        while frontier:
            current_cost, current_tile = heapq.heappop(frontier)

            if current_tile == goal:
                break

            for next_tile in self.get_neighbors(current_tile, env):
                new_cost = cost_so_far[current_tile] + 1 # the cost of the movement is one
                if next_tile not in cost_so_far or new_cost < cost_so_far[next_tile]:
                    cost_so_far[next_tile] = new_cost
                    priority = new_cost + self.manhattan_distance(next_tile, goal)
                    heapq.heappush(frontier, (priority, next_tile))
                    came_from[next_tile] = current_tile

        path = self.reconstruct_path(start, goal, came_from)
        return path

    def get_neighbors(self, tile, env) -> List[Tuple]:
        """Get neighboring tiles close to the agent"""
        x, y = tile
        neighbors = []

        if x > 0:
            neighbors.append((x - 1, y))
        if x < len(env.environment) - 1:
            neighbors.append((x + 1, y))
        if y > 0:
            neighbors.append((x, y - 1))
        if y < len(env.environment[0]) - 1:
            neighbors.append((x, y + 1)) 

        return neighbors

    def reconstruct_path(self, start, goal, came_from) -> List:
        """Reconstruct path from start to goal, this backtracks from our current tile which is our goal tile.
        Then appends the path to a list and eventually reverses the list to return the path. 
        """
        current_tile = goal
        path = []

        while current_tile != start:
            path.append(current_tile)
            current_tile = came_from[current_tile]

        path.append(start)
        path.reverse()
        return path

    def clean_environment(self, env) -> None:
        """Clean the environment using A* algorithm"""
        start = (self.current_x, self.current_y)
        while not env.check_clean():

            closest_dirty_tile = self.find_closest_dirty_tile(start, env)
            
            if closest_dirty_tile:

                path_to_dirty_tile = self.astar_search(start, closest_dirty_tile, env)
                self.follow_path(path_to_dirty_tile)

                self.clean(env.environment)
                start = closest_dirty_tile

            else:
                print("Cleaning Complete")
                break

    def find_closest_dirty_tile(self, start, env):
        """
        As A* algorithm is an informed search algorithm, we must find out the closest dirty tile from the roomba.
        """
        dirty_tiles = []
        for x in range(len(env.environment)):
            for y in range(len(env.environment[0])):
                if env.environment[x][y].state == 'waste':
                    dirty_tiles.append((x, y))

        if dirty_tiles:
            # finds the cloesest dirty tile from the roomba from the given array and uses manhatten distance to evaulate it returns the tile.
            closest_dirty_tile = min(dirty_tiles, key=lambda tile: self.manhattan_distance(start, tile))
            return closest_dirty_tile
        else:
            return None

    def follow_path(self, path):
        """Follow path is an array of tuples, which moves the agent based on the list of moves present.
        It checks both the x and y values and checks if the x or y value is greater or less than the current
        x and y value of the cleaner, then performs an action based on that information.
        
        @params: path - a list of tuples which contain coordinates.
        """
        for tile in path[1:]: 
            print(env.print_environment())
            x, y = tile
            if x < self.current_x:
                self.move_up()
            elif x > self.current_x:
                self.move_down()
            elif y < self.current_y:
                self.move_left()
            elif y > self.current_y:
                self.move_right()

    def move_left(self) -> None:
        """Moves the cleaner left from current position"""
        if self.current_x < len(env.environment) - 1:
            self.current_y -= 1
            print(f"Moved Left To: {self.current_x}, {self.current_y}")

    def move_right(self) -> None:
        """Moves the cleaner right from current position"""
        if self.current_y < len(env.environment[0]) - 1:
            self.current_y += 1
            print(f"Moved Right To: {self.current_x}, {self.current_y}")

    def move_up(self) -> None:
        """Moves the cleaner up from current position"""
        if self.current_x > 0:
            self.current_x -= 1
            print(f"Moved Up To: {self.current_x}, {self.current_y}")

    def move_down(self) -> None:
        """Moves cleaner down from current position"""
        if self.current_x < len(env.environment) - 1:
            self.current_x += 1
            print(f"Moved Down To: {self.current_x}, {self.current_y}")

    def clean(self, env) -> None:
        """Cleans the current tile the cleaner is on using the change state function which is a method in tile object."""
        env[self.current_x][self.current_y].change_state()
        print(f"Cleaned: {self.current_x}, {self.current_y}")


def get_environment_size() -> int:
    """Gets enivronment size from user"""
    while True:
        try:
            env_size = int(input("Enter Environment Size (e.g 2, 3, 4, 5): "))

            if env_size > 5 or env_size < 2:
                print("Invalid environment size must be inbetween 1 and 6.")
            else:
                return env_size
            
        except:
            print("Invalid Integer.")


def get_cleaner_position(env_size) -> int:
    """Gets cleaner position from user..."""
    while True:
        try:
            x = int(input("Enter X Coordinate: "))
            y = int(input("Enter Y Coordinate: "))

            if x > env_size-1 or x < 0 and y > env_size-1 and y < 0:
                print(f"Coordinates must be (0,0) -> ({env.size-1, env.size-1})")
            else:
                return x, y
            
        except:
            print("Invalid Integer.")
    

if __name__ == "__main__":

    env_size = get_environment_size() # get environment size from user
    cleaner_x, cleaner_y = get_cleaner_position(env_size) # get x, y position of the cleaner
    
    env = Environment(env_size) # Define environment_size 

    cleaner = Agent(cleaner_x, cleaner_y)  # Agent Class A* Algorithm

    env.select_waste_tile() # select the waste which is user prompted

    cleaner.clean_environment(env) # clean the environment

    print(env.print_environment()) # print the clean environment
    

    if env.check_clean() == True: # checks if environment is clean and operation is successful. 
        print("Successfully Cleaned the Environment.")
    else:
        print("Failed to Clean the Environment.")
