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

#Add Path for subclasses
from sys import path
from os import getcwd
path.append(getcwd() + "\\classes") 

#Imports
import matplotlib.pyplot as plt
import DataCollector
import random
from matplotlib.backends.backend_pdf import PdfPages

#Custome Classes
import Wire
import RTD
import WheatstoneBridge

#Insantiate the Data collector
DC = DataCollector.DataCollector()

#Instantiate the Wire and the RTD
Wire = Wire.Wire(100,16)
RTD = RTD.RTD(100 , 0.00385, 0.10863, 1.4999, Wire)

#Instantiate the bridgets
Vs = 5.0
r=20
CVTwoWire = WheatstoneBridge.CVTwoWire( r, Vs, RTD)

#Instantiate the bridgets
Rg = 5000
OpAmpGn = (1+100000/Rg)

############################################
# Simulation - Effects of r on Linearity
############################################ 
Wire.set_L(0.0)
r_values = [1,4,8,20]
temps = range(-50, 300)

DC.addParams(['Vs','tsense','r','RTD.R','Rcalc','Rerr','Tcalc','Terr','CVTwoWire.V','Vg','CVTwoWire.R1_eff','CVTwoWire.R2_eff','CVTwoWire.R3_eff','CVTwoWire.R4_eff','CVTwoWire.i1','CVTwoWire.i2','Rg','OpAmpGn','OpAmpGn_Exp'])

for i in range(len(temps)):
    tsense = temps[i]
    
    #Apply random Variation based on resistor variation
    for s in range(0,10):
        #Apply a 0.1% Variation on resistor Values
        variation = random.randrange(-100,100)/100000
        CVTwoWire.set_R2(r*RTD.R0*(1+variation))
        variation = random.randrange(-100,100)/100000
        CVTwoWire.set_R3(r*RTD.R0*(1+variation))
        variation = random.randrange(-100,100)/100000
        CVTwoWire.set_R4(RTD.R0*(1+variation))
        
        #Update the RTD Temps
        RTD.set_Ts(tsense)
        CVTwoWire.calculate()
        
        #Calculate Op Amp Gain with Variation
        Rg = 5000*1+(random.randrange(-100,100)/100000)
        OpAmpGn = (1+100000/Rg)
        OpAmpGn_Exp = (1+100000/5000)
        Vg = OpAmpGn*CVTwoWire.V
        
    
        #Based on out output voltage back-calculate the RTD resistance (assuming no variation in Resistor Values)
        R2 = r*RTD.R0
        R3 = r*RTD.R0
        R4 = RTD.R0
        
        Rcalc_num = (R2*R4 + ((Vg/OpAmpGn_Exp)/Vs)*(R2*(R3 + R4)))
        Rcalc_den = (R3 - ((Vg/OpAmpGn_Exp)/Vs)*(R3+R4))
        Rcalc = Rcalc_num/Rcalc_den
        Tcalc = RTD.tLookup(Rcalc)
        Terr = Tcalc- tsense
        Rerr = Rcalc - RTD.R
        DC.slurp()

#----------------------------------------------
# Plots 
with PdfPages('RTDSim.pdf') as pdf:
    plt.figure(1)
    plt.plot(DC.Data['tsense'],DC.Data['RTD.R'])
    plt.plot(DC.Data['tsense'],DC.Data['Rcalc'])
    plt.title("RTD Resistance vs. Tsense")
    plt.xlabel("Tsense (degC)")
    plt.ylabel("RTD Resistance (Ohm)")
    plt.grid(True)
    pdf.savefig()
    
    plt.figure(2)
    plt.plot(DC.Data['tsense'],DC.Data['Rerr'])
    plt.title("RTD Calculation Error vs. Tsense")
    plt.xlabel("Tsense (degC)")
    plt.ylabel("RTD Resistance Error (Ohm)")
    plt.grid(True)
    pdf.savefig()
    
    plt.figure(3)
    plt.plot(DC.Data['tsense'],DC.Data['Terr'])
    plt.title("Temp Calculation Error vs. Tsense")
    plt.xlabel("Tsense (degC)")
    plt.ylabel("Tcalc (degC)")
    plt.grid(True)
    pdf.savefig()
    
    plt.figure(4)
    plt.hold(True)
    plt.plot(DC.Data['tsense'],DC.Data['Vs'],'--r')
    plt.plot(DC.Data['tsense'],DC.Data['CVTwoWire.V'])
    plt.plot(DC.Data['tsense'],DC.Data['Vg'])
    plt.ylim([-1,6])
    plt.title("Vout vs. Tsense")
    plt.xlabel("Tsense (degC)")
    plt.ylabel("Vout (volts)")
    plt.grid(True)
    pdf.savefig()
    
    plt.figure(5)
    plt.hold(True)
    plt.plot(DC.Data['tsense'],DC.Data['CVTwoWire.i1'])
    plt.plot(DC.Data['tsense'],DC.Data['CVTwoWire.i2'])
    plt.title("Bridge Currents vs. Tsense")
    plt.xlabel("Tsense (degC)")
    plt.ylabel("Current (amps)")
    plt.grid(True)
    pdf.savefig()
    
    plt.figure(6)
    plt.hold(True)
    PwrLim = [x*0+0.25 for x in DC.Data['CVTwoWire.i1']]
    PwrR1 = [CVTwoWire.R1_eff*x**2 for x in DC.Data['CVTwoWire.i1']]
    PwrR2 = [CVTwoWire.R2_eff*x**2 for x in DC.Data['CVTwoWire.i1']]
    PwrR3 = [CVTwoWire.R3_eff*x**2 for x in DC.Data['CVTwoWire.i2']]
    PwrR4 = [CVTwoWire.R4_eff*x**2 for x in DC.Data['CVTwoWire.i2']]
    #plt.plot(DC.Data['tsense'],PwrLim, '--r')
    plt.plot(DC.Data['tsense'],PwrR1,label='R1_pwr')
    plt.plot(DC.Data['tsense'],PwrR2,label='R2_pwr')
    plt.plot(DC.Data['tsense'],PwrR3,label='R3_pwr')
    plt.plot(DC.Data['tsense'],PwrR4,label='R4_pwr')
    plt.title("Bridge Resistor Power vs. Tsense")
    plt.xlabel("Tsense (degC)")
    plt.ylabel("Power (Watts)")
    plt.legend()
    plt.grid(True)
    pdf.savefig()

    plt.figure(7)
    plt.plot(DC.Data['tsense'],DC.Data['OpAmpGn'])
    plt.plot(DC.Data['tsense'],DC.Data['OpAmpGn_Exp'])
    plt.title("OpAmp Gain vs vs. Tsense")
    plt.xlabel("Tsense (degC)")
    plt.ylabel("Gain")
    plt.ylim([20.99,21.01])
    plt.legend()
    plt.grid(True)
    pdf.savefig()

#----------------------------------------------
# Save Figures to PDF

