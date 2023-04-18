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
from multistroke import Point, Multistroke

# cwd = os.getcwd() + '\\src' + '\\dataset\\' + '\\10-stylus-MEDIUM'
cwd = os.getcwd() + '\\src' + '\\mmg' + '\\10-stylus-MEDIUM'
print(cwd)
# dirs = [x[0] for x in next(os.walk('.'))]
directory_contents = os.listdir(cwd)
print(directory_contents)

data_mmg = {}
data_mmg_flattened = []

for file in directory_contents:
    document_path = cwd + '\\' + file
    print(document_path)
    document = ET.parse(document_path)
    gesture_name = document.getroot().attrib['Name']
    digit_index = re.search(r"\d", gesture_name)
    gesture_label = gesture_name[0: digit_index.start()-1]
    print(gesture_label)
    points = []
    stroke_num = 1

    if gesture_label in data_mmg and len(data_mmg[gesture_label]) == 3:
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
    gesture_obj = Multistroke(label=gesture_name, points=points)
    gesture_obj.points = preprocess_points(gesture_obj.points)

    if gesture_label in data_mmg:
        # print("length: " + str(len(points)) + ", name: " + gesture_name)
        temp_points = data_mmg[gesture_label]
        # temp_points.append(points)
        temp_points.append(gesture_obj)
        data_mmg[gesture_label] = temp_points
    else:
        # print("length: " + str(len(points)) + ", name: " + gesture_name)
        # data[user][gesture_name] = [points]
        data_mmg[gesture_label] = [gesture_obj]
# dirs = [x[0] for x in os.walk(cwd)]

print(len(data_mmg.keys()))
print(len(data_mmg['X']))

for key in data_mmg.keys():
    for gesture_obj in data_mmg[key]:
        data_mmg_flattened.append(gesture_obj)
