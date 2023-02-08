import math
import numpy as np


def resample_points(points, n):
    """
    Method to execute 1st step of preprocessing for $1 recogniser. Resample points array to have consistent
    number of points
    :param points: All points identified from user's gesture
    :param n: Size of points array
    :return: new_points array after applying Resampling step.
    """

    path_length = get_path_length(points)
    length = path_length / (n-1)
    d = 0
    temp_points = points[:]
    new_points = [points[0]]
    i = 1
    while i < len(temp_points):
        prev_point = temp_points[i-1]
        curr_point = temp_points[i]
        dist = get_distance([prev_point, curr_point])
        if (d + dist) >= length:
            qx = temp_points[i-1][0] + ((length - d) / dist) * (temp_points[i][0] - temp_points[i-1][0])
            qy = temp_points[i-1][1] + ((length - d) / dist) * (temp_points[i][1] - temp_points[i-1][1])
            new_points.append([qx, qy])
            temp_points.insert(i, [qx, qy])
            d = 0
        else:
            d = d + dist
        i = i + 1

    return new_points


def rotate_to_zero(points):
    """
    Method to apply 2nd step of preprocessing. Rotate all points so that 1st point and centroid have an angle of 0.
    :param points: array of coordinates
    :return: array of coordinates after applying rotation
    """

    centroid_x, centroid_y = get_centroid(np.array(points))
    angle = math.atan2(centroid_y - points[0][1], centroid_x - points[0][0])
    # Not sure if rotate by angle or -angle...paper says -angle but it rotates anticlockwise
    new_points = rotate_by(points, -angle, [centroid_x, centroid_y])
    # new_points.insert(0, [centroid_x, centroid_y])
    return new_points


def rotate_by(points, angle, centroid):
    """
    Method to rotate all points by angle
    :param points: array of coordinates
    :param angle: angle between 1st point and centroid
    :param centroid: coordinates of centroid
    :return: array of points after rotation
    """

    centroid_x = centroid[0]
    centroid_y = centroid[1]
    new_points = []
    for point in points:
        qx = (point[0] - centroid_x) * math.cos(angle) - (point[1] - centroid_y) * math.sin(angle) + centroid_x
        qy = (point[0] - centroid_x) * math.sin(angle) + (point[1] - centroid_y) * math.cos(angle) + centroid_y
        new_points.append([qx, qy])

    return new_points


def get_distance(points):
    """
    Utility method to get distance b/w 2 points
    :param points: array of points
    :return: dist b/w 2 points within the array
    """

    dist_x = (points[1][0] - points[0][0]) ** 2
    dist_y = (points[1][1] - points[0][1]) ** 2
    dist = math.sqrt(dist_x + dist_y)
    return dist


def get_path_length(points):
    """
    Utility method to calculate total path length from all points of user's gesture
    :param points: array of points retrieved from user's gesture
    :return: Total path length of all points
    """

    path_length = 0
    n = len(points)
    for i in range(n-1):
        curr_point = points[i]
        next_point = points[i + 1]
        dist = get_distance([curr_point, next_point])
        path_length = path_length + dist

    return path_length

def get_centroid(points):
    """
    Utility method to get centroid of points
    :param points: array of coordinates
    :return: x, y coordinate of centroid
    """
    
    n = points.shape[0]
    sum_x_coords = np.sum(points[:, 0])
    sum_y_coords = np.sum(points[:, 1])
    return sum_x_coords / n, sum_y_coords / n

def scale_to_square(points , square_size):
    """
    Method to scale the points
    :param points: array of coordinates , size of the square.
    :return: new points as an array after scaling
    """
    maximum_x, maximum_y = np.max(points, 0)
    minimum_x, minimum_y = np.min(points, 0) 

    box_width = maximum_x - minimum_x
    box_height = maximum_y - minimum_y

    new_points = np.zeros((1,2))

    for point in points:
        q = np.array([0.,0.])
        q[0] = point[0] * (square_size / box_width)
        q[1] = point[1] * (square_size / box_height)
        new_points = np.append(new_points, [q] , 0)
    
    return new_points[1:]

def translate_to_origin(points):
    
    """
    Method to translate the points to origin
    :param points: array of coordinates
    :return: new points as an array after translating to origin
    """

    centroid_x, centroid_y = get_centroid(np.array(points))
    # centroid = np.array([centroid_x,centroid_y])
    new_points = np.zeros((1,2))

    # new_points = points-centroid


    for point in points:
        q = np.array([0.,0.])
        q[0] = point[0] - centroid_x
        q[1] = point[1] - centroid_y
        new_points = np.append(new_points, [q] , 0)
    
    return new_points[1:]


