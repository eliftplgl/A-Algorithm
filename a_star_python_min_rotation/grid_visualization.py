# This function is used from grid visualization.
import matplotlib.pyplot as plt


def grid_visualization(grid, start, goal, forward_list):
    fig, ax = plt.subplots(figsize=(3, 3))  # Adjust the size of the plot window and create a figure and axis

    # Calculate grid size assuming square grid since the dictionary has N^2 elements, think grid as nxn matrix
    size = int(len(grid)**0.5)

    for x in range(1, size+1):
        for y in range(1, size+1):
            cell = grid[(x, y)]
            row = y - 0.5  # Adjust x coordinate for plotting, starting from 0.5 up to 4.5 for size
            colm = size - x + 0.5  # Adjust y coordinate for plotting starting from 4.5 to 0.5 for 5x5 grid

            if cell['E'] == 0:  # Obstacles are show bold
                ax.plot([row + 1, row + 1], [colm, colm + 1], color='black', linewidth=3)
            else:
                ax.plot([row + 1, row + 1], [colm, colm + 1], color='black', linewidth=0.7)

            if cell['W'] == 0:
                ax.plot([row, row], [colm, colm + 1], color='black', linewidth=3)
            else:
                ax.plot([row, row], [colm, colm + 1], color='black', linewidth=0.7)

            if cell['N'] == 0:
                ax.plot([row, row + 1], [colm + 1, colm + 1], color='black', linewidth=3)
            else:
                ax.plot([row, row + 1], [colm + 1, colm + 1], color='black', linewidth=0.7)

            if cell['S'] == 0:
                ax.plot([row, row + 1], [colm, colm], color='black', linewidth=3)
            else:
                ax.plot([row, row + 1], [colm, colm], color='black', linewidth=0.7)

            # Indicate the start and goal points
            ax.fill_between([start[1] - 0.5, start[1] + 0.5], size - start[0] + 0.5, size + 1.5 - start[0],
                            color='red', alpha=0.01)
            ax.fill_between([goal[1] - 0.5, goal[1] + 0.5], size - goal[0] + 0.5, size + 1.5 - goal[0],
                            color='green', alpha=0.01)

            # Indicate the route
            for point in forward_list:
                row = point[1]
                colm = size + 1 - point[0]
                ax.plot(row, colm, marker='o', markersize=10, color='blue', fillstyle='none')

    ax.set_xlim(-1, size + 2)  # Arrange the grid limits
    ax.set_ylim(-1, size + 2)
    ax.set_aspect('equal')  # Equalize the grid axis to obtain an exact square
    ax.set_xticks(range(size + 2))  # Arrange the axis numbers from 0 to N+1
    ax.set_yticks(range(size + 2))
    ax.grid(True, linestyle='--', linewidth=0.3)  # Grid lines are set
    ax.set_xlabel('S')
    ax.set_ylabel('W')
    ax.set_title('A* Algorithm')
    my_list = [str(i) for i in range(size + 1, -1, -1)]
    plt.gca().set_yticklabels(my_list)  # Reverse the plot labels for readability
    plt.show()
