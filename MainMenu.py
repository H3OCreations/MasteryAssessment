import os, csv, math, random, collections, fileinput, shutil, sys
import tkinter as tk
import tkinter.messagebox
from tkinter import filedialog  
from datetime import datetime

# Custom package import
from AssessmentMainPage import *

class MainMenu(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # Makes sure that the directories we wish to access are present
        self.workingDirectory = os.getcwd()
        self.directories = [self.workingDirectory + "\\Units",
                            self.workingDirectory + "\\Past Data"
                            ]
        for folder in self.directories:
            if not os.path.isdir(folder):
                os.mkdir(folder)
       
        self.top_frame = tk.Frame(self, bg='cyan', width=450, height=50, pady=3)
        self.center_frame = tk.Frame(self, bg='gray2', width=50, height=40, padx=3, pady=3)
        self.bottom_frame = tk.Frame(self, bg='white', width=450, height=45, pady=3)

        self.top_frame.grid(row = 1, sticky = "ew")
        self.center_frame.grid(row = 2, sticky = "nsew")
        self.bottom_frame.grid(row = 3, sticky = "nsew")

        title = tk.Label(self.top_frame, text = "Welcome")
        title.pack()

        self.directoryList = self.listSections()

        initButton = tk.Button(self.center_frame, text = "Initialize Unit", width = 15, pady = 10)
        initButton.bind("<Button-1>", self.initialize)
        initButton.grid(row = 1)

        recordButton = tk.Button(self.center_frame, text = "Record Assessment", width = 15, pady = 10)
        recordButton.bind("<Button-1>", self.recordData)
        recordButton.grid(row = 2)

        calculateButton = tk.Button(self.center_frame, text = "Calculate Marks", width = 15, pady = 10)
        calculateButton.bind("<Button-1>", self.calculateData)
        calculateButton.grid(row = 3)
           
        exitButton = tk.Button(self.bottom_frame, text = "Exit", width = 15)
        exitButton.bind("<Button-1>", self.exitWindow)
        exitButton.pack(side = "right")

    def exitWindow(self, event):
        self.withdraw()
        self.destroy()

    def initialize(self, event):
        '''
        Initializes directories by creating file structures the program will use 
        for the program itself
        '''
                    
        # Set up the student data and format the directories for student Data
        tk.messagebox.showinfo("Alert", "Select the TeachAssist Classlist")  
        classListPath = filedialog.askopenfilename(initialdir = os.getcwd(), title = "Select Class list", filetypes = (("CSV files", "*.csv"),("TXT files", "*.txt"), ("All files", "*.*")))
        tk.messagebox.showinfo("Alert", "Select Unit Assessment Chart in .csv format")
        chartTemplatePath = filedialog.askopenfilename(initialdir = os.getcwd(), title = "Select Assessment Chart", filetypes = (("CSV files", "*.csv"),("TXT files", "*.txt"), ("All files", "*.*")))
        
        # formatting for unit path name
        delim = (chartTemplatePath[::-1]).index("/")
        unitName = chartTemplatePath[-delim:-4]
        unitDirectory = self.directories[0] + "\\" + unitName
        
        # formatting for section path name
        delim1 = (classListPath[::-1]).index("/")
        delim2 = len(classListPath) - classListPath.index("_")
        className = classListPath[-delim1:-delim2]
        classDirectory = unitDirectory + "\\" + className
        
        # Function is protected within the initialization function (for some reason, I decided this)
        # The reason is probably to reuse the variables within the initialize function
        def cleanData(fileName):
            '''
            The function takes in the target .csv file and removes all the formatting from the
            direct copy and paste from word to excel.  It also ensures that all  rows are the 
            exact same length 
            '''
            with open(fileName , encoding = "utf-8", errors = "ignore") as file:
                fileReader = csv.reader(file)
                fileData = list(fileReader)

                # Removes all unicode and utf-8 from strings
                for row in fileData:
                    (column.encode("ascii", "ignore").decode("ascii") for column in row)
                
                # Removes blank rows
                if (max(len(i) for i in row)) == 0:
                    del fileData[fileData.index(row)]

                for i in range(0, len(fileData)):
                    if "-" in fileData[i][0]:
                        if "-" in fileData[i][0][:3]:
                            fileData[i][0] = fileData[i][0].replace("-", "~", 1)
            
            return fileData

        # Also one of the protected functions within the initialize function
        def writeFiles(assessmentData, classList):
            '''
            The function copies the cleaned assessment chart and renames them the student name
            '''
            assessmentData = cleanData(assessmentData)
            
            with open(classList, "r") as file:
                classReader = csv.reader(file)
                classData = list(classReader)      
                file.close()
            
            for line in classData[1:]:
                fileName = classDirectory + "\\" + str(line[2] + ", " + line[1] + ".csv")
                
                # Formatting the Assessment Charts
                newFile = open(fileName, "a")
                writer = csv.writer(newFile, delimiter = ",", quoting = csv.QUOTE_MINIMAL)
                for row in assessmentData:
                    writer.writerow(row)
                newFile.close()     
        
        # Here is where we create the file directories
        try:
            os.mkdir(unitDirectory)
            try:
                os.mkdir(classDirectory)
                writeFiles(chartTemplatePath, classListPath)
                tk.messagebox.showinfo("Done", "Initialization Complete!")  
            except FileExistsError:
                tk.messagebox.showinfo("Alert", "This unit has already been created.  To reinitialize a unit, you must delete the %s class folder" %(className))

        except FileExistsError:
            try:
                os.mkdir(classDirectory)
                writeFiles(chartTemplatePath, classListPath)

            except FileExistsError:
                tk.messagebox.showinfo("Alert", "This unit has already been created.  To reinitialize a unit, you must delete the %s folder" %(unitName))
        
    def listSections(self):
        
        #Export Format
        #Unit                                       | Unit               
        #{section: classlist, section: classlist}   |   {section: classlist, section: classlist} 
        
        unitList = os.listdir(self.directories[0])
        sectionRow = []
        sectionGroups = []
        for unit in unitList:
            sectionList = os.listdir(self.directories[0] + "\\" + unit)
            sectionRow.append(sectionList)
            sectionDict = {}
            for section in sectionList:
                sectionDict[section] = os.listdir(self.directories[0] + "\\" + unit + "\\" + section)
            sectionGroups.append(sectionDict)

        df = [unitList, sectionRow, sectionGroups]
        return df
    
    def recordData(self, event):
        tk.Label(self.center_frame, 
                text = "Select The Unit, then Click OK", 
                bg = "black", 
                fg = "white").grid(row = 1, column = 2)
        units = self.listSections()[0]
        
        self.unitMenu = DropdownMenu(self.center_frame, "Unit Name", units, 2, rw = 2)
        
        okButton = tk.Button(self.center_frame, 
                            text = "OK", 
                            width = 15)
        okButton.bind("<Button-1>", self.populateSectionMenu)
        okButton.grid(row = 4, column = 2)


    def populateSectionMenu(self, event):
        tk.Label(self.center_frame, 
        text = "Select The Section, then Click OK", 
        bg = "black", 
        fg = "white").grid(row = 1, column = 3)
        classSection = self.listSections()[2]
        self.sectionMenu = DropdownMenu(self.center_frame, "Section Number", self.listSections()[1][0], 3, rw = 2)
        
        okButton = tk.Button(self.center_frame, 
                        text = "OK", 
                        width = 15)
        
        okButton.bind("<Button-1>", self.populateAssessmentChart)
        okButton.grid(row = 4, column = 3)

    def populateAssessmentChart(self, event):
        unitChart = self.unitMenu.selected
        classSection = self.sectionMenu.selected
        classList = self.directoryList[2][self.directoryList[0].index(unitChart)].get(classSection)
        classPath = os.getcwd() + "\\Units\\" + unitChart + "\\"  + classSection
        self.destroy()
        configInfo = [unitChart, classSection, classList]
        app = AssessmentPage(classPath, configInfo)

    def calculateData(self, event):
        # Export csv with all calculated marks
        # Export all chart pdfs
        # Export all radar diagrams
        
        # archive data
        archiveName = datetime.now()
        archiveName = archiveName.strftime("%Y-%m-%d-(%H-%M)")
        try:
            backupName = self.directories[1] + "\\" + archiveName
            os.mkdir(backupName)
        except FileExistsError:
            response = tk.messagebox.askquestion("Archive Error", "Your Data has been archived today already.  Would you like to override today's existing archive?")
            # If user clicks 'Yes' then it returns "yes" else it returns 'no'
            if response == "yes":
                shutil.rmtree(backupName)
                os.mkdir(backupName)
            else:
                pass
        tk.messagebox.showinfo("Alert", "Archive Complete")
    

if __name__ == "__main__":
    root = MainMenu()
    winWidth = "500"
    winLength = "350"
    root.geometry('{}x{}'.format(winWidth, winLength))
    root.title("Main Menu")
    root.grid_rowconfigure(1, weight=1)
    root.grid_columnconfigure(0, weight=1)
    root.mainloop()