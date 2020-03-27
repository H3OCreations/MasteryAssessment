import os, csv, shutil, sys
import tkinter as tk
import tkinter.messagebox
from tkinter import filedialog  
from datetime import datetime

# Custom package import
from AssessmentMainPage import *
from MasteryTools import *
from DropDownMenu import *
from InputButton import *

class MainMenu(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # Makes sure that the directories we wish to access are present
        self.workingDirectory = os.getcwd()
        self.subdirectories = [self.workingDirectory + "\\Units",
                            self.workingDirectory + "\\Past Data"
                            ]
        for folder in self.subdirectories:
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
        initButton.bind("<Button-1>", self.initializeFile)
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

    def initializeFile(self, event):
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
        unitDirectory = self.subdirectories[0] + "\\" + unitName
        
        # formatting for section path name
        delim1 = (classListPath[::-1]).index("/")
        delim2 = len(classListPath) - classListPath.index("_")
        className = classListPath[-delim1:-delim2]
        self.classDirectory = unitDirectory + "\\" + className
        
        # Here is where we create the file directories
        try:
            os.mkdir(unitDirectory)
            try:
                os.mkdir(self.classDirectory)
                self.writeFiles(chartTemplatePath, classListPath)
                tk.messagebox.showinfo("Done", "Initialization Complete!")  
            except FileExistsError:
                tk.messagebox.showinfo("Alert", "This unit has already been created.  To reinitialize a unit, you must delete the %s class folder" %(className))

        except FileExistsError:
            try:
                os.mkdir(self.classDirectory)
                self.writeFiles(chartTemplatePath, classListPath)

            except FileExistsError:
                tk.messagebox.showinfo("Alert", "This unit has already been created.  To reinitialize a unit, you must delete the %s folder" %(unitName))
    
    def cleanData(self, fileName):
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

    
    def writeFiles(self, assessmentData, classList):
        '''
        The function cleans the assessment chart that was inputted and then proceeds to 
        name each file based on each student name in the class list
        '''
        
        assessmentData = self.cleanData(assessmentData)
        
        with open(classList, "r") as file:
            classReader = csv.reader(file)
            classData = list(classReader)      
            file.close()
        
        for line in classData[1:]:
            fileName = self.classDirectory + "\\" + str(line[2] + ", " + line[1] + ".csv")
            
            # Formatting the Assessment Charts
            newFile = open(fileName, "a")
            writer = csv.writer(newFile, delimiter = ",", quoting = csv.QUOTE_MINIMAL)
            for row in assessmentData:
                writer.writerow(row)
            newFile.close()     

        # Cloning a random file to get around the current saving issue    
        shutil.copyfile(fileName, self.classDirectory + "\\AAAAA_Template.csv")
        
    def listSections(self):
        '''
        Creates a dictionary containing an organized structure of the directories.  The outer most 
        dictionary has keys for the units (unit 1, unit 2, unit 3...)
        The values of these keys are sepreate dictionaries in the format: <course-code>:<classlist>

        Visualization of the data structure is below:
        Unit                                       | Unit               
        {section: classlist, section: classlist}   |   {section: classlist, section: classlist} 
        '''

        unitList = os.listdir(self.subdirectories[0])
        sectionRow = []
        sectionGroups = []
        for unit in unitList:
            sectionList = os.listdir(self.subdirectories[0] + "\\" + unit)
            sectionRow.append(sectionList)
            sectionDict = {}
            for section in sectionList:
                sectionDict[section] = os.listdir(self.subdirectories[0] + "\\" + unit + "\\" + section)
            sectionGroups.append(sectionDict)

        df = [unitList, sectionRow, sectionGroups]
        return df
    
    def recordData(self, event):
        '''
        Generates appropriate drop down menues to select the desired charts and allows the user
        to select which unit they wish to input marks
        '''

        tk.Label(self.center_frame, 
                text = "Select The Unit, then Click OK", 
                bg = "black", 
                fg = "white").grid(row = 1, column = 2)
        
        # Refresh directory list just in case new directories were initialized
        self.directoryList = self.listSections()
        units = self.listSections()[0]      # Need to fix this over-call on listSections now that directories is fixes
        
        self.unitMenu = DropdownMenu(self.center_frame, "Unit Name", units, 2, rw = 2)
        
        okButton = tk.Button(self.center_frame, 
                            text = "OK", 
                            width = 15)
        okButton.bind("<Button-1>", self.populateSectionMenu)
        okButton.grid(row = 4, column = 2)

    def populateSectionMenu(self, event):
        '''Creates drop down menu for the list of classes'''

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
        ''' Generates the list of files and directory locations in order to generate the charts'''

        unitChart = self.unitMenu.selected
        classSection = self.sectionMenu.selected
        classList = self.directoryList[2][self.directoryList[0].index(unitChart)].get(classSection)
        classPath = os.getcwd() + "\\Units\\" + unitChart + "\\"  + classSection
        self.destroy()
        configInfo = [unitChart, classSection, classList]
        app = AssessmentMainPage(classPath, configInfo)

    def calculateData(self, event):
        ''' Export csv with all calculated marks of a selected directory'''
        
        # Identifies path for calculations to execute
        tk.messagebox.showinfo("Alert", "Select the folder witht he class's unit you wish to calculate")  
        unitPath = filedialog.askdirectory(initialdir = self.subdirectories[0], title = "Select Class")
        
        # Ittereatively calculating the marks for each csv
        for file in os.listdir(unitPath):
            filePath = unitPath + "//" + file
            MasteryTools(filePath).save_results()

        # Backing up data into archive directory
        archiveName = datetime.now()
        archiveName = archiveName.strftime("%Y-%m-%d-(%H-%M)") 

        try:
            backupName = self.subdirectories[1] + "\\" + archiveName 
            #os.mkdir(backupName)
            shutil.copytree(unitPath, backupName)

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