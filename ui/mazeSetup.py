import tkinter as tk
from prolog import *
from tkmacosx import Button, CircleButton
import selectionUI as selection
import resultMaze as rm
import subprocess
from grid import draw_grid

# declare global variables
maze_root = None
canvas = None

# declare start and end node variables
start_mode = False
end_mode = False
start_placed = False
end_placed = False
start_position = None
end_position = None
columns = 0
rows = 0

# map of walls and maze
walls = {}


def show_mac_alert(message):
    script = f'display dialog "{message}" buttons "OK" default button "OK"'
    subprocess.run(['osascript', '-e', script])


def create_grid():
    grid = [(i, j) for i in range(0, rows) for j in range(0, columns)]
    return grid


def initialise_walls():
    global walls
    grid = create_grid()
    walls = {cell: {'E': 0, 'W': 0, 'N': 0, 'S': 0} for cell in grid}


def prolog_aStar():
    global start_position, end_position, walls
    grid = create_grid()
    # Convert walls to Prolog predicates
    convert_walls_to_prolog(walls)
    # Convert cells to Prolog predicates
    convert_grid_to_prolog(grid)
    # Find the shortest path
    query = f'a_star({start_position}, {end_position}, Path, Cost)'
    result = list(prolog.query(query))

    print(result)
    return result


# a-star section
# def h(cell1, cell2):
#     x1, y1 = cell1
#     x2, y2 = cell2
#
#     return abs(x1 - x2) + abs(y1 - y2)
#
#
# def aStar():
#     grid = create_grid()
#     g_score = {cell: float('inf') for cell in grid}
#     g_score[start_position] = 0
#     f_score = {cell: float('inf') for cell in grid}
#     f_score[start_position] = h(start_position, end_position)
#
#     open_set = PriorityQueue()
#     open_set.put((f_score[start_position], start_position))
#     aPath = {}
#
#     while not open_set.empty():
#         _, currCell = open_set.get()
#         if currCell == end_position:
#             break
#
#         for d in 'ESNW':
#             if walls[currCell][d] == 0:
#                 if d == 'S':
#                     childCell = (currCell[0], currCell[1] + 1)
#                 elif d == 'N':
#                     childCell = (currCell[0], currCell[1] - 1)
#                 elif d == 'W':
#                     childCell = (currCell[0] - 1, currCell[1])
#                 elif d == 'E':
#                     childCell = (currCell[0] + 1, currCell[1])
#
#                 if 0 <= childCell[0] < columns and 0 <= childCell[1] < rows:
#                     temp_g_score = g_score[currCell] + 1
#                     temp_f_score = temp_g_score + h(childCell, end_position)
#
#                     if temp_f_score < f_score[childCell]:
#                         aPath[childCell] = currCell
#                         g_score[childCell] = temp_g_score
#                         f_score[childCell] = temp_f_score
#                         open_set.put((f_score[childCell], childCell))
#
#     path = []
#     curr = end_position
#     while curr != start_position:
#         path.append(curr)
#         try:
#             curr = aPath[curr]
#         except KeyError:
#             message = "No path found, click OK to continue"
#             show_mac_alert(message)
#             return None
#     path.append(start_position)
#     path.reverse()
#     return path


# when a line is clicked, change the color of the line and add it to the walls list
def on_line_click(tag, event):
    direction, j, i = tag.split("_")
    i, j = int(i), int(j)

    line = event.widget
    x, y = event.x, event.y
    item = line.find_closest(x, y)[0]

    line_color = line.itemcget(item, "fill")

    # if the line is grey, change it to red and add it to the walls list
    if line_color == "#CCCCCC":
        line.itemconfig(item, fill="red")
        walls[(i, j)][direction] = 1
        if direction == 'E':
            walls[(i + 1, j)]['W'] = 1
        elif direction == 'W':
            walls[(i - 1, j)]['E'] = 1
        elif direction == 'N':
            walls[(i, j - 1)]['S'] = 1
        elif direction == 'S':
            walls[(i, j + 1)]['N'] = 1

    # if the line is red, change it to grey and remove it from the walls list
    else:
        line.itemconfig(item, fill="#CCCCCC")
        walls[(i, j)][direction] = 0
        if direction == 'E':
            walls[(i + 1, j)]['W'] = 0
        elif direction == 'W':
            walls[(i - 1, j)]['E'] = 0
        elif direction == 'N':
            walls[(i, j - 1)]['S'] = 0
        elif direction == 'S':
            walls[(i, j + 1)]['N'] = 0


