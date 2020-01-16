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
        
        bottom_frame = tk.Frame(self, bg = "black")
        bottom_frame.grid(row = 2)

        # Temporary to keep track of what file the object is accessing and the save feature
        saveButton = tk.Button(bottom_frame, text = "Save")
        saveButton.bind("<Button-1>", self.savePage)
        saveButton.pack()

        with open(self.fileName, 'r') as file:
            fileReader = csv.reader(file)
            self.fileData = list(fileReader)
            # Cleaning out all blank lines
            self.fileData = [value for value in self.fileData if value != []]
        
        # Temporarily declare linebreak for exiting the creation stage
        self.lineBreak = -1

        for rowNum in range(len(self.fileData)):
            # For the sake of not having to reindex self.fileData over and over
            row = self.fileData[rowNum]

            for columnNum in range(len(row)):

                ################################################################################
                #                                First Column                                  #
                ################################################################################ 

                # Verifying that whether we're placing assessment boxes or labels or checkboxes
                # Constructing logic for the remainder of the columns
                if columnNum == 0:
                    self.assessmentLine = False
            
                    # PageOne ends in the communciation section
                    if "Communication" in row[columnNum]:
                        self.lineBreak = rowNum
                        break
            
                    # Checks to see whether we are working with
                    if "~" in row[columnNum]:
                        self.assessmentLine = True

                    # Placing the assessment strand text and omiting blank lines at the end 
                    # of the file before communication section
                    if len(row) == 0 and (row[columnNum + 1].isspace() or len(row[columnNum + 1]) == 0):
                        continue

                    # Omits the blank lines
                    if len(row[columnNum]) == 0:
                        pass
                    else:
                        strandLabel = tk.Label(self.center_frame, 
                                            text = row[columnNum], 
                                            borderwidth = 1, 
                                            relief = "solid", 
                                            fg = "black", 
                                            bg = "white", 
                                            font = ('arial', 11), 
                                            width = 93, 
                                            anchor = "w")
                        strandLabel.grid(row = rowNum, 
                                        column = columnNum, 
                                        sticky = "W")

                ################################################################################
                #                               Middle Columns                                 #
                ################################################################################
            
                # Placing Assessment Buttons in the appropriate locations.  
                elif columnNum <= len(row) -3:
                    try:
                        value = row[columnNum]
                        # Skip all empty lines
                        if value.isspace() or len(value) == 0:
                            pass
                        else:
                            int(value)
                    
                        if self.assessmentLine == True:    
                            button = InputButton(self.center_frame, 
                                                text = value, 
                                                x = rowNum,
                                                y = columnNum)
                            # Place the input button into the location and contain the value 
                            self.fileData[rowNum][columnNum] = button
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
                
            if self.lineBreak == rowNum:
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
        

    def savePage(self, event):
        '''
        The save function has two stages.  The first is to clean self.fileData back from a 2D list
        of objects into a list of primitives.
        Note that we ignore all the Tkinter labels since we have left the string fields untouched 
        when populating the labels
        '''
        for rowNum in range(len(self.fileData)):
            row = self.fileData[rowNum]
            for columnNum in range(len(row)):
                value = row[columnNum]
                
                # Input Button logic
                if isinstance(value, InputButton):
                    self.fileData[rowNum][columnNum] = value.getText()

                # Entry for the note column
                elif isinstance(value, tk.Entry):
                    self.fileData[rowNum][columnNum] = value.get()
        
        # Writes file to .csv 
        with open(self.fileName, 'w') as file:
            writer = csv.writer(file)
            writer.writerows(self.fileData) 
        