#! /usr/bin/env python2.7
# -*- coding: iso-8859-1 -*-

import rospy
import Tkinter
from qsr.msg import QSR
import numpy as np
from networkx import *
#-----------------------------------------------------------------------------------------------------#
global f

f = open('/home/omari/catkin_ws/src/graphs/src/language.txt', 'w')

#-----------------------------------------------------------------------------------------------------#

#-------------------------------------------------------------------------------------#
def callback_graphs(data):
	global A
	A = data

#-----------------------------------------------------------------------------------------------------#
class simpleapp_tk(Tkinter.Tk):
    global A
    def __init__(self,parent):
        Tkinter.Tk.__init__(self,parent)
        self.parent = parent
        self.initialize()

    def initialize(self):
        self.grid()

        self.entryVariable = Tkinter.StringVar()
        self.entry = Tkinter.Entry(self,textvariable=self.entryVariable)
        self.entry.grid(column=0,row=0,sticky='EW')
        self.entry.bind("<Return>", self.OnPressEnter)
        self.entryVariable.set(u"Enter feature name.")

        button = Tkinter.Button(self,text=u"Add feature",command=self.OnButtonClick)
        button.grid(column=1,row=0)

        button2 = Tkinter.Button(self,text=u"Finish",command=self.Finish)
        button2.grid(column=2,row=0)

        button3 = Tkinter.Button(self,text=u"Learn",command=self.Learn)
        button3.grid(column=3,row=0)

        self.labelVariable = Tkinter.StringVar()
        label = Tkinter.Label(self,textvariable=self.labelVariable,
                              anchor="w",fg="white",bg="blue")
        label.grid(column=0,row=1,columnspan=4,sticky='EW')
        self.labelVariable.set(u"Ready !")

        self.grid_columnconfigure(0,weight=1)
        self.resizable(True,False)
        self.update()
        self.geometry(self.geometry())       
        self.entry.focus_set()
        self.entry.selection_range(0, Tkinter.END)

    def OnButtonClick(self):
	global A
	#-----# try list all A. and try list without str
	msg = ""
	for i in range(len(A.o1)):
		msg += ','
		msg += A.o1[i]

	for i in range(len(A.spatial)):
		msg += ','
		msg += A.spatial[i]

	for i in range(len(A.o2)):
		msg += ','
		msg += A.o2[i]

	for i in range(len(A.temporal)):
		msg += ','
		msg += A.temporal[i]

	for i in range(len(A.objects)):
		msg += ','
		msg += A.objects[i]


	print msg

	indexing = str(len(A.o1))+','+str(len(A.o2))+','+str(len(A.spatial))+','+str(len(A.temporal))+','+str(len(A.objects))
	f.write(indexing+','+self.entryVariable.get()+msg+'\n')
	
	#print self.entryVariable.get()+','+A.o1+','+A.spatial+','+A.o2+','+A.temporal+'\n'
        self.labelVariable.set( self.entryVariable.get()+" (Saved)" )
        self.entry.focus_set()
        self.entry.selection_range(0, Tkinter.END)

    def Finish(self):
	global f
	f.write('END')
	f.close()
	print 'Finish'
        self.labelVariable.set( "(Done)" )
        self.entry.focus_set()
        self.entry.selection_range(0, Tkinter.END)

    def Learn(self):
	global f
	print 'Reading file ...'
	
	print 'Learning ...'
        self.labelVariable.set( "(Done Learning)" )
        self.entry.focus_set()
        self.entry.selection_range(0, Tkinter.END)

    def OnPressEnter(self,event):
        self.labelVariable.set( self.entryVariable.get()+" (You pressed ENTER)" )
        self.entry.focus_set()
        self.entry.selection_range(0, Tkinter.END)

#-----------------------------------------------------------------------------------------------------#
def listener():

    rospy.init_node('Learning_GUI')
    rospy.Subscriber("QSRs", QSR, callback_graphs)

#-----------------------------------------------------------------------------------------------------#
if __name__ == "__main__":
    global A
    A = []
    app = simpleapp_tk(None)
    app.title('Learning Language')

    print('Language learning running...  ')

    listener()
    app.mainloop()
