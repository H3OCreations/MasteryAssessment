import os, csv, math, random, collections, fileinput

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.path import Path
from matplotlib.spines import Spine
from matplotlib.projections.polar import PolarAxes
from matplotlib.projections import register_projection


class Mastery:
    # take in the file name to create the object?
    def __init__(self, originalFile):
        # need to write a part that parces through a csv
        self.fileName = originalFile
        
        # The data is stored in the form of a dictionary with the strand as the
        # key and a 2D list containing each strand's results
        self.assessmentData = collections.OrderedDict()
        #assessmentData =  {"Knowledge":[], "Thinking":[], "Communication":[], "Application":[]}
        self.assessmentData["Knowledge"] = []
        self.assessmentData["Thinking"] = []
        self.assessmentData["Communication"] = []
        self.assessmentData["Application"] = []

        KICA = ["Knowledge", "Thinking", "Communication", "Application"]        

        with open(self.fileName, 'r') as file:
            fileReader = csv.reader(file)
            self.fileData = list(fileReader)
             
            for line in self.fileData:
                # Formatting data into dictionary based on strands
                try:
                    bracketLocation = line[0].index("[")
                    
                    # checks to see if we're working with strand.  
                    # rejects if not part of KICA
                    if line[0][:bracketLocation - 1] in KICA:
                        strand = line[0][:bracketLocation - 1]
                        # removes duplicates from the search and identifies what strand
                        # we are working on
                        KICA.remove(strand)
                        
                except ValueError:
                    indent = "-\xa0\xa0\xa0\xa0\xa0\xa0 "
                    if indent in line[0]:
                        line[0] = line[0][len(indent):]
                        for column in line[2:5]:
                            line.append(collections.Counter(column))
                        self.assessmentData[strand].append(line)            

        # subtract 3 to remove the 3 dictionaries at the end of the data frame
        self.vertexNum = max([len(self.assessmentData[i]) for i in self.assessmentData])
        file.close()
            
    def markInput(self, strand):
        masteryResult = input("What is the mastery result? ")
        
        if masteryResult == "2":
            understandingResult = masteryResult
            developingResult = understandingResult
            
        elif masteryResult != "1" or masteryResult != "0":
            understandingResult = input("What is the understanding result?: ")
            if understandingResult == "2":
                developingResult = understandingResult
            elif understandingResult != "2":
                developingResult = input("What is the developping result?: ")
            else:
                self.markInput(strand)

        else:
            self.markInput(strand)
        
        # Assessment Data is written here
        self.assessmentData[strand][0] = self.assessmentData[strand][0] + developingResult 
        self.assessmentData[strand][1] = self.assessmentData[strand][1] + understandingResult 
        self.assessmentData[strand][2] = self.assessmentData[strand][2] + masteryResult 

    def calculate(self, strand):
        """Calculate the score of line within assessment chart.

    This function calculates the corresponding score of a row in the assessment chart.It begins at 
    the Not Attempted Column and moves towards the Mastery column.  This is the logest method of 
    calculating the mark, but it gurentees that you must complete developing and understanding to 
    achieve mastery    

    Parameters
    ----------
    strand : list(string, string, string, string, string, dict, dict, dict)
        Formatted row of the assessment chart

    TODO
        Figure out how to reduce the number of comparisions in order to reduce the calculation time.
        
        Fix the multi-input mastery column.  It currently calculates by only looking at the presence of
        two checks rather than most recent and most consistent.

    """
        score = 0
        baseNum = 5
        # Consider only the last three entries of the row since we've appended our counting dictionaries
        # to the end of the object's assessment data
        for columnNum  in range(-3, 0):
            # If the column only has one entry so far
            column = strand[columnNum]
            
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
                    return score

                masteryData = strand[-5]

                if "2" in column:
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
        return score

    def plotData(self):
        '''
        Reformats the data into a dataframe for the data export
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
        

        return data

    
    def export(self):
        '''
        This function is meant to search through line by line and replace the appropriate 
        rows corresponding to the dictionary
        '''
       # with open(self.fileName, 'w') as file:
        for line in fileinput.FileInput(self.fileName, inplace=1):
            print(line)
                #if "-\xa0\xa0\xa0\xa0\xa0\xa0" in line:
                #    line=line.replace("old","new")

#########################################################################################################
#                                                                                                       #
#                                       DATA VISUALIZATION                                              #
#                                                                                                       #
#########################################################################################################
'''
The following is a package taken online
https://python-graph-gallery.com/390-basic-radar-chart/
'''
def radar_factory(num_vars, frame='circle'):
    """Create a radar chart with `num_vars` axes.

    This function creates a RadarAxes projection and registers it.

    Parameters
    ----------
    num_vars : int
        Number of variables for radar chart.
    frame : {'circle' | 'polygon'}
        Shape of frame surrounding axes.

    """
    # calculate evenly-spaced axis angles
    theta = np.linspace(0, 2*np.pi, num_vars, endpoint=False)
    # rotate theta such that the first axis is at the top
    theta += np.pi/2

    def draw_poly_patch(self):
        verts = unit_poly_verts(theta)
        return plt.Polygon(verts, closed=True, edgecolor='k')

    def draw_circle_patch(self):
        # unit circle centered on (0.5, 0.5)
        return plt.Circle((0.5, 0.5), 0.5)

    patch_dict = {'polygon': draw_poly_patch, 'circle': draw_circle_patch}
    if frame not in patch_dict:
        raise ValueError('unknown value for `frame`: %s' % frame)

    class RadarAxes(PolarAxes):

        name = 'radar'
        # use 1 line segment to connect specified points
        RESOLUTION = 1
        # define draw_frame method
        draw_patch = patch_dict[frame]

        def fill(self, *args, **kwargs):
            """Override fill so that line is closed by default"""
            closed = kwargs.pop('closed', True)
            return super(RadarAxes, self).fill(closed=closed, *args, **kwargs)

        def plot(self, *args, **kwargs):
            """Override plot so that line is closed by default"""
            lines = super(RadarAxes, self).plot(*args, **kwargs)
            for line in lines:
                self._close_line(line)

        def _close_line(self, line):
            x, y = line.get_data()
            # FIXME: markers at x[0], y[0] get doubled-up
            if x[0] != x[-1]:
                x = np.concatenate((x, [x[0]]))
                y = np.concatenate((y, [y[0]]))
                line.set_data(x, y)

        def set_varlabels(self, labels):
            self.set_thetagrids(np.degrees(theta), labels)

        def _gen_axes_patch(self):
            return self.draw_patch()

        def _gen_axes_spines(self):
            if frame == 'circle':
                return PolarAxes._gen_axes_spines(self)
            # The following is a hack to get the spines (i.e. the axes frame)
            # to draw correctly for a polygon frame.

            # spine_type must be 'left', 'right', 'top', 'bottom', or `circle`.
            spine_type = 'circle'
            verts = unit_poly_verts(theta)
            # close off polygon by repeating first vertex
            verts.append(verts[0])
            path = Path(verts)

            spine = Spine(self, spine_type, path)
            spine.set_transform(self.transAxes)
            return {'polar': spine}

    register_projection(RadarAxes)
    return theta


def unit_poly_verts(theta):
    """Return vertices of polygon for subplot axes.

    This polygon is circumscribed by a unit circle centered at (0.5, 0.5)
    """
    x0, y0, r = [0.5] * 3
    verts = [(r*np.cos(t) + x0, r*np.sin(t) + y0) for t in theta]
    return verts


def example_data():
    data = [
        ["Category", "Strand 1", "Strand 2", "Strand 3", "Strand 4", "Strand 5"],
        ("Knowledge", [
            [0, 1, 2, 3, 4]]),
        ('Thinking', [
            [3, 2, 2.5, 3.5, 3.25]]),
        ('Communication', [
            [2, 2, 3, 4, 4]]),
        ('Application', [
            [3.5, 0, 0, 0, 0]])
    ]
    
    return data
#########################################################################################################
#                                                                                                       #
#                                              MAIN METHOD                                              #
#                                                                                                       #
#########################################################################################################
   

if __name__ == '__main__':
    #example = Mastery("Assessment_Chart_filled_in.csv")
    example = Mastery("Assessment_Chart_filled_in_single_value.csv")
    # To see the plot data
    data = example.plotData()
    for line in data:
        print(line)
    
    
    '''
    # To see what the data looks like
    for KICA in example.assessmentData:
        for lines in example.assessmentData[KICA]:
            print(lines)
    '''
    
    # Example on how the program will plot the data
    N = example.vertexNum
    theta = radar_factory(N, frame='polygon')

    data = example.plotData()
    vertex_labels = data[0][1:]
    spoke_labels = data.pop(0)

    fig, axes = plt.subplots(figsize=(9, 9), nrows=2, ncols=2,
                             subplot_kw=dict(projection='radar'))
    # Draw one axe per variable + add labels labels yet
    #plt.xticks(theta, vertex_labels, color='grey', size=15)
    
    
    fig.subplots_adjust(wspace=0.25, hspace=0.20, top=0.85, bottom=0.05)

    colors = ['b', 'r', 'g', 'm', 'y']
    
    # Plot the four cases from the example data on separate axes
    for ax, (title, case_data) in zip(axes.flatten(), data):
        ax.set_rgrids([2, 3, 4])
        ax.set_title(title, weight='bold', size='medium', position=(0.5, 1.1),
                     horizontalalignment='center', verticalalignment='center')
        
        for d, color in zip(case_data, colors):
            ax.plot(theta, d, color=color)
            
            ax.fill(theta, d, facecolor=color, alpha=0.25)
        
        #ax.set_varlabels(spoke_labels)

    # add legend relative to top-left plot
    ax = axes[0, 0]
    #labels = ('Factor 1', 'Factor 2', 'Factor 3', 'Factor 4', 'Factor 5')
    #legend = ax.legend(labels, loc=(0.9, .95),
    #                   labelspacing=0.1, fontsize='small')

    fig.text(0.5, 0.965, 'Sample Unit Divided by Strands',
             horizontalalignment='center', color='black', weight='bold',
             size='large')

    plt.show()
 