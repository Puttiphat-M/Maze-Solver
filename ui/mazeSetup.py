import tkinter as tk
from tkmacosx import Button, CircleButton
import selectionUI as selection
from tkinter import ttk

# Add these global variables at the beginning of your script
start_mode = False
end_mode = False
start_placed = False
end_placed = False
canvas = None
columns = 0
rows = 0

def on_line_click(event):
    line = event.widget
    item = line.find_closest(event.x, event.y)[0]  # Access the first element of the tuple
    line_color = line.itemcget(item, "fill")

    if line_color == "#CCCCCC":
        line.itemconfig(item, fill="red")
    else:
        line.itemconfig(item, fill="#CCCCCC")

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
    global start_mode, end_mode
    global canvas
    if start_mode:
        # Calculate the center of the cell
        x_center = (event.x // (868 // columns)) * (868 // columns) + (868 // (2 * columns))
        y_center = (event.y // (560 // rows)) * (560 // rows) + (560 // (2 * rows))
        canvas.create_oval(x_center-15, y_center-15, x_center+15, y_center+15, fill="green", outline="green")
        start_mode = False
    elif end_mode:
        # Calculate the center of the cell
        x_center = (event.x // (868 // columns)) * (868 // columns) + (868 // (2 * columns))
        y_center = (event.y // (560 // rows)) * (560 // rows) + (560 // (2 * rows))
        canvas.create_oval(x_center-15, y_center-15, x_center+15, y_center+15, fill="red", outline="red")
        end_mode = False

def create_maze(row, column):
    global columns, rows
    columns = column
    rows = row
    maze_root = tk.Tk()
    maze_root.title(f"Maze Setup{rows}x{columns}")

    maze_root.geometry("1200x840")  # Adjust the window size as needed
    maze_root.resizable(False, False)  # Disable resizing
    maze_root.configure(bg="#8AB0AB")  # Declare bg as 8AB0AB in global

    def go_back():
        maze_root.destroy()
        selection.create_selection()

    def clear():
        pass

    button_width = 80
    button_height = 30

    button_style = {
        'background': '#3E505B',
        'foreground': 'white',  # Text color
        'font': ('Inter', 15, 'bold'),
        'highlightbackground': "#8AB0AB",  # Set the button's border color to match the background
        'highlightcolor': "#8AB0AB",
        'overbackground': "#64727b",
        'borderless': 1,
    }

    back_button = Button(maze_root, text="Back", **button_style, width=button_width, height=button_height,
                         command=go_back)
    back_button.pack(side="top", anchor="nw", padx=(10, 0), pady=(10, 0))

    # Create a canvas for the grid
    global canvas
    canvas = tk.Canvas(maze_root, width=880, height=565, borderwidth=0,
                       highlightthickness=0)
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
                    canvas.tag_bind(tag, "<Button-1>", on_line_click)

    button_width = 80
    button_height = 30

    button_style = {
        'background': '#3E505B',
        'foreground': 'white',  # Text color
        'font': ('Inter', 15, 'bold'),
        'highlightbackground': "#8AB0AB",  # Set the button's border color to match the background
        'highlightcolor': "#8AB0AB",
        'overbackground': "#64727b",
        'borderless': 1,
    }

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

    solve_button = Button(button_frame, text="Solve", **button_style, width=button_width, height=button_height)
    solve_button.pack(side="right")
    clear_button = Button(button_frame, text="Clear", **button_style, width=button_width, height=button_height)
    clear_button.pack(side="right", padx=10)

    canvas.bind("<Button-1>", on_cell_click)

    maze_root.mainloop()