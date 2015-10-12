#!/usr/bin/env python

import numpy as np
import pylab as pl

from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import load_iris
from sklearn.cross_validation import StratifiedKFold
from sklearn.grid_search import GridSearchCV
from sklearn.externals import joblib
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

print X_2d[0:counter-1,:],Y_2d[0:counter-1],names

X_2d = X_2d[0:counter-1,:]
Y_2d = Y_2d[0:counter-1]

##############################################################################
# Train classifier

# Now we need to fit a classifier for all parameters in the 2d version
# (we use a smaller set of parameters here because it takes a while to train)
C_2d_range = [1e3, 1e4, 1e5]
gamma_2d_range = 5*np.linspace(.5,1.5,5)
C_2d_range = [1e4]
gamma_2d_range = [3]
#C_2d_range = [1e4]
#gamma_2d_range = [1]

classifiers = []
for C in C_2d_range:
    for gamma in gamma_2d_range:
        clf = SVC(C=C, gamma=gamma, degree=3)
        clf.fit(X_2d, Y_2d)
        classifiers.append((C, gamma, clf))

joblib.dump(clf, '/home/omari/catkin_ws/src/cad120/src/act.pkl')
