import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

SD = np.loadtxt('solarRadiation.txt', dtype=int)

#print(SD)
# Panel Ligth Collection Area
PA = 0.1    # Panel area in m^2
PE = 0.20   # Eficiency panel
# Real Power Panel 
realPP = SD*PA*PE

# we refine the module to seconds, 5 minutes * 60 = 300 seconds each solar unit
oldSize = len(SD)
newSize = oldSize*300

timeSec =  np.linspace(0,newSize, newSize)
solarPower = np.repeat(realPP, 300)
 
print(timeSec.shape)
print(solarPower.shape)

# ----------- Plots
fig,ax1 = plt.subplots(figsize=(15,5),dpi=200) # plot size

# Data to plot
ax1.plot(timeSec,solarPower,'.k') # plot of solarPower
#ax1.plot(time,realPP,'-r')

# General plot parameters
plt.grid('--',alpha=0.5)

# Y axis
plt.ylabel('Power from panels w',fontsize=14)
plt.yticks(fontsize=12)

# X axis
plt.xlabel('Time units (seconds)',fontsize=14)
plt.xticks(fontsize=12)
plt.xticks(rotation=90)

fig.tight_layout()
plt.show()
plt.close()

# ----------- Battery
batCapacity = 10 # Battery capacity in Amps
batVoltage = 3.8 # Mean voltage batery to calculate power in Volts

# (maximun charge teorically in 1 second) 1h to seconds 3600s = 13.3wh*3600s/1h = 74880ws 
global batC          # Battery capacity in w 3.5A*3.8V = 13.3wh, 
global maxC          # Max chargin power in w (normaly 1Capacity->batC) 13.3wh
global batCharge     # initial battery charge, we start in 50%

batC = batCapacity*batVoltage*3600 
maxC = batCapacity*batVoltage 
batCharge = batC*0.5 
print(batC)
print(maxC)
print(batCharge)

# Model of battery in seconds
def battery(chargeChange):
    global batC
    global maxC
    global batCharge
    #print(batCharge)
    # Future improvements: limit charge/discharge, model, manage overflow last charge
    # The chargeChange could be chargin(positive) or dischargin(negative)
    if chargeChange < 0:
        # Discharging
        if batCharge > abs(chargeChange):
            batCharge = batCharge + chargeChange # Battery reduce charge
            return -chargeChange # Battery deliver the charge requiered
    else:
        # Charging
        if batCharge < batC*0.8: # The battery is under 80% charge, speed charging continue
            if chargeChange > maxC:
                batCharge = batCharge + maxC # Charge acepted at maximun speed
                return -maxC  # The battery accept the max charge
            
            else: # If there is less power available
                batCharge = batCharge + chargeChange # Charge acepted at available speed
                return -chargeChange  # The battery accept the available charge
            
        else:  # Battery in top chargin, reduce the charge speed linearly 
                chargeTaked = maxC*(1-(batCharge/batC)) # Reduce charge
                if chargeTaked > (batC-batCharge):      # If charge taked is over charge lasting
                    chargeTaked = batC-batCharge        # We fit the charge to take to the lasting to full
                    
                if chargeChange > chargeTaked:          # Charge available > Charge to take, We take chargeTaked 
                    batCharge = batCharge + chargeTaked
                    return -chargeTaked
                else:                                   # Charge available < Charge to take, We take chargeChange 
                    batCharge = batCharge + chargeChange
                    return -chargeChange
           
    return 0

# ---- Test the battery model
#global batTestPower
batTestPower = np.zeros(newSize)
batTestPower1 = np.zeros(newSize)

#battery(10)


for t in range(0,newSize):
    # Power imput
    load = 1*np.sin(t/10000) + 1
    powerChange = battery(solarPower[t] - load) # We update the power in time t
    batTestPower[t] = batCharge  # record power in time t
    batTestPower1[t] = load  # record power in time t

# ----------- Plots
fig,ax1 = plt.subplots(figsize=(15,5),dpi=200) # plot size

# Data to plot
ax1.plot(timeSec,solarPower,'-g')
#ax1.plot(time,realPP,'-r')

# General plot parameters
plt.grid('--',alpha=0.5)

# Y axis
plt.ylabel('Efective Solar Energy [ws]',fontsize=14,color='g')
plt.yticks(fontsize=12,color='g',)

# X axis
plt.xlabel('Time units (seconds)',fontsize=14)
plt.xticks(fontsize=12)
#ax1.set_xlim([dt.index.min(), dt.index.max()])
ax1.xaxis.set_major_locator(plt.MaxNLocator(30))
plt.xticks(rotation=90)


ax2 = ax1.twinx()
ax2.plot(timeSec,batTestPower,'-r',timeSec,batTestPower1*40000,'-b')
ax2.set_ylabel('Battery Capacity [ws]',fontsize=14,color='r')
#ax2.set_ylim([realPP.min(),realPP.max()])
plt.yticks(fontsize=12,)
ax2.tick_params('y',color='r',labelsize=12,labelcolor='r')
#ax1.xaxis.set_major_locator(plt.MaxNLocator(10))

#ax3 = ax2.twinx()
#ax3.plot(timeSec,batTestPower1,'-b')
#ax3.set_ylabel('Load [w]',fontsize=14,color='b')
#ax2.set_ylim([realPP.min(),realPP.max()])

#ax3.tick_params('y',color='r',labelsize=12,labelcolor='')
#ax1.xaxis.set_major_locator(plt.MaxNLocator(10))
plt.title('October Radiation Autonomy, Battery: ' + str(batCapacity) + 'Ah, Panel Area: ' + str(PA) + '$m^2$, Load function: 1w+1w*Sin(t)' )

fig.tight_layout()
plt.show()
plt.close()