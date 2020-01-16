import os, csv, math, random, collections, fileinput, shutil, sys
import tkinter as tk
from InputTools import *
from AssessmentPageOne import *
from AssessmentPageTwo import *
#from MainMenu import *


class AssessmentPage(tk.Tk):

    def __init__(self, path, chartConfig, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others

        top_frame = TopFrame(self, chartConfig, bg='red', pady= 3, padx = 3, controller = self) 
        top_frame.configure(background = "red")
        top_frame.pack(side = "top", fill = "both")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        bottom_frame = BottomFrame(parent=self, controller=self)
        bottom_frame.pack(side = "bottom", fill = "both")

        # Generating All Pages
        classList = os.listdir(path)
        files = [path + "\\" + i for i in classList]
        self.frames = {}

        for i in range(0, len(classList)):
            # In the future, create a system that queues the next two charts in each direction
            # allow it to update as the next button is clicked and delete the outer most charts
            for F in (PageOne, PageTwo):
                page_name = classList[i] + F.__name__
                frame = F(parent=container, path = files[i], controller=self)
                self.frames[page_name] = frame

                # put all of the pages in the same location;
                # the one on the top of the stacking order
                # will be the one that is visible.
                #frame.grid(row=0, column=0, sticky="nsew")

        

        self.current_student = classList[0]
        self.current_page = "PageOne"
        self.show_frame(self.current_student + self.current_page)

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.grid(row=0, column=0, sticky="nsew")
        frame.tkraise()
################################################################################
#                                   Top Frame                                  #
################################################################################  
class TopFrame(tk.Frame):
    
    def __init__(self, parent, chartConfig, controller, *args, **kwargs):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller

        # Dependancies on Dropdown Menus
        
        '''
        # This section will be fixed once we figure out how to dynamically populate dropdowns as
        # we go within the code.  Otherwise, we'll just be using fixed labels

        units = self.listSections()[0]
        unitMenu = DropdownMenu(self, "Unit Name \n (Developing)", units, 2)
        unitChart = unitMenu.selected

        classSection = self.listSections()[1]
        sectionMenu = DropdownMenu(self, "Section Number \n Developing", classSection[0], 3)
        classSection = sectionMenu.selected
    
        studentNames = self.listSections()[2][0].get(classSection)
        studentMenu = DropdownMenu(self, "Student Name", studentNames, 1)
        studentChart = studentMenu.selected
        '''

        tempUnitLabel =  tk.Label(self, text = "Unit",font = ('arial', 13, 'bold'), bg = "red", fg = "white", width = 15, padx = 20, pady = 5).grid(row = 1, column = 2)
        unit = tk.Label(self, text = chartConfig[0],font = ('arial', 13, 'bold'), bg = "red", fg = "white", width = 15, padx = 20, pady = 5)
        unit.grid(row = 2, column = 2)

        tempSectionLabel =  tk.Label(self, text = "Section",font = ('arial', 13, 'bold'), bg = "red", fg = "white", width = 15, padx = 20, pady = 5).grid(row = 1, column = 3)
        section = tk.Label(self, text = chartConfig[1], font = ('arial', 13, 'bold'), bg = "red", fg = "white", width = 15, padx = 20, pady = 5)
        section.grid(row = 2, column = 3)

        self.studentList = chartConfig[2]
        self.studentMenu = DropdownMenu(self, "Student Name", self.studentList, 1)
        self.studentMenu.tkvar.trace('w', self.switchStudentChart)

        # Buttons
        previousStudentButton = tk.Button( self, 
                                            text = "Previous Student",
                                            width = 15)
        previousStudentButton.bind("<Button-1>", self.previousStudent)
        previousStudentButton.grid(row = 2, 
                                    column = 4, 
                                    padx = 20, 
                                    pady = 5)

        nextStudentButton = tk.Button(self, 
                                        text = "Next Student", 
                                        width = 15)
        nextStudentButton.bind("<Button-1>", self.nextStudent)
        nextStudentButton.grid(row = 2, 
                                column = 5, 
                                padx = 20, 
                                pady = 5)

        visualizeButton = tk.Button(self, 
                                    text = "Visualize Data \n (Developing)", 
                                    width = 15
                                    ).grid(row = 2, 
                                            column = 6, 
                                            padx = 20, 
                                            pady = 5)   
        # Force the raise to see if this fixes the page change bug                                    
        #self.controller.show_frame(self.studentList[0] + "PageOne")

    def nextStudent(self, event):
        try:           
            nextStudent = self.studentList[self.studentList.index(self.studentMenu.selected) + 1]
            self.controller.show_frame(nextStudent + "PageOne")
            
        except IndexError:
            nextStudent = self.studentList[0]
            self.controller.show_frame(nextStudent + "PageOne")

        self.studentMenu.tkvar.set(nextStudent)
    
    def previousStudent(self, event):
        try:           
            previousStudent = self.studentList[self.studentList.index(self.studentMenu.selected) - 1] 
            self.controller.show_frame(previousStudent + "PageOne")
            self.studentMenu.tkvar.set(previousStudent)

        except IndexError:
            # Just in case
            self.controller.show_frame(self.studentList[0] + "PageOne")
            self.studentMenu.tkvar.set(self.studentList[0])

    def visualizeData(self, event):
        pass

    def switchStudentChart(self, *args):
        self.controller.current_student = self.studentMenu.tkvar.get()
        self.controller.current_page = "PageOne"
        self.controller.show_frame(self.controller.current_student + self.controller.current_page)
        


   
################################################################################
#                                   Bottom Frame                               #
################################################################################  
class BottomFrame(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.parent = parent
        self.switchButton = tk.Button(self, 
                                text = "Next Page", 
                                width = 15)
        self.switchButton.bind("<Button-1>", self.switchPage)
        self.switchButton.pack(side = "right")
        
        '''
        saveButton = tk.Button(self, 
                                text = "Save", 
                                width = 15)
        #saveButton.bind("<Button-1>", self.savePage)
        saveButton.pack(side = "right")
        '''

        exitButton = tk.Button(self, 
                             text = "Exit \n (Bugged and Slow)", 
                             width = 15)
        exitButton.bind("<Button-1>", self.closeWindow)
        exitButton.pack(side = "left")
        
    def switchPage(self, event):
        if  self.controller.current_page == "PageOne":
            self.controller.current_page = "PageTwo"
            self.controller.show_frame(self.controller.current_student + self.controller.current_page)
            self.switchButton.config(text = "Previous Page")

        elif self.controller.current_page == "PageTwo":
             self.controller.current_page = "PageOne"
             self.controller.show_frame(self.controller.current_student + self.controller.current_page)
             self.switchButton.config(text = "Next Page")

    def closeWindow(self, event):
        self.parent.destroy()
        newMenu = MainMenu()

'''
def getter(widget):
    from PIL import ImageGrab
    x = root.winfo_rootx() + widgetwinfo_x()
    y = root.winfo_rooty() + widgetwinfo_y()
    x1 = x + widget.winfo_width()
    y1 = y + widget.winfo_height()
    ImageGrab.grab().crop((x,y,x1,y1).save("file.txt"))
'''


if __name__ == "__main__":
    classPath = os.getcwd() + "\\Units\\Assessment Chart\\SPH3U1-02"
    chartConfig = ['Assessment Chart', 'SPH3U1-02', os.listdir(classPath)]
    app = AssessmentPage(classPath, chartConfig)
    
    app.mainloop()