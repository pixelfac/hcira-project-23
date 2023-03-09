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
from preprocess_dollar_one import preprocess_points
from unistroke import Unistroke, Point

data = {}

cwd = os.getcwd() + '\\src' + '\\dataset\\'
print(cwd)
# dirs = [x[0] for x in next(os.walk('.'))]
directory_contents = os.listdir(cwd)
# print(directory_contents)
# dirs = [x[0] for x in os.walk(cwd)]
users = []
for x in directory_contents:
    # print(x)
    # if os.path.isdir(x):
    index = x.find('pilot')
    index = x.find('fix_xml')
    if index < 0:
        users.append(x)

# print(users)

gestures = []
for user in users:
    # print("user: " + user)
    path = cwd + user + "\\"
    print(path)
    # print(os.listdir(path))
    temp = []
    for file in os.listdir(path):
        temp.append(path + file)
    gestures.append(temp)
    # print(gestures)
# print(len(gestures[0]))
# print(gestures[0][0])

# document = xml.dom.minidom.parse(gestures[0][0])
# document = ET.parse(gestures[0][0])
# print(document.getroot().tag)
# root = document.getroot()
# points = []
# for child in root:
#     attributes = child.attrib
#     points.append([attributes['X'], attributes['Y']])
#     # print(attributes['X'])
# # print(document.firstchild.tagName)
# print(len(users))
# print("user: " + users[0])

for user_index in range(0, len(users)):
    # print("user_index: " + str(user_index))
    # print(index)
    user = 'user' + '_' + str(user_index)
    data[user] = {}
    # print("gesture: " + str(len(gestures[user_index])))
    for gesture_index in range(0, len(gestures[user_index])):
        print(gestures[user_index][gesture_index])
        document = ET.parse(gestures[user_index][gesture_index])
        gesture_name = document.getroot().attrib['Name']
        digit_index = re.search(r"\d", gesture_name)
        # gesture_name = gesture_name[0: digit_index.start()]
        gesture_label = gesture_name[0: digit_index.start()]
        # print(gesture_name)
        # print(document.getroot().attrib['Name'])

        points = []
        for point in document.getroot():
            attributes = point.attrib
            # print(type(attributes['X']))
            # points.append([int(attributes['X']), int(attributes['Y'])])
            temp_point = Point(int(attributes['X']), int(attributes['Y']))
            points.append(temp_point)

        # if gesture_index == 0:
        #     data[user][gesture_name] = points
        # else:
        #     temp_points = data[user][gesture_name]
        #     temp_points.append(points)
        #     data[user][gesture_name] = temp_points

        # points = preprocess_points(points)
        # print("--------------- length: " + str(len(points)) + " -----------------")
        gesture_obj = Unistroke(label=gesture_name, points=points)
        gesture_obj.points = preprocess_points(gesture_obj.points)
        if gesture_label in data[user]:
            # print("length: " + str(len(points)) + ", name: " + gesture_name)
            temp_points = data[user][gesture_label]
            # temp_points.append(points)
            temp_points.append(gesture_obj)
            data[user][gesture_label] = temp_points
        else:
            # print("length: " + str(len(points)) + ", name: " + gesture_name)
            # data[user][gesture_name] = [points]
            data[user][gesture_label] = [gesture_obj]


print("data size----------------------------------")
print(len(data['user_0']['arrow'][7].points))

print(len(data['user_0']['triangle']))
print(data.keys())