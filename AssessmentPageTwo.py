import os, csv, math, random, sys
import tkinter as tk
from InputTools import *


class PageTwo(tk.Frame):
    
    def __init__(self, parent, path, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        # Create all main containers
       # self.top_frame = TopFrame(self, bg='red', pady= 3, padx = 3) 
        #self.top_frame.configure(background = "red") 
        
        self.center_frame = tk.LabelFrame(self, bg='white')
        #self.bottom_frame = tk.Frame(self, bg='lavender', pady=3)

        # Layout all main containers
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        #self.top_frame.grid(row=0, sticky="ew")
        self.center_frame.grid(row=1, sticky="nsew")
        #self.bottom_frame.grid(row=4, sticky="ew")

        self.fileName = path
        with open(self.fileName, 'r') as file:
            fileReader = csv.reader(file)
            self.fileData = list(fileReader)
            self.fileData = [value for value in self.fileData if value != []]

        # Initializing variables 
        length = len(self.fileData)
        width = len(self.fileData[0])
        rowNum = 0
        columnNum = 0
        self.frameData = []
        applicationRows = False
        continueRow = 0

        for i in range(0, len(self.fileData)):
            if "Communication" in self.fileData[i][0]:
                continueRow = i
                break

        for line in self.fileData[continueRow:]:
            # Verifying that whether we're placing 
            assessmentLine = True
            
            if "Application" in line[0]:
                applicationRows = True
            
            if "[" in line[0]:
                assessmentLine = False
                
            rowNum = rowNum + 1
            columnNum = 0
            startNum = 2

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
                
                if applicationRows == True:
                    startNum = 1

                else:
                    columnNum = columnNum + 1
                    tk.Label(self.center_frame, 
                            text = line[1], 
                            borderwidth = 1, 
                            relief = "solid", 
                            fg = "black", 
                            bg = "white", 
                            font = ('arial', 11), 
                            width = 13, 
                            anchor = "w",
                            ).grid(row = rowNum, 
                                    column = columnNum, 
                                    sticky = "W") 
                                
            rowData = []
            
            # Placing Assessment Buttons in the appropriate locations 
            for value in line[startNum:-1]:   
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
                        rowData.append(value)
                        
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
                try:
                    outputRow.append(cell.getText())
                    
                except AttributeError:
                    # Ignores cells when they're not input buttons
                    #print("An exception was made")
                    outputRow.append(cell.get())
                    
            if len(outputRow) < 2:
                # Ignores rows not a part of the assessment data
                pass
            else:
                outputData.append(outputRow)

        appendCount = 0

        for line in self.fileData[:self.lineBreak]:
            try:
                # Sometimes, lines are empty and will cause an index error
                if "~" in line[0] and "~" == line[0][0]:
                    num = self.fileData.index(line)
                    self.fileData[self.fileData.index(line)] = [line[0]] + outputData[appendCount]
                    appendCount = appendCount + 1
            except IndexError:
                pass

        with open(self.fileName, 'w') as file:
            writer = csv.writer(file)
            writer.writerows(self.fileData) 