################################################################################
# RTD Simulation
################################################################################
# Author:      N. Dodds
# Written on:  Python xy (python 2.7)
# References:  
#   [1] J.DALLY. "Instrumentation for Engineering Measurements" 2nd Edition
#   [2] Wikipedia: "Electrical resistivity and conductivity"
#       http://en.wikipedia.org/wiki/Electrical_resistivity_and_conductivity
#   [3] Hyperphysics Resistivity and Conductivity
#       http://hyperphysics.phy-astr.gsu.edu/hbase/electric/resis.html
#   [4] American wire gauge
#       http://en.wikipedia.org/wiki/American_wire_gauge
################################################################################

import Wire
import LUT1D

############################################
# Defines the Class for a 2 or 3 Wire RTD
############################################
class RTD:
    #Class instantiation
    def __init__(self, R0, alpha, beta, delta, Wr):
        #Class instantiation of Wire
        self.Wire = Wr
        
        Xvals = [80.31, 84.27, 88.22, 92.16, 96.09, 100, 103.9, 107.79, 111.67, 115.54, 119.4, 123.24, 127.08, 130.9, 134.71, 138.51, 142.29, 146.07, 149.83, 153.58, 157.33, 161.05, 164.77, 168.48, 172.17, 175.86, 179.53, 183.19, 186.84, 190.47, 194.1, 197.71, 201.31, 204.9, 208.48, 212.05]
        Zvals = [-50, -40, -30, -20, -10, 0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 210, 220, 230, 240, 250, 260, 270, 280, 290, 300]
    
        self.LUT = LUT1D.LUT1D(Xvals,Zvals)    
        self.RevLUT = LUT1D.LUT1D(Zvals,Xvals)
        
        #Basic Properties of RTD from DataSheet
        self.R0 = R0          #Ohm (temp at 0decC)
        self.alpha = alpha    #1/decC 
        self.beta = beta      #decC
        self.delta = delta    #decC
        
        #Calculate the RTD Constants for Describing function.
        self.A = self.alpha + self.alpha*self.delta/100
        self.B = -1*self.alpha * self.delta/100**2
        self.C = -1*self.alpha * self.beta/100**4
        
        #Initialize the Ts to 0
        self.set_Ts(0)
        self.calculate()
        
    #Default get function - Standard Function to get access to class members 
    def __get__(self, obj, objtype):
        return self.val
        
    #Set the sensed temperature (true temperature) in degC
    def set_Ts(self, tsens):
        self.Ts = tsens
        self.calculate()
        
    #Set the sensed temperature (true temperature) in degC
    def tLookup(self, R):
        return self.LUT.lookup(R)
        
    def calculate(self):
        #Calculate the Sensor Resistance (based on approximation)
        self.Rs = self.R0*(1 + self.A*self.Ts + self.B*self.Ts**2 - 100 * self.C*self.Ts**3 + self.C*self.Ts**4)
        #Calculate the sensor Resistance (based on LUT)
        self.Rs = self.RevLUT.lookup(self.Ts)
        self.Rw = self.Wire.Rw
        
        #Calculate the total Resistancs
        self.R = self.Rs + 2*self.Rw
        
        