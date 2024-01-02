import random
from collections import deque

class colors:
    RED = '\033[91m'  # Red color for walls
    BLUE = '\033[94m'  # Blue color for open space
    GREEN = '\033[92m'  # Green color for path
    END = '\033[0m'  # Reset color

def generate_maze(n, wall_percentage):
    maze = [[colors.BLUE + '◌' + colors.END for _ in range(n)] for _ in range(n)]
    maze[0][0] = colors.GREEN + 'S' + colors.END
    maze[n - 1][n - 1] = colors.RED + 'E' + colors.END

    num_walls = int(n * n * wall_percentage / 100)
    for _ in range(num_walls):
        x = random.randint(0, n - 1)
        y = random.randint(0, n - 1)
        if maze[x][y] != colors.GREEN + 'S' + colors.END and maze[x][y] != colors.RED + 'E' + colors.END:
            maze[x][y] = colors.RED + '▓' + colors.END

    return maze

def print_colored_maze(maze):
    red_plus = colors.RED + '+' + colors.END
    redline = colors.RED + '---+' + colors.END
    for row in maze:
        print( red_plus + redline * len(row))
        print('|', end='')
        for cell in row:
            print(f' {cell} |', end='')
        print()
    print(red_plus + redline * len(maze[0]))

def find_shortest_path(maze):
    start_x, start_y = 0, 0
    end_x, end_y = len(maze) - 1, len(maze[0]) - 1
    queue = deque([(start_x, start_y)])
    visited = set([(start_x, start_y)])
    parent = {}

    while queue:
        x, y = queue.popleft()

        if (x, y) == (end_x, end_y):
            path = []
            while (x, y) != (start_x, start_y):
                path.append((x, y))
                x, y = parent[(x, y)]
            path.append((start_x, start_y))
            path.reverse()
            return path

        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(maze) and 0 <= ny < len(maze[0]) and maze[nx][ny] != colors.RED + '▓' + colors.END and (nx, ny) not in visited:
                queue.append((nx, ny))
                visited.add((nx, ny))
                parent[(nx, ny)] = (x, y)

    return []
def visualize_shortest_path(maze, path):
    for x, y in path:
        maze[x][y] = colors.GREEN + '◍' + colors.END  # Representing path as '◍'

    print("\nShortest Path Found:")
    print_colored_maze(maze)

while True:
    size = int(input("Enter the size of the maze (n x n): "))
    wall_percent = int(input("Enter the percentage of walls (0-100): "))

    maze = generate_maze(size, wall_percent)
    print("\nGenerated Maze:")
    print_colored_maze(maze)

    while True:
        
        choice = input("\nChoose an option:\n1. Print the path\n2. Generate another maze\n3. Exit the game\nEnter your choice (1/2/3): ")

        if choice == '1':
            shortest_path = find_shortest_path(maze)
            if shortest_path:
                visualize_shortest_path([row[:] for row in maze], shortest_path)
            else:
                print("\nNo path found!")
        elif choice == '2':
            break
        elif choice == '3':
            exit()
        else:
            print("Invalid choice! Please enter 1, 2, or 3.")
