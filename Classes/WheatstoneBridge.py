################################################################################
# 2 Wire RTD Calculations
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
# Constant Current 2 Wire RTD
############################################
class TwoWire:
    #Class instantiation
    def __init__(self, r, ics, RTD):
        self.r = r      #Defines r where R3=R4=rRt where Rt = RTD resistance when T=0degC
        self.ics = ics  #Constant Current Source (amps)
        self.RTD = RTD  #RTD
        self.R2 = r*self.RTD.R0        #Constant R2 (ohms)
        self.R3 = r*self.RTD.R0         #Constant R3 (ohms)
        self.R4 = self.RTD.R0           #Constant R4 (ohms)
        self.calculate()
        
    #Default get function - Standard Function to get access to class members 
    def __get__(self, obj, objtype):
        return self.val
    
    def set_Ics(self, value):
        self.ics = value
        self.calculate()
            
    def set_r(self, value):
        self.r = value
        self.R2 = value*self.RTD.R0    #Constant R2 (ohms)
        self.R3 = value*self.RTD.R0    #Constant R3 (ohms)
        self.calculate()

    def Vout(self):
        self.calculate
        return self.V
        
    #Set the Sensed Temperature (true temperature) in degC
    def calculate(self): 
        #Linear Gain Approximation
        self.A = self.ics*(self.r/(2*(1+self.r)))
        
        #Set R1 from self.RTD
        self.R1_eff = self.RTD.Rs + self.RTD.Rw
        self.R2_eff = self.R2 + self.RTD.Rw
        self.R3_eff = self.R3
        self.R4_eff = self.R4
    
        #Calculate Currents
        self.i1 = self.ics*(self.R3_eff+self.R4_eff)/(self.R1_eff+self.R2_eff+self.R3_eff+self.R4_eff)
        self.i2 = self.ics*(self.R1_eff+self.R2_eff)/(self.R1_eff+self.R2_eff+self.R3_eff+self.R4_eff)
        
        #Calculate vout
        self.V = self.i1*self.R1_eff - self.i2*self.R4_eff
        self.Rcalc = (self.V*(self.R2+self.R3+self.R4)+self.ics*self.R2*self.R4)/(self.R3*(self.ics)-self.V)
        
        #Calculate the total voltage across the bridge        
        self.Vt = self.i1*(self.R1_eff + self.R2_eff)
        
        #self.Req = (self.R1+self.R2)**2/(self.R1+self.R2+self.R3+self.R4)
        #self.Pt = self.ics**2*(self.Req)
        #self.Vout = self.ics*((self.R1*self.R3 - self.R2*self.R4)/(self.R1+self.R2+self.R3+self.R4))
        #self.Rcalc = (self.Vout*(self.R2+self.R3+self.R4)+self.ics*self.R2*self.R4)/(self.R3*(self.ics)-self.Vout)
        
############################################
# Constant Current 3 Wire RTD
############################################
class ThreeWire:
    #Class instantiation
    def __init__(self, r, ics, RTD):
        self.r = r      #Defines r where R3=R4=rRt where Rt = RTD resistance when T=0degC
        self.ics = ics  #Constant Current Source (amps)
        self.RTD = RTD  #RTD
        self.R2 = r*self.RTD.R0        #Constant R2 (ohms)
        self.R3 = r*self.RTD.R0         #Constant R3 (ohms)
        self.R4 = self.RTD.R0           #Constant R4 (ohms)
        self.calculate()
        
    #Default get function - Standard Function to get access to class members 
    def __get__(self, obj, objtype):
        return self.val
        
    def set_Ics(self, value):
        self.ics = value
        self.calculate()
            
    def set_r(self, value):
        self.r = value
        self.R2 = value*self.RTD.R0    #Constant R2 (ohms)
        self.R3 = value*self.RTD.R0    #Constant R3 (ohms)
        self.calculate()
     
    def Vout(self):
        self.calculate
        return self.__Vout
        
    #Set the Sensed Temperature (true temperature) in degC
    def calculate(self): 
        #Linear Gain Approximation
        self.A = self.ics*(self.r/(2*(1+self.r)))
        
        #Set R1 from self.RTD
        self.R1_eff = self.RTD.Rs + self.RTD.Rw
        self.R2_eff = self.R2 + self.RTD.Rw
        self.R3_eff = self.R3
        self.R4_eff = self.R4
    
        #Calculate Currents
        self.i1 = self.ics*(self.R3_eff+self.R4_eff)/(self.R1_eff+self.R2_eff+self.R3_eff+self.R4_eff)
        self.i2 = self.ics*(self.R1_eff+self.R2_eff)/(self.R1_eff+self.R2_eff+self.R3_eff+self.R4_eff)
        
        #Calculate vout
        self.V = self.i1*self.R1_eff - self.i2*self.R4_eff
        #self.Req = (self.R1+self.R2)**2/(self.R1+self.R2+self.R3+self.R4)
        #self.Pt = self.ics**2*(self.Req)
        #self.Vout = self.ics*((self.R1*self.R3 - self.R2*self.R4)/(self.R1+self.R2+self.R3+self.R4))
        #self.Rcalc = (self.Vout*(self.R2+self.R3+self.R4)+self.ics*self.R2*self.R4)/(self.R3*(self.ics)-self.Vout)
        

        
############################################
# Constant Voltage 2 Wire RTD
############################################
class CVTwoWire:
    #Class instantiation
    def __init__(self, r, Vs, RTD):
        self.r = r      #Defines r where R3=R4=rRt where Rt = RTD resistance when T=0degC
        self.Vs = Vs  #Constant Current Source (amps)
        self.RTD = RTD  #RTD
        self.R2 = r*self.RTD.R0        #Constant R2 (ohms)
        self.R3 = r*self.RTD.R0         #Constant R3 (ohms)
        self.R4 = self.RTD.R0           #Constant R4 (ohms)
        self.calculate()
        
    #Default get function - Standard Function to get access to class members 
    def __get__(self, obj, objtype):
        return self.val
    
    def set_Vs(self, value):
        self.Vs = value
        self.calculate()
            
    def set_r(self, value):
        self.r = value
        self.R2 = value*self.RTD.R0    #Constant R2 (ohms)
        self.R3 = value*self.RTD.R0    #Constant R3 (ohms)
        self.calculate()

            
    def set_R1(self, value):
        self.R1 = value
        self.calculate()    
                
    def set_R2(self, value):
        self.R2 = value
        self.calculate() 
                   
    def set_R3(self, value):
        self.R3 = value
        self.calculate()
        
    def set_R4(self, value):
        self.R4 = value
        self.calculate()
        
    def Vout(self):
        self.calculate
        return self.V
        
    #Set the Sensed Temperature (true temperature) in degC
    def calculate(self): 
        
        #Set R1 from self.RTD
        self.R1_eff = self.RTD.Rs
        self.R2_eff = self.R2
        self.R3_eff = self.R3
        self.R4_eff = self.R4
    
        #Calculate Voltages
        self.Vab = self.Vs*self.R1_eff/(self.R1_eff+self.R2_eff)
        self.Vad = self.Vs*self.R4_eff/(self.R3_eff+self.R4_eff)
        
        #Calculate Currents
        self.i1 = self.Vs/(self.R1_eff+self.R2_eff)
        self.i2 = self.Vs/(self.R3_eff+self.R4_eff)
        
        #Calculate vout
        self.V = self.Vab - self.Vad
        
        
        

