#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-
"""
@author: omari
"""
import os
import numpy as np
import cv2
import csv
from QSR_functions import *

#-------------------------------------------------------------------------------------#
if __name__ == '__main__':

    #-------------- File Path -------------------#
    skeleton_data_dir_path = '/home/omari/Desktop/CAD-120-Full/Subject1_annotations/'
    image_data_dir_path = '/home/omari/Desktop/CAD-120-Full/RGBD_images/Subject1_rgbd_images/'
    activity_list = ['arranging_objects/','cleaning_objects/','having_meal/','making_cereal/','microwaving_food/','nothing/','stacking_objects/','taking_food/','taking_medicine/','unstacking_objects/']
    
    super_activity_list = ['cleaning/','cleaning/','having_meal/','having_meal/','having_meal/','nothing/','cleaning/','having_meal/','taking_medicine/','cleaning/']


    daily_list =['taking_medicine/','nothing/','nothing/','arranging_objects/','unstacking_objects/','stacking_objects/','cleaning_objects/','nothing/','making_cereal/','microwaving_food/','taking_food/','having_meal/']

    person_id_list = {}
    person_id_list[0] = {}
    person_id_list[0] = ['0510175411','0510175431','0510175554']
    person_id_list[1] = ['0510181236','0510181310','0510181415']
    person_id_list[2] = ['0510182019','0510182057','0510182137']
    person_id_list[3] = ['1204142055','1204142227','1204142500','1204142616']
    person_id_list[4] = ['1204150645','1204150828','1204151136']
    person_id_list[5] = ['0510175829','0510175855','0510175921']
    person_id_list[6] = ['1204144410','1204144736','1204145234']
    person_id_list[7] = ['0510180218','0510180342','0510180532']
    person_id_list[8] = ['1204142858','1204143959','1204144120']
    person_id_list[9] = ['1204145527','1204145630','1204145902']


    TOTAL_JOINTS = 15
    joints_enum = {1:'HEAD',
                   2:'NECK',
                   3:'TORSO',
                   4:'LEFT_SHOULDER',
                   5:'LEFT_ELBOW',
                   6:'RIGHT_SHOULDER',
                   7:'RIGHT_ELBOW',
                   8:'LEFT_HIP',
                   9:'LEFT_KNEE',
                  10:'RIGHT_HIP',
                  11:'RIGHT_KNEE',
                  12:'LEFT_HAND',
                  13:'RIGHT_HAND',
                  14:'LEFT_FOOT',
                  15:'RIGHT_FOOT',
                 }

    # constants for calibration
    fx = 525.0  # focal length x
    fy = 525.0  # focal length y
    cx = 319.5  # optical center x
    cy = 239.5  # optical center y

    activity_counter = 0			# here u can chose where to start (which activity)
    daily_counter = 0
    tmp_counter = 0
    activity_counter = activity_list.index(daily_list[daily_counter])
    person_id_counter = 0

    Counter = 0
    while 1:

	Counter += 1
	if Counter > len(np.loadtxt('/home/omari/catkin_ws/src/cad120/src/Month_Data/Month.txt'))-1:
		print 'Finished'
		break
#--------------------------------------------------------------------------------------------------------#
	if np.loadtxt('/home/omari/catkin_ws/src/cad120/src/Month_Data/Month.txt')[Counter]==5:
		activity = 'taking_medicine/'
	elif np.loadtxt('/home/omari/catkin_ws/src/cad120/src/Month_Data/Month.txt')[Counter]==3:
		activity = 'having_meal/'
	else:
		activity = 'nothing/'

	# msgs
	x_world_msg = []
	y_world_msg = []
	z_world_msg = []
	Head_msg = []
	RH_msg = []
	LH_msg = []
	

