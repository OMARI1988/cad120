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
from Graph_functions import *

#-------------------------------------------------------------------------------------#
def callback_graphs(data):
	global A
	A = data


#-------------------------------------------------------------------------------------#
def listener():

    rospy.init_node('Graphs')
    rospy.Subscriber("QSRs", QSR, callback_graphs)
    r = rospy.Rate(10) # 10hz

    fig=plt.figure()
    plt.ion()
    plt.show()
    
    time.sleep(1)

    while not rospy.is_shutdown():
	plotting = True
	G = graph_maker(A.o1,A.o2,A.spatial,A.temporal,A.objects,plotting)
    	plt.draw()
        r.sleep()
        plt.cla()
	


#-------------------------------------------------------------------------------------#
if __name__ == '__main__':
	global G,spatial_nodes_counter,labels,A
	A = ['o1','spa','o2']
	spatial_nodes_counter = 0
	labels={}
	G=Graph()		# the graph structure from QSR

    	listener()
