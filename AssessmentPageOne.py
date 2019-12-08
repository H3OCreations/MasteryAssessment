import os, csv, math, random, sys
import tkinter as tk
from InputTools import *


class PageOne(tk.Frame):
    
    def __init__(self, parent, path, controller):

        # Inherits the appropriate frame properties for the main frame to control it
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.fileName = path

        # Create main container
        self.center_frame = tk.LabelFrame(self, bg='white') 

        # Layout main container
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.center_frame.grid(row=1, sticky="nsew")
        
        self.bottom_frame = tk.Frame(self, bg = "black")
        self.bottom_frame.grid(row = 2)

        # Temporary to keep track of what file the object is accessing and the save feature
        self.saveButton = tk.Button(self.bottom_frame, text = "Save")
        self.saveButton.bind("<Button-1>", self.savePage)
        self.saveButton.pack()
        tracker = tk.Label(self.bottom_frame, text = path).pack()

        with open(self.fileName, 'r') as file:
            fileReader = csv.reader(file)
            self.fileData = list(fileReader)
            # Cleaning out all blank lines
            self.fileData = [value for value in self.fileData if value != []]

        # Initializing variables 
        rowNum = 0
        self.frameData = []

        for line in self.fileData:

            # Verifying that whether we're placing assessment boxes or labels
            assessmentLine = False
            
            # PageOne ends in the communciation section
            if "Communication" in line[0]:
                self.lineBreak = self.fileData.index(line)
                break
            
            # Checks to see whether we are working with
            if "~" in line[0]:
                assessmentLine = True
                
            rowNum = rowNum + 1
            columnNum = 0
            rowData = []

            # Placing the assessment strand text
            if len(line[0]) == 0 and (line[1].isspace() or len(line[1]) == 0):
                continue
            
            elif len(line[0]) == 0:
                pass
            else:
                rowData.append( tk.Label(self.center_frame, 
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
                               )
            
            
            # Placing Assessment Buttons in the appropriate locations 
            for value in line[1:-2]:  
                #addData = False
                try:
                    columnNum = columnNum + 1
                    
                    if value.isspace() or len(value) == 0:
                        pass
                    else:
                        int(value)
                    
                    if assessmentLine == True:    
                        #addData = True    
                        rowData.append(InputButton(self.center_frame, 
                                                text = value, 
                                                x = rowNum,
                                                y = columnNum)
                                        )
                        
                        
                    else:
                        int("Force ValueError")
                        
                except ValueError:
                    rowData.append( tk.Label(self.center_frame,
                                    text = value,
                                    fg = "black",
                                    bg = "white",
                                    borderwidth = 1,
                                    relief = "solid",
                                    width = 13,
                                    ).grid(row = rowNum,
                                            column = columnNum)
                                    )
            # For the Note Column
            #if assessmentLine == True and ("Mastery" not in line[-2]) and ("[4]" not in line[-2]):
            if assessmentLine == True:
                noteBox = tk.Entry(self.center_frame,
                                borderwidth = 1,
                                relief = "solid",
                                width = 15)
                noteBox.insert(0, line[-2])
                noteBox.grid(row = rowNum,
                            column = columnNum + 1)
                rowData.append(noteBox)
            
            else:
                rowData.append( tk.Label(self.center_frame,
                                text = line[-2],
                                fg = "black",
                                bg = "white",
                                borderwidth = 1,
                                relief = "solid",
                                width = 13,
                                ).grid(row = rowNum,
                                       column = columnNum + 1)        
                              )
            #if addData == True:
            # Temporary fix to make sure my rows are the same size
            (rowData.append("") for i in range(len(self.fileData[0]) - len(rowData)))

            self.frameData.append(rowData)   
        
        '''
        for i in self.frameData:
            print(i)
        print()
        '''

    def savePage(self, event):
        outputData = []
        for row in self.frameData:
            outputRow = []
            for cell in row:
                try:
                    outputRow.append(cell.getText())
                    
                except AttributeError:
                    
                    # Try for Entry Boxes
                    try:
                        outputRow.append(cell.get())
                    
                    except AttributeError:
                        outputRow.append(cell)

            outputData.append(outputRow)
        appendCount = 0

        for line in self.fileData[:self.lineBreak]:
            try:
                # Sometimes, lines are empty and will cause an index error
                if "~" in line[0]:
                    num = self.fileData.index(line)
                    self.fileData[self.fileData.index(line)] = [line[0]] + outputData[appendCount]
                    appendCount = appendCount + 1
            except IndexError:
                pass

        with open(self.fileName, 'w') as file:
            writer = csv.writer(file)
            writer.writerows(self.fileData) 