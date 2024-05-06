from grid_generation import divide_grid_into_areas, generate_target_sequence
from grid_generation import grid_generation
from grid_animation import grid_visualization
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

    if start_cell < (0, 0) or goal_cell < (0, 0) or start_cell > (grid_size - 1, grid_size - 1) or goal_cell > (
    grid_size - 1, grid_size - 1):
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

                new_g = g[current_cell] + 1
                if from_dir == prev_dir:
                    new_g = new_g - r

                new_f = new_g + h(child_cell, goal_cell)

                # If newly cost is smaller, update the cost. This also eliminated implicitly the need for closed list.
                if new_f < f[child_cell]:
                    g[child_cell] = new_g
                    f[child_cell] = new_f
                    open_list.put((new_f, h(current_cell, child_cell), child_cell, from_dir))
                    a_path[child_cell] = current_cell

    forward_path = {}
    cell = goal_cell
    forward_list = []
    while cell != start_cell:
        forward_path[a_path[cell]] = cell
        cell = a_path[cell]
    for i in forward_path.values():
        forward_list = [i] + forward_list
    forward_list = [start_cell] + forward_list
    return forward_list, from_dir


# --------------------------- Total Route ---------------------------------------------
def full_route(grid, area, direction, targets, base):
    route = []
    from_dir = direction
    for i in range(len(targets) - 1):
        start_cell = targets[i]
        goal_cell = targets[i + 1]
        forward_list, from_dir = a_star(grid, start_cell, goal_cell, from_dir)
        route = route + forward_list[1:]

    area_list = list(area.keys())

    # Find elements that are in area_list but not in route
    remaining_cells = list(set(area_list) - set(route))
    if base in remaining_cells:
        remaining_cells.remove(base)  # remove base cell as it is unpassable
    remaining_cells.sort()  # arrange the list in increasing order

    if remaining_cells:
        remaining_cells = [route[-1]] + remaining_cells  # Add last element of the route list to the beginning
        for i in range(len(remaining_cells) - 1):
            goal_cell = remaining_cells[i + 1]
            start_cell = remaining_cells[i]
            forward_list, from_dir = a_star(grid, start_cell, goal_cell, from_dir)
            route = route + forward_list[1:]
    return route

# ------------------------------------------------------------------------------------------

# ------------------------------------ SETUP ------------------------------------------


grid_size = 8
base = (4, 4)
base_mu1 = (3, 4)  # In order not to crash base
MU1 = (1, 1)
direction1 = 'N'
obstacle_positions = [(1.5, 6), (4, 6.5), (5.5, 3), (4.5, 1), (7, 2.5), (3.5, 4), (4.5, 4), (4, 3.5), (4, 4.5)]
mu_route = []
grid_with_obstacles = grid_generation(grid_size, obstacle_positions)

# Call A* algorithm for each unit with the goal set to the location of the base; in other words,
# we should go to the base initially base will assign a random search area to unit

forward_route_mu1, last_dir = a_star(grid_with_obstacles, MU1, base_mu1, direction1)  # Last directory of this path
mu_route = mu_route + forward_route_mu1
areas = divide_grid_into_areas(grid_with_obstacles, grid_size)
keys = list(areas.keys())
area_key = keys[2]  # this key will be given by base unit
area_mu = areas[area_key]
target_sequence = generate_target_sequence(area_key, base_mu1)
full_route = full_route(grid_with_obstacles, area_mu, last_dir, target_sequence, base)
mu_route = mu_route + full_route
end = mu_route[len(mu_route) - 1]
grid_visualization(grid_with_obstacles, mu_route[0], end, mu_route, base)
