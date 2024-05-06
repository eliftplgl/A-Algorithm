# ------------------------------ Grid Generation----------------------------------
# Grid is generated with obstacles included. N+1xN+1 grid size is given as input.
# Obstacle positions are given as follows: (1.5,1) means that there exists an obstacle between the cells (1,1) and (2,1)
# Grid matrix is generated as follows:
# 00 01 ... 0N
# 10 11 ... 1N
# ...      ...
# N0 N1 ... NN

def grid_generation(grid_size, obstacle_positions):

    # create NxN grid including 4 directions where all of them are accessible where cell values are the matrix indexes
    grid = {(a, b): {'E': 1, 'W': 1, 'N': 1, 'S': 1} for a in range(0, grid_size) for b in range(0, grid_size)}

    # Mark outer edges of the grid as unpassable
    for i in range(0, grid_size):
        grid[(0, i)]['N'] = 0
        grid[(grid_size-1, i)]['S'] = 0
        grid[(i, 0)]['W'] = 0
        grid[(i, grid_size-1)]['E'] = 0

    # Place obstacles along the edges
    for obstacle in obstacle_positions:
        row, colm = obstacle

        # Obstacles cannot be on the boundaries or out of the grid.
        if row >= grid_size-0.5 or row <= 0 or colm >= grid_size-0.5 or colm <= 0:
            raise ValueError("Invalid obstacle coordinates. Coordinates must be within the grid boundaries.")

        else:
            if colm % 1 == 0.5:  # Obstacle parallel to the y-axis - vertical obstacle
                colm_west = int(colm - 0.5)
                colm_east = int(colm + 0.5)
                grid[(row, colm_west)]['E'] = 0
                grid[(row, colm_east)]['W'] = 0

            elif row % 1 == 0.5:  # Obstacle parallel to the x-axis - horizontal obstacle
                row_north = int(row - 0.5)
                row_south = int(row + 0.5)
                grid[(row_north, colm)]['S'] = 0
                grid[(row_south, colm)]['N'] = 0
    return grid


# ------------------------------ Area Division ----------------------------------
#     _________________
#     |     Area 1    |        Areas are as follows
#     |_______________|
#     |     Area 2    |
#     |_______________|
#     |     Area 3    |
#     |_______________|

def divide_grid_into_areas(grid, grid_size):
    # Calculate the boundaries of each area
    area_boundaries = {
        'Area 1': ((0, 0), (1, grid_size-1)),
        'Area 2': ((2, 0), (4, grid_size-1)),
        'Area 3': ((5, 0), (grid_size-1, grid_size-1))
    }

    # Extract cells for each area
    areas = {}
    for area, ((start_row, start_col), (end_row, end_col)) in area_boundaries.items():
        area_cells = {}
        for row in range(start_row, end_row + 1):
            for col in range(start_col, end_col + 1):
                area_cells[(row, col)] = grid[(row, col)]
        areas[area] = area_cells
    return areas


# ------------------------------ Target Sequence ----------------------------------
def generate_target_sequence(area_key, base):
    if area_key == 'Area 1':
        return [base, (0, 0), (0, 7), (1, 7), (1, 0)]
    elif area_key == 'Area 2':
        return [base, (2, 0), (2, 7), (3, 7), (3, 0), (4, 0), (4, 7)]
    elif area_key == 'Area 3':
        return [base, (7, 7), (7, 0), (6, 0), (6, 7), (5, 7), (5, 0)]
    else:
        raise ValueError("Invalid area name")


"""
obstacles = [(3.5, 1), (2, 4.5), (2.5, 4), (4, 3.5)]
grid_with_obstacles = grid_generation(8, obstacles)
area = divide_grid_into_areas(grid_with_obstacles, 8)
for area, cells in area.items():
    print("Area:", area)
    print(cells)
    print()"""
