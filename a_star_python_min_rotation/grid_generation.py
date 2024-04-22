# Grid is generated with obstacles included. NxN grid size is given as input.
# Obstacle positions are given as follows: (1.5,1) means that there exists an obstacle between the cells (1,1) and (2,1)
# Grid matrix is generated as follows:
# 11 21 ... N1
# 21 22 ... N2
# ...      ...
# N1 N2 ... NN

def grid_generation(grid_size, obstacle_positions):

    # create NxN grid including 4 directions where all of them are accessible where cell values are the matrix indexes
    grid = {(a, b): {'E': 1, 'W': 1, 'N': 1, 'S': 1} for a in range(1, grid_size+1) for b in range(1, grid_size+1)}

    # Mark outer edges of the grid as unpassable
    for i in range(1, grid_size+1):
        grid[(1, i)]['N'] = 0
        grid[(grid_size, i)]['S'] = 0
        grid[(i, 1)]['W'] = 0
        grid[(i, grid_size)]['E'] = 0

    # Place obstacles along the edges
    for obstacle in obstacle_positions:
        row, colm = obstacle

        # Obstacles cannot be on the boundaries or out of the grid.
        if row >= grid_size+0.5 or row <= 0.5 or colm >= grid_size+0.5 or colm <= 0.5:
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
