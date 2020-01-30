import tkinter as tk

class InputButton(tk.Frame):

    def __init__(self, parent, text = "value", x = 0, y = 0, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.text = text
        self.displayText = []
        self.checkmark = u"\u2713"
        self.xMark = "\u2718" 
        self.crosscheck = "\u2717"
        '''
        checkmark = u"\u2713"
        xMark = "\u2718" 
        crosscheck = "\u2717"
        '''     
        for i in self.text:
            if i == "0":
                self.displayText.append(self.xMark)
            elif i == "1":
                self.displayText.append(self.crosscheck)
            elif i == "2":
                self.displayText.append(self.checkmark)

        self.count = 0
        
        self.tempFrame = tk.LabelFrame(self.parent, 
                                       width = 13)

        self.tempFrame.grid(row = x, column = y, sticky = 'w')

        self.simpleButton = tk.Button(self.tempFrame, 
                                      text = "".join(self.displayText), 
                                      bg= "white",
                                      fg = "black",
                                      borderwidth = 1,
                                      relief = "solid",
                                      width = 13,
                                      command = self.update_button)
        self.simpleButton.pack()
        
        
    def update_button(self):
        newText = self.text
        newDisplayText = self.displayText

        if self.count == 0:
            newText = newText + "2"
            newDisplayText.append(self.checkmark)
            self.simpleButton.configure(background = "yellow")

        elif self.count == 1:
            newText = newText[:-1] + "1"
            newDisplayText[-1]= self.crosscheck

        elif self.count == 2:
            newText = newText[:-1] + "0"
            newDisplayText[-1] = self.xMark

        else:
            newText = newText[:-1]
            del newDisplayText[-1]
            self.simpleButton.configure(background = "white")

        self.simpleButton.configure(text = ''.join(newDisplayText))
        self.count = self.count + 1
        self.text = newText
        self.displayText = newDisplayText
        
        # if the count exceeds 3, reset back to 1
        if self.count > 3:
            self.count = 0

      def getText(self):
          return self.text




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
        


if __name__ == '__main__':

    root = tk.Tk()
    root.geometry('500x400')
    root.title('Test GUI')
    root.configure(background = "white")
    top_frame = tk.Frame(root, bg='red', pady= 3) #, width=450, height=50, pady=3)
    center_frame = tk.LabelFrame(root, bg='white') #,width=50, height=40)
    bottom_frame = tk.Frame(root, bg='lavender', pady=3) #,width=450, height=45)    
    top_frame.grid(row = 0)
    center_frame.grid(row = 2)
    bottom_frame.grid(row = 3)
    
    
    tk.Label(top_frame, 
             text = "title", 
             bg = "red", 
             fg = "white", 
             font = ('arial', 13, 'bold')
             ).grid(row = 0, 
                    column = 0, 
                    sticky = "w", 
                    padx = 20)
                    
    a = InputButton(center_frame, text = "00", x = 0, y = 0)
    
    b = InputButton(center_frame, text = "11", x = 0, y = 1)
    
    studentNames = ["Rory Williams", "Amelia Ponds", "River Song", "Sangeev Narayanaswami"]    
    c = DropdownMenu(top_frame, "Student Name", studentNames, 1)
    root.mainloop()
