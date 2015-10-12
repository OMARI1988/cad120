#!/usr/bin/env python

import rospy
import numpy as np
from cad120.msg import Activity,ActivityName
import time
import cv2
import datetime

#-------------------------------------------------------------------------------------#
def callback_act(data):
    global activity
    activity = data.Activity							# read sub activity msgs

#-------------------------------------------------------------------------------------#
def callback_act_name(data):
    global ground_truth
    ground_truth = data.super_activity						# read activity msgs


#########################################################################################
#				Main function						#
#########################################################################################

if __name__ == '__main__':
    	global activity,ground_truth

	print 'Super Activity Recognition'
	
	rospy.init_node('super_activity')					# initialize node
    	rospy.Subscriber('activity', Activity, callback_act)			# subscribe to sub activities msg
    	rospy.Subscriber('CAD120_act', ActivityName, callback_act_name)		# subscribe to the ground truth msg

    	r = rospy.Rate(5) # 2hz						# set the ROS rate
	real_rate = 5*60						# ROS rate x 60 = 1 minute
	#real_rate = 1
    	# important delay - keep it
    	time.sleep(1)							# wait to make sure that sub activity msg is published


	Super_Activity = ['cleaning','having_meal','taking_medicine']
	number = len(Super_Activity)+1					# +1 for the time


	# prepare the image
    	window = 60*24							# 60 minutes x 24 hours = 1 day
    	th = 20								# thickness of super activity lines
    	name_window = 200						# left margin to write activity names
	save_image = 1							# save image every 1 minutes
    	A_vector = np.zeros(shape=(number-1, window), dtype=int)  	# initilize the supper_activity matrix actual one
    	A = np.zeros(shape=(th*(number-1), window, 3), dtype=int)+255  	# initilize the supper_activity matrix for image

    	# preparing the image
    	img = np.zeros((th*number,window+name_window,3), np.uint8)+255		# initializing the image	
    	img[:,name_window-5:name_window,:] = np.zeros((th*number,5,3), np.uint8)	
	for i in range(number+1):
    	    img[i*th:i*th+1,:,:] = np.zeros((1,window+name_window,3), np.uint8)

	# writing on the image
	counter = 0
	for i in Super_Activity:
		#print i
		cv2.putText(img,i,(10,(th*(counter+1))-5), cv2.FONT_HERSHEY_SIMPLEX, .5,(0,0,0),1)
		counter = counter+1
	# writing the time
	date = datetime.datetime.now().strftime("%Y-%m-%d")
	cv2.putText(img,'Time'+' '+date,(10,(th*(counter+1))-5), cv2.FONT_HERSHEY_SIMPLEX, .5,(0,0,0),1)
	
    	Time_line = np.zeros((th*number,1,3), np.uint8)
	for i in xrange(th*number):
	    if i % 2:
		Time_line[i,:,:] = 255
	for i in range(24):
	    cv2.putText(img,str(i)+':00',(name_window+i*60,(th*(counter+1))-5), cv2.FONT_HERSHEY_SIMPLEX, .5,(0,0,0),1)	
    	    img[:,name_window+i*60:name_window+i*60+1,:] = Time_line
		

	#------------------------------------------------------------------------------#
	time = 0
	save_image_time = 0
    	while not rospy.is_shutdown():					# main loop
		#print activity,ground_truth
		hour = int(datetime.datetime.now().strftime("%H"))
		minute = int(datetime.datetime.now().strftime("%M"))

		if time == real_rate:
			time = 0
				# update activity counter
			activity = np.array(activity)
			activity[activity<85] = 0
			v1 = activity[0] + activity[2] + activity[7] + activity[8]
			v2 = activity[3] + activity[4] + activity[5] + activity[6] 
			v3 = activity[1]
			print v1,v2,v3
				# update activity counterS

			A[th*0:th*1,hour*60+minute,:] = [255-v1/1,255-v1/1,255-v1/1]		# update image matrix
			A[th*1:th*2,hour*60+minute,:] = [255-v2/1,255-v2/1,255-v2/1]		# update image matrix
			A[th*2:th*3,hour*60+minute,:] = [255-v3/1,255-v3/1,255-v3/1]		# update image matrix
			A_vector[:,hour*60+minute] = np.transpose([v1,v2,v3])				# update actual matrix
			#print hour,minute,hour*60+minute
			counter = 0
			for i in Super_Activity:
			    if ground_truth[0].split('/')[0] == i:						# marking the ground truth
				A[th*counter:th*(counter)+3,hour*60+minute,:] = [0,0,255]			# update image matrix
				A[th*(counter+1)-3:th*(counter+1),hour*60+minute,:] = [0,0,255]		# update image matrix
			    counter += 1

    			img[0:th*(number-1),name_window:window+name_window,:] = A
	
			for i in range(number+1):							# draw horizental lines
    	    		    img[i*th:i*th+1,:,:] = np.zeros((1,window+name_window,3), np.uint8)

			for i in range(24):								# draw vertical lines
	    		    cv2.putText(img,str(i)+':00',(name_window+i*60,(th*(counter+1))-5), cv2.FONT_HERSHEY_SIMPLEX, .5,(0,0,0),1)	
    	 		    img[:,name_window+i*60:name_window+i*60+1,:] = Time_line

			#---------------------------#
			save_image_time += 1
			if save_image_time == save_image:
		            cv2.imwrite('/home/omari/catkin_ws/src/cad120/src/images/super_activity_'+date+' '+str(hour)+':'+str(minute)+'.png',img)
			    save_image_time = 0
			    # save the data in a file
        		    np.savetxt('/home/omari/catkin_ws/src/cad120/src/Data/'+date+'.txt', np.transpose(A_vector), fmt='%-4i')

		else:
			time += 1

    		cv2.imshow('super activities',img)
    		k = cv2.waitKey(1) & 0xFF

		r.sleep()







		

