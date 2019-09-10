import os, csv, math, random, sys
import tkinter as tk
from InputTools import *


class PageOne(tk.Frame):
    
    def __init__(self, parent, path, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.fileName = path

        # Create main container

        self.center_frame = tk.LabelFrame(self, bg='white') 

        # Layout main container
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.center_frame.grid(row=1, sticky="nsew")

        with open(self.fileName, 'r') as file:
            fileReader = csv.reader(file)
            self.fileData = list(fileReader)
            # Cleaning out all blank lines
            self.fileData = [value for value in self.fileData if value != []]
        
        # Initializing variables 
        length = len(self.fileData)
        width = len(self.fileData[0])
        rowNum = 0
        columnNum = 0
        self.frameData = []

        for line in self.fileData:
            # Verifying that whether we're placing 
            assessmentLine = True
            
            if "Communication" in line[0]:
                break
            
            if "[" in line[0]:
                assessmentLine = False
                
            rowNum = rowNum + 1
            columnNum = 0
            
            # Placing the assessment strand text
            if len(line[0]) == 0 and (line[1].isspace() or len(line[1]) == 0):
                continue
            
            elif len(line[0]) == 0:
                pass
            else:
                tk.Label(self.center_frame, 
                        text = line[0], 
                        borderwidth = 1, 
                        relief = "solid", 
                        fg = "black", 
                        bg = "white", 
                        font = ('arial', 11), 
                        width = 93, 
                        anchor = "w",
                        ).grid(row = rowNum, 
                                column = columnNum, 
                                sticky = "W")
            rowData = []
            
            # Placing Assessment Buttons in the appropriate locations 
            for value in line[1:-1]:   
                addData = False
                try:
                    columnNum = columnNum + 1
                    
                    if value.isspace() or len(value) == 0:
                        pass
                    else:
                        int(value)
                    
                    if assessmentLine == True:    
                        addData = True    
                        newButton = InputButton(self.center_frame, 
                                                text = value, 
                                                x = rowNum,
                                                y = columnNum)
                        rowData.append(newButton)
                        
                    else:
                        int("Force ValueError")
                        
                except ValueError:
                    tk.Label(self.center_frame,
                            text = value,
                            fg = "black",
                            bg = "white",
                            borderwidth = 1,
                            relief = "solid",
                            width = 13,
                            ).grid(row = rowNum,
                                    column = columnNum)
            # For the Note Column
            if assessmentLine == True and ("Mastery" not in line[-2]) and ("[4]" not in line[-2]):
                noteBox = tk.Entry(self.center_frame,
                                borderwidth = 1,
                                relief = "solid",
                                width = 15)
                noteBox.insert(0, line[-1])
                noteBox.grid(row = rowNum,
                            column = columnNum + 1)
            
            else:
                tk.Label(self.center_frame,
                        text = line[-1],
                        fg = "black",
                        bg = "white",
                        borderwidth = 1,
                        relief = "solid",
                        width = 13,
                        ).grid(row = rowNum,
                                column = columnNum + 1)        

            if addData == True:
                self.frameData.append(rowData)   

    def savePage(self, event):
        outputData = []
        for row in self.frameData:
            outputRow = []
            for cell in row:
                (outputRow.append(cell.getText()) for cell in row)
            outputData.append(outputRow)
