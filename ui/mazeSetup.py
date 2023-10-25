import tkinter as tk
from queue import PriorityQueue
from tkmacosx import Button, CircleButton
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
walls = {}


def create_grid():
    grid = [(i, j) for i in range(0, rows) for j in range(0, columns)]
    return grid


def h(cell1, cell2):
    x1, y1 = cell1
    x2, y2 = cell2

    return abs(x1 - x2) + abs(y1 - y2)


def initialise_walls():
    global walls
    grid = create_grid()
    walls = {cell: {'E': 0, 'W': 0, 'N': 0, 'S': 0} for cell in grid}
    print(walls)


def aStar():
    start = start_position
    grid = create_grid()
    g_score = {cell: float('inf') for cell in grid}
    g_score[start] = 0
    f_score = {cell: float('inf') for cell in grid}
    f_score[start] = h(start, end_position)

    open_set = PriorityQueue()
    open_set.put((f_score[start], start))
    aPath = {}

    while not open_set.empty():
        _, currCell = open_set.get()
        if currCell == end_position:
            break

        for d in 'ESNW':
            if walls[currCell][d] == 0:  # Check if there's no wall in this direction
                print(f"currCell{currCell}")
                print(f"maze_map{walls}")
                print(f"maze_map[currCell]{walls[currCell]}")
                print(walls[currCell][d])
                if d == 'S':
                    childCell = (currCell[0], currCell[1] + 1)
                elif d == 'N':
                    childCell = (currCell[0], currCell[1] - 1)
                elif d == 'W':
                    childCell = (currCell[0] - 1, currCell[1])
                elif d == 'E':
                    childCell = (currCell[0] + 1, currCell[1])

                print(f"childCell{childCell}")

                if 0 <= childCell[0] < columns and 0 <= childCell[1] < rows:
                    temp_g_score = g_score[currCell] + 1
                    temp_f_score = temp_g_score + h(childCell, end_position)

                    if temp_f_score < f_score[childCell]:
                        aPath[childCell] = currCell
                        g_score[childCell] = temp_g_score
                        f_score[childCell] = temp_f_score
                        open_set.put((f_score[childCell], childCell))

    path = []
    curr = end_position
    while curr != start_position:
        path.append(curr)
        curr = aPath[curr]
    path.append(start_position)
    path.reverse()
    return path




# when a line is clicked, change the color of the line and add it to the walls list
def on_line_click(tag, event):
    direction, j, i = tag.split("_")
    i, j = int(i), int(j)

    line = event.widget
    x, y = event.x, event.y
    item = line.find_closest(x, y)[0]

    line_color = line.itemcget(item, "fill")

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
    walls = {}
    selection.create_selection()


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
    global start_position, end_position, rows, columns
    if start_position is None or end_position is None:
        print("error")
    else:
        start_position = int((start_position[0] - (868 // (2 * columns))) / (868 // columns)), int(
            (start_position[1] - (560 // (2 * rows))) / (560 // rows))
        end_position = int((end_position[0] - (868 // (2 * columns))) / (868 // columns)), int(
            (end_position[1] - (560 // (2 * rows))) / (560 // rows))
        maze_root.destroy()
        print(start_position)
        print(end_position)
        print(walls)
        path = aStar()
        print(path)
        rm.resultMaze(rows, columns, start_position, end_position, walls, path)


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

            # Create the tags for each direction
            canvas.create_line(x1, y1, x2, y1, fill="#CCCCCC", tags=f"N_{i}_{j}")
            canvas.create_line(x1, y1, x1, y2, fill="#CCCCCC", tags=f"W_{i}_{j}")
            canvas.create_line(x2, y1, x2, y2, fill="#CCCCCC", tags=f"E_{i}_{j}")
            canvas.create_line(x1, y2, x2, y2, fill="#CCCCCC", tags=f"S_{i}_{j}")

    initialise_walls()

    # Bind click events to the direction
    for i in range(rows):
        for j in range(columns):
            for direction in ["N", "W", "E", "S"]:
                tag = f"{direction}_{i}_{j}"
                if not ((direction == "N" and i == 0) or (direction == "W" and j == 0) or (
                        direction == "E" and j == columns - 1) or (direction == "S" and i == rows - 1)):
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
