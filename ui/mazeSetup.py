import tkinter as tk
from tkmacosx import Button, CircleButton
from tkinter import messagebox
import selectionUI as selection
import resultMaze as rm


# declare global variables
maze_root = None
canvas = None
start_mode = False
end_mode = False
start_placed = False
end_placed = False
start_position = None
end_position = None
columns = 0
rows = 0
walls = set()


# a-star algorithm section
def neighbors(node, grid):
    global walls
    i, j = node
    possible_neighbors = [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]
    valid_neighbors = [(x, y) for x, y in possible_neighbors if
                       0 <= x < len(grid) and 0 <= y < len(grid[0]) and (x, y) not in walls]
    return valid_neighbors


def astar(grid, start, goal):
    global walls
    open_list = [start]
    closed_list = set()
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}
    while open_list:
        current = min(open_list, key=lambda node: f_score[node])

        if current == goal:
            path = []
            while current in came_from:
                path.insert(0, current)
                current = came_from[current]
            return path

        open_list.remove(current)
        closed_list.add(current)

        for neighbor in neighbors(current, grid):
            if neighbor in closed_list:
                continue
            tentative_g_score = g_score[current] + 1

            if neighbor not in open_list or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = g_score[neighbor] + heuristic(neighbor, goal)

                if neighbor not in open_list:
                    open_list.append(neighbor)

    return "No path found"


def heuristic(node, goal):
    if node is not None and goal is not None:
        return abs(node[0] - goal[0]) + abs(node[1] - goal[1])
    else:
        return float('inf')


# when a line is clicked, change the color of the line and add it to the walls list
def on_line_click(tag, event):
    side, i, j = tag.split("_")
    i, j = int(i), int(j)

    line = event.widget
    x, y = event.x, event.y
    item = line.find_closest(x, y)[0]

    line_color = line.itemcget(item, "fill")

    if line_color == "#CCCCCC":
        line.itemconfig(item, fill="red")
        # if walls already has the wall, don't add it
        if ((i, j, side)) in walls:
            return
        elif side == "top" or side == "left":
            walls.add((i, j, side))

    else:
        line.itemconfig(item, fill="#CCCCCC")
        # if walls doesn't have the wall, don't remove it
        if ((i, j, side)) not in walls:
            return
        elif side == "top" or side == "left":
            walls.remove((i, j, side))


def place_start():
    global start_mode, end_mode, start_placed, end_placed
    if not start_placed:
        start_mode = True
        end_mode = False
        start_placed = True


def place_end():
    global start_mode, end_mode, start_placed, end_placed
    if not end_placed:
        end_mode = True
        start_mode = False
        end_placed = True


