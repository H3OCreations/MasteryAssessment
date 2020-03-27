import csv
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

        with open(self.fileName, 'r') as file:
            fileReader = csv.reader(file)
            self.fileData = list(fileReader)
            # Cleaning out all blank lines
            self.fileData = [value for value in self.fileData if value != []]

        # Temporarily declare linebreak for exiting the creation stage
        self.lineBreak = -1
        KICA = ["Knowledge", "Thinking", "Communication", "Application"]

        for rowNum in range(len(self.fileData)):
            # For the sake of not having to reindex self.fileData over and over
            self.row = self.fileData[rowNum]
            rowLength = len(self.row)

            for columnNum in range(rowLength):

                # Verifying that whether we're placing assessment boxes or labels or checkboxes
                # Constructing logic for the remainder of the columns
                if columnNum == 0:
                    self.assessmentLine = False
            
                    # PageOne ends in the communciation section
                    if "Communication" in self.row[columnNum]:
                        self.lineBreak = rowNum
                        break
            
                    # Checks to see whether we are working with
                    if "~" in self.row[columnNum]:
                        self.assessmentLine = True

                    # Placing the assessment strand text and omiting blank lines at the end 
                    # of the file before communication section
                    if rowLength == 0 and (self.row[columnNum + 1].isspace() or len(self.row[columnNum + 1]) == 0):
                        break

                    # Omits the blank lines
                    if len(self.row[columnNum]) == 0:
                        break

                    else:
                        self.populateFirstColumn(rowNum, columnNum)
            
                # Placing Assessment Buttons in the appropriate locations.  
                elif columnNum <= rowLength -3:
                    self.populateBody(rowNum, columnNum)
                                        
                # For the Note Column
                else:
                    self.drawNoteBox(rowNum, columnNum)
                    break
            
            # Final exit condition if we reach the strands outside of the page
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
                                bg = "light grey",
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

        for rowNum in range(self.lineBreak):
            row = self.fileData[rowNum]
            for columnNum in range(len(row)):
                value = row[columnNum]
                
                # Input Button logic
                if isinstance(value, InputButton):
                    # Add section to reset the colour and input status of button
                    #value.setColour("white")
                    #value.count = 0     # This is a sloppy solution to access the attribute
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
        '''
        Combines data from the live editted version of the data with the csv on file
        '''

        with open(self.fileName, "r") as file:
            fileReader = csv.reader(file)
            cloneData = list(fileReader)
            cloneData = [value for value in cloneData if value != []]
            
            for i in range(self.lineBreak):
                if cloneData[i] != self.fileData[i]:
                    cloneData[i] = self.fileData[i]
        self.fileData = cloneData

    def populateFirstColumn(self, rowNum, columnNum):
        '''
        Populates the first column by deciding whether to place an entry box
        or a label
        '''

        assessment_box = False
        if "[" in self.row[columnNum] and "]" in self.row[columnNum]:
            assessment_box = True

        if assessment_box:
            # Width is currently hardcoded until we "get" the regular length
            assessment_entry = tk.Entry(self.center_frame,    
                                width = 105,               
                                relief = "solid",
                                font = ('arial', 11),
                                bg = "light grey")
            assessment_entry.insert(0, self.fileData[rowNum][columnNum])
            assessment_entry.grid(row = rowNum,
                            column = columnNum)
            self.fileData[rowNum][columnNum] = assessment_entry

        else:
            data = self.formatLabelData(self.row[columnNum])
            
            tk.Label(self.center_frame, 
                text = data, 
                borderwidth = 1, 
                relief = "solid", 
                fg = "black", 
                bg = "white", 
                font = ('arial', 11), 
                width = 93, 
                justify = "left",
                anchor = "w").grid( row = rowNum, 
                                    column = columnNum, 
                                    sticky = "W")

    def populateBody(self, rowNum, columnNum):
        '''        
        Populates the the remaining columns with by deciding whether to place an input button
        or a label to fill the space for the empty rows
        '''

        try:
            value = self.row[columnNum]
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
                        #fg = "black",
                        bg = "white",
                        borderwidth = 1,
                        relief = "solid",
                        width = 13,
                        ).grid(row = rowNum,
                            column = columnNum)

    def formatLabelData(self, text, length_delim = 125):
        '''
        Formats text to create a pseudo textwrap function
        '''
        
        if len(text) > length_delim:
            for space in range(-(len(text) - length_delim), -len(text) - 1, -1):
                if text[space] == " ":
                    length_delim = space
                    break
            text = text[:length_delim] + "\n" + text[length_delim:]

        return text