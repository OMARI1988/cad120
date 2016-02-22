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
    person_id_list['1']['arranging_objects/'] = ['0510175431','0510175554','0510175411']
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

    for person in ['1']:
        skeleton_data_dir_path = '/home/omari/Datasets/CAD120/annotations/Subject'+person+'_annotations/'
        image_data_dir_path = '/home/omari/Datasets/CAD120/RGBD_images/Subject'+person+'_rgbd_images/'
        for activity in activity_list:
            for person_id_counter in range(len(person_id_list[person][activity])):
                f = open('/home/omari/Python/cad120/src/QSR_data/person'+person+'/'+activity.split('/')[0]+'_'+person_id_list[person][activity][person_id_counter]+'.txt', 'r')
                for count,line in enumerate(f):
                    print count,line
                f.close()
