################################################################################
# Wire Simulation
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


############################################
# Defines the class for simulating a wire
############################################
class Wire:
    #Class instantiation
    def __init__(self, Length, Gauge):
        #Basic Properties of RTD from DataSheet
        self.L = Length      #Wire Length (ft)
        self.Gauge = Gauge   #Wire Gauge (10,12,14,16)
        self.set_T(0)        #Temp (degC) %Set initial value to 0
        self.calculate()       #Calculate initial values
    
    #Default get function - Standard Function to get access to class members 
    def __get__(self, obj, objtype):
        return self.val

    #Set Wire Length in ft
    def set_L(self,value):
        self.L = value
        self.calculate()
    
    #Set Wire Gauge
    def set_G(self,value):
        self.G = value
        self.calculate()
    
    #Set Temp in degC
    def set_T(self,value):
        self.T = value
        self.calculate()
        
    #Set the sensed temperature (true temperature) in degC
    def calculate(self):
        #Wire Resistance Calculation (from [2])
        rho_Copper = 1.7*10**(-8)                   # ohm-m @ 20 degC
        alpha_Copper = 0.003862                     # C^-1
        
        #Gauge to Crossectional Area Calculation in mm^2 (from [4])
        Gauge_to_A = { 10: 5.26, 12: 3.31, 14: 2.08, 16: 1.31}

        #Calculate the Wire Resistance - Copper Assumed (based on reference [2])
        rho = rho_Copper*(1+alpha_Copper*(self.T - 20))  #Updated resistivity based on temp
        self.Rw = 1000*rho*1000*self.L/Gauge_to_A[self.Gauge]

        