def on_cell_click(event):
    global start_mode, end_mode, start_position, end_position, canvas
    x_center = (event.x // (868 // columns)) * (868 // columns) + (868 // (2 * columns))
    y_center = (event.y // (560 // rows)) * (560 // rows) + (560 // (2 * rows))
    if start_mode:
        # Calculate the center of the cell
        canvas.create_oval(x_center - 15, y_center - 15, x_center + 15, y_center + 15, fill="green", outline="green")
        start_position = (x_center, y_center)
        start_mode = False
    elif end_mode:
        # Calculate the center of the cell
        canvas.create_oval(x_center - 15, y_center - 15, x_center + 15, y_center + 15, fill="red", outline="red")
        end_mode = False
        end_position = (x_center, y_center)


def go_back():
    global maze_root, start_placed, end_placed, start_mode, end_mode, walls
    maze_root.destroy()
    start_placed = False
    end_placed = False
    start_mode = False
    end_mode = False
    walls = set()
    selection.create_selection()


def clear():
    global start_position, end_position, start_mode, end_mode, walls, maze_root, start_placed, end_placed
    start_position = None
    end_position = None
    start_mode = False
    end_mode = False
    walls = set()

    maze_root.destroy()
    start_placed = False
    end_placed = False
    create_maze(rows, columns)
    if canvas.find_withtag("start"):
        canvas.delete("start")
    if canvas.find_withtag("end"):
        canvas.delete("end")


def solve_maze():
    global start_position, end_position, rows, columns
    if start_position is None or end_position is None:
        messagebox.showerror("Error", "Please place start and end points")
    grid = create_grid()
    start_position = int((start_position[0] - (868 // (2 * columns))) / (868 // columns)), int(
        (start_position[1] - (560 // (2 * rows))) / (560 // rows))
    end_position = int((end_position[0] - (868 // (2 * columns))) / (868 // columns)), int(
        (end_position[1] - (560 // (2 * rows))) / (560 // rows))
    path = astar(grid, start_position, end_position)
    maze_root.destroy()
    print(f"Path from {start_position} to {end_position}: {path}")
    print(start_position)
    print(end_position)
    print(walls)
    rm.resultMaze(rows, columns, start_position, end_position, walls, path)


def create_grid():
    global rows, columns
    grid = []
    for i in range(rows):
        row = []
        for j in range(columns):
            row.append((i, j))
        grid.append(row)
    return grid


def create_maze(row, column):
    global columns, rows, maze_root, canvas
    columns = column
    rows = row
    maze_root = tk.Tk()
    maze_root.title(f"Maze Setup{rows}x{columns}")

    maze_root.geometry("1200x840")
    maze_root.resizable(False, False)
    maze_root.configure(bg="#8AB0AB")

    button_width = 80
    button_height = 30

    button_style = {
        'background': '#3E505B',
        'foreground': 'white',
        'font': ('Inter', 15, 'bold'),
        'highlightbackground': "#8AB0AB",
        'highlightcolor': "#8AB0AB",
        'overbackground': "#64727b",
        'borderless': 1,
    }

    back_button = Button(maze_root, text="Back", **button_style, width=button_width, height=button_height,
                         command=go_back)
    back_button.pack(side="top", anchor="nw", padx=(10, 0), pady=(10, 0))

    canvas = tk.Canvas(maze_root, width=880, height=565, borderwidth=0, highlightthickness=0)
    canvas.pack(pady=30, padx=10)
    canvas.configure(bg=maze_root.cget('bg'))

    row_cell = 560 / rows
    column_cell = 868 / columns

    for i in range(rows):
        for j in range(columns):
            x1 = j * column_cell
            y1 = i * row_cell
            x2 = x1 + column_cell
            y2 = y1 + row_cell

            # Create the tags for each side
            canvas.create_line(x1, y1, x2, y1, fill="#CCCCCC", tags=f"top_{i}_{j}")
            canvas.create_line(x1, y1, x1, y2, fill="#CCCCCC", tags=f"left_{i}_{j}")
            canvas.create_line(x2, y1, x2, y2, fill="#CCCCCC", tags=f"right_{i}_{j}")
            canvas.create_line(x1, y2, x2, y2, fill="#CCCCCC", tags=f"bottom_{i}_{j}")

    # Bind click events to the sides
    for i in range(rows):
        for j in range(columns):
            for side in ["top", "left", "right", "bottom"]:
                tag = f"{side}_{i}_{j}"
                if not ((side == "top" and i == 0) or (side == "left" and j == 0) or (
                        side == "right" and j == columns - 1) or (side == "bottom" and i == rows - 1)):
                    canvas.tag_bind(tag, "<Button-1>", lambda event, tag=tag: on_line_click(tag, event))

    canvas.bind("<Button-1>", on_cell_click)

    button_width = 80
    button_height = 30

    frame = tk.Frame(maze_root, bg="#8AB0AB")
    frame.pack(pady=(10, 0), fill='x', side='top')

    component_frame = tk.Frame(frame, width=400, height=30, bg="#8AB0AB")
    component_frame.pack(side='left', padx=(250, 5))

    button_frame = tk.Frame(frame, width=400, height=30, bg="#8AB0AB")
    button_frame.pack(side='left', padx=(300, 10))

    start_button = CircleButton(component_frame, text="start", **button_style, width=60, height=60, command=place_start)
    start_button.pack(side="left", padx=10)
    end_button = CircleButton(component_frame, text="end", **button_style, width=60, height=60, command=place_end)
    end_button.pack(side="left", padx=10)

    solve_button = Button(button_frame, text="Solve", **button_style, width=button_width, height=button_height,
                          command=solve_maze)
    solve_button.pack(side="right")
    clear_button = Button(button_frame, text="Clear", **button_style, width=button_width, height=button_height,
                          command=clear)
    clear_button.pack(side="right", padx=10)

    canvas.bind("<Button-1>", on_cell_click)

    maze_root.mainloop()


if __name__ == '__main__':
    create_maze(8, 8)
