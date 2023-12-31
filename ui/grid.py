def draw_grid(root, tk, rows, columns, column_cell, row_cell):
    canvas = tk.Canvas(root, width=880, height=565, borderwidth=0,
                       highlightthickness=0)
    canvas.pack(pady=30, padx=10)
    canvas.configure(bg=root.cget('bg'))

    for i in range(rows):
        for j in range(columns):
            x1 = j * column_cell
            y1 = i * row_cell
            x2 = x1 + column_cell
            y2 = y1 + row_cell

            # Create the tags for each side
            canvas.create_line(x1, y1, x2, y1, fill="#CCCCCC", tags=f"n_{i}_{j}")
            canvas.create_line(x1, y1, x1, y2, fill="#CCCCCC", tags=f"w_{i}_{j}")
            canvas.create_line(x2, y1, x2, y2, fill="#CCCCCC", tags=f"e_{i}_{j}")
            canvas.create_line(x1, y2, x2, y2, fill="#CCCCCC", tags=f"s_{i}_{j}")

    return canvas
