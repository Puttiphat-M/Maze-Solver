import tkinter as tk
from tkmacosx import Button
from grid import draw_grid

canvas = None


# function to get where to draw the line
def get_line_coordinates(i, j, side, row_cell, column_cell):
    x1, y1, x2, y2 = 0, 0, 0, 0
    if side == "N":
        x1 = i * column_cell
        y1 = j * row_cell
        x2 = x1 + column_cell
        y2 = y1
    elif side == "W":
        x1 = i * column_cell
        y1 = j * row_cell
        x2 = x1
        y2 = y1 + row_cell
    elif side == "E":
        x1 = (i + 1) * column_cell
        y1 = j * row_cell
        x2 = x1
        y2 = y1 + row_cell
    elif side == "S":
        x1 = i * column_cell
        y1 = (j + 1) * row_cell
        x2 = x1 + column_cell
        y2 = y1
    return x1, y1, x2, y2


def resultMaze(rows, columns, start_position, end_position, walls, path):
    global canvas
    result_root = tk.Tk()
    result_root.title("Maze Solver Result")

    result_root.geometry("1200x840")
    result_root.resizable(False, False)
    result_root.configure(bg="#8AB0AB")

    # Draw the grid
    draw_grid(result_root, tk, rows, columns)

    ok_button = Button(result_root, text="OK", command=lambda: result_root.destroy(), bg="#3E505B", fg="white",
                       font=("Inter", 15, 'bold'), borderless=1, width=80, height=30)
    ok_button.pack(side="right", padx=(0, 175), pady=(0, 175))

    # Draw the start and end positions
    # start
    x_center = (start_position[0] * (868 // columns)) + (868 // (2 * columns))
    y_center = (start_position[1] * (560 // rows)) + (560 // (2 * rows))
    canvas.create_oval(x_center - 15, y_center - 15, x_center + 15, y_center + 15, fill="green", outline="green")
    # end
    x_center = (end_position[0] * (868 // columns)) + (868 // (2 * columns))
    y_center = (end_position[1] * (560 // rows)) + (560 // (2 * rows))
    canvas.create_oval(x_center - 15, y_center - 15, x_center + 15, y_center + 15, fill="red", outline="red")

    # Draw the path
    for x, y in path:
        x_center = (x * (868 // columns)) + (868 // (2 * columns))
        y_center = (y * (560 // rows)) + (560 // (2 * rows))
        canvas.create_rectangle(x_center - 15, y_center - 15, x_center + 15, y_center + 15, fill="green",
                                outline="green")

    # Draw the walls
    for (i, j), sides in walls.items():
        for side, value in sides.items():
            if value:
                x1, y1, x2, y2 = get_line_coordinates(i, j, side, row_cell, column_cell)
                canvas.create_line(x1, y1, x2, y2, fill="red", width=2)

    result_root.mainloop()
