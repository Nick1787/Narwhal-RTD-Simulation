################################################################################
# Differential Op Amp
################################################################################
# Author:      N. Dodds
# Written on:  Python xy (python 2.7)
# References:  
#   [1] http://www.electronics-tutorials.ws/opamp/opamp_5.html
################################################################################


############################################
# Defines the class for simulating a differential Op Amp
############################################
class DiffentialOpAmp:
    
    #Class instantiation
    def __init__(self, R1, R2, R3, R4):
        #Basic Properties of RTD from DataSheet
        self.R1 = R1    # Resistor Connected to Negative OpAmp input to Vin1
        self.R2 = R2    # Resistor Connected to Positive OpAmp input to Vin2
        self.R3 = R3    # Resistor Connected to Feedback loop to Negative OpAmp input.
        self.R4 = R4    # Resistor Connected to Positive OpAmp input to ground.
        self.V1 = 0
        self.V2 = 0
        self.Gn = 0     #Calculated Gain
        self.calculate()       #Calculate initial values
    
    #Default get function - Standard Function to get access to class members 
    def __get__(self, obj, objtype):
        return self.val

    #Set V1 input voltage
    def set_V1(self,value):
        self.v1 = value
        self.calculate()

    #Set V2 input voltage
    def set_V2(self,value):
        self.v2 = value
        self.calculate()
       
    #Set the sensed temperature (true temperature) in degC
    def calculate(self):
        #
        self.Vout = -self.V1*(self.R3/self.R1) + self.V2*(self.R4/(Self.R2+self.R4))*((self.R1 + self.R3)/self.R1)
        
        