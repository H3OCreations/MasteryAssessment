import numpy as np
import matplotlib.pyplot as plt

class DataVisualization:
    def __init__(self, data):
        self.points = []
        self.vertexNum = len(data)
        
        # temporarily setting the frame to be 200 pixels x 200 pixels
        self.frame = (200, 200)
        self.midpoint = (self.frame[0]/2, self.frame[1]/2)
        '''
        Here we populate the points of the spider graph relative to the midpoint
        Each point is equally spaced by 2pi divided by the number of points in the data
        then they are adjusted using spherical coordinates
        '''
        for n in range(1, self.vertexNum + 1):
            x = self.midpoint[0] + data[n-1]*n*math.sin(math.pi/self.vertexNum)
            y = self.midpoint[1] + data[n-1]*n*math.cos(math.pi/self.vertexNum)
            self.points.append((x, y))

    def totalArea(self):
        area = 0
        # First we need to find the vectors constructed by the vertex and the midpoint
        # We let u be the last vector
        u = (self.points[-1] - self.midpoint[0], self.points[-1] - self.midpoint[-1])

        for vertex in self.points:
            v = (vertex[0] - self.midpoint[0], vertex[1] - self.midpoint[1])
            
            '''
             Area calculation is done using the magnitude of the cross product (2x2 determinant)
             Since the cross product give the area of a parallelogram, all you need to do is
             divide it by 2 to get the triangle within it
            '''
            areaSegment = abs(u[1]*v[0] - u[0]*v[1])/2
            area = area + areaSegment
            
            # Set u to become v so that on the next for loop itteration, we switch the vectors
            u = v

        return area
               

    def optimizeGraph(self):
        '''
        Rather than running the exact number of permutations of the list and writing an algorithm to do
        so, randomizing the list an arbitrary number of generations should produce enough variation for
        the moment.  

        TODO
        Write a method for it to intellegently make swaps
        '''
        optimalPoints = self.points
        optimalArea = self.totalArea()
        sensitivity = 0.5 # for how many of the total permutations we will consider

        for i in range(int(sensitivity * math.factorial(self.vertexNum))):
            random.shuffle(self.points)
            newArea = self.totalArea()

            # Exchange values if a more optimal area is found
            if optimalArea < newArea:
                optimalPoints = self.points
                optimalArea = newArea
        
        # Set the order of the points to be in the optimal position for the calculation
        self.points = optimalPoints

    def drawGraph(self):
        pass

if __name__ == '__main__':
    pass