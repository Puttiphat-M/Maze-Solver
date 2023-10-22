from tkmacosx import Button
import tkinter as tk
import mazeSetup as ms

def create_selection():
    root = tk.Tk()
    root.title("Maze Solver Login")

    # Set the window size
    root.geometry("1200x840")  # Adjust the window size as needed
    root.resizable(False, False)  # Disable resizing
    root.configure(bg="#8AB0AB")  # Declare bg as 8AB0AB in global

    title_label = tk.Label(root, text="MAZE SOLVER", font=("Inter", 55, 'bold'), fg="black", )
    title_label.pack(pady=35)
    title_label.configure(bg=root.cget('bg'))

    image = tk.PhotoImage(file='../image/maze_solve.png')

    # Resize the image using subsample
    image = image.subsample(2, 2)

    # Image label
    image_label = tk.Label(root, image=image)
    image_label.pack()
    image_label.configure(bg=root.cget('bg'))

    def start_solver(rows, columns):
        root.destroy()  # Close the current window
        ms.create_maze(rows, columns)  # Create the maze setup page


    # Styling for buttons
    button_style = {
        'background': '#3E505B',
        'foreground': 'white',  # Text color
        'font': ('Inter', 25, 'bold'),
        'highlightbackground': "#8AB0AB",  # Set the button's border color to match the background
        'highlightcolor': "#8AB0AB",
        'overbackground': "#64727b",
        'borderless': 1,
    }

    button_frame = tk.Frame(root)
    button_frame.pack(pady=40)
    button_frame.configure(bg=root.cget('bg'))

    button_width = 280
    button_height = 80

    btn_8x8 = Button(button_frame, text="8x8", command=lambda: start_solver(8, 8),**button_style , width=button_width, height=button_height)
    btn_10x10 = Button(button_frame, text="10x10", command=lambda: start_solver(10, 10), **button_style,width=button_width, height= button_height)
    btn_12x12 = Button(button_frame, text="12x12", command=lambda: start_solver(12, 12), **button_style, width=button_width, height=button_height)

    btn_8x8.pack(side="left", padx=20)
    btn_10x10.pack(side="left", padx=20)
    btn_12x12.pack(side="left", padx=20)

    root.mainloop()

if __name__ == "__main__":
    create_selection()