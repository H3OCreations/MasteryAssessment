import os, csv, collections

class MasteryTools:
    # take in the file name to create the object with visualization and file reading 
    # and writing capabilies

    def __init__(self, originalFile):
        # need to write a part that parces through a csv
        self.fileName = originalFile
        
        # The data is stored in the form of a dictionary with the strand as the
        # key and a 2D list containing each strand's results
        self.assessmentData = collections.OrderedDict()
        self.assessmentData["Knowledge"] = []
        self.assessmentData["Thinking"] = []
        self.assessmentData["Communication"] = []
        self.assessmentData["Application"] = []

        KICA = ["Knowledge", "Thinking", "Communication", "Application"]        
        self.delim = "~"
        self.mark_location = {"Knowledge":-1, "Thinking":-1, "Communication": -1, "Application":-1}



        with open(self.fileName, 'r') as file:
            fileReader = csv.reader(file)
            self.fileData = list(fileReader)
            # Cleaning out all blank lines
            self.fileData = [value for value in self.fileData if value != []]

            for line in self.fileData:
                # Formatting data into dictionary based on strands
                try:
                    # Searches for the location of different sections
                    bracketLocation = line[0].index("[")
                    
                    # checks to see if we're working with strand.  
                    # rejects if not part of KICA
                    if line[0][:bracketLocation - 1] in KICA:
                        strand = line[0][:bracketLocation - 1]
                        # removes duplicates from the search and identifies what strand
                        # we are working on
                        self.mark_location[strand] = self.fileData.index(line)
                        KICA.remove(strand)
                        
                except ValueError:
                    if self.delim in line[0]:
                        for column in line[2:5]:
                            line.append(collections.Counter(column))
                        self.assessmentData[strand].append(line)
                        '''
                        if "[" in line[0]:
                            print("continue", line[0])
                            continue
                        # This elif is left in until we fix the self.delim formatting issue
                        elif self.delim == line[0][0]:
                            #line[0] = line[0][len(self.delim):]
                            for column in line[2:5]:
                                line.append(collections.Counter(column))
                            self.assessmentData[strand].append(line)   
                       '''
                
                except IndexError:
                    pass     
      
        # subtract 3 to remove the 3 dictionaries at the end of the data frame
        self.vertexNum = max([len(self.assessmentData[i]) for i in self.assessmentData])
        file.close()
    
    
    ################################################################################
    #                                Calculations                                  #
    ################################################################################ 
            
    def calculate(self, strand):
        """Calculate the score of line within assessment chart.

    This function calculates the corresponding score of a row in the assessment chart.It begins at 
    the Not Attempted Column and moves towards the Mastery column.  This is the logest method of 
    calculating the mark, but it gurentees that you must complete developing and understanding to 
    achieve mastery    

    Parameters
    ----------
    strand: list(string, string, string, string, string, dict, dict, dict)
        Formatted row of the assessment chart

    return: calculated mark rounded to 2 decimal places

    TODO   
        Fix the multi-input mastery column.  It currently calculates by only looking at the presence of
        two checks rather than most recent and most consistent.

    """
        result = []

        for row in self.assessmentData[strand]:
            score = 0
            baseNum = 5
            # Consider only the last three entries of the row since we've appended our counting dictionaries
            # to the end of the object's assessment data
            for columnNum in range(-3, 0):
                # If the column only has one entry so far
                column = row[columnNum]
                
                # Developing and Understanding
                if columnNum != -1: 
                    if "2" in column:
                        if column["2"] > 1 or (column["2"] == 1 and len(column) == 1):
                            score = baseNum + columnNum
                        elif "1" in column:
                            if column["1"] > 1:
                                score = baseNum - 0.5 + columnNum
                    elif "1" in column:
                        if column["1"] > 1 or (column["1"] == 1 and len(column) == 1):
                            score = baseNum -1 + columnNum
                        else:
                            score = baseNum - 1.5 + columnNum
                
                # Mastery Column
                else:
                    # This creates a threshold so that if they haven't achieved the previous strands
                    # They cannot achieve mastery
                    if score < 3:
                        pass

                    elif "2" in column:
                        masteryData = strand[-5]
                        if len(masteryData) == 1:
                            score = 4
                            
                        elif column["2"] > 1:
                            if masteryData[-2:] == "22":
                                score = 4

                        # at this point, we'll create a temporary scale and fix this later
                            elif "1" in column:
                                if column["1"] > 1:
                                    score = 3.75
                                else:
                                    score = 3.5      
            result.append(score)  

        try:
            return round(sum(result)/len(result), 2)
        except ZeroDivisionError:
            return 0


    def save_results(self):
        for strand in self.mark_location:
            strandLocation = self.mark_location[strand]
            line = self.fileData[strandLocation]
            edit_cell = self.fileData[strandLocation][0].split("[")

            # Double checks the value in front of the / is a space to make sure split works
            # the way we want it to
            space_location = edit_cell[1].index("/") - 1 

            if edit_cell[1][space_location] != " ":
                edit_cell[1] = edit_cell[1][:space_location + 1] + " " + edit_cell[1][space_location + 1:]

            # Remove any previously calculated values by setting the second value to the last 
            # value of the split.  
            # A space is inserted for futture .split() actions
            
            edit_cell[1] = " " + edit_cell[1].split()[-1]
            result = self.calculate(strand)

            # Temporary fix for the thinking section
            if strand == "Thinking":
                result = 2*result

            edit_cell.insert(1, result)
            edit_cell.insert(1, "[")
            edit_cell = ''.join([str(elem) for elem in edit_cell])
            self.fileData[strandLocation][0] = edit_cell
        
        # Need to clean the data from the calculations out by deleting the last 4 columns of
        # the data since we appended all that to the original fileData

        for line in self.fileData:
            if len(line) > 0:
                if self.delim in line[0]:
                    for i in range(-3, 0):
                        del line[i]

        # Writes file to .csv 
        with open(self.fileName, 'w') as file:
            writer = csv.writer(file)
            writer.writerows(self.fileData) 
        

        '''
        # Search for assessment result rows
        for line in self.fileData:
            if len(line) > 0:
                if "[" in line[0] and "]" in line[0]:                   
                    cell = line[0].split("[")
                    if cell[0] in KICA:
                        print(True)
                    else:
                        print(False)
                    #self.calculate(cell[0])
        '''

    ################################################################################
    #                              Radar Plotting                                  #
    ################################################################################     

    def formatPlotData(self):
        '''
        Reformats the data into a dataframe for the data visualization

        I need to format the data to fit the spider plot function.  
        Arguably, columns B-D are not useful and won't be used in the plotting unless
        I transpose the groups into the same frame.  Perhaps the null value should be -1
        and I can add a component that skips over values less than zero!

        dataframe = pandas.DataFrame({
                    'group': ['A','B','C','D'],
                    'var1': [38, 1.5, 30, 4],
                    'var2': [29, 10, 9, 34],
                    'var3': [8, 39, 23, 24],
                    'var4': [7, 31, 33, 14],
                    'var5': [28, 15, 32, 14]
                    })
        '''
        data = []

        # Formats the first line of the dataframe used for the plot
        firstRow = ["Category"]
        for strandNum in range(1, self.vertexNum + 1):
            firstRow.append("Strand " + str(strandNum))
        data.append(firstRow)

        for strand in self.assessmentData:
            rowData = [self.calculate(row) for row in self.assessmentData[strand]]
            while len(rowData) < self.vertexNum:
                rowData.append(0)
            data.append((strand, [rowData]))
        data = pandas.DataFrame(data)
       
        return data



if __name__ == '__main__':
    classPath = os.getcwd() + "\\Units\\Assessment Chart\\SPH3U1-02"
    studentList = os.listdir(classPath)
    example = MasteryTools(classPath + "\\" + studentList[0])
    #print(example.calculate("Knowledge"))
    example.save_results()

    #print("New Run")
    #print(example.formatPlotData())
    #from spider_plots import *
    #spider_plot(example.formatPlotData())
    #for i in example.assessmentData:
    #    print(example.assessmentData[i])
    '''
    
    # To see the plot data
    data = example.plotData()
    for line in data:
        print(line)
    '''
    
    '''
    # To see what the data looks like
    for KICA in example.assessmentData:
        for lines in example.assessmentData[KICA]:
            print(lines)
    '''
    
   
