import tkinter as tk
from tkmacosx import Button


def get_line_coordinates(i, j, side, row_cell, column_cell):
    x1, y1, x2, y2 = 0, 0, 0, 0
    if side == "top":
        x1 = i * column_cell
        y1 = j * row_cell
        x2 = x1 + column_cell
        y2 = y1
    elif side == "left":
        x1 = i * column_cell
        y1 = j * row_cell
        x2 = x1
        y2 = y1 + row_cell
    elif side == "right":
        x1 = (i + 1) * column_cell
        y1 = j * row_cell
        x2 = x1
        y2 = y1 + row_cell
    elif side == "bottom":
        x1 = i * column_cell
        y1 = (j + 1) * row_cell
        x2 = x1 + column_cell
        y2 = y1
    return x1, y1, x2, y2


def resultMaze(rows, columns, start_position, end_position, walls, path):
    result_root = tk.Tk()
    result_root.title("Maze Solver Result")

    result_root.geometry("1200x840")  # Adjust the window size as needed
    result_root.resizable(False, False)  # Disable resizing
    result_root.configure(bg="#8AB0AB")  # Declare bg as 8AB0AB in global

    global canvas
    canvas = tk.Canvas(result_root, width=880, height=565, borderwidth=0,
                       highlightthickness=0)
    canvas.pack(pady=30, padx=10)
    canvas.configure(bg=result_root.cget('bg'))

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
                    canvas.tag_bind(tag, "<Button-1>")

    ok_button = Button(result_root, text="OK", command=lambda: result_root.destroy(), bg="#3E505B", fg="white", font=("Inter", 15, 'bold'), borderless=1, width=80, height=30)
    ok_button.pack(side="right", padx=(0, 175), pady=(0, 175))
    x_center = (start_position[0] * (868 // columns)) + (868 // (2 * columns))
    y_center = (start_position[1] * (560 // rows)) + (560 // (2 * rows))
    canvas.create_oval(x_center - 15, y_center - 15, x_center + 15, y_center + 15, fill="green", outline="green")
    x_center = (end_position[0] * (868 // columns)) + (868 // (2 * columns))
    y_center = (end_position[1] * (560 // rows)) + (560 // (2 * rows))
    canvas.create_oval(x_center - 15, y_center - 15, x_center + 15, y_center + 15, fill="red", outline="red")

    for x, y in path:
        x_center = (x * (868 // columns)) + (868 // (2 * columns))
        y_center = (y * (560 // rows)) + (560 // (2 * rows))
        canvas.create_rectangle(x_center-15, y_center-15, x_center+15, y_center+15, fill="green", outline="green")

    # Mock up the clicked lines in red
    for line in walls:
        i, j, side = line
        x1, y1, x2, y2 = get_line_coordinates(i, j, side, row_cell, column_cell)
        canvas.create_line(x1, y1, x2, y2, fill="red", width=2)

    result_root.mainloop()


if __name__ == '__main__':
    walls = [(2, 1, "left"), (1, 2, "left"), (3, 1, "left"), (3, 2, "right"), (3, 3, "top")]
    resultMaze(8, 8, (1, 1), (6, 4), walls, [(2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (6, 2), (6, 3), (6, 4)])
