# Name: Rezwan Rahman
# Date-Modified: 01/02/2024
# Student-ID: RAH25520907

from typing import List
from tabulate import tabulate

class Tile:
    """
    Tile Class
    Defines the indiviual tiles/cells inside the environment. They can either be dirty or waste.
    """
    
    def __init__(self, x, y) -> None:
        self.state = 'clean'
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
    Environment Class.
    Defines the environment which the agent will traverse. 

    """
    def __init__(self, size) -> None:
        self.size = size
        self.environment = self.create_environment(size)

    def create_environment(self, size) -> List[List[Tile]]:
        grid = [[Tile(x, y) for y in range(size)] for x in range(size)]
        return grid

    def print_environment(self):
        formatted_table = [[str(tile) for tile in row] for row in self.environment]
        print(tabulate(formatted_table, tablefmt="grid"))
    
    def dirty_tile_selection(self, x, y):
        self.environment[x][y].change_state()


class Agent:
    """
    The Smart Waste Management Robot Class (Agent)
    
    """
    def __init__(self, x, y) -> None:
        self.current_x = x
        self.current_y = y
    
    def manhatten_distance(self, goal_distance) -> None:
        distance_cost = abs(self.current_x - goal_distance[0]) + abs(self.current_y - goal_distance[1])
        return distance_cost

    def move_left(self, env) -> None:
        if self.current_y > 0:
            self.current_y -= 1
            print(f"Moved Left To: {self.current_x}, {self.current_y}")
    
    def move_right(self, env) -> None:
        if self.current_y < len(env[0]) - 1:
            self.current_y += 1
            print(f"Moved Right To: {self.current_x}, {self.current_y}")
    
    def move_up(self, env) -> None:
        if self.current_x > 0:
            self.current_x -= 1
            print(f"Moved Up To: {self.current_x}, {self.current_y}")
    
    def move_down(self, env) -> None:
        if self.current_x < len(env) - 1:
            self.current_x += 1
            print(f"Moved Down To: {self.current_x}, {self.current_y}")
    
    def clean(self, env) -> None:
        env[self.current_x][self.current_y].change_state()
        print(f"Cleaned: {self.current_x}, {self.current_y}")


if __name__ == "__main__":
    env = Environment(5)
    cleaner = Agent(0, 0)
    env.dirty_tile_selection(0, 1)
    env.print_environment()

    print(cleaner.manhatten_distance((2, 2)))

    cleaner.move_right(env.environment) # clean using cleaner
    cleaner.clean(env.environment) # clean the environment.
    cleaner.move_down(env.environment) # move down
    cleaner.move_left(env.environment)
    env.print_environment() # output the environment