def place_start():
    global start_mode, end_mode
    if not start_placed:
        start_mode = True
        end_mode = False


def place_end():
    global start_mode, end_mode
    if not end_placed:
        end_mode = True
        start_mode = False


def on_cell_click(event):
    global start_mode, end_mode, start_position, end_position, canvas, start_placed, end_placed
    x_center = (event.x // (868 // columns)) * (868 // columns) + (868 // (2 * columns))
    y_center = (event.y // (560 // rows)) * (560 // rows) + (560 // (2 * rows))
    if start_mode:
        # Calculate the center of the cell
        canvas.create_oval(x_center - 15, y_center - 15, x_center + 15, y_center + 15, fill="green", outline="green")
        start_position = (x_center, y_center)
        start_mode = False
        start_placed = True
        start_position = int((start_position[0] - (868 // (2 * columns))) / (868 // columns)), int(
            (start_position[1] - (560 // (2 * rows))) / (560 // rows))
    elif end_mode:
        # Calculate the center of the cell
        canvas.create_oval(x_center - 15, y_center - 15, x_center + 15, y_center + 15, fill="red", outline="red")
        end_position = (x_center, y_center)
        end_position = int((end_position[0] - (868 // (2 * columns))) / (868 // columns)), int(
            (end_position[1] - (560 // (2 * rows))) / (560 // rows))
        end_mode = False
        end_placed = True


# go back to the selection screen
def go_back():
    global maze_root, start_placed, end_placed, start_mode, end_mode, walls
    maze_root.destroy()
    start_placed = False
    end_placed = False
    start_mode = False
    end_mode = False
    walls = {}
    selection.create_selection()


# clear the maze
def clear():
    global start_position, end_position, start_mode, end_mode, walls, maze_root, start_placed, end_placed
    start_position = None
    end_position = None
    start_mode = False
    end_mode = False
    walls = {}

    maze_root.destroy()
    start_placed = False
    end_placed = False
    create_maze(rows, columns)
    if canvas.find_withtag("start"):
        canvas.delete("start")
    if canvas.find_withtag("end"):
        canvas.delete("end")


def solve_maze():
    global start_position, end_position, rows, columns, start_mode, end_mode, walls, maze_root, start_placed, end_placed

    if start_position is None or end_position is None:
        message = "Please place start and end point, click OK to continue"
        show_mac_alert(message)

    # path = aStar()
    path = prolog_aStar()
    # if no path is found, do not create the result maze, stay on the maze setup screen
    if path is not None:
        maze_root.destroy()
        rm.resultMaze(rows, columns, start_position, end_position, walls, path)


# main function to create the maze setup screen
def create_maze(row, column):
    global columns, rows, maze_root, canvas, start_position, end_position, start_mode, end_mode, walls, start_placed, end_placed
    start_position = None
    end_position = None
    start_mode = False
    end_mode = False
    walls = {}
    start_placed = False
    end_placed = False
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

    # Draw the grid
    row_cell = 560 / rows
    column_cell = 868 / columns
    canvas = draw_grid(maze_root, tk, rows, columns, column_cell, row_cell)

    initialise_walls()

    # Bind click events to the direction
    for i in range(rows):
        for j in range(columns):
            for direction in ["N", "W", "E", "S"]:
                tag = f"{direction}_{i}_{j}"
                if not ((direction == "N" and i == 0) or (direction == "W" and j == 0) or (
                        direction == "E" and j == columns - 1) or (direction == "S" and i == rows - 1)):
                    canvas.tag_bind(tag, "<Button-1>", lambda event, tag=tag: on_line_click(tag, event))

    # pack the canvas and bind click events to the cells
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
