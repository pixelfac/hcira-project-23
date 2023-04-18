# xml files are read and loaded into variable called 'data' that matches the form expected
# in test.py (see comments at top of file)

"""
data - list of users
    user - list of gestures
        gestures - list of examples (each xml file)


data
    user 1
        arrow
            arrow1
            arrow2
        check
            check1
            check2
    user 2
        arrow
            arrow1
            arrow2
        check
            check1
            check2
"""


import os
import re
# import xml.dom.minidom
import xml.etree.ElementTree as ET
# from preprocess_dollar_one import preprocess_points
from preprocess_dollar_p import preprocess_points
import unistroke
from multistroke import Point, Multistroke
# from preprocess_dollar_p import normalize

# cwd = os.getcwd() + '\\src' + '\\dataset\\' + '\\10-stylus-MEDIUM'
# cwd = os.getcwd() + '\\src' + '\\mmg' + '\\10-stylus-MEDIUM'
cwd = os.getcwd() + '\\src' + '\\mmg'
print(cwd)
# dirs = [x[0] for x in next(os.walk('.'))]
directory_contents = os.listdir(cwd)
directory_contents = [k for k in directory_contents if 'MEDIUM' in k]
directory_contents = directory_contents[0:2]
# print(directory_contents[0:4])

users = []
for x in directory_contents:
    users.append(x)

gestures = []
for user in users:
    print("user: " + user)
    path = cwd + '\\' +user + "\\" #'\\src' + '\\mmg\\' 
    print(path)
    # print(os.listdir(path))
    temp = []
    print(os.listdir(path))
    for file in os.listdir(path):
        temp.append(path + file)
    gestures.append(temp)

data_mmg = {}
data_mmg_flattened = []

for user_index in range(0, len(users)):
    user = users[user_index]
    
    # user_string = str(user)

    # user_index_string = 
    
    # data[user] = {}

    for gesture_index in range(0, len(gestures[user_index])):
        # for file in directory_contents:
        file_name = gestures[user_index][gesture_index]
        
            # document_path = cwd + '\\' + file
            # print(document_path)
            # document = ET.parse(document_path)
        document = ET.parse(file_name)
        gesture_name = document.getroot().attrib['Name']
        user_name = document.getroot().attrib['Subject']
        if user_name not in data_mmg:
            data_mmg[user_name] = {}
      
        digit_index = re.search(r"\d", gesture_name)
        gesture_label = gesture_name[0: digit_index.start()-1]
        print(gesture_label)
        points = []
        points_1 = []
        stroke_num = 1

        if gesture_label in data_mmg and len(data_mmg[gesture_label]) == 1:
            continue

        for stroke in document.getroot():
            # stroke_points = []
            for point in stroke:
                # print(point.tag)
                attributes = point.attrib
                temp_point = Point(int(attributes['X']), int(attributes['Y']), stroke_num)
                # print(temp_point.coords)
                points.append(temp_point)
            # points.append(stroke_points)
            stroke_num = stroke_num + 1
        # print(len(points))
        gesture_obj = Multistroke(label=gesture_label, points=points)
        # gesture_obj.points = normalize(gesture_obj.points , 32)
        gesture_obj.points = preprocess_points(gesture_obj.points)

        if gesture_label in data_mmg[user_name]:
            # print("length: " + str(len(points)) + ", name: " + gesture_name)
        
            temp_points = data_mmg[user_name][gesture_label]
            # temp_points.append(points)
            temp_points.append(gesture_obj)
            data_mmg[user_name][gesture_label] = temp_points
        else:
            # print("length: " + str(len(points)) + ", name: " + gesture_name)
            # data[user][gesture_name] = [points]
            data_mmg[user_name][gesture_label] = [gesture_obj]
    # dirs = [x[0] for x in os.walk(cwd)]

print(len(data_mmg.keys()))
print(len(data_mmg['10']['X'][0].points))
# print(len(data_mmg['X']))

for user in data_mmg.keys():
    for gesture in data_mmg[user]:
        for gesture_obj in data_mmg[user][gesture]:
            data_mmg_flattened.append(gesture_obj)

# for key in data_mmg_1.keys():
#     for gesture_obj in data_mmg_1[key]:
#         data_mmg_1_flattened.append(gesture_obj)
