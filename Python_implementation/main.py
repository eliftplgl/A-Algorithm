from grid_generation import grid_generation
from grid_visualization import grid_visualization
from queue import PriorityQueue


def h(cell1, cell2):  # Heuristic function definition using Manhattan distance
    x1, y1 = cell1
    x2, y2 = cell2
    return abs(x1 - x2) + abs(y1 - y2)  # Manhattan distance between two points


def a_star(grid, start_cell, goal_cell):

    if start_cell < (1, 1) or goal_cell < (1, 1) or start_cell > (5, 5) or goal_cell > (5, 5):
        raise ValueError("Invalid start or goal coordinates. Coordinates must be within the grid boundaries.")

    g = {cell: float('inf') for cell in grid}  # cost from start cell to current cell
    g[start_cell] = 0
    f = {cell: float('inf') for cell in grid}  # total cost
    h_start = h(start_cell, goal_cell)  # Heuristic cost from current cell to goal
    f[start_cell] = h_start

    open_list = PriorityQueue()  # Priority Queue selects th element with the lowest cost for this case
    open_list.put((h_start, h_start, start_cell))  # PriQue(f_cost,g_cost,cell_index)
    a_path = {}

    while not open_list.empty():
        current_cell = open_list.get()[2]  # take the index of the element
        if current_cell == goal_cell:
            break
        for d in 'WENS':
            if grid[current_cell][d]:
                if d == 'E':
                    child_cell = (current_cell[0], current_cell[1] + 1)
                if d == 'W':
                    child_cell = (current_cell[0], current_cell[1] - 1)
                if d == 'N':
                    child_cell = (current_cell[0] - 1, current_cell[1])
                if d == 'S':
                    child_cell = (current_cell[0] + 1, current_cell[1])

                # New g cost is just one larger than previous since no diagonal movement is done. Every movement adds
                # 1 to previous cost, g cost is cumulative and somehow explains the total movement done until the
                # current cell while h cost represents the distance remained to the goal where f cost is the sum of two.

                new_g = g[current_cell] + 1
                new_f = new_g + h(child_cell, goal_cell)

                # If newly cost is smaller, update the cost. This also eliminated implicitly the need for closed list.
                if new_f < f[child_cell]:
                    g[child_cell] = new_g
                    f[child_cell] = new_f
                    open_list.put((new_f, h(child_cell, goal_cell), child_cell))
                    a_path[child_cell] = current_cell

    forward_path = {}
    cell = goal_cell
    while cell != start_cell:
        forward_path[a_path[cell]] = cell
        cell = a_path[cell]

    forward_list = [i for i in forward_path.values()]
    forward_list.append(start_cell)
    return forward_list


grid_size = 5
start = (1, 1)
goal = (4, 4)
obstacle_positions = [(3.5, 4), (3, 4.5), (4, 3.5)]
grid_with_obstacles = grid_generation(grid_size, obstacle_positions)
forward_route = a_star(grid_with_obstacles, start, goal)
grid_visualization(grid_with_obstacles, start, goal, forward_route)
