import xlrd
from datetime import time
wb = xlrd.open_workbook('/home/piaktipik/Desktop/simplePower/Prueba_corrienteSCPv1.xlsm')
sh1 = wb.sheet_by_name(u'Movimientos')
#sh1 = wb.sheet_by_name(u'Sheet1')

print (sh1.col_values(0))  # column 0
print (sh1.col_values(1))  # column 1

sh2 = wb.sheet_by_name(u'Movimientos')

x = sh2.col_values(1)[1:-1]  # column 0
y = sh2.col_values(0)[1:-1]  # column 1

c=0
base = x[0]
for i,xx in enumerate(x):
    x[i] = int((xx-base) * 24 * 3600) # convert to number of second

import matplotlib.pyplot as plt
plt.plot(x, y)
plt.ylabel('Corriente',fontsize=14)
plt.ylim([0,1])
plt.yticks(fontsize=12)
plt.grid('--',alpha=0.5)
plt.xlabel('Tiempo [HH:mm:SS]',fontsize=14)
plt.xticks(fontsize=12,rotation=45)
plt.savefig('/home/piaktipik/Desktop/simplePower/SPower-1.png')
plt.show()