#--------------------------------------------------------------------------------------------------------#
	if activity != 'nothing/':
		activity_counter = activity_list.index(activity)

		if person_id_counter == len(person_id_list[activity_counter]):
			person_id_counter = 0

	    	skeleton_data_dir = skeleton_data_dir_path+activity
	    	image_data_dir = image_data_dir_path+activity
	    	person_id = person_id_list[activity_counter][person_id_counter]
	    	skeleton_file = person_id_list[activity_counter][person_id_counter]+'.txt'
		object_list_dir = skeleton_data_dir_path+activity+'activityLabel.txt'

	    	joints3D = {}
	    	joints2D = {}
	    
	    	# Get skeleton data
	    	full_skeleton_file = os.path.join(skeleton_data_dir, skeleton_file)
	    	skeleton_file_pointer = open(full_skeleton_file)
	    	for line in skeleton_file_pointer:
			if line == 'END':
		    		break
			line = line.strip(',\n')
			fields = line.split(',')
			fields = map(float, fields)
			frame = int(fields[0])
			joints3D[frame] = {}
			joints2D[frame] = {}
			position = 1
			for i in range(1, TOTAL_JOINTS+1):
		    		joints3D[frame][i] = {}
		    		joints2D[frame][i] = {}
		    		# The last value in the tuple is the confidence
		    		if i <= 11:
		        		# The last four joints have no orientation
		        		joints3D[frame][i]['orientation'] = tuple(fields[position:position+10])
		        		position += 10
		    		joints3D[frame][i]['position'] = tuple(fields[position:position+4])
		    		(x,y,z,c) = joints3D[frame][i]['position']
		    		x_2D = 156.8584456124928*2 + (0.0976862095248 * x - 0.0006444357104 * y + 0.0015715946682 * z)*3
		    		y_2D = 125.5357201011431*2 + (0.0002153447766 * x - 0.1184874093530 * y - 0.0022134485957 * z)*3
		    		joints2D[frame][i]['position'] = (x_2D, y_2D, c)
		    		position += 4

		#-------------------------------------------------------------------#
		# get object names
		object_list_file_pointer = open(object_list_dir)
		line = list(object_list_file_pointer)[person_id_counter]
		line = line.strip(',\n')
		fields = line.split(',')
		obj_name = []
		for i in fields[3:len(fields)+1]:
			obj_name = np.append(obj_name,i.split(':')[1])

	

		# Update of video sequence
		person_id_counter +=1

	    	obj = {}
		for i in range(len(obj_name)):
	    	    obj[i] = {}
		    # Get object data
	    	    full_object_file = os.path.join(skeleton_data_dir, person_id + '_obj'+str(i+1)+'.txt')
	    	    object_file_pointer = open(full_object_file)
	    	    for line in object_file_pointer:
			if line == 'END':
		    		break
			line = line.strip(',\n')
			fields = line.split(',')
			fields = map(float, fields)
			frame = int(fields[0])
			obj[i][frame] = tuple(fields[2:6])

		print Counter,activity,obj_name
	    	frames = joints2D.keys()
	    	frames.sort()
	    	current_frame = 1

		x_world_msg = np.zeros(shape=(len(obj_name),len(frames)), dtype=int)
		y_world_msg = np.zeros(shape=(len(obj_name),len(frames)), dtype=int)
		z_world_msg = np.zeros(shape=(len(obj_name),len(frames)), dtype=int)
		Head_msg = np.zeros(shape=(3,len(frames)), dtype=int)
		RH_msg = np.zeros(shape=(3,len(frames)), dtype=int)
		LH_msg = np.zeros(shape=(3,len(frames)), dtype=int)

	    	for current_frame in frames:

			img_d = cv2.imread(image_data_dir+person_id+'/Depth_'+str(current_frame)+'.png')
			#img_rgb = cv2.imread(image_data_dir+person_id+'/RGB_'+str(current_frame)+'.png')
		
			x_world = []
			y_world = []
			z_world = []

			for j in range(len(obj_name)):
				corners = obj[j][current_frame][:4]
				x1 = int(corners[0])
				y1 = int(corners[1])
				x2 = int(corners[2])
				y2 = int(corners[3])
				z = 1600+40*(img_d[y2/2+y1/2,x2/2+x1/2,0]-20)
				z_world = np.append(z_world,z)
				x_world = np.append(x_world,(x2/2+x1/2 - cx) * z / fx)
				y_world = np.append(y_world,-(y2/2+y1/2 - cy) * z / fy)

			x_world_msg[:,current_frame-1] = x_world
			y_world_msg[:,current_frame-1] = y_world
			z_world_msg[:,current_frame-1] = z_world

			Head = list(joints3D[current_frame][1]['position'][0:3]) 
			RH = list(joints3D[current_frame][12]['position'][0:3]) 
			LH = list(joints3D[current_frame][13]['position'][0:3]) 

			Head_msg[:,current_frame-1] = Head
			RH_msg[:,current_frame-1] = RH
			LH_msg[:,current_frame-1] = LH
			#print Head,RH,LH
			#pub_obj.publish(tuple(x_world),tuple(y_world),tuple(z_world),tuple(obj_name))
			#pub_act.publish(tuple([activity_list[activity_counter]]),tuple([person_id]),tuple([super_activity_list[activity_counter]]))
				
		qsr = QSR(Head_msg,RH_msg,LH_msg,x_world_msg,y_world_msg,z_world_msg,['Head','RH','LH']+list(obj_name))
		print qsr
	else:
		print Counter,activity


#--------------------------------------------------------------------------------------------------------#			
	#qsr = QSR(Head_msg,RH_msg,LH_msg,x_world_msg,y_world_msg,z_world_msg,['Head','RH','LH',obj_name])

    	#cv2.destroyAllWindows()



