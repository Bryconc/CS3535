__author__ = 'Brycon'

import Tkinter as tk


def sample_button():
    title = "Sample Button"

    top = tk.Tk()
    B = tk.Button(top, text="Sample Button")

    B.pack()
    top.title(title)
    top.mainloop()


def sample_canvas():
    title = "Sample Canvas"

    top = tk.Tk()
    C = tk.Canvas(top, bg="black", height=100, width=100)
    C.create_polygon(50, 10, 10, 60, 80, 60, fill="white")

    C.pack()
    top.title(title)
    top.mainloop()


def sample_checkbox():
    title = "Sample Checkbox"

    top = tk.Tk()
    C1 = tk.Checkbutton(top, text="Sample Option 1")
    C2 = tk.Checkbutton(top, text="Sample Option 2")
    C3 = tk.Checkbutton(top, text="Sample Option 3")

    C1.pack()
    C2.pack()
    C3.pack()
    top.title(title)
    top.mainloop()


sample_checkbox()