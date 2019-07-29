# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 12:37:37 2019

@author: Luis Felipe Arcos
"""

import numpy as np


Input=[[1,1,2,3,2,1,2,3,4,3,2,1,1],[1,1,2,3,2,1,2,3,4,3,2,1,1]] 
battery_charge=np.zeros((len(Input),len(Input[0])))


#defining the load as a constant
load= .1 # example value of the load in W

#define the battery capacity
capacity= 2000 #example of the battery capacity in mAh 

#define the inicial charce of the battery
initial_charge= 800 #example of the initial capacity of the battery in mAh

#define the battery efficiency
batt_eff=0.95 #example of the battery efficiency between 0 and 1

#define the input efficiency
input_eff=0.4 #example of the input efficiency between 0 and 1

#define the load efficiency
load_eff=0.7 #example of the load efficiency between 0 and 1

#define the unit of time frequency in seconds
time=60 #example for sample each minute of the day

#define the selfdischarge rate in percentage per month
self_desch=2

#filling the charge of the battery


def delta(Input,batt_charg):
    time_change=(1/3600)*time#a sample per minute
    timech=(1/100)*(1/(30*3600*24))*time
    a=(Input*input_eff-load/load_eff)*batt_eff*time_change-self_desch*timech*capacity*battery_voltage(batt_charg)/1000
    return a # change of charge in watt/hr

def battery_voltage(charge):
    b=float(charge/capacity)
    a=42.244*(b**5)-116.24*(b**4)+124.6*(b**3)-64.995*(b**2)+16.607*b+2.0406
    return a #returns the battery voltage according to the charge




for x in range(len(Input)):
    for y in range(len(Input[0])):
        if x == 0 and y == 0:
            if initial_charge<capacity:
                c=initial_charge+delta(Input[x][y],initial_charge)/(battery_voltage(initial_charge)*1000)# to fefine rest of equation
                if c<0:
                    battery_charge[x][y]=0
                else:
                    battery_charge[x][y]=c
            else:
                battery_charge[x][y]=initial_charge
        elif y==0:
             if battery_charge[x-1][y-1]<capacity:
                 c=battery_charge[x-1][y-1]+delta(Input[x][y],battery_charge[x-1][y-1])/(battery_voltage(battery_charge[x-1][y-1])*1000)# to fefine rest of equation
                 if c<0:
                    battery_charge[x][y]=0
                 else:
                    battery_charge[x][y]=c
             else:
                 battery_charge[x][y]=battery_charge[x-1][y-1]
        else:
            if battery_charge[x][y-1]<capacity:
                c=battery_charge[x][y-1]+delta(Input[x][y],battery_charge[x][y-1])/(battery_voltage(battery_charge[x][y-1])*1000)# to fefine rest of equation
                if c<0:
                    battery_charge[x][y]=0
                else:
                    battery_charge[x][y]=c
            else:
                battery_charge[x][y]=battery_charge[x][y-1]
print(battery_charge)

