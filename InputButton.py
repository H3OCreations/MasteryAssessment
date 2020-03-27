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
        self.multi_edit = False         # For future feature where we can populate multiple values in the 
                                        # same instance of inputting
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