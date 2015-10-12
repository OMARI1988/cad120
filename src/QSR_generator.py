#!/usr/bin/env python

import rospy
from cad120.msg import Skeleton,Objects,QSR,ActivityName
import numpy as np
import cv2
import math
import time


th = 20			# thickness of qsr lines
n = []
n_qsr = []	# number of qsrs (n is the number of objects + skeleton joints u have)
window = 30
window_filter = 8
name_window = 200
A = {}			#join two dicts python
A_sk = {}
A_ob = {}
qsr1 = []
#-------------------------------------------------------------------------------------#
def features_calc(A,B):
	distance = np.sqrt((A[0]/100-B[0]/100)**2 + (A[1]/100-B[1]/100)**2 + (A[2]/1000-B[2]/1000)**2)
	distance = distance/10

	if distance<.25:
		var = [255,0,0]
		b='touch'
	elif distance<.8:
		var = [0,255,0]
		b='near'
	else:
		var = [0,0,255]
		b='far'
	return (var,b)

#-------------------------------------------------------------------------------------#
def Direction_calc(A,B):
	Y = A[0]/100-B[0]/100
	X = A[1]/100-B[1]/100
	Z = A[2]/100-B[2]/100
	if np.all(np.absolute(X)>np.absolute(Y) and np.absolute(X)>np.absolute(Z)):
		if X>0:
			var='buttom'
		else:
			var='top'

	elif np.all(np.absolute(Y)>np.absolute(X) and np.absolute(Y)>np.absolute(Z)):
		if Y>0:
			var='left'
		else:
			var='right'

	else:
		if Z>0:
			var='front'
		else:
			var='Back'

	return var
#-------------------------------------------------------------------------------------#
def Allen(x1,y1,x2,y2):

	temp = []
	if x1==x2 and y1==y2:
		temp='equal'
	elif x1!=x2 and y1==y2:
		temp='finishes'
	elif x1==x2 and y1!=y2:
		temp='starts'
	elif (x1>x2 and y1<y2) or (x1<x2 and y1>y2):
		temp='during'
	elif (x1<x2 and y1<y2 and y1>x2) or (x2<x1 and y2<y1 and y2>x1):
		temp='overlap'
	elif (x1<x2 and y1==x2 and y2>y1) or (x2<x1 and y2==x1 and y1>y2):
		temp='meets'
	elif (x1<x2 and y1<x2) or (x2<x1 and y2<x1):
		temp='before'
	else:
		temp='problem'

	return temp

#-------------------------------------------------------------------------------------#
def callback_activity(data):
    global activity,ID
    activity = data.activity
    ID = data.id

#-------------------------------------------------------------------------------------#
def callback_objects(data):
    global A_ob,Names_memory

    A_ob1 = {}
    Names_memory1 = ['Head','RH','LH']						# names of joints added to Names
    for i in range(len(data.z)):
    	Ox = data.x[i]
    	Oy = data.y[i]
    	Oz = data.z[i]
    	Names_memory1 = np.append(Names_memory1,data.Name[i])			# names of joints added to Names
	A_ob1[i+3] = [Ox,Oy,Oz]
    A_ob = A_ob1
    Names_memory = Names_memory1

#-------------------------------------------------------------------------------------#
def callback_skeleton(data):
    global A_sk

    A_sk1 = {}
    A_sk1[0] = list(data.Head)
    A_sk1[1] = list(data.RH)
    A_sk1[2] = list(data.LH)
    A_sk = A_sk1

