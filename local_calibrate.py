import csv
import numpy as np

xVals = []
yVals = []
zVals = []

with open('data.csv', 'r') as csvfile:
        dataReader = csv.reader(csvfile, delimiter=',')
        for row in dataReader:
        	x, y, z = row
        	xVals.append(float(x))
        	yVals.append(float(y))
        	zVals.append(float(z))

'''
hard iron
'''

x_bias=(max(xVals)+min(xVals))/2
y_bias=(max(yVals)+min(yVals))/2
z_bias=(max(zVals)+min(zVals))/2
print(' x_bias:',x_bias, ' y_bias:', y_bias, ' z_bias:',z_bias)
xVals_2 = np.array(xVals)-x_bias
yVals_2 = np.array(yVals)-y_bias
zVals_2 = np.array(zVals)-z_bias

x_scale=(max(xVals)-min(xVals))/2.0
y_scale=(max(yVals)-min(yVals))/2.0
z_scale=(max(zVals)-min(zVals))/2.0

avg_scale = (x_scale+y_scale+z_scale) / 3.0


xVals_3 = xVals_2 * avg_scale / x_scale
yVals_3 = yVals_2 * avg_scale / y_scale
zVals_3 = zVals_2 * avg_scale / z_scale
print(' x_scale:',avg_scale / x_scale, ' y_scale:', avg_scale /y_scale, ' z_scale:',avg_scale /z_scale)

with open('data_3.csv', 'w', newline='') as csvfile:
        dataWriter = csv.writer(csvfile, delimiter=',')
        for i in range(len(xVals)):
            dataWriter.writerow((xVals_3[i],yVals_3[i],zVals_3[i]) )
