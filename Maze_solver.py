import pygame
from queue import Queue
import heapq

# Initialize pygame
#-> Initializes all pygame modules, preparing the program for rendering and event handling.
pygame.init() 
# Define constants
WIDTH, HEIGHT = 600, 600
ROWS, COLS = 20, 20
CELL_WIDTH = WIDTH // COLS
CELL_HEIGHT = HEIGHT // ROWS
#-> Defines RGB color values for the grid, buttons, and visualization.
WHITE, BLACK, GRAY = (255, 255, 255), (0, 0, 0), (200, 200, 200)
GREEN, RED = (0, 255, 0), (255, 0, 0)
BUTTON_COLOR = (200, 200, 200)  # Light gray for buttons
BUTTON_TEXT_COLOR = BLACK

# Set up the display
screen = pygame.display.set_mode((WIDTH + 200, HEIGHT))  # Expanded width to fit buttons
pygame.display.set_caption("Maze Solver [ AI Project ]")

# Initialize the grid
grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]
start, goal = None, None

# Draw the grid
def draw_grid():
    for i in range(ROWS):
        for j in range(COLS):
            color = WHITE
            if grid[i][j] == 1:
                color = BLACK  # Obstacle
            elif grid[i][j] == 2:
                color = GREEN  # Start
            elif grid[i][j] == 3:
                color = RED  # Goal
            #-> pygame.draw.rect: This function is used to draw a rectangle on the screen.

            pygame.draw.rect(screen, color, (j * CELL_WIDTH, i * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT))
            pygame.draw.rect(screen, GRAY, (j * CELL_WIDTH, i * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT), 1)
# Draw the path
def draw_path(path, color):
    for x, y in path:
        if (x, y) != start and (x, y) != goal:
            pygame.draw.rect(screen, color, (y * CELL_WIDTH, x * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT))
            pygame.display.flip()
            pygame.time.delay(50)

# Get neighbors of a cell
def get_neighbors(x, y):
    neighbors = []
    for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:  # Right, Down, Left, Up
        nx, ny = x + dx, y + dy
        if 0 <= nx < ROWS and 0 <= ny < COLS and grid[nx][ny] != 1:
            neighbors.append((nx, ny))
    return neighbors
def Breadth_First_Search():
    if not start or not goal:
        return "Set start and goal points!", 0, 0  # Default values if start or goal isn't set
    visited = set()
    queue = Queue()
    queue.put((start, []))  # Store (current node, path)
    while not queue.empty():
        (x, y), path = queue.get()
        # Check if the current node has already been visited
        if (x, y) in visited:
            continue
        visited.add((x, y))
        # Add the current node to the path
        path = path + [(x, y)]

        # Visualize the exploration (except for the start and goal nodes)
        if (x, y) != start and (x, y) != goal:
            pygame.draw.rect(screen, (0, 255, 255), (y * CELL_WIDTH, x * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT))
            pygame.display.flip()
            pygame.time.delay(50)

        # Check if the goal has been reached
        if (x, y) == goal:
            draw_path(path, (0, 255, 255))  # Cyan path
            return "Goal Found", 0, 0  # BFS does not return path cost

        # Add neighbors to the queue
        for nx, ny in get_neighbors(x, y):
            if (nx, ny) not in visited:
                queue.put(((nx, ny), path))

    return "Goal Not Found", 0, 0


# Depth-First Search (DFS)
def depth_first_search():
    if not start or not goal:
        return "Set start and goal points!", 0, 0

    visited = set()
    stack = [(start, [])]  # Store (current node, path)

    while stack:
        (x, y), path = stack.pop()

        if (x, y) in visited:
            continue
        visited.add((x, y))

        path = path + [(x, y)]

        if (x, y) == goal:  # Found the goal
            draw_path(path, (255, 165, 0))  # Orange path
            return "Goal Found", 0, 0  # No path cost for DFS

        for nx, ny in get_neighbors(x, y):
            if (nx, ny) not in visited:
                stack.append(((nx, ny), path))

    return "Goal Not Found", 0, 0

def heuristic(current, goal):
    # Manhattan distance
    return abs(current[0] - goal[0]) + abs(current[1] - goal[1])

