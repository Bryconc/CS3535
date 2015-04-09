# Problem #
We want to be able to program GUIs to our applications in python.

# Questions #
1. What is Python's native GUI toolkit?
2. What third party python libraries can help build GUIs?

# Resources #
1. [Python GUI Programming (Tkinter)]
2. [Jython Documentation]

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
| Message     | Multi-line text input field                                             | <img src="https://github.com/Bryconc/CS3535/blob/master/Inquiry%20Report%204%20-%20GUI%20Programming/Sample%20Images/Sample%20Checkbox.png?raw=true">  |
| Radiobutton | Displays options as radio buttons. The user can select multiple options | <img src="https://github.com/Bryconc/CS3535/blob/master/Inquiry%20Report%204%20-%20GUI%20Programming/Sample%20Images/Sample%20Checkbox.png?raw=true">  |
| Scale       | Serves as a slider widget                                               | <img src="https://github.com/Bryconc/CS3535/blob/master/Inquiry%20Report%204%20-%20GUI%20Programming/Sample%20Images/Sample%20Checkbox.png?raw=true">  |
| Scrollbar   | Adds a scroll bar to other widgets, such as list boxes                  | <img src="https://github.com/Bryconc/CS3535/blob/master/Inquiry%20Report%204%20-%20GUI%20Programming/Sample%20Images/Sample%20Checkbox.png?raw=true">  |
| Text        | Multi-line captions.                                                    | <img src="https://github.com/Bryconc/CS3535/blob/master/Inquiry%20Report%204%20-%20GUI%20Programming/Sample%20Images/Sample%20Checkbox.png?raw=true">  |
| PanedWindow | Contains any number of panes arranged horizontally or vertically        | <img src="https://github.com/Bryconc/CS3535/blob/master/Inquiry%20Report%204%20-%20GUI%20Programming/Sample%20Images/Sample%20Checkbox.png?raw=true">  |
### Mini-abstract and relevance of [Jython Documentation] ###

[Python GUI Programming (Tkinter)]: http://www.tutorialspoint.com/python/python_gui_programming.htm
[Jython Documentation]: http://www.jython.org/docs/index.html