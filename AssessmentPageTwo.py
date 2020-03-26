import os, csv, math, random, sys
import tkinter as tk
from InputTools import *

class PageTwo(tk.Frame):
    
    def __init__(self, parent, path, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        self.center_frame = tk.LabelFrame(self, bg='white')

        # Layout all main containers
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.center_frame.grid(row=1, sticky="nsew")

        bottom_frame = tk.Frame(self, bg = "black")
        bottom_frame.grid(row = 2)

        # Temporary to keep track of what file the object is accessing and the save feature
        #saveButton = tk.Button(bottom_frame, text = "Save")
        #saveButton.bind("<Button-1>", self.savePage)
        #saveButton.pack()

        self.fileName = path
        with open(self.fileName, 'r') as file:
            fileReader = csv.reader(file)
            self.fileData = list(fileReader)
            self.fileData = [value for value in self.fileData if value != []]

        self.continueRow = -1
        self.applicationRows = False    # Flips a switch to allow for application to append the same way
                                        # the rest of page one does

        # Search for the row to start writing from
        for i in range(0, len(self.fileData)):
            if "Communication" in self.fileData[i][0]:
                self.continueRow = i
                break

        for rowNum in range(self.continueRow,len(self.fileData)):
            # For the sake of not having to reindex self.fileData over and over
            row = self.fileData[rowNum]

            for columnNum in range(len(row)):
                

                ################################################################################
                #                                First Column                                  #
                ################################################################################ 

                # Verifying that whether we're placing assessment boxes or labels or checkboxes
                # Constructing logic for the remainder of the columns
                if columnNum == 0:
                    self.assessmentLine = True
                
                    if "Application" in row[0]:
                        self.applicationRows = True
                    
                    if "[" in row[0]:
                        self.assessmentLine = False

                    # Placing the assessment strand text
                    if len(row[0]) == 0 and (row[1].isspace() or len(row[1]) == 0):
                        break
                    
                    elif len(row[0]) == 0:
                        break
                    else:
                         # Testing to see whether we can update the KICA box into an entry box for filler
                        assessment_box = False
                        if "[" in row[columnNum] and "]" in row[columnNum]:
                                assessment_box = True
                        if assessment_box:
                            # Width is currently hardcoded until we "get" the regular length
                            assessment_entry = tk.Entry(self.center_frame,    
                                                width = 140,               
                                                relief = "solid",
                                                bg = "light grey")
                            assessment_entry.insert(0, self.fileData[rowNum][columnNum])
                            assessment_entry.grid(row = rowNum,
                                            column = columnNum)
                            self.fileData[rowNum][columnNum] = assessment_entry
                        else:
                            tk.Label(self.center_frame, 
                                    text = row[0], 
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

                ################################################################################
                #                               Middle Columns                                 #
                ################################################################################
            
                # Placing Assessment Buttons in the appropriate locations.  
                elif columnNum <= len(row) -3:
                    if columnNum == 1 and self.applicationRows != True:
                        tk.Label(self.center_frame, 
                                text = row[columnNum], 
                                borderwidth = 1, 
                                relief = "solid", 
                                fg = "black", 
                                bg = "white", 
                                font = ('arial', 11), 
                                width = 10, 
                                anchor = "w",
                                ).grid(row = rowNum, 
                                        column = columnNum, 
                                        sticky = "W")
                    else:
                        # Placing Assessment Buttons in the appropriate locations 
                        try:
                            value = row[columnNum]
                            
                            if value.isspace() or len(value) == 0:
                                pass
                            else:
                                int(value)
                            
                            if self.assessmentLine == True:
                                newButton = InputButton(self.center_frame, 
                                                        text = value, 
                                                        x = rowNum,
                                                        y = columnNum)
                                self.fileData[rowNum][columnNum] = newButton
                                
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
                else:
                    self.drawNoteBox(rowNum, columnNum)
                    break

    def drawNoteBox(self, rowNum, columnNum):
        '''
        The following function selects between drawing an Entry Box or adding a simple label 
        as the last column.  Parameters are the locations of the double nested for loop used
        to populate the table
        '''
        
        if self.assessmentLine == True:
            noteBox = tk.Entry(self.center_frame,
                                borderwidth = 1,
                                relief = "solid",
                                width = 15)
            noteBox.insert(0, self.fileData[rowNum][columnNum])
            noteBox.grid(row = rowNum,
                            column = columnNum + 1)
            self.fileData[rowNum][columnNum] = noteBox

        else:
            tk.Label(self.center_frame,
                        text = self.fileData[rowNum][columnNum],
                        fg = "black",
                        bg = "white",
                        borderwidth = 1,
                        relief = "solid",
                        width = 13,
                        ).grid(row = rowNum,
                            column = columnNum + 1)  
  
    def save(self):
        '''
        The save function has two stages.  The first is to clean self.fileData back from a 2D list
        of objects into a list of primitives.
        Note that we ignore all the Tkinter labels since we have left the string fields untouched 
        when populating the labels
        '''
        for rowNum in range(self.continueRow, len(self.fileData)):
            row = self.fileData[rowNum]
            for columnNum in range(len(row)):
                value = row[columnNum]
                
                # Input Button logic
                if isinstance(value, InputButton):
                    # Add section to reset the colour and input status of button
                    #value.setColour("white")
                    #value.resetState()     # This is not a real function at this moment
                    self.fileData[rowNum][columnNum] = value.getText()

                # Entry for the note column
                elif isinstance(value, tk.Entry):
                    self.fileData[rowNum][columnNum] = value.get()
        
        self.mergeData()
        # Writes file to .csv 
        with open(self.fileName, 'w') as file:
            writer = csv.writer(file)
            writer.writerows(self.fileData) 

    def mergeData(self):
        with open(self.fileName, "r") as file:
            fileReader = csv.reader(file)
            cloneData = list(fileReader)
            cloneData = [value for value in cloneData if value != []]
            
            for i in range(self.continueRow, len(cloneData)):
                if cloneData[i] != self.fileData[i]:
                    cloneData[i] = self.fileData[i]
        self.fileData = cloneData