import tkinter as tk


def draw_visualizer():
    root = tk.Tk()
    root.overrideredirect(True)  # removes window borders
    root.attributes("-topmost", True)  # keeps the window on top
    # keeps it hidden -> will be shown once we follow gaze data
    root.withdraw()

    win_width = 90
    win_height = 90

    canvas = tk.Canvas(
        root,
        width=win_width,
        height=win_height,
        bg="white",
        highlightthickness=0)
    root.config(bg="white")
    root.attributes("-transparentcolor", "white")
    canvas.pack()
    canvas.create_oval(2, 2,
                       win_width-2,
                       win_height-2,
                       fill="",
                       outline="red",
                       width=3)

    return root


def update_position(x, y, window: tk.Tk):
    if (x is None and y is None):  # eyes are closed;
        window.withdraw()
        return

    window.deiconify()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    win_width = window.winfo_width()
    win_height = window.winfo_height()

    x_pos = int(x * screen_width - win_width / 2)
    y_pos = int(y * screen_height - win_height / 2)

    window.geometry(f"{win_width}x{win_height}+{x_pos}+{y_pos}")
