#!/usr/bin/env python

import numpy as np
import pylab as pl


import cv2

##############################################################################
# Load and prepare data set
X_2d = np.array(np.random.random((500,40)), dtype = np.float32)
Y_2d = np.array(np.random.random((500)), dtype = np.int)
names = ""

activity_list = ['nothing','arranging_objects','cleaning_objects','having_meal','making_cereal','microwaving_food','picking_objects','stacking_objects','taking_food','taking_medicine','unstacking_objects']
counter = 0
Objects_pointer = open('/home/omari/catkin_ws/src/cad120/src/histogram.txt', 'r')
for line in Objects_pointer:
    	line = line.strip(',\n')
        if line == 'END':
            break
	fields = line.split(',')
        X_2d[counter,:] = fields[1].split('[')[1].split(']')[0].split(' ')
	names = np.append(names,fields[0])
	counter2=0
	for i in activity_list:
	    if i==fields[0]:
		Y_2d[counter] = counter2
	    counter2 += 1
	counter = counter + 1

X_2d = X_2d[0:counter-1,:]
Y_2d = Y_2d[0:counter-1]
print X_2d
##############################################################################
# Train classifier
knn = cv2.KNearest()
knn.train(X_2d,Y_2d)
ret,result,neighbours,dist = knn.find_nearest(X_2d[0:1,:],k=1)
print result,Y_2d





