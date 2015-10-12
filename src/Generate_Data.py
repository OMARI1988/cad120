#!/usr/bin/env python

import rospy
import numpy as np
from cad120.msg import SubAct,ActivityName,Activity
import time
import cv2
import datetime

#########################################################################################
#				Main function						#
#########################################################################################

if __name__ == '__main__':

	def monthly_act(loc1,scale1,days,number,supper_act):
		c = np.random.normal(loc=loc1[0], scale=scale1[0], size=number)
		d = np.random.normal(loc=loc1[1], scale=scale1[1], size=number)
		ind = Super_Activity.index(supper_act)
		
		for i in days:
    			A_vector[i,int(c[i]):int(c[i])+int(d[i])] = ind  	# initilize the supper_activity matrix actual one
			A[th*i:th*(i+1),int(c[i]):int(c[i])+int(d[i]),:] = Super_Activity_color[ind]
		
	
	#-------------------------------------------------------------------------------#
	number = 1			# number of days
	number2 = number+1			# for image purposes

	lunch_c = np.random.normal(loc=13*60, scale=10, size=number)
	lunch_d = np.random.normal(loc=50, scale=5, size=number)

	dinner_c = np.random.normal(loc=19*60, scale=20, size=number)
	dinner_d = np.random.normal(loc=50, scale=10, size=number)

	cleaning_c = np.random.normal(loc=9.5*60, scale=30, size=number)
	cleaning_d = np.random.normal(loc=90, scale=40, size=number)


	#-------------------------------------------------------------------------------#
	Super_Activity = ['nothing','cleaning','working','having meal','cooking','taking medicine','talking on phone','brushing teeth','watching TV']
	Super_Activity_color = [[255,255,255],[255,0,0],[0,255,0],[0,0,255],[255,255,0],[0,255,255],[255,100,55],[80,0,80],[10,10,70]]


	# prepare the image
    	window = 60*24							# 60 minutes x 24 hours = 1 day
	label_window = 20
    	th = 20								# thickness of super activity lines
    	name_window = 200						# left margin to write activity names
	save_image = 1							# save image every 1 minutes
    	A_vector = np.zeros(shape=(number, window), dtype=int)  	# initilize the supper_activity matrix actual one
    	A = np.zeros(shape=(th*(number), window, 3), dtype=int)+255  	# initilize the supper_activity matrix for image

	# preparing the image
    	img = np.zeros((th*(number2),window+name_window,3), np.uint8)+255		# initializing the image	
    	img[:,name_window-5:name_window,:] = np.zeros((th*(number2),5,3), np.uint8)	
	
	# preparing the image label
	activity_number = len(Super_Activity)
    	img2 = np.zeros((th*(activity_number),label_window+name_window,3), np.uint8)+255		# initializing the image	
    	img2[:,label_window-5:label_window,:] = np.zeros((th*(activity_number),5,3), np.uint8)	
	for i in range(activity_number):
		print 'color',i	,Super_Activity[i]	
		img2[th*i:th*(i+1),0:label_window,:] = Super_Activity_color[i]
		cv2.putText(img2,Super_Activity[i],(30,(th*(i+1))-5), cv2.FONT_HERSHEY_SIMPLEX, .5,(0,0,0),1)
	
	#-------------------------------------------------------------------------------#
	# Creating the daily activities	
	workdays = range(0,number,7) + range(1,number,7) + range(2,number,7) + range(3,number,7) + range(4,number,7)
	
	monthly_act([6.5*60,5],[10,1],workdays,number,'taking medicine')	# taking medcine
	monthly_act([7*60,15],[10,5],workdays,number,'having meal')		# Breakfast
	monthly_act([9*60,9*60],[5,5],workdays,number,'working')		# Working
	monthly_act([13*60,40],[10,10],workdays,number,'having meal')		# Lunch
	monthly_act([20*60,60],[20,20],workdays,number,'having meal')		# Dinner
	monthly_act([12*60,3],[120,3],workdays,number,'talking on phone')	# phone
	monthly_act([16*60,3],[120,3],workdays,number,'talking on phone')	# phone
	monthly_act([10*60,3],[120,3],workdays,number,'talking on phone')	# phone
	monthly_act([7.5*60,3],[10,3],workdays,number,'brushing teeth')		# teeth
	monthly_act([22*60,3],[10,3],workdays,number,'brushing teeth')		# teeth
	monthly_act([23*60,30],[10,10],workdays,number,'watching TV')		# TV
	monthly_act([15*60,5],[60,5],workdays,number,'nothing')			# nothing
	monthly_act([17*60,5],[60,5],workdays,number,'nothing')			# nothing
	monthly_act([11*60,5],[60,5],workdays,number,'nothing')			# nothing
	monthly_act([17*60,5],[60,5],workdays,number,'nothing')			# nothing
	monthly_act([11*60,5],[60,5],workdays,number,'nothing')			# nothing
	# Creating the weekends activities
	weekend = range(5,number,7) + range(6,number,7)
	monthly_act([6.5*60,5],[10,1],weekend,number,'taking medicine')		# taking medcine
	monthly_act([7*60,15],[10,5],weekend,number,'having meal')		# Breakfast
	monthly_act([13*60,40],[10,10],weekend,number,'having meal')		# Lunch
	monthly_act([20*60,60],[20,20],weekend,number,'having meal')		# Dinner
	monthly_act([16*60,3],[120,3],weekend,number,'talking on phone')	# phone
	monthly_act([10*60,3],[120,3],weekend,number,'talking on phone')	# phone
	monthly_act([7.5*60,3],[10,3],weekend,number,'brushing teeth')		# teeth
	monthly_act([22*60,3],[10,3],weekend,number,'brushing teeth')		# teeth
	monthly_act([22*60,90],[10,10],weekend,number,'watching TV')		# TV
	monthly_act([11*60,90],[10,10],weekend,number,'watching TV')		# TV
	
    	img[0:th*(number),name_window:window+name_window,:] = A

	#-------------------------------------------------------------------------------#
	days = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
	for i in range(number2):
    	    img[i*th:i*th+1,:,:] = np.zeros((1,window+name_window,3), np.uint8)
	# writing on the image
	counter = 0
	for i in range(number):
		#print i
		cv2.putText(img,days[i%7],(10,(th*(counter+1))-5), cv2.FONT_HERSHEY_SIMPLEX, .5,(0,0,0),1)
		counter = counter+1
	# writing the time
	date = datetime.datetime.now().strftime("%Y-%m-%d")
	cv2.putText(img,'Time',(10,(th*(counter+1))-5), cv2.FONT_HERSHEY_SIMPLEX, .5,(0,0,0),1)
	
    	Time_line = np.zeros((th*(number2),1,3), np.uint8)
	for i in xrange(th*number2):
	    if i % 2:
		Time_line[i,:,:] = 255
	for i in range(24):
	    cv2.putText(img,str(i)+':00',(name_window+i*60,(th*(counter+1))-5), cv2.FONT_HERSHEY_SIMPLEX, .5,(0,0,0),1)	
    	    img[0:th*(number+1),name_window+i*60:name_window+i*60+1,:] = Time_line

    	cv2.imshow('super activities',img)
    	cv2.imshow('super activities labels',img2)

	
	np.savetxt('/home/omari/catkin_ws/src/cad120/src/Month_Data/Month.txt',np.transpose(A_vector), fmt='%-4i')
	
	while True:
		if cv2.waitKey(1) & 0xFF == 27:
            		break 

		

