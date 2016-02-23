
import numpy as np
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
def QSR(Head_msg,RH_msg,LH_msg,x_world_msg,y_world_msg,z_world_msg,Names):
	if Head_msg != []:
		window = len(Head_msg[1,:])
		window_filter = 8
		n = len(Names)
		n_qsr = np.sum(range(n))					# number of qsrs (n is the number of objects + skeleton joints u have)
		QSR_vector = np.zeros(shape=(n_qsr, window), dtype=int)  	# initilize the QSR matrix actual one
		Dir_vector = np.zeros(shape=(n, n), dtype=str)  		# initilize the direction matrix
	# initilize the filter
	A = {}
	A[0] = Head_msg
	A[1] = RH_msg
	A[2] = LH_msg

	for i in range(len(x_world_msg)):
		obj_msg = np.zeros(shape=(3,window), dtype=int)
		obj_msg[0,:] = x_world_msg[i,:]
		obj_msg[1,:] = y_world_msg[i,:]
		obj_msg[2,:] = z_world_msg[i,:]
		A[i+3] = obj_msg

	#print QSR_vector
	for k in range(window):
		counter = 0
		for i in range(n):
			for j in range(i+1,n):
				varr,Q = features_calc(A[i][:,k],A[j][:,k])
				# Dir_vector[i,j] = Direction_calc(A[i][:,k],A[j][:,k])
				# Dir_vector[j,i] = Direction_calc(A[j][:,k],A[i][:,k])
				if Q == 'touch':
					QSR_vector[counter,k] = 0
				if Q == 'near':
					QSR_vector[counter,k] = 1
				if Q == 'far':
					QSR_vector[counter,k] = 2
				counter +=1


	for i in range(counter):
		# print QSR_vector[i,:]
		l = QSR_vector[i,0]
		change = 0
		for k in range(1,window):
			change +=1
			if l != QSR_vector[i,k]:
				l = QSR_vector[i,k]
				if change < 6:
					# print i,k
					if k>6:
						QSR_vector[i,k-6:k] = np.repeat(QSR_vector[i,k-6], 6)
					# else:
					# 	QSR_vector[i,k-change:k] = np.repeat(QSR_vector[i,k-change], change)
				change = 0
		# print QSR_vector[i,:]
		# print '---------'

	return QSR_vector
