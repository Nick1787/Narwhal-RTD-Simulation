import sys
import csv
import numpy as np

class DataCollector:
    #Class instantiation
    def __init__(self):
        #Class instantiation 
        self.params = []
        self.Data = dict()
    
    #Default get function - Standard Function to get access to class members 
    def __get__(self, obj, objtype):
        return self.val
    
    #Get data from the collector, returns as an array
    def get(self,name):
        if (name not in self.params):
            print("Error! '" + name + "' doesnt exists in the data collector")
        else:
            return np.asarray(self.Data[name])
        
    #Get List of Parameters
    def params(self):
        return self.params
                   
    #add a single parameter
    def addParam(self, name):
            if (name not in self.params):
                self.params.append(name)
                self.Data[name]=[]
            else:
                print("Error '" + name + "' already exists in the data collector")
                
        
    #add a Parameter or list of parameters and stores the under different anmes
    def addParams(self, names):
        for name in names:
            if (name not in self.params):
                self.params.append(name)
                self.Data[name]=[]
            else:
                print("Error '" + names[name]+ "' already exists in the data collector")      
    
    #Write Dictionary to CSV file
    def writeToFile(self,filename):
        with open(filename, 'wb') as f:  # Just use 'w' mode in 3.x
            w = csv.DictWriter(f, self.Data.keys())
            w.writeheader()
            w.writerow(self.Data) 
        
    ###########################################
    # Data Recording Functions
    
    def slurp(self,):
        #The actual Data collection routine"
        for key in self.params:
            if key.find('.')>-1:
                part = key.split('.')
                suffix = ".".join(part[1:len(key)])
                cmd = "sys.modules['__main__'].__dict__['"+part[0]+"']." + suffix
                value = eval(cmd)
            else:
                value = sys.modules['__main__'].__dict__[key]
            self.Data[key].append(value)
            
            
            