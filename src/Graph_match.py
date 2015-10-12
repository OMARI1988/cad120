#!/usr/bin/env python

import rospy
from qsr.msg import QSR
import cv2
import math
import time
import numpy as np
from networkx import *
from itertools import permutations
import matplotlib.pyplot as plt
import networkx.algorithms.isomorphism as iso
from Graph_functions import *
from nltk.corpus import stopwords
from Speech_functions import *

#-------------------------------------------------------------------------------------#
def callback_graphs(data):
	global A
	A = data

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
	global G0
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
    global G,spatial_nodes_counter,temporal_nodes_counter,labels,A,G0,Activities

    rospy.init_node('Graphs2')
    rospy.Subscriber("QSRs", QSR, callback_graphs)
    r = rospy.Rate(10) # 10hz

    time.sleep(1)


    nm = iso.categorical_node_match('type1', '')
    em = iso.categorical_edge_match('dirx', '')

    while not rospy.is_shutdown():

	plotting = False
	G1 = graph_maker(A.o1,A.o2,A.spatial,A.temporal,A.objects,plotting)

	results = []
	for i in range(len(Activities)):
		flag = 1
		G_copy = G1
		counter = 0
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

	msg = []
	for i in range(len(activities_names)):
		msg = np.append(msg,activities_names[i]+'='+str(results[i]))
	print msg
        r.sleep()


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
