
from networkx import *
import numpy as np

#-------------------------------------------------------------------------------------#
def grapelet(g,obj1,spatial,obj2):
	global spatial_nodes_counter,labels
	g.add_node(spatial_nodes_counter,pos=(spatial_nodes_counter-object_nodes_counter,3),color='g',type1=spatial,type2='spatial')
	labels[spatial_nodes_counter] = spatial
	g.add_edge(spatial_nodes_counter,obj1,dirx='')
	g.add_edge(spatial_nodes_counter,obj2,dirx='')
	spatial_nodes_counter = spatial_nodes_counter+1

#-------------------------------------------------------------------------------------#
def grapelet_temporal(g,spa1,temporal,spa2):
	global temporal_nodes_counter,labels,spatial_nodes_counter
	g.add_node(temporal_nodes_counter,pos=(temporal_nodes_counter-spatial_nodes_counter,5),color='r',type1=temporal,type2='temporal')
	labels[temporal_nodes_counter] = temporal
	g.add_edge(temporal_nodes_counter,spa1,dirx='from '+G.node[spa1]['type1'])
	g.add_edge(temporal_nodes_counter,spa2,dirx='to '+G.node[spa2]['type1'])
	temporal_nodes_counter = temporal_nodes_counter+1

#-------------------------------------------------------------------------------------#
def update_graph():
	global G,labels
	tmp = get_node_attributes(G,'color')
	A = G.nodes()
	color = []
	for i in A:
		color = np.append(color,tmp[i])
	pos = get_node_attributes(G,'pos')
	draw_networkx_nodes(G,pos,node_size=[1000+2000/(spatial_nodes_counter+1)],node_color=color)
	#draw_networkx_nodes(G,pos)
	draw_networkx_edges(G,pos,width=1.0,alpha=1)
	draw_networkx_labels(G,pos,labels,font_size=10)

#-------------------------------------------------------------------------------------#
def graph_maker(o1,o2,spatial,temporal,All_Objects,plotting):
    	global G,object_nodes_counter,spatial_nodes_counter,temporal_nodes_counter,labels,Main_counter

    	object_nodes_counter = 0
    	spatial_nodes_counter = 0
    	temporal_nodes_counter = 0
	labels={}
	G = Graph()
	G.clear()
	Objects = []
	for i in All_Objects:
		if i in o1 or i in o2:
			Objects = np.append(Objects,i)	

	color = []
	for i in list(Objects):
		G.add_node(i,pos=(object_nodes_counter,1),color='c',type1=i,type2='object')
		labels[i] = i	
		object_nodes_counter += 1	

    	spatial_nodes_counter = object_nodes_counter
	for i in range(len(o1)):
		grapelet(G,o1[i],spatial[i],o2[i])		# QSR to Graph

	counter = 0
	temporal_nodes_counter = spatial_nodes_counter
	for i in range(len(spatial)-1):
	    for j in range(i+1,len(spatial)):
		grapelet_temporal(G,i+object_nodes_counter,temporal[counter],j+object_nodes_counter)		# QSR to Graph
		counter += 1

    	if plotting:
		update_graph()						# Graph generation
	#plt.savefig("/home/omari/Desktop/Python/language/graph"+str(Main_counter)+".png") # or .pdf
	#plt.clf()

	return G