#-------------------------------------------------------------------------------------#
def listener():
    global A_ob,A_sk,Names_memory,activity,ID

    rospy.init_node('QSR_generator')
    rospy.Subscriber('CAD120_sk', Skeleton, callback_skeleton)
    rospy.Subscriber('CAD120_ob', Objects, callback_objects)
    rospy.Subscriber('CAD120_act', ActivityName, callback_activity)

    pub = rospy.Publisher('QSRs', QSR)
    r = rospy.Rate(20) # 10hz
    spatial_relations = ['touch','near','far']
    directional_relation = ['top','buttom','right','left','front','back']


    time.sleep(1)
    n_old = 0
    names_old = 0



    #-------------------#
    activity = '0'
    ID = '1'
    activity_old = '0'
    ID_old = '0'
    #-------------------#

    while not rospy.is_shutdown():						# QSR generation

	# preparing matrix A
	A = dict(A_sk.items() + A_ob.items())
	Names = Names_memory


	# preparing the QSR matrix and the image
    	n = len(Names)
	#if n != n_old or np.any(names_old != Names) or ID_old != ID:
	if ID_old != ID or n != n_old:

		n_old = n
		ID_old = ID
		print 'change in qsr',n,activity,ID
		names_old = Names
    		n_qsr = np.sum(range(n))					# number of qsrs (n is the number of objects + skeleton joints u have)
    		QSR_vector = []
    		QSR_vector = np.zeros(shape=(n_qsr, window), dtype=int)  	# initilize the QSR matrix actual one
    		qsr1 = np.zeros(shape=(th*n_qsr, window, 3), dtype=int)+255  	# initilize the QSR matrix for image
    		Dir_vector = np.zeros(shape=(n, n), dtype=str)  	# initilize the direction matrix
		# initilize the filter
    		QSR_vector_filter = np.zeros(shape=(n_qsr, window_filter), dtype=int)  	# initilize the QSR matrix actual one
    		qsr1_filter = np.zeros(shape=(th*n_qsr, window_filter, 3), dtype=int)+255  	# initilize the QSR matrix for image
		n_old = n

    		img = np.zeros((th*n_qsr,window+name_window,3), np.uint8)+255		# initializing the image
		img[:,name_window-5:name_window,:] = np.zeros((th*n_qsr,5,3), np.uint8)

    		# writing on the image
    		counter = 0
    		for i in range(n):
	    	    for j in range(i+1,n):
	     		cv2.putText(img,Names[i]+'-'+Names[j],(10,(th*(counter+1))-5), cv2.FONT_HERSHEY_SIMPLEX, .5,(0,0,0),1)
	     		counter = counter+1



	#------- Filter -------#
    	qsr1_filter[:,0:window_filter-1,:] = qsr1_filter[:,1:window_filter,:]
	QSR_vector_filter[:,0:window_filter-1] = QSR_vector_filter[:,1:window_filter]

    	counter = 0
    	for i in range(n):
	    for j in range(i+1,n):
	     	qsr1_filter[th*counter:th*(counter+1),window_filter-1,:],Q = features_calc(A[i],A[j])
		Dir_vector[i,j] = Direction_calc(A[i],A[j])
		Dir_vector[j,i] = Direction_calc(A[j],A[i])
		if Q == 'touch':
			QSR_vector_filter[counter,window_filter-1] = 0
		if Q == 'near':
			QSR_vector_filter[counter,window_filter-1] = 1
		if Q == 'far':
			QSR_vector_filter[counter,window_filter-1] = 2
		counter +=1

	#print Dir_vector

    	for i in range(counter-1):
	    l = QSR_vector_filter[i,0]
	    change = 0
	    for k in range(1,window_filter):
		if l != QSR_vector_filter[i,k]:
		    change +=1
		    l = QSR_vector_filter[i,k]

	    if change > 1:
		QSR_vector_filter[i,1:window_filter-1] = np.repeat(QSR_vector_filter[i,0], window_filter-2)
		a = qsr1_filter[th*i:th*(i+1),0,:]
		for ll in range(1,window_filter-1):
			qsr1_filter[th*i:th*(i+1),ll,:] = a

	#------- End Filter -------#

    	# Computing the qsr
    	qsr1[:,0:window-1,:] = qsr1[:,1:window,:]
	QSR_vector[:,0:window-1] = QSR_vector[:,1:window]

	qsr1[:,window-1,:] = qsr1_filter[:,0,:]
	QSR_vector[:,window-1] = QSR_vector_filter[:,0]


    	# set the qsr on img
    	img[:,name_window:window+name_window,:] = qsr1

    	# preparing graph msg
	o1 = []
	o2 = []
	spa = []
	spa_interval = []
    	counter = 0
    	for i in range(n-1):
	    for j in range(i+1,n):
	    	o1 = np.append(o1,Names[i])
	    	o2 = np.append(o2,Names[j])
		spa = np.append(spa,spatial_relations[QSR_vector[counter,0]])
		l = QSR_vector[counter,0]
		spa_interval = np.append(spa_interval,0)
		for k in range(1,window):
			if l != QSR_vector[counter,k]:
				l = QSR_vector[counter,k]
	    			o1 = np.append(o1,Names[i])
	    			o2 = np.append(o2,Names[j])
				spa = np.append(spa,spatial_relations[l])
				spa_interval = np.append(spa_interval,k)
				spa_interval = np.append(spa_interval,k)
	     	counter = counter+1
	        spa_interval = np.append(spa_interval,window)

	temporal = []
	for i in range(len(spa)-1):
		for j in range(i+1,len(spa)):
			x1 = spa_interval[i*2]
			y1 = spa_interval[i*2+1]
			x2 = spa_interval[j*2]
			y2 = spa_interval[j*2+1]
			temporal = np.append(temporal,Allen(x1,y1,x2,y2))
			#print x1,y1,x2,y2,temporal

	Dir_msg = []
	for i in range(n):
		var = tuple(Dir_vector[i,:])
		Dir_msg = np.append(Dir_msg,var)

	pub.publish(tuple(o1),tuple(spa),tuple(o2),tuple(temporal),tuple(Names),Dir_msg)
        r.sleep()
    	# display the qsr
    	cv2.imshow('QSR',img)
    	k = cv2.waitKey(5) & 0xFF

    #rospy.spin()

#-------------------------------------------------------------------------------------#
if __name__ == '__main__':
    # check how many object
    Objects_pointer = open('/home/omari/catkin_ws/src/graphs/src/objects.txt', 'r')


    print('QSR generator running...  '+str(n)+' objects found')
    listener()
