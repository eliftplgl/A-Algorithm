import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


def grid_visualization(grid, start, goal, forward_list, base):
    fig, ax = plt.subplots(figsize=(7, 7))  # Adjust the size of the plot window and create a figure and axis

    # Calculate grid size assuming square grid since the dictionary has N^2 elements, think grid as nxn matrix
    size = int(len(grid)**0.5)

    def animate(i):
        ax.clear()  # Clear the previous plot
        ax.set_xlim(-1, size + 1)  # Arrange the grid limits
        ax.set_ylim(0, size + 2)
        ax.set_aspect('equal')  # Equalize the grid axis to obtain an exact square
        ax.set_xticks(range(size+2))  # Arrange the axis numbers from 0 to N+1
        ax.set_yticks(range(size+2))
        ax.grid(True, linestyle='--', linewidth=0.3)  # Grid lines are set
        ax.set_xlabel('S')
        ax.set_ylabel('W')
        ax.set_title('A* Algorithm')
        my_list = [str(i) for i in range(size + 1, -1, -1)]
        plt.gca().set_yticklabels(my_list)  # Reverse the plot labels for readability

        for x in range(0, size):
            for y in range(0, size):
                cell = grid[(x, y)]
                row = y - 0.5  # Adjust x coordinate for plotting, starting from -0.5 up to 4.5 for size
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

        # Indicate the start, goal, and base points by coloring their boundaries
        ax.plot([start[1] - 0.5, start[1] - 0.5, start[1] + 0.5, start[1] + 0.5, start[1] - 0.5],
                [size - start[0] + 0.5, size + 1.5 - start[0], size + 1.5 - start[0], size - start[0] + 0.5, size - start[0] + 0.5],
                color='orange', linewidth=2)
        ax.plot([goal[1] - 0.5, goal[1] - 0.5, goal[1] + 0.5, goal[1] + 0.5, goal[1] - 0.5],
                [size - goal[0] + 0.5, size + 1.5 - goal[0], size + 1.5 - goal[0], size - goal[0] + 0.5, size - goal[0] + 0.5],
                color='green', linewidth=2)
        ax.plot([base[1] - 0.5, base[1] - 0.5, base[1] + 0.5, base[1] + 0.5, base[1] - 0.5],
                [size - base[0] + 0.5, size + 1.5 - base[0], size + 1.5 - base[0], size - base[0] + 0.5, size - base[0] + 0.5],
                color='purple', linewidth=2)

        # Plot the cells the robot has passed with red dots
        for idx, point in enumerate(forward_list[:i+1]):
            row = point[1]
            colm = size + 1 - point[0]
            if idx < i:
                ax.plot(row, colm, marker='o', markersize=5, color='red')
            else:
                ax.plot(row, colm, marker='o', markersize=12, color='blue', fillstyle='none')

    anim = FuncAnimation(fig, animate, frames=len(forward_list), interval=200)
    plt.show()
