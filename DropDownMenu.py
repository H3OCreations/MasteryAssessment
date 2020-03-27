import tkinter as tk

class DropdownMenu:
    def __init__(self, frame, title, data, col, rw = 1):
        # Create a Tkinter variable
        self.tkvar = tk.StringVar(frame)
    
        # Dictionary with options
        self.tkvar.set(data[0]) # set the default option
        
        self.selected = data[0] # set the default option

        self.popupMenu = tk.OptionMenu(frame, self.tkvar, *data)
        tk.Label(frame, 
                 text = title, 
                 bg = "red", 
                 fg = "white", 
                 font = ('arial', 13, 'bold')
                 ).grid(row = rw, 
                        column = col, 
                        sticky = "w", 
                        padx = 20)
        self.popupMenu.grid(row = rw + 1, column = col)
        
        # on change dropdown value
        def change_dropdown(*args):
            self.selected = self.tkvar.get()
        
        #def setMenu(self, value):
        #    self.tkvar.set(value)
        # link function to change dropdown
        self.tkvar.trace('w', change_dropdown)