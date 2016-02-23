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
    activity_list = ['arranging_objects/', 'cleaning_objects/', 'having_meal/', 'making_cereal/', 'microwaving_food/', 'taking_food/', 'taking_medicine/']#, 'unstacking_objects/']

    person_id_list = {}
    person_id_list['1'] = {}
    person_id_list['1']['arranging_objects/'] = ['0510175411','0510175554','0510175431']
    person_id_list['1']['cleaning_objects/'] = ['0510181236','0510181310','0510181415']
    person_id_list['1']['having_meal/'] = ['0510182019','0510182057','0510182137']
    person_id_list['1']['making_cereal/'] = ['1204142055','1204142227','1204142500','1204142616']
    person_id_list['1']['microwaving_food/'] = ['1204150645','1204150828','1204151136']
    person_id_list['1']['stacking_objects/'] = ['1204144410','1204144736','1204145234']
    person_id_list['1']['taking_food/'] = ['0510180218','0510180342','0510180532']
    person_id_list['1']['taking_medicine/'] = ['1204142858','1204143959','1204144120']
    #person_id_list['1']['unstacking_objects/'] = ['1204145527','1204145630','1204145902']

    person_id_list['3'] = {}
    person_id_list['3']['arranging_objects/'] = ['0510143426','0510143446','0510143618']
    person_id_list['3']['cleaning_objects/'] = ['0510144324','0510144350','0510144450']
    person_id_list['3']['having_meal/'] = ['0510142336','0510142419','0510142800']
    person_id_list['3']['making_cereal/'] = ['1204173536','1204173846','1204174024','1204174314']
    person_id_list['3']['microwaving_food/'] = ['1204180344','1204180515','1204180612']
    person_id_list['3']['stacking_objects/'] = ['1204175103','1204175316','1204175451']
    person_id_list['3']['taking_food/'] = ['0510144057','0510144139','0510144215']
    person_id_list['3']['taking_medicine/'] = ['1204174554','1204174740','1204174844']
    #person_id_list['3']['unstacking_objects/'] = ['1204175622','1204175712','1204175902']

    person_id_list['4'] = {}
    person_id_list['4']['arranging_objects/'] = ['0510173051','0510173203','0510173217']
    person_id_list['4']['cleaning_objects/'] = ['0510172333','0510172425','0510172557']
    person_id_list['4']['having_meal/'] = ['0510173506','0510173634','0510173714']
    person_id_list['4']['making_cereal/'] = ['1130144242','1130144557','1130144713','1130144814']
    person_id_list['4']['microwaving_food/'] = ['0204140840','0204141007','0204141211']
    person_id_list['4']['stacking_objects/'] = ['1130150747','1130151025','1130151121']
    person_id_list['4']['taking_food/'] = ['0510171810','0510172015','0510172049']
    person_id_list['4']['taking_medicine/'] = ['1130145737','1130145835','1130150135']
    #person_id_list['4']['unstacking_objects/'] = ['1130151154','1130151500','1130151710']

    person_id_list['5'] = {}
    person_id_list['5']['arranging_objects/'] = ['0504235245','0504235647','0504235908']
    person_id_list['5']['cleaning_objects/'] = ['0511140410','0511140450','0511140553']
    person_id_list['5']['having_meal/'] = ['0511141007','0511141231','0511141338']
    person_id_list['5']['making_cereal/'] = ['0126141638','0126141850','0126142037','0126142253']
    person_id_list['5']['microwaving_food/'] = ['0129114054','0129114153','0129114356']
    person_id_list['5']['stacking_objects/'] = ['0129111131','0129112015','0129112226']
    person_id_list['5']['taking_food/'] = ['0505002750','0505002942','0505003237']
    person_id_list['5']['taking_medicine/'] = ['0126143115','0126143251','0126143431']
    #person_id_list['5']['unstacking_objects/'] = ['1130151154','1130151500','1130151710']

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

    person_id_counter = 1
    for person in ['1']:
        skeleton_data_dir_path = '/home/omari/Datasets/CAD120/annotations/Subject'+person+'_annotations/'
        image_data_dir_path = '/home/omari/Datasets/CAD120/RGBD_images/Subject'+person+'_rgbd_images/'
        for activity in activity_list:
            for person_id_counter in range(len(person_id_list[person][activity])):
                x_world_msg = []
                y_world_msg = []
                z_world_msg = []
                Head_msg = []
                RH_msg = []
                LH_msg = []

                skeleton_data_dir = skeleton_data_dir_path+activity
                image_data_dir = image_data_dir_path+activity
                person_id = person_id_list[person][activity][person_id_counter]
                skeleton_file = person_id_list[person][activity][person_id_counter]+'.txt'
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

                print person,activity,person_id_counter,obj_name
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

                qsr = QSR(Head_msg,RH_msg,LH_msg,x_world_msg,y_world_msg,z_world_msg,['Head','RH','LH']+list(obj_name))
                f = open('/home/omari/Python/cad120/src/QSR_data/person'+person+'/'+activity.split('/')[0]+'_'+person_id_list[person][activity][person_id_counter]+'.txt', 'w')
                L_names = ['Head','RH','LH']+list(obj_name)
                names = ''
                for n1 in range(len(L_names)-1):
                    names+=L_names[n1]+','
                names+=L_names[-1]
                f.write(names+'\n')
                count = 0
                for a1 in range(len(L_names)-1):
                    for a2 in range(a1+1,len(L_names)):
                        qsrs = ''
                        for a3 in range(len(qsr[count,:])-1):
                            qsrs += str(qsr[count,a3])+','
                        qsrs += str(qsr[count,-1])
                        f.write(L_names[a1]+','+L_names[a2]+':'+qsrs+'\n')
                        count += 1
                f.close()
                # break
            # break