def a_star_search():
    if not start or not goal:
        return "Set start and goal points!", 0, 0

    open_set = []
    heapq.heappush(open_set, (0, start, []))  # f_cost, current node, path
    g_cost = {start: 0}  # Cost from start to a node
    h_cost = {start: heuristic(start, goal)}  # Store heuristic costs for visualization
    visited = set()

    while open_set:
        _, (x, y), path = heapq.heappop(open_set)

        if (x, y) in visited:
            continue
        visited.add((x, y))

        path = path + [(x, y)]  # Add current node to the path

        if (x, y) == goal:  # Found the goal
            draw_path(path, (128, 0, 128))  # Purple path
            total_path_cost = g_cost[(x, y)]  # Path cost to the goal
            total_heuristic_cost = sum(h_cost[node] for node in path)  # Sum heuristic for all nodes in the path
            return "Goal Found", total_path_cost, total_heuristic_cost

        for nx, ny in get_neighbors(x, y):
            tentative_g_cost = g_cost[(x, y)] + 1  # Assuming uniform step cost
            h_value = heuristic((nx, ny), goal)  # Calculate heuristic for neighbor
            f_cost = tentative_g_cost + h_value

            if (nx, ny) not in g_cost or tentative_g_cost < g_cost[(nx, ny)]:
                g_cost[(nx, ny)] = tentative_g_cost
                h_cost[(nx, ny)] = h_value  # Store heuristic for this node
                heapq.heappush(open_set, (f_cost, (nx, ny), path))

    return "Goal Not Found", 0, 0  # If goal is not found

# Uniform Cost Search (UCS)
def uniform_cost_search():
    if not start or not goal:
        return "Set start and goal points!", 0, 0

    open_set = []
    heapq.heappush(open_set, (0, start, []))  # g_cost, current node, path
    visited = set()

    while open_set:
        current_cost, (x, y), path = heapq.heappop(open_set)

        if (x, y) in visited:
            continue
        visited.add((x, y))
        path = path + [(x, y)]
        if (x, y) == goal:  # Found the goal
            draw_path(path, (255, 105, 180))  # Pink path
            return "Goal Found", current_cost, 0  # Return path cost for UCS

        for nx, ny in get_neighbors(x, y):
            if (nx, ny) not in visited:
                heapq.heappush(open_set, (current_cost + 1, (nx, ny), path))

    return "Goal Not Found", 0, 0

# Draw buttons
def draw_buttons():
    font = pygame.font.Font(None, 36)
    pygame.draw.rect(screen, WHITE, (WIDTH, 0, 200, HEIGHT))  # Clear the button panel

    # Draw "OPTIONS" title
    title_text = font.render("OPTIONS", True, BLACK)
    screen.blit(title_text, (WIDTH + 50, 20))
    # Define button positions
    buttons = ["BFS", "DFS", "A*", "UCS"]
    button_functions = [Breadth_First_Search, depth_first_search, a_star_search, uniform_cost_search]
    button_rects = []

    for i, label in enumerate(buttons):
        x, y = WIDTH + 50, 70 + i * 60
        width, height = 100, 40
        pygame.draw.rect(screen, BUTTON_COLOR, (x, y, width, height))  # No border

        button_text = font.render(label, True, BUTTON_TEXT_COLOR)
        screen.blit(button_text, (x + 25, y + 5))

        button_rects.append(((x, y, width, height), button_functions[i]))

    return button_rects


def draw_result_message(message, total_cost, heuristic_cost):
    font = pygame.font.Font(None, 36)
    result_text = font.render(message, True, BLACK)
    screen.blit(result_text, (WIDTH + 50, 350))  # Message for result

    if message == "Goal Found":
        cost_text = font.render(f"Path Cost: {total_cost}", True, (0, 128, 0))  # Green for path cost
        heuristic_text = font.render(f"Heuristic: {heuristic_cost}", True, (0, 128, 0))  # Green for heuristic
    else:
        cost_text = font.render(f"Path Cost: {total_cost}", True, (255, 0, 0))  # Red for path cost
        heuristic_text = font.render(f"Heuristic: {heuristic_cost}", True, (255, 0, 0))  # Red for heuristic

    screen.blit(cost_text, (WIDTH + 50, 400))  # Display Path Cost
    screen.blit(heuristic_text, (WIDTH + 50, 450))  # Display Heuristic

# Main loop
def main():
    global start, goal
    running = True
    result_message = ""
    total_cost = 0
    heuristic_cost = 0

    while running:
        screen.fill(WHITE)
        draw_grid()
        button_rects = draw_buttons()
        if result_message:
            draw_result_message(result_message, total_cost, heuristic_cost)  # Display result
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if pygame.mouse.get_pressed()[0]:  # Left click
                x, y = pygame.mouse.get_pos()
                if x < WIDTH and y < HEIGHT:  # Ignore clicks outside the grid
                    x //= CELL_WIDTH
                    y //= CELL_HEIGHT
                    if not start:
                        start = (y, x)
                        grid[y][x] = 2
                    elif not goal:
                        goal = (y, x)
                        grid[y][x] = 3
                    else:
                        grid[y][x] = 1
                else:  # Check if a button is clicked
                    for rect, func in button_rects:
                        rx, ry, rw, rh = rect
                        if rx <= x <= rx + rw and ry <= y <= ry + rh:
                            message, cost, h_cost = func()
                            result_message = message
                            total_cost = cost
                            heuristic_cost = h_cost

    pygame.quit()
if __name__ == "__main__":
    main()