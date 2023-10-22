import tkinter as tk
from tkmacosx import Button

def on_line_click(event):
    line = event.widget
    item = line.find_closest(event.x, event.y)[0]  # Access the first element of the tuple
    line_color = line.itemcget(item, "fill")

    if line_color == "#CCCCCC":
        line.itemconfig(item, fill="red")
    else:
        line.itemconfig(item, fill="#CCCCCC")


def create_maze(rows, columns):
    maze_root = tk.Tk()
    maze_root.title(f"Maze Setup{rows}x{columns}")

    # Define the size of each cell
    cell_size = 50

    # Set the window size
    w_width = columns * cell_size + 100
    w_height = rows * cell_size + 100

    maze_root.geometry(f"{w_width}x{w_height}")
    maze_root.resizable(False, False)  # Disable resizing
    maze_root.configure(bg="#8AB0AB")  # Declare bg as 8AB0AB in global

    # Create a canvas for the grid
    canvas = tk.Canvas(maze_root, width=columns * cell_size + 5, height=rows * cell_size + 5, borderwidth=0,
                       highlightthickness=0)
    canvas.pack(pady=30, padx=10)
    canvas.configure(bg=maze_root.cget('bg'))

    for i in range(rows):
        for j in range(columns):
            x1 = j * cell_size
            y1 = i * cell_size
            x2 = x1 + cell_size
            y2 = y1 + cell_size

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
                if not((side == "top" and i == 0) or (side == "left" and j == 0) or (side == "right" and j == columns - 1) or (side == "bottom" and i == rows - 1)):
                    canvas.tag_bind(tag, "<Button-1>", on_line_click)

    maze_root.mainloop()