#!/usr/bin/env python

import rospy
import cv2
import time
import numpy as np
from networkx import *
import networkx.algorithms.isomorphism as iso
from Graph_functions import *
from Speech_functions import *
from cad120.msg import QSR,SubAct

#-------------------------------------------------------------------------------------#
def callback_graphs(data):
	global QSR_msg
	QSR_msg = data

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
def graph_msg(Names,QSR_vector,window,n,spatial_relations_names,objects_names):
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
		spa = np.append(spa,spatial_relations_names[QSR_vector[counter,0]])
		l = QSR_vector[counter,0]
		spa_interval = np.append(spa_interval,0)
		for k in range(1,window):
			if l != QSR_vector[counter,k]:
				l = QSR_vector[counter,k]
	    			o1 = np.append(o1,Names[i])
	    			o2 = np.append(o2,Names[j])
				spa = np.append(spa,spatial_relations_names[l])
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

	plotting = False
	G0 = graph_maker(o1,o2,spa,temporal,objects_names,plotting)
	return G0


#########################################################################################
#				Graph matching						#
#########################################################################################
def listener():
    global QSR_msg,Activities
    
    # initialize ROS node
    rospy.init_node('sub_activity')
    rospy.Subscriber('QSRs', QSR, callback_graphs)
    pub = rospy.Publisher('SubActivities', SubAct)
    r = rospy.Rate(5) # 5hz

    # important delay - keep it
    time.sleep(1)

    # matching proporties
    nm = iso.categorical_node_match('type1', '')
    em = iso.categorical_edge_match('dirx', '')

    # preparing the sub_activity matrix
    window = 150
    number = len(activities_names)
    th = 15			# thickness of qsr lines
    name_window = 200		# left margin to write activity names

    subA_vector = np.zeros(shape=(number, window), dtype=int)  		# initilize the sub_activity matrix actual one
    subA = np.zeros(shape=(th*number, window, 3), dtype=int)+255  	# initilize the sub_activity matrix for image
    #subA_interval = np.zeros(shape=(number, window, 1), dtype=int)  	# initilize the sub_activity matrix for intervals

    # preparing the image
    img = np.zeros((th*number,window+name_window,3), np.uint8)+255		# initializing the image	
    img[:,name_window-5:name_window,:] = np.zeros((th*number,5,3), np.uint8)

    # writing on the image
    counter = 0
    for i in range(len(activities_names)):
	cv2.putText(img,activities_names[i],(10,(th*(counter+1))-5), cv2.FONT_HERSHEY_SIMPLEX, .5,(0,0,0),1)
	counter = counter+1

    A1 = 0
    while not rospy.is_shutdown():

	# if A1 dont change then no need to do all the calculation !
	if A1 != QSR_msg:
		A1 = QSR_msg
		G1 = graph_maker(A1.o1,A1.o2,A1.spatial,A1.temporal,A1.objects,False)

		results = []
		for i in range(len(Activities)):
			flag = 1
			G_copy = G1
			counter = 0
			nodes1 = Activities[int(i)].nodes()
			nodes2 = G_copy.nodes()
			obj_nodes1 = []
			obj_nodes2 = []
			obj_nodes1 = np.append(obj_nodes1,[n for n in list(nodes1) if Activities[int(i)].node[n]['type2']=='object'])
			obj_nodes2 = np.append(obj_nodes2,[n for n in list(nodes2) if G_copy.node[n]['type2']=='object'])
			obj_exist = []
			for n in obj_nodes1:
				obj_exist = np.append(obj_exist, np.where(obj_nodes2==n))
			#print len(obj_exist),len(obj_nodes1)
			print i
			#print Activities[int(i)].node[n]['type2']=='temporal'
			if len(obj_exist)==len(obj_nodes1):
			    while flag==1:
				GM = iso.GraphMatcher(G_copy,Activities[int(i)],node_match=nm,edge_match=em)
				if GM.subgraph_is_isomorphic():
					counter +=1
				used_nodes1 = GM.mapping
				if used_nodes1 != {}:
					#print list(used_nodes1)
					#print [n for n in list(used_nodes1) if G_copy.node[n]['type2']=='temporal']
					used_nodes2 = []
					used_nodes2 = np.append(used_nodes2, [n for n in list(used_nodes1) if G_copy.node[n]['type2']=='temporal'])
					G_copy.remove_nodes_from(used_nodes2)	# remove temporal nodes from the graph
				else:
		 			flag = 0
			 		results = np.append(results,counter)

			else:
		 		flag = 0
				results = np.append(results,counter)
			#print i

    	subA[:,0:window-1,:] = subA[:,1:window,:]
	subA_vector[:,0:window-1] = subA_vector[:,1:window]

	counter = 0
	for i1 in results:
	    if i1>0:
		subA[th*counter:th*(counter+1),window-1,:] = [255,0,0]
		subA_vector[counter,window-1] = 1
	    else:
		subA[th*counter:th*(counter+1),window-1,:] = [255,255,255]
		subA_vector[counter,window-1] = 0
	    counter += 1


	# If you ever needed to do the interval,
	# 1 find sub_interval
	# 2 find the first positive number because thats where the first pick is
	"""
	subA_interval = subA[th,:,2]-subA[0,:,2]
	index_pk = list(np.where(subA_interval==255))
	index_pc = np.where(subA_interval==-255)
	if list(index_pk[0]) !=[]:
		I_pk = list(index_pk[0])[0]
		for j1 in range(len(list(index_pk[0]))-1):
		    if list(index_pk[0])[j1+1]-list(index_pk[0])[j1] > 1:
			I_pk = np.append(I_pk,list(index_pk[0])[j1+1])

	if list(index_pc[0]) !=[]:
		I_pc = list(index_pc[0])[0]
		for j1 in range(len(list(index_pc[0]))-1):
		    if list(index_pc[0])[j1+1]-list(index_pc[0])[j1] > 1:
			I_pc = np.append(I_pc,list(index_pc[0])[j1+1])
	"""
	counter_sub_acivities = np.zeros((number), np.uint8)
	for i1 in range(number):
	    index_pk = list(np.where(subA_vector[i1,:]==1))
	    if list(index_pk[0]) !=[]:
		counter_sub_acivities[i1] = 1
		for j1 in range(len(list(index_pk[0]))-1):
		    if list(index_pk[0])[j1+1]-list(index_pk[0])[j1] > 1:
			counter_sub_acivities[i1] += 1

	pub.publish(tuple(counter_sub_acivities))
    	img[:,name_window:window+name_window,:] = subA

        r.sleep()
    	cv2.imshow('sub activities',img)		
	if cv2.waitKey(1) & 0xFF == 27:
            	break 


#########################################################################################
#				Reading sentences					#
#########################################################################################

if __name__ == '__main__':


	Activities = {}

    	sentences_pt = '/home/omari/catkin_ws/src/cad120/src/language.txt'
    	time_words_pt = '/home/omari/catkin_ws/src/cad120/src/learned_time.txt'
    	spatial_relations_pt = '/home/omari/catkin_ws/src/cad120/src/learned_spatial.txt'
    	object_relations_pt = '/home/omari/catkin_ws/src/cad120/src/learned_objects.txt'

	activities_names,Final = speech_processing(sentences_pt,time_words_pt,spatial_relations_pt,object_relations_pt)

	counter = 0
	for i1 in Final:	
		Activities[counter] = graph_msg(i1[0],i1[1],i1[2],i1[3],i1[4],i1[5])
		counter +=1

    	listener()
