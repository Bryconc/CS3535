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


def sample_entry():
    title = "Sample Entry"

    top = tk.Tk()
    L = tk.Label(top, text="Sample Entry")
    E = tk.Entry(top)
    L.pack(side=tk.LEFT)
    E.pack(side=tk.RIGHT)

    E.insert(0, "Default Text")

    top.title(title)
    top.mainloop()


def sample_frame():
    title = "Sample Frame"

    top = tk.Tk()

    fr = tk.Frame(top)
    fr.pack()

    bFr = tk.Frame(top)
    bFr.pack(side=tk.BOTTOM)

    top1 = tk.Button(fr, text="Top 1")
    top2 = tk.Button(fr, text="Top 2")
    top1.pack(side=tk.LEFT)
    top2.pack(side=tk.LEFT)

    bottom = tk.Button(bFr, text="Bottom 1")
    bottom.pack()

    top.title(title)
    top.mainloop()


def sample_label():
    title = "Sample Label"

    top = tk.Tk()

    var = tk.StringVar()
    L = tk.Label(top, textvariable=var)
    var.set("Sample Text in the variable")
    L.pack()

    top.title(title)
    top.mainloop()


def sample_listbox():
    title = "Sample Listbox"

    top = tk.Tk()

    Lb = tk.Listbox(top)
    Lb.insert(1, "Option 1")
    Lb.insert(2, "Option 2")
    Lb.insert(3, "Option 3")
    Lb.pack()

    top.title(title)
    top.mainloop()


def sample_menubutton():
    title = "Sample Menubutton"

    top = tk.Tk()

    mb = tk.Menubutton(top, text="Menu")
    mb.grid()

    mb.menu = tk.Menu(mb)
    mb["menu"] = mb.menu

    mb.menu.add_checkbutton(label="Option 1")
    mb.menu.add_checkbutton(label="Option 2")

    mb.pack()

    top.title(title)
    top.mainloop()


def sample_message():
    title = "Sample Message"

    top = tk.Tk()
    M = tk.Message(top, text="Sample multiline message. Sample multiline message. Sample multiline message.")
    M.pack()

    top.title(title)
    top.mainloop()


def sample_radiobutton():
    def sel():
        selection = "You selected the option " + str(var.get())
        label.config(text=selection)

    title = "Sample Radiobutton"

    top = tk.Tk()
    var = tk.IntVar()
    R1 = tk.Radiobutton(top, text="Option 1", variable=var, value=1, command=sel)
    R1.pack(anchor=tk.W)

    R2 = tk.Radiobutton(top, text="Option 2", variable=var, value=2, command=sel)
    R2.pack(anchor=tk.W)

    R3 = tk.Radiobutton(top, text="Option 3", variable=var, value=3, command=sel)
    R3.pack(anchor=tk.W)

    label = tk.Label(top)
    label.pack()
    top.title(title)
    top.mainloop()


def sample_scale():
    title = "Sample Scale"

    top = tk.Tk()

    scale = tk.Scale(top, orient=tk.HORIZONTAL)
    scale.pack(anchor=tk.CENTER)

    top.title(title)
    top.mainloop()


sample_scale()