# Problem #
We want to be able to program GUIs to our applications in python.

# Questions #
1. What is Python's native GUI toolkit?

# Resources #
1. [Python GUI Programming (Tkinter)]

### Mini-abstract and relevance of [Python GUI Programming (Tkinter)] ###

Python's native GUI toolkit is Tkinter. Tkinter is object oriented so it feels very similar to programming GUIs with Java's Swing.

The standard formula for creating a Tkinter GUI is as follows:

> Import the Tkinter module.

> Create the GUI application main window.

> Add one or more of the Tkinter widgets to the GUI frame

> Enter the main event loop to take action against each event triggered by the user.

Tkinter has a variety of widgets that can be graphically rendered:

|    Widget   | Description                                                             | Sample Image  |
|:-----------:|-------------------------------------------------------------------------|---|
|    Button   | Renders a button in your application                                    | <img src="https://github.com/Bryconc/CS3535/blob/master/Inquiry%20Report%204%20-%20GUI%20Programming/Sample%20Images/Sample%20Button.png?raw=true">  |
|    Canvas   | Draws shapes in your application                                        | <img src="https://github.com/Bryconc/CS3535/blob/master/Inquiry%20Report%204%20-%20GUI%20Programming/Sample%20Images/Sample%20Canvas.png?raw=true">  |
| Checkbutton | Displays options as checkboxes. The user can select multiple options    | <img src="https://github.com/Bryconc/CS3535/blob/master/Inquiry%20Report%204%20-%20GUI%20Programming/Sample%20Images/Sample%20Checkbox.png?raw=true">  |
| Entry       | Single line text input field                                            | <img src="https://github.com/Bryconc/CS3535/blob/master/Inquiry%20Report%204%20-%20GUI%20Programming/Sample%20Images/Sample%20Entry.png?raw=true">  |
| Frame       | Container widget that can be used for organization purposes             | <img src="https://github.com/Bryconc/CS3535/blob/master/Inquiry%20Report%204%20-%20GUI%20Programming/Sample%20Images/Sample%20Frame.png?raw=true">  |
| Label       | Single line captions. Also can be used as images                        | <img src="https://github.com/Bryconc/CS3535/blob/master/Inquiry%20Report%204%20-%20GUI%20Programming/Sample%20Images/Sample%20Label.png?raw=true">  |
| Listbox     | A list of options for the user                                          | <img src="https://github.com/Bryconc/CS3535/blob/master/Inquiry%20Report%204%20-%20GUI%20Programming/Sample%20Images/Sample%20Listbox.png?raw=true">  |
| Menubutton  | Used to display menus                                                   | <img src="https://github.com/Bryconc/CS3535/blob/master/Inquiry%20Report%204%20-%20GUI%20Programming/Sample%20Images/Sample%20Menubutton.png?raw=true">  |
| Message     | Multi-line text field                                                   | <img src="https://github.com/Bryconc/CS3535/blob/master/Inquiry%20Report%204%20-%20GUI%20Programming/Sample%20Images/Sample%20Message.png?raw=true">  |
| Radiobutton | Displays options as radio buttons. The user can select multiple options | <img src="https://github.com/Bryconc/CS3535/blob/master/Inquiry%20Report%204%20-%20GUI%20Programming/Sample%20Images/Sample%20Radiobutton.png?raw=true">  |
| Scale       | Serves as a slider widget                                               | <img src="https://github.com/Bryconc/CS3535/blob/master/Inquiry%20Report%204%20-%20GUI%20Programming/Sample%20Images/Sample%20Scale.png?raw=true">  |
| Scrollbar   | Adds a scroll bar to other widgets, such as list boxes                  | <img src="https://github.com/Bryconc/CS3535/blob/master/Inquiry%20Report%204%20-%20GUI%20Programming/Sample%20Images/Sample%20Scrollbar.png?raw=true">  |
| Text        | Multi-line inputs. Can be formatted                                     | <img src="https://github.com/Bryconc/CS3535/blob/master/Inquiry%20Report%204%20-%20GUI%20Programming/Sample%20Images/Sample%20Text.png?raw=true">  |

I have included all the code required to produce the sample images above in gui_text.py

For instance the basic structure for creating a Tkinter can be seen in this sample_button() method.

```python

    def sample_button():
        title = "Sample Button"

        top = tk.Tk()
        B = tk.Button(top, text="Sample Button")

        B.pack()
        top.title(title)
        top.mainloop()
```

This creates a window titled "Sample Button". With a button with the text "Sample Button"

The standard structure is to pass the root frame for each widget in the constructor. The widget is then added to the root frame, by calling the pack() method. A variety of parameters will determine its placement; more can be seen on its tutorial page [Python Tkinter pack() Method]

The window is then displayed by calling the mainloop method.


[Python GUI Programming (Tkinter)]: http://www.tutorialspoint.com/python/python_gui_programming.htm
[Python Tkinter pack() Method]:http://www.tutorialspoint.com/python/tk_pack.htm