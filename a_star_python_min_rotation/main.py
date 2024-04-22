from grid_generation import grid_generation
from grid_visualization import grid_visualization
from queue import PriorityQueue


# Heuristic Function Implementation
def h(cell1, cell2):  # Heuristic function definition using Manhattan distance
    x1, y1 = cell1
    x2, y2 = cell2
    return abs(x1 - x2) + abs(y1 - y2)


# A* Algorithm Implementation
def a_star(grid, start_cell, goal_cell, initial_direction):

    # All directions of the start cell is unpassable.
    all_zero = all(grid[start_cell][d] == 0 for d in 'EWNS')
    if all_zero:
        raise ValueError("All grid values are zero for the start cell.")

    if start_cell < (1, 1) or goal_cell < (1, 1) or start_cell > (5, 5) or goal_cell > (5, 5):
        raise ValueError("Invalid start or goal coordinates. Coordinates must be within the grid boundaries.")

    g = {cell: float('inf') for cell in grid}  # cost from start cell to current cell
    g[start_cell] = 0
    f = {cell: float('inf') for cell in grid}  # total cost
    h_start = h(start_cell, goal_cell)  # Heuristic cost from current cell to goal
    f[start_cell] = h_start

    open_list = PriorityQueue()  # Priority Queue selects th element with the lowest cost for this case
    open_list.put((h_start, h_start, start_cell, initial_direction))  # f_cost,g_cost,cell_index,initial direction
    a_path = {}
    r = 0.3  # Cost decrease if no rotation exists

    while not open_list.empty():
        _, _, current_cell, prev_dir = open_list.get()
        print("prev_dir ", prev_dir)

        if current_cell == goal_cell:
            break
        for d in 'EWNS':
            if grid[current_cell][d]:
                if d == 'E':
                    child_cell = (current_cell[0], current_cell[1] + 1)
                    from_dir = d
                elif d == 'W':
                    child_cell = (current_cell[0], current_cell[1] - 1)
                    from_dir = d
                elif d == 'N':
                    child_cell = (current_cell[0] - 1, current_cell[1])
                    from_dir = d
                elif d == 'S':
                    child_cell = (current_cell[0] + 1, current_cell[1])
                    from_dir = d

                # New g cost is just one larger than previous since no diagonal movement is done. Every movement adds
                # 1 to previous cost, g cost is cumulative and somehow explains the total movement done until the
                # current cell while h cost represents the distance remained to the goal where f cost is the sum of two.
                # Current direction is d. Aldo if no rotation exists, g is reduced by the value r.

                print(prev_dir)
                print(from_dir)
                print("Current cell:", current_cell)
                print("Child cell:", child_cell)

                new_g = g[current_cell] + 1
                if from_dir == prev_dir:
                    new_g = new_g - r

                print(new_g)
                print("------------------------------------")
                new_f = new_g + h(child_cell, goal_cell)

                # If newly cost is smaller, update the cost. This also eliminated implicitly the need for closed list.
                if new_f < f[child_cell]:
                    g[child_cell] = new_g
                    f[child_cell] = new_f
                    open_list.put((new_f, h(current_cell, child_cell), child_cell, from_dir))
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
start = (2, 4)
goal = (4, 4)
direction = 'N'
obstacle_positions = [(3.5, 1), (2, 4.5), (2.5, 4)]
grid_with_obstacles = grid_generation(grid_size, obstacle_positions)
forward_route = a_star(grid_with_obstacles, start, goal, direction)
grid_visualization(grid_with_obstacles, start, goal, forward_route)
