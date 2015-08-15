
class LUT1D:
    
    #Class instantiation
    def __init__(self,Xvals,Zvals):
        #Class instantiation 
        self.X = Xvals
        self.Z = Zvals
    
    def lookup(self,X):
        for xi in range(0,len(self.X)-1):
            
            #At Left Edge of Table
            if (xi == 0) and (self.X[xi] >= X):
                return self.Z[xi]

            #At Right Edge of Table
            elif (xi == (len(self.X)-1)) and (self.X[xi] <= X):
                return self.Z[xi]
            
            #In middle of Table
            elif (self.X[xi] <= X) and (self.X[xi+1] >= X):
                retVal = (X-self.X[xi]) * (self.Z[xi+1]-self.Z[xi])/(self.X[xi+1]-self.X[xi]) + self.Z[xi]
                return retVal
        