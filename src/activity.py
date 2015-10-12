#!/usr/bin/env python

import rospy
import numpy as np
from cad120.msg import SubAct,ActivityName,Activity
import time
import cv2

#-------------------------------------------------------------------------------------#
def callback_sub_act(data):
    global sub_activity
    sub_activity = data.Sub							# read sub activity msgs

#-------------------------------------------------------------------------------------#
def callback_act_name(data):
    global ground_truth
    ground_truth = data.activity						# read activity msgs

#-------------------------------------------------------------------------------------#
def Classifier():
	# Load and prepare data set
	activities = {}
	names = []
	counter = 0
	Objects_pointer = open('/home/omari/catkin_ws/src/cad120/src/histogram.txt', 'r')
	for line in Objects_pointer:
	    	line = line.strip(',\n')
		if line == 'END':
		    break
		fields = line.split(',')
		data = np.array(map(int, fields[1].split('[')[1].split(']')[0].split(' ')))
		index = list(np.where(data!=0))
		name = fields[0]	
		if name in names:
			var = len(activities[name])
			activities[name][var] = {}
			for i in index[0]:
				activities[name][var][i] = [data[i]]
		else:
			names = np.append(names,name)
			activities[name] = {}
			activities[name][0] = {}
			for i in index[0]:
				activities[name][0][i] = [data[i]]
		
		counter = counter + 1

	return activities

#########################################################################################
#				Main function						#
#########################################################################################

if __name__ == '__main__':
    	global sub_activity,ground_truth

	print 'Activity Recognition'
	activities = Classifier()					# reading the activity histogram
	print activities
    	rospy.init_node('activity')					# initialize node
    	rospy.Subscriber('SubActivities', SubAct, callback_sub_act)	# subscribe to sub activities msg
    	rospy.Subscriber('CAD120_act', ActivityName, callback_act_name)	# subscribe to the ground truth msg
    	act = rospy.Publisher('activity', Activity)
    	r = rospy.Rate(5) # 2hz						# set the ROS rate
	real_rate = 5
    	# important delay - keep it
    	time.sleep(1)							# wait to make sure that sub activity msg is published

	#------------------------------------------------------------------------------#
	# prepare the image
    	window = 600
    	number = len(activities)
    	th = 20								# thickness of qsr lines
    	name_window = 200						# left margin to write activity names

    	A_vector_comp = np.zeros(shape=(number), dtype=int)  		# initilize the sub_activity matrix actual one
    	A_vector = np.zeros(shape=(number, window), dtype=int)  	# initilize the sub_activity matrix actual one
    	A = np.zeros(shape=(th*number, window, 3), dtype=int)+255  	# initilize the sub_activity matrix for image

    	# preparing the image
    	img = np.zeros((th*number,window+name_window,3), np.uint8)+255		# initializing the image	
    	img[:,name_window-5:name_window,:] = np.zeros((th*number,5,3), np.uint8)

	# writing on the image
	counter = 0
	for i in activities:
		print i
		cv2.putText(img,i,(10,(th*(counter+1))-5), cv2.FONT_HERSHEY_SIMPLEX, .5,(0,0,0),1)
		counter = counter+1

	#--------------------------------------------------------------------------------------	#
	#--------------------------------------------------------------------------------------#
	"""
    	def nothing(x):
	    pass

    	cv2.namedWindow('toolbar', flags=0)
    	cv2.moveWindow('toolbar', 1000, 0)
    	# create trackbars for color change
    	cv2.createTrackbar('R1','toolbar',0,255,nothing)
	cv2.setTrackbarPos('R1','toolbar',15)
	"""
	#------------------------------------------------------------------------------#
	time = 0
    	while not rospy.is_shutdown():					# main loop
  	    if time == real_rate:
		time = 0
		# activity recognition
		Errors = []
		counter = 0
		
	    	A[:,0:window-1,:] = A[:,1:window,:]		# image matrix shifting
		A_vector[:,0:window-1] = A_vector[:,1:window]

		for i in activities:
			Errors_act = []
			for j in activities[i]:
				total = 0
				error = []
				for k in activities[i][j]:
					total += activities[i][j][k][0]
					tmp = activities[i][j][k][0]-sub_activity[k]
					if tmp<0:
						tmp = 0
					error = np.append(error,tmp)
				#print i,j,total,error,(np.sum(error)/total-1)*100
				Errors_act = np.append(Errors_act,(1-np.sum(error)/total)*100)
				#print i,j,total,
			#print i,Errors_act
			Errors = map(int,np.append(Errors,np.max(Errors_act)))
			if len(i)<14:
				print i,'\t','\t',Errors[len(Errors)-1]
			else:
				print i,'\t',Errors[len(Errors)-1]
			var = int(2.55*Errors[len(Errors)-1])
			A[th*counter:th*(counter+1),window-1,:] = [255-var,255-var,255-var]		# update image matrix
			if ground_truth[0].split('/')[0] == i:						# marking the ground truth
				A[th*counter:th*(counter)+3,window-1,:] = [0,0,255]		# update image matrix
				A[th*(counter+1)-3:th*(counter+1),window-1,:] = [0,0,255]		# update image matrix
			counter += 1								# update activity counter
		A_vector[:,window-1] = np.transpose(Errors)
		#print Errors
		print 'Ground truth is : ',ground_truth[0].split('/')[0]
		print '****************************'
    		img[:,name_window:window+name_window,:] = A
		
    		img2 = img
    		cv2.imshow('activities',img)
    		k = cv2.waitKey(1) & 0xFF

		#A_vector[A_vector<80] = 0
		#A_vector[A_vector>=80] = 100
		for i in range(number):
		    #for j in range(window/10):
			#print window/60*j,window/60*(j+1)
			A_vector_comp[i] = np.sum(A_vector[i,window-60:window])/60
		print A_vector_comp		

		act.publish(A_vector_comp)
	    else:
		time += 1
		r.sleep()







		

