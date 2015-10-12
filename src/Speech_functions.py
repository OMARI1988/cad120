
import numpy as np
from nltk.corpus import stopwords
from itertools import permutations

#-------------------------------------------------------------------------------------#	
def my_split(s, seps):
    res = [s]
    for sep in seps:
        s, res = res, []
        for seq in s:
            res += seq.split(sep)
    return res

#-------------------------------------------------------------------------------------#
def speech_processing(sentences_pt,time_words_pt,spatial_relations_pt,object_relations_pt):
	Final = []
#---------------------------#
    	Objects_pointer = open(sentences_pt, 'r')
	sentences = []
	activities = []
    	for line in Objects_pointer:
        	line = line.strip(',\n')
        	if line == 'END':
            		break
        	fields = line.split(',')
		activities = np.append(activities,fields[0])
		sentences = np.append(sentences,fields[1])

#---------------------------#
	# words that describe time
    	time_words_pointer = open(time_words_pt, 'r')
	time_words = []
    	for line in time_words_pointer:
        	line = line.strip(',\n')
        	if line == 'END':
            		break
        	fields = line.split(',')
		time_words = np.append(time_words,fields)

#---------------------------#
	# words that describe milti changes in same time perios
	multi_changes = ['and']

#---------------------------#
	# words that describe spatial relations
    	spatial_relations_pointer = open(spatial_relations_pt, 'r')
	spatial_relations = []
	spatial_relations_names = []
	counter = 0
    	for line in spatial_relations_pointer:
		spatial_relations2 = []
        	line = line.strip(',\n')
        	if line == 'END':
            		break
        	fields = line.split(',')
		spatial_relations2 = np.append(spatial_relations2,fields)
		spatial_relations.append(spatial_relations2)
		spatial_relations_names = np.append(spatial_relations_names,fields[1])
	
#---------------------------#
	# words that should be removed from the sentence according to NLP
	stop = stopwords.words('english')
	stop = np.append(stop,'ing')
	stop = np.append(stop,'es')

#---------------------------#
	# words that describe objects
    	object_relations_pointer = open(object_relations_pt, 'r')
	objects= []
	objects_names = []
    	for line in object_relations_pointer:
		objects2 = []
        	line = line.strip(',\n')
        	if line == 'END':
            		break
        	fields = line.split(',')
		objects2 = np.append(objects2,fields)
		objects.append(objects2)
		objects_names = np.append(objects_names,fields[0])




	# checking the time intervals
	for i in range(len(sentences)):
		print '*********************************************************'
		print sentences[i]
		print '---------------------------------------------------------'
		time_intervals = my_split(sentences[i],time_words)
		
		#-----------------------------------------------------------------#
				    # Generating the QSRs
		# checking multiple changes in same interval
		obj = []
		for j in range(len(time_intervals)):
		    changes = my_split(time_intervals[j],multi_changes)
		    for k in changes:
			for l in spatial_relations:
			    for l1 in l:
			    	spatial_R = k.split(l1)
			    	if spatial_R[0] != k:
				    temp = []
				    for m in range(len(spatial_R)):
					object_words = ' '.join([n for n in spatial_R[m].split() if n not in stop])
					temp = np.append(temp,object_words)
					obj_temp = [o[0] for o in objects if temp[m] in o]
					if obj_temp == []:
						print temp,' object not found'
						obj_temp = 'object not found'
					obj = np.append(obj,obj_temp)
		list_of_obj = []
		for k1 in obj:
		    if k1 not in list_of_obj:
			    list_of_obj = np.append(list_of_obj,k1)

		# generating the QSR matrix
		n_qsr = np.sum(range(len(list_of_obj)))
		qsr = []
		qsr = np.zeros((n_qsr,1000), dtype=int)			# can have up to 1000 interval

		qsr_options = []
    		for i1 in range(len(list_of_obj)-1):
		    for j1 in range(i1+1,len(list_of_obj)):
		    		A = list(permutations([list_of_obj[i1],list_of_obj[j1]]))
				qsr_options = np.append(qsr_options,A[0])
				qsr_options = np.append(qsr_options,A[1])


				    # Finished Generating the QSRs
		#-----------------------------------------------------------------#

		# checking multiple changes in same interval
		for j in range(len(time_intervals)):
		    changes = my_split(time_intervals[j],multi_changes)

		    # checking for spatial relations
		    for k in changes:
			for l in spatial_relations:
			    for l1 in l:
			    	spatial_R = k.split(l1)
			    	if spatial_R[0] != k:
				    temp = []
				    obj = []
				    for m in range(len(spatial_R)):
					object_words = ' '.join([n for n in spatial_R[m].split() if n not in stop])
					temp = np.append(temp,object_words)
					obj_temp = [o[0] for o in objects if temp[m] in o]
					if obj_temp == []:
						print temp,' object not found'
						obj_temp = 'object not found'
					obj = np.append(obj,obj_temp)
				    print j,l[1],temp,obj

				    # updating the qsr matrix
				    if j>0:
					qsr[:,j] = qsr[:,j-1] 

				    for i1 in range(len(qsr_options)/2):
					    if np.all(obj == qsr_options[i1*2:i1*2+2]):
					        #print int(i1/2)
					    	qsr[int(i1/2),j] = int(l[0]) 
						
		    print '---------------------------------------------------------'
		print qsr[:,0:j+1],list_of_obj

		Final.append([list_of_obj,qsr[:,0:j+1],j+1,len(list_of_obj),spatial_relations_names,objects_names])

	return activities,Final
